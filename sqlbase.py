from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
import environ
import openai

import requests

def is_openai_api_key_valid(api_key):
    """
    Check if an OpenAI API key is valid by making a simple request to the API.

    Args:
        api_key (str): The OpenAI API key to be checked.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    # Define the API endpoint you want to test
    api_endpoint = "https://api.openai.com/v1/models"

    # Set up the request headers with the API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        # Make a GET request to the API
        print(1)
        response = requests.get(api_endpoint, headers=headers)
        print(response)
        print(2)
        # Check the response status code
        if response.status_code == 200:
            return True  # API key is valid
        else:
            return False  # API key is invalid

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False  # An error occurred, assume the key is invalid

def ask_question(api_key,query):
    env = environ.Env()
    environ.Env.read_env()
    

    #OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

    mssql_uri = f"mssql+pymssql://{env('DBUSER')}:{env('DBPASS')}@{env('DATABASE')}.database.windows.net:1433/{env('SERVER')}"
    try:
        db = SQLDatabase.from_uri(mssql_uri)
    except Exception as e:
        st.warning("Error Connecting to Database",icon="🚨")
    gpt = ChatOpenAI(openai_api_key=api_key, model_name='gpt-3.5-turbo-16k')

    toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
    agent_executor = create_sql_agent(
        llm=gpt,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
    
    try:
        st.write("Answer:\n\n",agent_executor.run(query))
    except Exception as e:
        response = str(e)
        if not response.startswith("Could not parse LLM output: `"):
            raise e
        response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")

st.title("QueryGPT 🧳 👨🏾‍⚖️")
api_key = st.text_input("OpenAI API Key:")
question_input = st.text_input("Ask a Question on the Database:")
if st.button("Submit Question"):
    #question_input = st.text_input("Ask a Question on the Database:")
    if is_openai_api_key_valid(api_key):
        if question_input!="":
            
            with st.spinner("Searching. Please hold..."):

                try:
                    ask_question(api_key,question_input)
                except Exception as e:
                    print(e)
        else:
            st.warning("Question cannot be empty",icon="⚠️")
    else :
        st.warning("Invalid API Key",icon="⚠️")

   
        #st.write("Answer:\n\n",agent_executor.run(question_input))

