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

def is_api_key_valid():
    # try:
    #     response = openai.Completion.create(
    #         engine="davinci",
    #         prompt="This is a test.",
    #         max_tokens=5
    #     )
    #     print(response)
    # except:
    #     print('1')
    #     return False
    # print('2')
    return True
def ask_question(api_key,query):
    env = environ.Env()
    environ.Env.read_env()
    

    #OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

    mssql_uri = f"mssql+pymssql://{env('DBUSER')}:{env('DBPASS')}@{env('DATABASE')}.database.windows.net:1433/{env('SERVER')}"
    try:
        db = SQLDatabase.from_uri(mssql_uri)
    except Exception as e:
        st.write(e)
    gpt = ChatOpenAI(openai_api_key=api_key, model_name='gpt-4')

    toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
    agent_executor = create_sql_agent(
        llm=gpt,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
    
    try:
        st.write("Answer:\n\n",agent_executor.run(query))
    except Exception as e:
        print(e)

st.title("QueryGPT 🧳 👨🏾‍⚖️")
api_key = st.text_input("OpenAI API Key:")
if is_api_key_valid():
    question_input = st.text_input("Ask a Question on the Database:")

    if question_input!="":
        
        with st.spinner("Searching. Please hold..."):

            try:
                ask_question(api_key,question_input)
            except Exception as e:
                print(e)
else :
    st.warning("Invalid API Key",icon="⚠️")

   
        #st.write("Answer:\n\n",agent_executor.run(question_input))

