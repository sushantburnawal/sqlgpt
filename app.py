from flask import Flask, request, jsonify, render_template
import openai
import os
from langchain.agents import create_sql_agent 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.llms.openai import OpenAI 
from langchain.agents import AgentExecutor 
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
import environ
# Set up Flask app and OpenAI API key
app = Flask(__name__)

# Define route to render HTML template
@app.route("/")
def home():
    return render_template("index.html")

# Define route for API endpoint
@app.route("/api", methods=["POST"])
def api():
    env = environ.Env()
    environ.Env.read_env()
    # Get question from form data
    query = request.json["question"]
    
    
    
    mssql_uri = f"mssql+pymssql://{env('DBUSER')}:{env('DBPASS')}@{env('DATABASE')}.database.windows.net:1433/{env('SERVER')}"
    try:
        db = SQLDatabase.from_uri(mssql_uri)
    except Exception as e:
        return jsonify({"error": e})
    gpt = ChatOpenAI(openai_api_key=env('OPENAI_API_KEY'), model_name='gpt-4')

    toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
    agent_executor = create_sql_agent(
        llm=gpt,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
    
    try:
        return jsonify({"answer": agent_executor.run(query)})
    except Exception as e:
        return jsonify({"error": e})
# Run app
if __name__ == "__main__":
    app.run(debug=True)