import os
import chainlit as cl
from crewai import Agent, Task, Crew
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM (Groq)
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Set it in the .env file.")

llm = ChatGroq(
    model="groq/llama3-8b-8192",  # Specify the provider and model
    api_key=groq_api_key
)

# Function to set up FAISS Vector Store
def setup_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    loader = PyPDFDirectoryLoader("rest_rag\\restaurant_docs")  # Ensure this directory exists
    docs = loader.load()

    if not docs:
        raise ValueError("No restaurant-related PDFs found in './restaurant_docs'.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs[:20] if len(docs) >= 20 else docs)

    if not final_documents:
        raise ValueError("Document splitting failed. Ensure PDFs contain readable text.")

    return FAISS.from_documents(final_documents, embeddings)

# Initialize Vector Store
vector_store = setup_vector_store()
retriever = vector_store.as_retriever()

# CrewAI Agents
reservation_agent = Agent(
    role="Reservation Specialist",
    goal="Assist customers with booking tables and managing reservations.",
    backstory="An experienced staff member handling customer reservations efficiently.",
    memory=True,
    verbose=True,
    llm=llm,
    system_message="You are a friendly restaurant reservation assistant. Answer inquiries clearly and professionally.",
)

menu_agent = Agent(
    role="Menu Expert",
    goal="Provide detailed information about the restaurant menu.",
    backstory="A culinary specialist familiar with all menu items, ingredients, and dietary options.",
    memory=True,
    verbose=True,
    llm=llm,
    system_message="You are a helpful assistant providing menu details, ingredients, and recommendations.",
)

policy_agent = Agent(
    role="Policy Advisor",
    goal="Explain restaurant policies clearly to customers.",
    backstory="A well-trained staff member knowledgeable about restaurant policies, including reservations, cancellations, and seating rules.",
    memory=True,
    verbose=True,
    llm=llm,
    system_message="You provide accurate information about restaurant policies in a clear and friendly manner.",
)

# Tasks for each agent
reservation_task = Task(
    description="Handle customer inquiries related to restaurant reservations.",
    expected_output="A clear response regarding available tables, booking process, and confirmation.",
    agent=reservation_agent,
)

menu_task = Task(
    description="Answer questions related to the restaurant's menu, including dish details and dietary options.",
    expected_output="A detailed and engaging response about menu items, ingredients, and availability.",
    agent=menu_agent,
)

policy_task = Task(
    description="Provide customers with restaurant policies on reservations, cancellations, and seating.",
    expected_output="A clear explanation of restaurant policies in simple terms.",
    agent=policy_agent,
)

# Crew to manage agents
restaurant_crew = Crew(
    agents=[reservation_agent, menu_agent, policy_agent],
    tasks=[reservation_task, menu_task, policy_task],
    verbose=True,
)

# Chainlit Chat Interface
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="🍽️ Welcome to our restaurant assistance chat! How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    question = message.content
    msg = cl.Message(content="🔍 Checking restaurant information...")
    await msg.send()

    # Determine the best agent for the task
    if "book" in question.lower() or "reserve" in question.lower():
        selected_task = reservation_task
    elif "menu" in question.lower() or "food" in question.lower():
        selected_task = menu_task
    elif "policy" in question.lower() or "rules" in question.lower():
        selected_task = policy_task
    else:
        selected_task = None

    if selected_task:
        response = selected_task.execute({"query": question})
        answer = response.get("raw", "Sorry, I couldn't find relevant information.")
    else:
        response = restaurant_crew.kickoff(inputs={"query": question})
        answer = response.get("raw", "I'm not sure, but I can check for you.")

    # Send the response
    await cl.Message(content=answer).send()

if __name__ == "__main__":
    cl.run()
