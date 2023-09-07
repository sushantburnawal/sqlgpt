from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st

import environ


def ask_question(query):
    env = environ.Env()
    environ.Env.read_env()

    OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

    mssql_uri = f"mssql+pymssql://{st.secrets['DBUSER']}:{st.secrets['DBPASS']}@{st.secrets['DATABASE']}.database.windows.net:1433/{st.secrets['SERVER']}"

    db = SQLDatabase.from_uri(mssql_uri)
    gpt = OpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

    toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
    agent_executor = create_sql_agent(
        llm=gpt,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    
    try:
        st.write("Answer:\n\n",agent_executor.run(query))
    except Exception as e:
        print(e)

st.title("QueryGPT 🧳 👨🏾‍⚖️")
question_input = st.text_input("Ask a Question on the Database:")

if question_input!="":
    
    with st.spinner("Searching. Please hold..."):

        try:
            ask_question(question_input)
        except Exception as e:
            print(e)
   
        #st.write("Answer:\n\n",agent_executor.run(question_input))

