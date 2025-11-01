import streamlit as st
from pathlib import Path
import sqlite3
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
import pymysql

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon=":robot_face:")
st.title("LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar selection
radio_opt = ["Use SQLite3 Database - student.db", "Connect to your MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host", "localhost")
    mysql_port = st.sidebar.text_input("MySQL Port", "3306")
    mysql_user = st.sidebar.text_input("MySQL User", "root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database", "student_db")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input(label="GROQ API Key", type="password")

if not api_key:
    st.info("Please enter your GROQ API Key to proceed.")

# LLM Model
llm = ChatGroq(
    groq_api_key=api_key,
    streaming=True,
    model="Llama3-8b-8192"
)

# Database configuration
@st.cache_resource(ttl=7200)
def configure_db(db_uri, mysql_host=None, mysql_port=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        db_path = (Path(__file__).parent / "student.db").absolute()
        print(f"Connecting to local SQLite database at {db_path}")
        create = lambda: sqlite3.connect(db_path)
        return SQLDatabase(create_engine("sqlite://", creator=create))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(
            create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}")
        )
    else:
        return None

db = configure_db(db_uri,
                  mysql_host if db_uri == MYSQL else None,
                  mysql_port if db_uri == MYSQL else None,
                  mysql_user if db_uri == MYSQL else None,
                  mysql_password if db_uri == MYSQL else None,
                  mysql_db if db_uri == MYSQL else None)

# Create toolkit and agent
if db:
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

# Initialize chat history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display previous chat messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User query input
user_query = st.chat_input(placeholder="Ask anything from the database")

# Handle user query
if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.write(response)
