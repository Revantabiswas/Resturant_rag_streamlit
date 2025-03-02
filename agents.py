import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

# Load API key directly from environment
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Validate API key
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file or environment variables.")

# Initialize LLM with explicit API key
llm = ChatGroq(
    model="groq/llama3-8b-8192",
    api_key=groq_api_key
)

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
