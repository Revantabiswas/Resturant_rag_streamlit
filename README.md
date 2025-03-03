# Indian Palace Restaurant AI Assistant

![Restaurant Banner](https://img.shields.io/badge/Indian%20Palace-Restaurant%20AI%20Assistant-orange)

An AI-powered restaurant reservation and inquiry system built with Streamlit, CrewAI, and Groq. This application provides a professional interface for customers to make reservations, explore the menu, and interact with an AI assistant for information about the restaurant.

## Features

- **AI-Powered Responses**: Uses advanced language models to provide accurate and helpful responses.
- **Reservation Management**: Handles restaurant reservations efficiently.
- **Customer Support**: Answers questions about restaurant policies, menu, and general inquiries.
- **PDF Document Loading**: Loads and processes restaurant-related documents for better information retrieval.
- **Custom Styling**: Provides a visually appealing interface with custom CSS.

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
   git clone https://github.com/Revantabiswas/Resturant_rag_streamlit.git
   cd Resturant_rag_streamlit
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

Project Link: (https://github.com/Revantabiswas/Resturant_rag_streamlit)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Groq](https://groq.com/)
- [LangChain](https://langchain.com/)

