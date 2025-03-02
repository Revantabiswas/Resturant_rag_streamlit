import pdfplumber
import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

# Load API Key with better error handling
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Display API key status (for debugging, remove in production)
if not groq_api_key:
    st.error("GROQ_API_KEY is not set in your environment variables or .env file.")
    st.info("Please create a .env file in the root directory with your GROQ_API_KEY or set it as an environment variable.")
    st.code("GROQ_API_KEY=your-api-key-here", language="text")
    st.stop()

# Initialize LLM with explicit API key
try:
    llm = ChatGroq(
        model="groq/llama3-8b-8192",
        api_key=groq_api_key
    )
except Exception as e:
    st.error(f"Error initializing Groq LLM: {str(e)}")
    st.stop()

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
st.sidebar.image("Resturant_rag_streamlit\\1.png", use_container_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

# Main Header with Background Image
st.image("Resturant_rag_streamlit\\2.jpg", use_container_width=True)
st.title("🍽️ Welcome To Indian Palace")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Initialize Vector Store
if st.sidebar.button("Initialize Knowledge Base"):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        pdf_directory = "Resturant_rag_streamlit\\restaurant_docs"
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
        # Retrieve relevant context from the vector store
        similar_docs = st.session_state.vectors.similarity_search(question, k=3)
        # Combine retrieved contexts into one string. Use .page_content if available.
        retrieved_context = "\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in similar_docs])
        
        # Inject the retrieved context into the prompt
        enhanced_question = f"Context:\n{retrieved_context}\n\nQuestion:\n{question}"

        # Create Agents
        reservation_agent = create_reservation_agent()
        inquiry_agent = create_inquiry_agent()

        # Determine Task Type
        if "reservation" in question.lower() or "book a table" in question.lower():
            task = create_reservation_task(reservation_agent, enhanced_question)
            agent = reservation_agent
        else:
            task = create_inquiry_task(inquiry_agent, enhanced_question)
            agent = inquiry_agent

        # Create Crew and Execute
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"question": enhanced_question})
        
        st.success("✅ Answer:")
        st.info(result)
    else:
        st.warning("⚠️ Please enter a question.")
