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

def process_mass_booking(selected_dates, number_of_people, base_booking_text):
    """Process multiple bookings for group events"""
    try:
        for date in selected_dates:
            booking_message = f"{base_booking_text} for {number_of_people} people on {date}."
            
            # Add booking to database first to ensure it's recorded
            add_booking(date, number_of_people)
            
            # Generate AI response if knowledge base is ready
            if st.session_state.get("vector_ready", False):
                try:
                    # Create enhanced booking question
                    enhanced_booking_question = f"Please confirm and process the following booking: {booking_message}"
                    
                    # Create agent and task
                    reservation_agent = create_reservation_agent()
                    task = create_reservation_task(reservation_agent, enhanced_booking_question)
                    
                    # Execute with crew
                    crew = Crew(
                        agents=[reservation_agent], 
                        tasks=[task], 
                        process=Process.sequential, 
                        verbose=True
                    )
                    
                    # Get response from AI
                    llm_response = crew.kickoff(inputs={"question": enhanced_booking_question})
                    
                    # Add messages to chat history
                    if 'messages' in st.session_state:
                        st.session_state.messages.append({"role": "user", "content": booking_message})
                        st.session_state.messages.append({"role": "assistant", "content": f"✅ Booking for {number_of_people} people on {date} has been recorded."})
                        st.session_state.messages.append({"role": "assistant", "content": llm_response})
                except Exception as e:
                    # Handle AI processing errors
                    st.warning(f"Error processing AI response for booking on {date}: {str(e)}")
                    if 'messages' in st.session_state:
                        st.session_state.messages.append({"role": "assistant", "content": f"✅ Booking for {number_of_people} people on {date} has been recorded, but I couldn't generate a detailed confirmation."})
            else:
                # If knowledge base isn't ready, still confirm the booking
                if 'messages' in st.session_state:
                    st.session_state.messages.append({"role": "user", "content": booking_message})
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ Booking for {number_of_people} people on {date} has been recorded."})
    except Exception as e:
        st.error(f"Error processing bookings: {str(e)}")
        return False
    return True

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'vector_ready' not in st.session_state:
    st.session_state.vector_ready = False

# Load environment variables from .env file and project config.
load_dotenv('.env')
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
        /* Main Theme */
        :root {
            --primary: #D92B04;
            --secondary: #F2B705;
            --accent: #590902;
            --background: #FFF9F1;
            --text: #2E1A1F;
        }
        
        /* Global Styles */
        .main .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }
        
        body {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Playfair Display', serif;
        }
        
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
        }
        
        /* Custom Header */
        .restaurant-header {
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('header-bg.jpg');
            background-size: cover;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border-radius: 30px;
            padding: 8px 25px;
            font-weight: 500;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            padding: 10px 15px;
            color: var(--text);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: white;
            border-radius: 15px;
            padding: 12px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        .stChatMessage.user {
            background-color: #E8F0FE;
            margin-left: 15%;
        }
        
        .stChatMessage.assistant {
            background-color: white;
            margin-right: 15%;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #2E1A1F;
        }
        
        .sidebar .sidebar-content {
            background-color: #2E1A1F;
            color: white;
        }
        
        /* Cards */
        .menu-card, .reservation-card, .info-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .menu-card:hover, .reservation-card:hover, .info-card:hover {
            transform: translateY(-5px);
        }
        
        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #f0f0f0;
            border-radius: 4px 4px 0px 0px;
            border: none;
            padding: 10px 16px;
            color: var(--text);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary);
            color: white;
        }
    </style>
    
    <!-- Import custom fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Add floating action button for quick reservation
st.markdown("""
<style>
.floating-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: var(--primary);
    color: white;
    padding: 15px 20px;
    border-radius: 50px;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 999;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
}
.floating-button:hover {
    background-color: var(--accent);
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.25);
}
</style>
<a href="#" class="floating-button" onclick="window.location.href='/?page=Reservations'">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM16 14V5H0v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zm-3.5-7h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5z"/>
    </svg>
    Reserve Now
</a>
""", unsafe_allow_html=True)

# Create App Layout
st.sidebar.image("1.png", use_container_width=True)
st.sidebar.title("🍽️ Indian Palace")
st.sidebar.markdown("---")

# Sidebar Navigation
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("", ["Home", "Menu", "Reservations", "Contact"])
st.sidebar.markdown("---")

# Knowledge Base Initialization
with st.sidebar.expander("📚 Admin Options"):
    if st.button("Initialize Knowledge Base"):
        initialize_knowledge_base()

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Indian Palace Restaurant")

# Main Content Area Based on Navigation Selection
if page == "Home":
    # Hero Section
    st.markdown('<div class="restaurant-header">', unsafe_allow_html=True)
    st.image("2.jpg", use_container_width=True)
    st.title("🍽️ Welcome to Indian Palace")
    st.markdown("**Experience authentic Indian cuisine in the heart of the city**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # About Section
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown("### Our Story")
        st.write("""
        At Indian Palace, we bring the rich flavors of India to your table. 
        Established in 2010, our restaurant combines traditional cooking techniques 
        with the finest ingredients to create an unforgettable dining experience.
        
        Our chefs come from different regions of India, each bringing their own unique 
        expertise and recipes passed down through generations.
        """)
    
    # Features Section
    st.markdown("### What We Offer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios-filled/50/000000/dining-room.png", width=50)
        st.markdown("#### Elegant Dining")
        st.write("Our restaurant offers a warm, elegant atmosphere perfect for any occasion.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios-filled/50/000000/food-and-wine.png", width=50)
        st.markdown("#### Authentic Cuisine")
        st.write("Experience the true flavors of India with our authentic recipes.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/?size=100&id=9KPN5HvQHsvg&format=png&color=000000", width=50)
        st.markdown("#### Private Events")
        st.write("Host your special events with us for an unforgettable experience.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Menu":
    st.title("Our Menu")
    
    # Menu Tabs
    menu_tab1, menu_tab2, menu_tab3, menu_tab4 = st.tabs(["Appetizers", "Main Course", "Desserts", "Beverages"])
    
    with menu_tab1:
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://source.unsplash.com/100x100/?samosa", width=100)
        with col2:
            st.markdown("### Vegetable Samosas")
            st.write("Crispy pastry filled with spiced potatoes and peas")
            st.write("**$6.99**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="menu-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://source.unsplash.com/100x100/?pakora", width=100)
        with col2:
            st.markdown("### Onion Bhaji")
            st.write("Crispy onion fritters with chickpea flour and spices")
            st.write("**$5.99**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Similar structure for other menu tabs
    # (Add your actual menu items here)

elif page == "Reservations":
    st.title("Make a Reservation", anchor="reservation-section")  # Add anchor for the floating button
    
    # Reservation Tabs
    res_tab1, res_tab2 = st.tabs(["New Reservation", "Check Availability"])
    
    with res_tab1:
        st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
        with st.form("reservation_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
            
            with col2:
                date = st.date_input("Reservation Date")
                time = st.selectbox("Time", ["5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"])
                guests = st.number_input("Number of Guests", min_value=1, max_value=20, value=2)
            
            special_requests = st.text_area("Special Requests (Optional)")
            submit_button = st.form_submit_button("Reserve Table")
            
            if submit_button:
                if name and email and phone:
                    add_booking(date.strftime('%Y-%m-%d'), guests)
                    st.success(f"Reservation confirmed for {name} on {date.strftime('%Y-%m-%d')} at {time} for {guests} guests.")
                else:
                    st.error("Please fill out all required fields.")
        st.markdown('</div>', unsafe_allow_html=True)

    with res_tab2:
        # Show availability calendar
        st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
        st.subheader("Check Table Availability")
        check_date = st.date_input("Select Date", key="check_date")
        
        # Get bookings for the selected date
        existing_bookings = get_bookings()
        date_bookings = [b for b in existing_bookings if b[1] == check_date.strftime('%Y-%m-%d')]
        total_guests = sum(b[2] for b in date_bookings)
        max_capacity = get_max_capacity()
        
        # Display availability
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Reserved Seats", total_guests)
        with col2:
            st.metric("Available Seats", max_capacity - total_guests)
            
        # Show availability by time slot (simplified example)
        st.subheader("Availability by Time")
        times = ["5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM"]
        for time in times:
            # In a real app, you would check availability for each time slot
            # For this example, we'll just show random availability
            import random
            availability = random.choice(["Available", "Limited", "Booked"])
            color = {"Available": "green", "Limited": "orange", "Booked": "red"}[availability]
            st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                       f"<span>{time}</span>"
                       f"<span style='color: {color};'>{availability}</span>"
                       f"</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Group & Event Reservations"):
        st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
        st.subheader("Book Multiple Dates")
        
        with st.form("group_booking_form"):
            col1, col2 = st.columns(2)
            with col1:
                group_name = st.text_input("Group/Event Name")
                contact_person = st.text_input("Contact Person")
                contact_email = st.text_input("Contact Email")
            
            with col2:
                number_of_people = st.number_input("Number of People per Reservation", 
                                                min_value=1, 
                                                max_value=50, 
                                                value=10)
                event_type = st.selectbox("Event Type", 
                                        ["Corporate Meeting", "Birthday Party", "Wedding Reception", 
                                        "Anniversary", "Other"])
            
            # Calendar selector with visual cues
            st.subheader("Select Dates")
            # Generate next 14 days
            available_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 15)]
            selected_dates = st.multiselect("Select all dates needed:", available_dates)
            
            # Special requirements
            special_requirements = st.text_area("Special Requirements or Notes",
                                            placeholder="Please let us know about any dietary restrictions, room setup preferences, or other special needs.")
            
            submit_group = st.form_submit_button("📅 Request Group Booking")
            
            if submit_group and selected_dates and group_name and contact_person and contact_email:
                base_booking_text = f"Group reservation for {group_name}, {event_type} event"
                
                # Show confirmation
                st.success(f"Group booking request received for {len(selected_dates)} date(s). Our team will contact you at {contact_email} to confirm.")
                
                # Process bookings in the background
                process_mass_booking(selected_dates, number_of_people, base_booking_text)
            elif submit_group:
                st.warning("Please fill out all required fields and select at least one date.")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Contact":
    st.title("Contact Us")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Visit Us")
        st.markdown("""
        **Address:**  
        123 Main Street  
        New York, NY 10001
        
        **Hours:**  
        Monday-Thursday: 5:00 PM - 10:00 PM  
        Friday-Saturday: 5:00 PM - 11:00 PM  
        Sunday: 4:00 PM - 9:00 PM
        
        **Phone:**  
        (555) 123-4567
        
        **Email:**  
        info@indianpalace.com
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Send Us a Message")
        with st.form("contact_form"):
            st.text_input("Name")
            st.text_input("Email")
            st.text_area("Message")
            st.form_submit_button("Send Message")
        st.markdown('</div>', unsafe_allow_html=True)
        
# Chatbot Section (Always Present)
st.markdown("---")
st.subheader("💬 Ask Our Virtual Assistant")

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
