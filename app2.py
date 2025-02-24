import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

import os


load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key is None:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize LLM with Groq
llm = ChatGroq(
    model="groq/llama3-8b-8192",  # Specify the provider and model
    api_key=groq_api_key
)

# Streamlit UI
st.title("Restaurant Reservation & Inquiry System")

# Initialize Vector Database with Hugging Face Embeddings
def setup_vector_store():
    if "vectors" not in st.session_state:
        try:
            # Use Hugging Face Sentence Transformers for embedding
            st.session_state.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            
            # Load restaurant-related documents
            st.session_state.loader = PyPDFDirectoryLoader("rest_rag\\restaurant_docs")  # Directory with restaurant PDFs
            st.session_state.docs = st.session_state.loader.load()
            
            # Check if documents are loaded
            if not st.session_state.docs:
                st.error("No documents found in ./restaurant_docs. Please add PDFs and try again.")
                return
            
            # Split documents into smaller chunks
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(
                st.session_state.docs[:20] if len(st.session_state.docs) >= 20 else st.session_state.docs
            )

            # Check if there are any final documents after splitting
            if not st.session_state.final_documents:
                st.error("Document splitting failed. Ensure your PDFs contain readable text.")
                return
            
            # Create FAISS vector store
            st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
            st.session_state.vector_ready = True
            st.success("Knowledge Base is Ready!")
        except Exception as e:
            st.error(f"Error during vector embedding: {str(e)}")

if st.button("Initialize Knowledge Base"):
    setup_vector_store()

# Define Reservation Agent
def create_reservation_agent():
    return Agent(
        role="Reservation Manager",
        goal="Handle restaurant reservations efficiently.",
        backstory="You are responsible for taking reservations, checking table availability, and managing booking requests.",
        llm=llm,
        verbose=True
    )

# Define Inquiry Agent
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
question = st.text_input("Enter your question (Reservation or Inquiry):")

if st.button("Get Response"):
    if "vector_ready" not in st.session_state:
        st.error("Please initialize the knowledge base first.")
    elif question:
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

        # Create Crew and Execute
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"question": question})

        # Display Answer
        st.write("Answer:", result)
    else:
        st.warning("Please enter a question.")
