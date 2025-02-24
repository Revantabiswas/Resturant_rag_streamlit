# Restaurant AI Assistant

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

4. Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your GROQ API key:
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

- [app3.py](http://_vscodecontentref_/2): Main application file.
- [requirements.txt](http://_vscodecontentref_/3): List of dependencies.
- [restaurant_docs](http://_vscodecontentref_/4): Directory containing restaurant-related PDF documents.
- [.env](http://_vscodecontentref_/5): Environment variables file (not included in the repository).

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

