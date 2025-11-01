# LongChain-SQL-chatbot-
LangChain SQL Chatbot with Streamlit This project is a Streamlit-based chatbot that connects to a SQLite or MySQL database and uses LangChain with Groq LLM (Llama3-8b-8192) to answer natural language queries by automatically generating and executing SQL commands.

🚀 Features 💬 Chat interface with memory support (Streamlit chat UI)

🔗 Connect to SQLite3 (student.db) or MySQL dynamically

🤖 Uses LangChain SQL Agent for intelligent SQL query generation

⚡ Powered by Groq's Llama3-8b-8192 model for fast, accurate responses

🧠 Keeps chat history with an option to clear it

🛠️ Tech Stack Python 3.9+

Streamlit

LangChain

SQLAlchemy

Groq LLM API

MySQL or SQLite3 database

⚙️ Setup Instructions 1️⃣ Clone the repository bash Copy Edit git clone https://github.com/yourusername/LangChain-SQL-Chatbot.git cd LangChain-SQL-Chatbot 2️⃣ Create a virtual environment bash Copy Edit python -m venv venv source venv/bin/activate # On macOS/Linux venv\Scripts\activate # On Windows 3️⃣ Install dependencies bash Copy Edit pip install -r requirements.txt 4️⃣ Add your Groq API key Get your API key from Groq Console

Enter it in the Streamlit sidebar after launching the app

▶️ Run the Application bash Copy Edit streamlit run app.py 🗄️ Database Options

SQLite3 (Default) Keep a file named student.db in the project folder
The app connects automatically

MySQL Database Provide connection details in the sidebar:
Host (default: localhost)

Port (default: 3306)

Username

Password

Database name (e.g., student_db)

💬 Example Queries "Show me all students with marks greater than 80."

"Who scored the highest marks?"

"Count students in class BCA."

✅ Requirements nginx Copy Edit streamlit sqlalchemy pymysql langchain langchain-groq openai 📜 License This project is licensed under the MIT License.
