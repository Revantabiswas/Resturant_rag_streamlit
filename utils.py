import os
import pdfplumber
import re
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

def load_environment():
    load_dotenv()

def get_max_capacity():
    """Return the maximum restaurant capacity"""
    # You can hardcode this value or store it in a configuration file
    return 50  # Default restaurant capacity

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
