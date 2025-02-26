import pdfplumber
import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from datetime import datetime, timedelta

# Load API Key
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key is None:
    st.error("GROQ_API_KEY is not set. Please check your environment variables.")
    st.stop()

# Initialize LLM
llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)

# Custom CSS for styling
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

# Sidebar
st.sidebar.image("Resturant_rag_streamlit/1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

# Main Header with Background Image
st.image("Resturant_rag_streamlit/2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Define Agents and Tasks before using them in the chat section

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

# Chatbot section
st.header("Chatbot Assistant")

# Initialize session state for messages if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Unified Chat Input (combining inquiry and chat)
if prompt := st.chat_input("How can I assist you today?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if Knowledge Base has been initialized
    if not st.session_state.get("vector_ready", False):
        response = "⚠️ Please initialize the knowledge base first using the sidebar button."
    else:
        # Retrieve context from the vector store
        similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
        retrieved_context = "\n".join(
            [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
        )

        # Enhance the prompt with context
        enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"

        # Create Agents
        reservation_agent = create_reservation_agent()
        inquiry_agent = create_inquiry_agent()

        # Determine Task Type based on keywords in the user's prompt
        if "reservation" in prompt.lower() or "book a table" in prompt.lower():
            task = create_reservation_task(reservation_agent, enhanced_question)
            agent = reservation_agent
        else:
            task = create_inquiry_task(inquiry_agent, enhanced_question)
            agent = inquiry_agent

        # Execute task with Crew
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        response = crew.kickoff(inputs={"question": enhanced_question})

    # Append chatbot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Mass booking button
if st.button("Mass Booking"):
    st.header("Available Dates")

    # Generate a list of available dates for the next 7 days
    available_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    # Display available dates with checkboxes
    selected_dates = st.multiselect("Select dates for booking:", available_dates)

    # If dates are selected, input them into the chatbot
    if selected_dates:
        booking_message = f"Booking requested for dates: {', '.join(selected_dates)}"
        st.session_state.messages.append({"role": "user", "content": booking_message})
        with st.chat_message("user"):
            st.markdown(booking_message)

        # Simulate chatbot response for booking
        response = "Your booking request has been received. We will confirm availability soon."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Initialize Vector Store
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
