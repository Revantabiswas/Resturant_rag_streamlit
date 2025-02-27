import os
import re
from datetime import datetime, timedelta

import streamlit as st
from dotenv import load_dotenv

from database import init_db, add_booking, get_bookings
from agents import create_reservation_agent, create_inquiry_agent, create_reservation_task, create_inquiry_task
from utils import load_environment, get_max_capacity, initialize_knowledge_base
from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew, Process

# Load environment variables from .env file and project config.
load_dotenv('Resturant_rag_streamlit\\.env')
load_environment()

# Initialize database
init_db()

# Configure LangChain LLM
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)

# CSS Styles
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

# Sidebar and header image setups
st.sidebar.image("Resturant_rag_streamlit/1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")
st.image("Resturant_rag_streamlit/2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Chat session initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

def process_reservation(prompt: str, enhanced_question: str):
    # Extract booking details
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', prompt)
    booking_date = date_match.group(1) if date_match else (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    num_match = re.search(r'\b(\d+)\b', prompt)
    number_of_people = int(num_match.group(1)) if num_match else 2

    # Capacity check
    MAX_CAPACITY = get_max_capacity()
    existing_bookings = get_bookings()
    total_guests = sum(b[2] for b in existing_bookings if b[1] == booking_date)

    if total_guests + number_of_people > MAX_CAPACITY:
        return f"Sorry, we are fully booked for {booking_date} (Max capacity: {MAX_CAPACITY} guests). Please choose another date or reduce the party size.", None

    add_booking(booking_date, number_of_people)
    confirmation = f"Reservation recorded for {number_of_people} people on {booking_date}."
    reservation_agent = create_reservation_agent()
    task = create_reservation_task(reservation_agent, enhanced_question)
    crew = Crew(agents=[reservation_agent], tasks=[task], process=Process.sequential, verbose=True)
    return confirmation, crew.kickoff(inputs={"question": enhanced_question})

def process_inquiry(enhanced_question: str):
    inquiry_agent = create_inquiry_agent()
    task = create_inquiry_task(inquiry_agent, enhanced_question)
    crew = Crew(agents=[inquiry_agent], tasks=[task], process=Process.sequential, verbose=True)
    return crew.kickoff(inputs={"question": enhanced_question})

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I assist you today?"):
    add_message("user", prompt)
    if not st.session_state.get("vector_ready", False):
        response = "⚠️ Please initialize the knowledge base first using the sidebar button."
    else:
        similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
        retrieved_context = "\n".join(
            [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
        )
        enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"
        if "reservation" in prompt.lower() or "book a table" in prompt.lower():
            response_msg, llm_response = process_reservation(prompt, enhanced_question)
            add_message("assistant", response_msg)
            if llm_response:
                response = llm_response
            else:
                response = response_msg
        else:
            response = process_inquiry(enhanced_question)
    add_message("assistant", response)

def process_mass_booking(selected_dates, number_of_people, base_booking_text):
    for date in selected_dates:
        booking_message = f"{base_booking_text} for {number_of_people} people on {date}."
        add_message("user", booking_message)
        enhanced_booking_question = f"Please confirm and process the following booking: {booking_message}"
        reservation_agent = create_reservation_agent()
        task = create_reservation_task(reservation_agent, enhanced_booking_question)
        crew = Crew(agents=[reservation_agent], tasks=[task], process=Process.sequential, verbose=True)
        llm_response = crew.kickoff(inputs={"question": enhanced_booking_question})
        add_booking(date, number_of_people)
        confirmation_message = f"Booking for {number_of_people} people on {date} has been recorded."
        add_message("assistant", confirmation_message)
        add_message("assistant", llm_response)

# Mass booking section
if st.button("Mass Booking"):
    st.header("Available Dates")
    available_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    with st.form("booking_form"):
        selected_dates = st.multiselect("Select dates for booking:", available_dates)
        number_of_people = st.number_input("Number of People", min_value=1, max_value=20, value=1)
        base_booking_text = st.text_area("Edit your booking message (this will be sent to our system):",
                                         value="Mass booking request",
                                         height=80)
        submit_booking = st.form_submit_button("Confirm Booking")
        if submit_booking and selected_dates:
            process_mass_booking(selected_dates, number_of_people, base_booking_text)

# Knowledge Base Initialization
if st.sidebar.button("Initialize Knowledge Base"):
    initialize_knowledge_base()
