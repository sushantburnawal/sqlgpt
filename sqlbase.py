from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

mssql_uri = f"mssql+pymssql://sushant:Solarsystem$123@sqlgpt.database.windows.net:1433/sqlgpt"

db = SQLDatabase.from_uri(mssql_uri)

OPENAI_API_KEY = "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"
gpt = OpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
agent_executor = create_sql_agent(
    llm=gpt,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

question = "Total number of users in the database"
agent_executor.run(question)
