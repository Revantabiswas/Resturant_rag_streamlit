import os
import re
from datetime import datetime, timedelta
import streamlit as st
from dotenv import load_dotenv
from database import init_db, add_booking, get_bookings, check_availability
from agents import create_reservation_agent, create_inquiry_agent, create_reservation_task, create_inquiry_task
from utils import load_environment, get_max_capacity, initialize_knowledge_base
from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew, Process

# ---------- CONFIGURATION AND SETUP ----------
def initialize_app():
    """Initialize the application state and configuration"""
    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'vector_ready' not in st.session_state:
        st.session_state.vector_ready = False

    # Load environment variables
    load_dotenv('.env')
    load_environment()

    # Initialize database
    init_db()

    # Configure LangChain LLM
    groq_api_key = os.getenv('GROQ_API_KEY')
    return ChatGroq(model="groq/llama3-8b-8192", api_key=groq_api_key)

# ---------- HELPER FUNCTIONS ----------
def process_mass_booking(selected_dates, time_slot, number_of_people, group_name, contact_person, contact_email, event_type, special_requirements):
    """Process multiple bookings for group events"""
    successful_dates = []
    failed_dates = []
    
    try:
        for date in selected_dates:
            # Check availability first
            is_available, _ = check_availability(date, time_slot, number_of_people)
            
            if is_available:
                # Add booking to database
                add_booking(
                    date=date,
                    time=time_slot,
                    guests=number_of_people,
                    name=group_name,
                    email=contact_email,
                    special_requests=f"Event Type: {event_type}. {special_requirements}"
                )
                successful_dates.append(date)
            else:
                failed_dates.append(date)
                
        return successful_dates, failed_dates
    except Exception as e:
        st.error(f"Error processing bookings: {str(e)}")
        return successful_dates, failed_dates

def add_message(role: str, content: str):
    """Add a message to the chat history"""
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

def process_reservation(prompt: str, enhanced_question: str):
    """Process a reservation request from the chatbot"""
    # Extract booking details
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', prompt)
    booking_date = date_match.group(1) if date_match else (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    num_match = re.search(r'\b(\d+)\b', prompt)
    number_of_people = int(num_match.group(1)) if num_match else 2
    
    # Try to extract time, otherwise use default
    time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm|AM|PM)', prompt)
    booking_time = time_match.group(0) if time_match else "7:00 PM"  # Default time
    
    # Standardize time format
    if ":" not in booking_time:
        booking_time = booking_time.replace(" ", ":00 ")

    # Capacity check
    MAX_CAPACITY = get_max_capacity()
    existing_bookings = get_bookings()
    total_guests = sum(b[2] for b in existing_bookings if b[1] == booking_date)

    if total_guests + number_of_people > MAX_CAPACITY:
        return f"Sorry, we are fully booked for {booking_date} (Max capacity: {MAX_CAPACITY} guests). Please choose another date or reduce the party size.", None

    # Fix: Include all required parameters for add_booking
    add_booking(
        date=booking_date,
        time=booking_time,
        guests=number_of_people,
        name="Chat Reservation", 
        email="",
        phone="",
        special_requests="Booked via chatbot"
    )
    
    confirmation = f"Reservation recorded for {number_of_people} people on {booking_date} at {booking_time}."
    reservation_agent = create_reservation_agent()
    task = create_reservation_task(reservation_agent, enhanced_question)
    crew = Crew(agents=[reservation_agent], tasks=[task], process=Process.sequential, verbose=True)
    return confirmation, crew.kickoff(inputs={"question": enhanced_question})

def process_inquiry(enhanced_question: str):
    """Process a general inquiry from the chatbot"""
    inquiry_agent = create_inquiry_agent()
    task = create_inquiry_task(inquiry_agent, enhanced_question)
    crew = Crew(agents=[inquiry_agent], tasks=[task], process=Process.sequential, verbose=True)
    return crew.kickoff(inputs={"question": enhanced_question})

# ---------- UI COMPONENTS ----------
def load_css():
    """Load CSS styles for the application"""
    st.markdown("""
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
        
        /* Cards & Components */
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
        
        /* UI Elements */
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
        
        /* Floating Button */
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

        .left-align {
            padding-left: 0;
            margin-left: 0;
        }
    </style>
    
    <!-- Import custom fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
    
    <!-- Reserve Now button -->
    <a href="#reservation-section" class="floating-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM16 14V5H0v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zm-3.5-7h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5z"/>
        </svg>
        Reserve Now
    </a>
    """, unsafe_allow_html=True)

def setup_sidebar():
    """Set up the sidebar navigation and options"""
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
    
    return page

# ---------- PAGE COMPONENTS ----------
def render_home_page():
    """Render the Home page content"""
    # Hero Section
    st.markdown('<div class="restaurant-header">', unsafe_allow_html=True)
    st.image("2.jpg", use_container_width=True)
    st.title("🍽️ Welcome to Indian Palace")
    st.markdown("**Experience authentic Indian cuisine in the heart of the city**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # About Section
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="left-align">', unsafe_allow_html=True)
        st.markdown("### Our Story")
        st.write("""
        At Indian Palace, we bring the rich flavors of India to your table. 
        Established in 2010, our restaurant combines traditional cooking techniques 
        with the finest ingredients to create an unforgettable dining experience.
        
        Our chefs come from different regions of India, each bringing their own unique 
        expertise and recipes passed down through generations.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### What We Offer")
    col1, col2, col3 = st.columns(3)
    
    # Feature 1: Elegant Dining
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios-filled/50/000000/dining-room.png", width=50)
        st.markdown("#### Elegant Dining")
        st.write("Our restaurant offers a warm, elegant atmosphere perfect for any occasion.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature 2: Authentic Cuisine    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios-filled/50/000000/food-and-wine.png", width=50)
        st.markdown("#### Authentic Cuisine")
        st.write("Experience the true flavors of India with our authentic recipes.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature 3: Private Events
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/?size=100&id=9KPN5HvQHsvg&format=png&color=000000", width=50)
        st.markdown("#### Private Events")
        st.write("Host your special events with us for an unforgettable experience.")
        st.markdown('</div>', unsafe_allow_html=True)

def render_menu_page():
    """Render the Menu page content"""
    st.title("Our Menu")
    
    # Menu Tabs
    menu_tab1, menu_tab2, menu_tab3, menu_tab4 = st.tabs(["Appetizers", "Main Course", "Desserts", "Beverages"])
    
    # Appetizers Tab
    with menu_tab1:
        render_menu_item(
            image_url="https://www.indianhealthyrecipes.com/wp-content/uploads/2021/12/samosa-recipe.jpg",
            name="Vegetable Samosas",
            description="Crispy pastry filled with spiced potatoes and peas",
            price="$6.99"
        )
        
        render_menu_item(
            image_url="https://www.kitchensanctuary.com/wp-content/uploads/2021/01/Onion-Bhaji-square-FS-23.jpg",
            name="Onion Bhaji",
            description="Crispy onion fritters with chickpea flour and spices",
            price="$5.99"
        )

def render_menu_item(image_url, name, description, price):
    """Helper function to render a menu item card"""
    st.markdown('<div class="menu-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_url, width=100)
    with col2:
        st.markdown(f"### {name}")
        st.write(description)
        st.write(f"**{price}**")
    st.markdown('</div>', unsafe_allow_html=True)

def render_reservation_page():
    """Render the Reservations page content"""
    st.title("Make a Reservation", anchor="reservation-section") 
    
    # Reservation Tabs
    res_tab1, res_tab2 = st.tabs(["New Reservation", "Check Availability"])
    
    # New Reservation Tab
    with res_tab1:
        render_new_reservation_form()

    # Check Availability Tab
    with res_tab2:
        render_availability_checker()

    # Group & Event Reservations
    with st.expander("Group & Event Reservations"):
        render_group_booking_form()

def render_new_reservation_form():
    """Render the new reservation form"""
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
        
        process_reservation_submission(submit_button, name, email, phone, date, time, guests, special_requests)
    st.markdown('</div>', unsafe_allow_html=True)

def process_reservation_submission(submit_button, name, email, phone, date, time, guests, special_requests):
    """Process the reservation form submission"""
    if submit_button:
        if name and email and phone:
            # Check availability first
            date_str = date.strftime('%Y-%m-%d')
            is_available, seats_left = check_availability(date_str, time, guests)
            
            if is_available:
                # Add booking with all details
                add_booking(
                    date=date_str,
                    time=time,
                    guests=guests,
                    name=name,
                    email=email,
                    phone=phone,
                    special_requests=special_requests
                )
                st.success(f"Reservation confirmed for {name} on {date_str} at {time} for {guests} guests.")
            else:
                st.error(f"Sorry, we don't have enough space for {guests} guests at {time}. We have {seats_left} seats left at that time.")
        else:
            st.error("Please fill out all required fields.")

def render_availability_checker():
    """Render the availability checker"""
    st.markdown('<div class="reservation-card">', unsafe_allow_html=True)
    st.subheader("Check Table Availability")
    check_date = st.date_input("Select Date", key="check_date")
    
    # Get bookings for the selected date
    date_str = check_date.strftime('%Y-%m-%d')
    existing_bookings = get_bookings(date=date_str)
    
    # Calculate total guests for the day
    total_guests = sum(booking[3] for booking in existing_bookings) if existing_bookings else 0
    max_capacity = get_max_capacity()
    
    # Display availability stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Reserved Seats", total_guests)
    with col2:
        st.metric("Total Capacity", max_capacity)
        
    # Show availability by time slot
    display_time_slot_availability(existing_bookings, max_capacity)
    st.markdown('</div>', unsafe_allow_html=True)

def display_time_slot_availability(existing_bookings, max_capacity):
    """Display availability for each time slot"""
    st.subheader("Availability by Time")
    times = ["5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM"]
    
    for time_slot in times:
        # Get bookings for this specific time slot
        time_bookings = [b for b in existing_bookings if b[2] == time_slot]
        time_guests = sum(b[3] for b in time_bookings) if time_bookings else 0
        seats_left = max_capacity - time_guests
        
        # Determine availability status
        if seats_left >= 10:
            status = "Available"
            color = "green"
        elif seats_left > 0:
            status = f"Limited ({seats_left} seats)"
            color = "orange"
        else:
            status = "Fully Booked"
            color = "red"
        
        st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                  f"<span>{time_slot}</span>"
                  f"<span style='color: {color};'>{status}</span>"
                  f"</div>", unsafe_allow_html=True)

def render_group_booking_form():
    """Render the group booking form"""
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
                                            min_value=1, max_value=50, value=10)
            event_type = st.selectbox("Event Type", 
                                    ["Corporate Meeting", "Birthday Party", "Wedding Reception", 
                                    "Anniversary", "Other"])
            time_slot = st.selectbox("Preferred Time", 
                                    ["5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"], 
                                    key="group_time")
        
        # Calendar selector
        st.subheader("Select Dates")
        available_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 15)]
        selected_dates = st.multiselect("Select all dates needed:", available_dates)
        
        # Special requirements
        special_requirements = st.text_area("Special Requirements or Notes",
                                        placeholder="Please let us know about any dietary restrictions, room setup preferences, or other special needs.")
        
        submit_group = st.form_submit_button("📅 Request Group Booking")
        
        process_group_booking_submission(submit_group, selected_dates, group_name, contact_person, contact_email,
                                         time_slot, number_of_people, event_type, special_requirements)
    st.markdown('</div>', unsafe_allow_html=True)

def process_group_booking_submission(submit_group, selected_dates, group_name, contact_person, contact_email,
                                    time_slot, number_of_people, event_type, special_requirements):
    """Process the group booking form submission"""
    if submit_group and selected_dates and group_name and contact_person and contact_email:
        successful_dates, failed_dates = process_mass_booking(
            selected_dates, 
            time_slot,
            number_of_people, 
            group_name, 
            contact_person, 
            contact_email,
            event_type,
            special_requirements
        )
        
        if successful_dates:
            st.success(f"Successfully booked: {', '.join(successful_dates)}")
        
        if failed_dates:
            st.error(f"No availability for these dates: {', '.join(failed_dates)}")
    elif submit_group:
        st.warning("Please fill out all required fields and select at least one date.")

def render_contact_page():
    """Render the Contact page content"""
    st.title("Contact Us")
    
    col1, col2 = st.columns(2)
    
    # Contact Information
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
    
    # Contact Form
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Send Us a Message")
        with st.form("contact_form"):
            st.text_input("Name", key="contact_name")
            st.text_input("Email", key="contact_email")
            st.text_area("Message", key="contact_message")
            if st.form_submit_button("Send Message"):
                st.success("Message sent! We'll get back to you soon.")
        st.markdown('</div>', unsafe_allow_html=True)

def render_chatbot():
    """Render the chatbot section"""
    st.markdown("---")
    st.subheader("💬 Ask Our Virtual Assistant")

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I assist you today?"):
        add_message("user", prompt)
        
        if not st.session_state.get("vector_ready", False):
            response = "⚠️ Please initialize the knowledge base first using the sidebar button."
            add_message("assistant", response)
        else:
            # Get context from vector database
            similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
            retrieved_context = "\n".join(
                [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
            )
            enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"
            
            # Process based on query type
            if "reservation" in prompt.lower() or "book a table" in prompt.lower():
                response_msg, llm_response = process_reservation(prompt, enhanced_question)
                add_message("assistant", response_msg)
                if llm_response:
                    add_message("assistant", llm_response)
            else:
                response = process_inquiry(enhanced_question)
                add_message("assistant", response)

# ---------- MAIN APP ----------
def main():
    """Main application entry point"""
    llm = initialize_app()
    load_css()
    page = setup_sidebar()
    
    # Render appropriate page based on navigation
    if page == "Home":
        render_home_page()
    elif page == "Menu":
        render_menu_page()
    elif page == "Reservations":
        render_reservation_page()
    elif page == "Contact":
        render_contact_page()
    
    # Always render chatbot
    render_chatbot()

if __name__ == "__main__":
    main()
