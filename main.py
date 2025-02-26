from dotenv import load_dotenv
load_dotenv('Resturant_rag_streamlit\\.env')

import streamlit as st
from database import init_db, add_booking, get_bookings, update_booking_status
from agents import create_reservation_agent, create_inquiry_agent, create_reservation_task, create_inquiry_task
from utils import load_environment, get_max_capacity, initialize_knowledge_base
from langchain_groq import ChatGroq
import os
from crewai import Agent, Task, Crew, Process

from datetime import datetime, timedelta
import re

groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)

# Load environment variables
load_environment()

# Initialize database
init_db()

# Load CSS styles
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

# Sidebar and main header setup
st.sidebar.image("Resturant_rag_streamlit/1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

st.image("Resturant_rag_streamlit/2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Chatbot section
st.header("Chatbot Assistant")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Unified chat input reservation logic
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

# Mass booking section
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

# Vector store initialization
if st.sidebar.button("Initialize Knowledge Base"):
    initialize_knowledge_base()
