
# Restaurant AI Assistant

This project is an AI-powered restaurant assistant built using Streamlit. It leverages various AI models and libraries to provide information about the restaurant, handle reservations, and answer customer inquiries.

## Features

- **AI-Powered Responses**: Uses advanced language models to provide accurate and helpful responses.
- **Reservation Management**: Handles restaurant reservations efficiently.
- **Customer Support**: Answers questions about restaurant policies, menu, and general inquiries.
- **PDF Document Loading**: Loads and processes restaurant-related documents for better information retrieval.
- **Custom Styling**: Provides a visually appealing interface with custom CSS.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Revantabiswas/restaurant-ai-assistant.git
    cd restaurant-ai-assistant
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a .env file in the root directory and add your GROQ API key:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app3.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the application.

## Project Structure

- app3.py: Main application file.
- requirements.txt: List of dependencies.
- restaurant_docs: Directory containing restaurant-related PDF documents.
- .env: Environment variables file (not included in the repository).

## Dependencies

- Streamlit
- Python-dotenv
- CrewAI
- Langchain-groq
- Langchain-community
- PyPDF
- FAISS-cpu
- Sentence-transformers

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Restaurant AI Assistant

This project is an AI-powered restaurant assistant built using Streamlit. It leverages various AI models and libraries, including CrewAI and Groq, to provide information about the restaurant, handle reservations, and answer customer inquiries.

## Features

- **AI-Powered Responses**: Uses advanced language models to provide accurate and helpful responses.
- **Reservation Management**: Handles restaurant reservations efficiently.
- **Customer Support**: Answers questions about restaurant policies, menu, and general inquiries.
- **PDF Document Loading**: Loads and processes restaurant-related documents for better information retrieval.
- **Custom Styling**: Provides a visually appealing interface with custom CSS.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/restaurant-ai-assistant.git
    cd restaurant-ai-assistant
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a .env file in the root directory and add your GROQ API key:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app3.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the application.

## Project Structure

- app3.py: Main application file.
- requirements.txt: List of dependencies.
- restaurant_docs: Directory containing restaurant-related PDF documents.
- .env: Environment variables file (not included in the repository).

## Dependencies

- Streamlit
- Python-dotenv
- CrewAI
- Langchain-groq
- Langchain-community
- PyPDF
- FAISS-cpu
- Sentence-transformers

## Detailed Explanation

### CrewAI

CrewAI is used to manage and execute tasks with different agents. In this project, we define two agents:

- **Reservation Agent**: Handles restaurant reservations efficiently.
- **Inquiry Agent**: Provides answers about restaurant policies, menu, and general inquiries.

Each agent is created with a specific role, goal, and backstory, and uses the Groq language model for generating responses.

### Groq

Groq is an advanced language model used for generating responses. In this project, we initialize the Groq model with the following configuration:

```python
llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)
```

The Groq model is used by the agents to process tasks and generate accurate and helpful responses.

### PDF Document Loading and Vector Store

The project uses `PyPDFDirectoryLoader` to load restaurant-related PDF documents and `FAISS` to create a vector store for efficient information retrieval. The documents are split into chunks using `RecursiveCharacterTextSplitter` and embedded using `HuggingFaceEmbeddings`.

### Custom Styling

The application includes custom CSS for styling the Streamlit components, providing a visually appealing interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```

Make sure to replace `yourusername` with your actual GitHub username and `your_groq_api_key` with your actual GROQ API key.
Make sure to replace `yourusername` with your actual GitHub username and `your_groq_api_key` with your actual GROQ API key.

Revantabiswas: debug current file

GitHub Copilot: To debug the current file, you can follow these steps:

1. **Check for Errors in the Code**: Ensure there are no syntax errors or issues with the code logic.
2. **Add Debugging Statements**: Use `print` statements or Streamlit's `st.write` to output intermediate values and check the flow of the program.
3. **Run the Application**: Use the terminal to run the Streamlit application and observe the output for any errors or unexpected behavior.

Here are some debugging steps and suggestions for your app.py file:

### Step 1: Check for Errors

Ensure that all necessary libraries are installed and there are no syntax errors in the code.

### Step 2: Add Debugging Statements

Add `print` statements or `st.write` to output intermediate values and check the flow of the program.

```python
import pdfplumber
import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb  # Ensure ChromaDB is installed

# Load API Key
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key is None:
    st.error("GROQ_API_KEY is not set. Please check your environment variables.")
    st.stop()

# Initialize LLM
llm = ChatGroq(
    model="groq/gemma2-9b-it",
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
st.sidebar.image("1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

# Main Header with Background Image
st.image("2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Initialize Vector Store
if st.sidebar.button("Initialize Knowledge Base"):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        pdf_path = "restaurant_docs/menu.pdf"  # Replace with your actual PDF path
        all_text = []

        # Extract text from PDF
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)

        if not all_text:
            st.sidebar.error("No text extracted from the PDF. Please check the document and retry.")
        else:
            combined_text = "\n".join(all_text)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_documents = text_splitter.split_text(combined_text)

            # Store in ChromaDB instead of FAISS
            db = Chroma.from_texts(final_documents, embeddings, persist_directory="./chroma_db")

            # Save ChromaDB in session state
            st.session_state.vectors = db
            st.session_state.vector_ready = True
            st.sidebar.success("Knowledge Base Initialized with ChromaDB!")
    except Exception as e:
        st.sidebar.error(f"Error initializing: {e}")

# Ensure ChromaDB is loaded on app start
if "vector_ready" not in st.session_state:
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        st.session_state.vectors = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        st.session_state.vector_ready = True
    except Exception:
        st.session_state.vector_ready = False

# Define Agents
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

# Define Tasks
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

# User Input
question = st.text_input("💬 Ask a question about reservations or our menu:")
if st.button("🔍 Get Response"):
    if "vector_ready" not in st.session_state:
        st.error("⚠️ Please initialize the knowledge base first.")
    elif question:
        # Retrieve relevant context using ChromaDB
        retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        # Debugging: Print retrieved documents
        print("Retrieved Docs:", [doc.page_content for doc in relevant_docs])

        # If no relevant docs, notify user
        if not context.strip():
            st.warning("⚠️ No relevant data found in the knowledge base.")
        else:
            # Create Agents
            reservation_agent = create_reservation_agent()
            inquiry_agent = create_inquiry_agent()

            # Determine Task Type
            if "reservation" in question.lower() or "book a table" in question.lower():
                task = create_reservation_task(reservation_agent, question)
                agent = reservation_agent
            else:
                task = create_inquiry_task(inquiry_agent, question)
                agent = inquiry_agent

            # Create Crew and Execute (Pass Context Properly)
            crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
            result = crew.kickoff(inputs={"question": f"{question}\n\nContext:\n{context}"})

            st.success("✅ Answer:")
            st.info(result)
    else:
        st.warning("⚠️ Please enter a question.")
```

### Step 3: Run the Application

Use the terminal to run the Streamlit application and observe the output for any errors or unexpected behavior.

```sh
streamlit run app.py
```

Check the terminal and the Streamlit interface for any error messages or warnings. Use the debugging statements to trace the flow of the program and identify any issues.

Revantabiswas: help me make this a great looking profesional frontend on resturant reservation and inquiry system which has an chatbot for inquiry and doubts take refrences 

GitHub Copilot: Enable Claude 3.7 Sonnet Thinking (Preview) for all clients
Enable access to the latest Claude 3.7 Sonnet model from Anthropic. [Learn more about how GitHub Copilot serves Claude 3.7 Sonnet](https://docs.github.com/copilot/using-github-copilot/using-claude-sonnet-in-github-copilot).

Revantabiswas: @GitHubCopilot Enable: "Enable Claude 3.7 Sonnet Thinking (Preview) for all clients"

GitHub Copilot: # Professional Restaurant Reservation & Inquiry System Frontend

Here's how to transform your restaurant application into a professional, visually appealing system:

## 1. Enhanced UI with Custom CSS

Replace your current CSS with this more polished styling:

```python
# Replace the CSS Styles section with:

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
```

## 2. Updated Layout Structure

Replace your sidebar and header with this structured layout:

```python
# Replace the sidebar and header section with:

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
    st.image("2.jpg", use_column_width=True)
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
        st.image("https://img.icons8.com/ios-filled/50/000000/catering.png", width=50)
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
    st.title("Make a Reservation")
    
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
```

## 3. Enhanced Chatbot Interface

Improve the chatbot interface with a more visually appealing design:

```python
# Replace the chat section at the bottom with:

# Chat interface with styled container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display previous chat messages with improved styling
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🍽️"):
            st.markdown(message["content"])

# Chat input with processing
if prompt := st.chat_input("Ask about our menu, hours, or make a reservation..."):
    # Add user message to chat
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show typing indicator
    with st.chat_message("assistant", avatar="🍽️"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("*Thinking...*")
        
        if not st.session_state.get("vector_ready", False):
            response = "⚠️ Please initialize the knowledge base first using the sidebar button."
        else:
            try:
                # Retrieve context from vector store
                similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
                retrieved_context = "\n".join(
                    [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
                )
                enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"
                
                # Process based on query type
                if "reservation" in prompt.lower() or "book" in prompt.lower() or "table" in prompt.lower():
                    response_msg, llm_response = process_reservation(prompt, enhanced_question)
                    response = f"{response_msg}\n\n{llm_response}" if llm_response else response_msg
                else:
                    response = process_inquiry(enhanced_question)
            except Exception as e:
                response = f"I'm sorry, I encountered an error: {str(e)}. Please try again later."
        
        # Replace typing indicator with actual response
        typing_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)
```

## 4. Improved Mass Booking Interface

Create a more professional mass booking interface:

```python
# Replace the mass booking section with:

# Only show mass booking on the Reservations page
if page == "Reservations":
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
```

## 5. Additional Visual Assets

To complete the professional look, you should include:

1. High-quality restaurant images for:
   - Header background (replace 2.jpg)
   - Restaurant logo (replace 1.png)
   - Menu item images
   - Interior photos

2. Icons for your features (you can use icons from Font Awesome or similar services)

3. Consider adding these custom elements:

```python
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
<a href="#" class="floating-button" onclick="document.getElementById('reservation-section').scrollIntoView({behavior: 'smooth'});">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
        <path d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v1h16V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5zM16 14V5H0v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2zm-3.5-7h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5z"/>
    </svg>
    Reserve Now
</a>
""", unsafe_allow_html=True)
```

## 6. Additional Recommendations

1. **Mobile Responsiveness**: Test your app on different screen sizes
2. **Loading States**: Add loading spinners during AI operations
3. **Error Handling**: Add more user-friendly error messages
4. **Animations**: Consider adding subtle animations for element transitions
5. **Testimonials Section**: Add customer reviews on the homepage
6. **Gallery**: Add a photo gallery of your restaurant and dishes
7. **Accessibility**: Ensure your app meets accessibility guidelines

By implementing these changes, you'll have a professional-looking restaurant application with a modern, intuitive interface that enhances the user experience for both inquiries and reservations.

Similar code found with 3 license types

Revantabiswas: solve the errors in this

GitHub Copilot: I've identified several potential issues in your code. Here are the fixes:

### 1. Fix Missing ID Reference

The floating button refers to 'reservation-section' but this ID doesn't exist in your HTML:

```python
# Add this ID to your reservation section
if page == "Reservations":
    st.title("Make a Reservation", anchor="reservation-section")  # Add anchor for the floating button
```

Or fix the JavaScript reference:

```python
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
```

### 2. Ensure Image Paths Are Correct

Check your image paths:

```python
# Update image paths to use the correct relative paths
st.sidebar.image("restaurant_images/1.png", use_container_width=True)
...
st.image("restaurant_images/2.jpg", use_column_width=True)
```

### 3. Fix Knowledge Base Initialization

Ensure your utils.py initializes the session state properly:

```python
# Add this function if it's not already in your utils.py

def initialize_knowledge_base():
    """Initialize the knowledge base with restaurant data"""
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        import pdfplumber
        import os
        import streamlit as st

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        pdf_directory = "restaurant_docs"
        all_text = []

        # Check if directory exists
        if not os.path.exists(pdf_directory):
            st.sidebar.error(f"Directory {pdf_directory} not found. Creating empty directory.")
            os.makedirs(pdf_directory, exist_ok=True)
            st.session_state.vector_ready = False
            return

        # List PDF files
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
        if not pdf_files:
            st.sidebar.error(f"No PDF files found in {pdf_directory}.")
            st.session_state.vector_ready = False
            return

        # Extract text from PDFs
        for pdf_file in pdf_files:
            try:
                with pdfplumber.open(os.path.join(pdf_directory, pdf_file)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            all_text.append(text)
            except Exception as e:
                st.sidebar.warning(f"Error processing {pdf_file}: {str(e)}")

        if not all_text:
            st.sidebar.error("No text extracted from PDFs. Please check the documents and retry.")
            st.session_state.vector_ready = False
            return

        # Process text
        combined_text = "\n".join(all_text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_text(combined_text)
        
        # Create vector store
        vectors = FAISS.from_texts(final_documents, embeddings)
        st.session_state.vectors = vectors
        st.session_state.vector_ready = True
        st.sidebar.success("Knowledge Base Initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing knowledge base: {str(e)}")
        st.session_state.vector_ready = False
```

### 4. Add Session State Initialization

Add this near the beginning of your script:

```python
# Add after imports

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'vector_ready' not in st.session_state:
    st.session_state.vector_ready = False
```

### 5. Fix the `process_mass_booking` Function

Make sure this function handles errors correctly:

```python
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
```

### 6. Improve Error Handling in Chat Section

Update your chat input handling for better error management:

```python
# Replace the chat input handling section

if prompt := st.chat_input("How can I assist you today?"):
    add_message("user", prompt)
    
    try:
        if not st.session_state.get("vector_ready", False):
            response = "⚠️ Please initialize the knowledge base first using the sidebar button."
        else:
            # Show typing indicator
            with st.chat_message("assistant"):
                typing_placeholder = st.empty()
                typing_placeholder.markdown("*Thinking...*")
                
                # Get relevant context
                similar_docs = st.session_state.vectors.similarity_search(prompt, k=3)
                retrieved_context = "\n".join(
                    [doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in similar_docs]
                )
                enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{prompt}"
                
                # Process the request
                if "reservation" in prompt.lower() or "book a table" in prompt.lower():
                    response_msg, llm_response = process_reservation(prompt, enhanced_question)
                    response = f"{response_msg}\n\n{llm_response}" if llm_response else response_msg
                else:
                    response = process_inquiry(enhanced_question)
                
                # Update with real response
                typing_placeholder.markdown(response)
        
        # Add response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while processing your request: {str(e)}"
        add_message("assistant", error_msg)
```

These changes should address the main errors in your code while maintaining the professional appearance of your restaurant application frontend.

Similar code found with 2 license types

Revantabiswas: The use_column_width parameter has been deprecated and will be removed in a future release. Please utilize the use_container_width parameter instead.

GitHub Copilot: The error is related to a deprecated parameter in your Streamlit image display. Let's fix this and make a few other improvements:

```python
# Replace the line in the Hero Section:

# FROM:
st.image("2.jpg", use_column_width=True)

# TO:
st.image("2.jpg", use_container_width=True)
```

This warning appears because `use_column_width` has been deprecated in newer versions of Streamlit and will be removed in a future release. The parameter `use_container_width` is the recommended replacement with identical functionality.

### Additional improvements I recommend:

1. Add error handling for image loading:

```python
try:
    st.sidebar.image("1.png", use_container_width=True)
except FileNotFoundError:
    st.sidebar.error("Logo image not found. Please check the file path.")
    
try:
    st.image("2.jpg", use_container_width=True)
except FileNotFoundError:
    st.warning("Header image not found. Please check the file path.")
```

2. Improve the chat interface with a message count to avoid excessive messages:

```python
# Add this near the beginning of your script
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

# And modify your add_message function
def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.message_count += 1
    
    # Limit to last 20 messages to avoid performance issues
    if st.session_state.message_count > 20:
        st.session_state.messages = st.session_state.messages[-20:]
    
    with st.chat_message(role):
        st.markdown(content)
```

3. Check if external images exist and provide fallbacks:

```python
# Replace the icons with a try/except block
try:
    st.image("https://img.icons8.com/ios-filled/50/000000/dining-room.png", width=50)
except:
    st.markdown("🍽️")  # Fallback emoji
```

These changes will help prevent errors and improve the robustness of your restaurant application.

Revantabiswas: "process_mass_booking" is not definedPylancereportUndefinedVariable
(function) process_mass_booking: Any

GitHub Copilot: The error message `"process_mass_booking" is not defined` indicates that you're trying to use the function before it's defined in your code. Python reads code from top to bottom, so you need to define functions before using them.

You have two options to fix this:

### Option 1: Move the function definition up (Recommended)

Move the `process_mass_booking` function definition to the top of your file, right after your other function definitions:

```python
# Add this after your imports and before the session state initialization

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

# Continue with your existing code...
# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
```

### Option 2: Define utility functions in a separate file

A better practice for larger applications is to organize your code by moving utility functions to separate files:

```python
# Create this new file with the function

import streamlit as st
from crewai import Agent, Task, Crew, Process
from database import add_booking

def process_mass_booking(selected_dates, number_of_people, base_booking_text, 
                         create_reservation_agent, create_reservation_task):
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
```

Then import it in your main.py:

```python
# Add to your imports at the top
from booking_utils import process_mass_booking
```

The first option is simpler for now, but the second approach will help keep your code more maintainable as your application grows.

Revantabiswas: change reserve now side button text from blue to white

GitHub Copilot: To change the "Reserve Now" floating button text from blue to white, you need to make the CSS styling more specific for the anchor tag. The current CSS rule is being overridden by the default browser styling for links.

Here's how to fix it:

```python
# Replace the Floating Button CSS section with this updated version:

        /* Floating Button */
        .floating-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: var(--primary);
            color: white !important;
            padding: 15px 20px;
            border-radius: 50px;
            text-decoration: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 999;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        .floating-button:hover,
        .floating-button:visited,
        .floating-button:active {
            color: white !important;
            text-decoration: none !important;
        }
        .floating-button:hover {
            background-color: var(--accent);
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        }
```

The key changes are:
1. Added `!important` to the color property to ensure it overrides any browser defaults
2. Added explicit styles for link states (`:visited`, `:active`)
3. Added `text-decoration: none !important` to remove any underlines
4. Used the same approach for the hover state

These changes will force the text to appear white in all link states, overriding the default blue browser styling.

Revantabiswas: create a new github readme file for the project

GitHub Copilot: # Indian Palace Restaurant AI Assistant

![Restaurant Banner](https://img.shields.io/badge/Indian%20Palace-Restaurant%20AI%20Assistant-orange)

An AI-powered restaurant reservation and inquiry system built with Streamlit, CrewAI, and Groq. This application provides a professional interface for customers to make reservations, explore the menu, and interact with an AI assistant for information about the restaurant.

## ✨ Features

### 🍽️ Reservation System
- **Individual Bookings**: Easy reservation form with date, time and party size selection
- **Group Bookings**: Special form for events and large parties across multiple dates
- **Availability Checker**: Real-time seat availability by date and time slot

### 🧠 AI-Powered Assistant
- **CrewAI Integration**: Specialized agents handle different types of customer interactions
  - Reservation Agent: Processes booking requests intelligently
  - Inquiry Agent: Answers questions about menu, policies, and general information
- **Groq LLM**: Utilizes advanced Llama 3 8B model for natural language understanding
- **RAG System**: Retrieves relevant restaurant information to provide accurate responses

### 🥘 Menu Management
- Categorized display of restaurant offerings
- Visually appealing menu item cards with images and descriptions
- Easy navigation between different menu sections

### 🎨 Professional UI
- Custom styled interface with restaurant branding
- Responsive design that works on desktop and mobile
- Intuitive navigation and user experience

## 📋 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/indian-palace-assistant.git
   cd indian-palace-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a .env file in the project root with:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Prepare restaurant documents**
   - Create a folder named restaurant_docs
   - Add PDF documents containing menu, policies, and other restaurant information

## 🚀 Usage

1. **Run the application**
   ```bash
   streamlit run main.py
   ```

2. **Initialize the knowledge base**
   - Navigate to the application in your browser (typically http://localhost:8501)
   - Open the sidebar and expand "Admin Options"
   - Click "Initialize Knowledge Base"

3. **Explore the features**
   - Browse the restaurant menu
   - Check table availability
   - Make reservations
   - Use the AI assistant to ask questions

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. Database initialization and schema are handled in the database.py file.

### AI Model Configuration
The application is configured to use the Groq Llama 3 8B model. You can modify this in the `initialize_app()` function:

```python
return ChatGroq(model="groq/llama3-8b-8192", api_key=groq_api_key)
```

### Restaurant Capacity
You can adjust the restaurant's maximum capacity in the utils.py file.

## 📁 Project Structure

- main.py: Main application file with UI components and core functionality
- agents.py: Defines CrewAI agents and tasks
- database.py: Database operations for reservation management
- utils.py: Utility functions including knowledge base initialization
- restaurant_docs: Directory containing restaurant PDFs for the knowledge base
- .env: Environment variables (not tracked in git)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Project Link: [https://github.com/yourusername/indian-palace-assistant](https://github.com/Revantabiswas/indian-palace-assistant)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Groq](https://groq.com/)
- [LangChain](https://langchain.com/)

Similar code found with 2 license types
