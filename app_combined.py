import os
import sqlite3
import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime, timedelta
import re

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            number_of_people INTEGER,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Database Functions ---
def add_booking(date, number_of_people, status="Pending"):
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (date, number_of_people, status)
        VALUES (?, ?, ?)
    ''', (date, number_of_people, status))
    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def update_booking_status(booking_id, status):
    conn = sqlite3.connect('restaurant_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bookings
        SET status = ?
        WHERE id = ?
    ''', (status, booking_id))
    conn.commit()
    conn.close()

# --- Initialization & Setup ---
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key is None:
    st.error("GROQ_API_KEY is not set. Please check your environment variables.")
    st.stop()

llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)

st.markdown(
    """
    <style>
        body {
            background-color: #f8f9fa;
        }
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
        }
        .stTextInput > div > div > input {
            background-color: #f5f5f5;
            border-radius: 8px;
            color: #333333;
        }
        .stTitle {
            color: #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar & Main Header ---
st.sidebar.image("Resturant_rag_streamlit/1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

st.image("Resturant_rag_streamlit/2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# --- Define Agents and Tasks ---
def create_reservation_agent():
    return Agent(
        role="Reservation Manager",
        goal="Handle restaurant reservations efficiently.",
        backstory="You are responsible for taking reservations, checking table availability, and managing booking requests.",
        llm=llm,
        verbose=True
    )

def create_inquiry_agent():
    return Agent(
        role="Customer Support",
        goal="Provide answers about restaurant policies, menu, and general inquiries.",
        backstory="You are an expert in restaurant policies and menu details, assisting customers with accurate information.",
        llm=llm,
        verbose=True
    )

def create_reservation_task(agent, question):
    return Task(
        description=f"Process the reservation request and respond appropriately: {question}",
        expected_output="A response confirming the reservation status.",
        agent=agent
    )

def create_inquiry_task(agent, question):
    return Task(
        description=f"Answer the customer's inquiry using restaurant policies and menu information: {question}",
        expected_output="An informative response based on the restaurant's official documentation.",
        agent=agent
    )

# --- Chatbot Section ---
st.header("Chatbot Assistant")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_max_capacity():
    pdf_path = "Resturant_rag_streamlit/restaurant_docs/restaurant_policy.pdf"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                match = re.search(r"Max Capacity:\s*(\d+)", text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
    except Exception as e:
        print(f"Error reading max capacity from PDF: {e}")
    # Return a default capacity if not found
    return 50

# --- Unified Chat Input Reservation Logic ---
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    if not st.session_state.get("vector_ready", False):
        response = "⚠️ Please initialize the knowledge base first using the sidebar button."
    else:
        similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
        retrieved_context = "\n".join(
            [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
        )
        enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"
        reservation_agent = create_reservation_agent()
        inquiry_agent = create_inquiry_agent()
        # If the prompt is a reservation request, process booking with capacity check
        if "reservation" in prompt.lower() or "book a table" in prompt.lower():
            # Extract booking date and number of people from the prompt
            date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', prompt)
            booking_date = date_match.group(1) if date_match else (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            num_match = re.search(r'\b(\d+)\b', prompt)
            number_of_people = int(num_match.group(1)) if num_match else 2

            # Get max capacity from PDF
            MAX_CAPACITY = get_max_capacity()

            # Check existing bookings for the same date
            existing_bookings = get_bookings()
            total_guests = sum(b[2] for b in existing_bookings if b[1] == booking_date)

            if total_guests + number_of_people > MAX_CAPACITY:
                capacity_msg = f"Sorry, we are fully booked for {booking_date} (Max capacity: {MAX_CAPACITY} guests). Please choose another date or reduce the party size."
                st.session_state.messages.append({"role": "assistant", "content": capacity_msg})
                with st.chat_message("assistant"):
                    st.markdown(capacity_msg)
                response = capacity_msg
            else:
                # Record the new booking in the database
                add_booking(booking_date, number_of_people)
                booking_confirmation = f"Reservation recorded for {number_of_people} people on {booking_date}."
                st.session_state.messages.append({"role": "assistant", "content": booking_confirmation})
                with st.chat_message("assistant"):
                    st.markdown(booking_confirmation)
                task = create_reservation_task(reservation_agent, enhanced_question)
                agent = reservation_agent
                crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
                response = crew.kickoff(inputs={"question": enhanced_question})
        else:
            task = create_inquiry_task(inquiry_agent, enhanced_question)
            agent = inquiry_agent
            crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
            response = crew.kickoff(inputs={"question": enhanced_question})
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# --- Mass Booking Section ---
if st.button("Mass Booking"):
    st.header("Available Dates")
    available_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    # Use a form to combine date selection and number of people
    with st.form("booking_form"):
        selected_dates = st.multiselect("Select dates for booking:", available_dates)
        number_of_people = st.number_input("Number of People", min_value=1, max_value=20, value=1)
        submit_booking = st.form_submit_button("Confirm Booking")
        if submit_booking and selected_dates:
            for date in selected_dates:
                # Add each booking to the database
                add_booking(date, number_of_people)
                booking_message = f"Booking requested for {number_of_people} people on {date}"
                st.session_state.messages.append({"role": "user", "content": booking_message})
                with st.chat_message("user"):
                    st.markdown(booking_message)
                # Simulated chatbot response for booking requests (you can invoke a real flow if needed)
                response = "Your booking request has been received. We will confirm availability soon."
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

# # --- Booking Display Section ---
# st.header("Current Bookings")
# bookings = get_bookings()
# for booking in bookings:
#     st.write(f"ID: {booking[0]}, Date: {booking[1]}, People: {booking[2]}, Status: {booking[3]}")

# --- Vector Store Initialization ---
if st.sidebar.button("Initialize Knowledge Base"):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        pdf_directory = "Resturant_rag_streamlit/restaurant_docs"
        all_text = []
        for pdf_file in os.listdir(pdf_directory):
            if pdf_file.endswith(".pdf"):
                with pdfplumber.open(os.path.join(pdf_directory, pdf_file)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            all_text.append(text)
        if not all_text:
            st.sidebar.error("No text extracted from PDFs. Please check the documents and retry.")
        else:
            combined_text = "\n".join(all_text)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_documents = text_splitter.split_text(combined_text)
            vectors = FAISS.from_texts(final_documents, embeddings)
            st.session_state.vectors = vectors
            st.session_state.vector_ready = True
            st.sidebar.success("Knowledge Base Initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing: {e}")
