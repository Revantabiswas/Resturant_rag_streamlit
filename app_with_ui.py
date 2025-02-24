import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

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
        }
        .stTitle {
            color: #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.image("https://source.unsplash.com/400x200/?restaurant,dining", use_column_width=True)
st.sidebar.title("Navigation")
st.sidebar.markdown("👋 Welcome to the AI-powered Restaurant Assistant!")

# Main Header with Background Image
st.image("https://source.unsplash.com/1200x400/?restaurant,food", use_column_width=True)
st.title("🍽️ Restaurant Reservation & Inquiry System")
st.markdown("**Ask anything about our restaurant, menu, and reservations!**")

# Initialize Vector Store
if st.sidebar.button("Initialize Knowledge Base"):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        loader = PyPDFDirectoryLoader("rest_rag/restaurant_docs")
        docs = loader.load()

        if not docs:
            st.sidebar.error("No PDFs found. Please add documents and retry.")
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_documents = text_splitter.split_documents(docs)
            vectors = FAISS.from_documents(final_documents, embeddings)
            st.session_state.vectors = vectors
            st.session_state.vector_ready = True
            st.sidebar.success("Knowledge Base Initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing: {e}")

# Define Agents

def create_reservation_agent():
    return Agent(
        role="Reservation Manager",
        goal="Handle table bookings efficiently.",
        backstory="Expert in managing restaurant reservations.",
        llm=llm,
        verbose=True
    )

def create_inquiry_agent():
    return Agent(
        role="Customer Support",
        goal="Answer restaurant-related questions.",
        backstory="Knows the menu, policies, and services.",
        llm=llm,
        verbose=True
    )

# User Input
question = st.text_input("💬 Ask a question about reservations or our menu:")
if st.button("🔍 Get Response"):
    if "vector_ready" not in st.session_state:
        st.error("⚠️ Please initialize the knowledge base first.")
    elif question:
        reservation_agent = create_reservation_agent()
        inquiry_agent = create_inquiry_agent()
        
        if "reservation" in question.lower() or "book" in question.lower():
            task = Task(
                description=f"Process reservation: {question}",
                expected_output="Confirm reservation status.",
                agent=reservation_agent
            )
            agent = reservation_agent
        else:
            task = Task(
                description=f"Answer customer inquiry: {question}",
                expected_output="Provide details on the restaurant.",
                agent=inquiry_agent
            )
            agent = inquiry_agent
        
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"question": question})
        st.success("✅ Answer:")
        st.info(result)
    else:
        st.warning("⚠️ Please enter a question.")
