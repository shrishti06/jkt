from langchain_community.llms import Ollama
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType

# Ensure this matches a model installed in your Ollama
llm = Ollama(model='llama3')

# Connect to the SQLite DB
db = SQLDatabase.from_uri("sqlite:///chinook.db")

# Optional: Print DB structure info
print("Dialect:", db.dialect)
print("Tables:", db.get_usable_table_names())

# Create and run agent
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent_executor.invoke({"input": "List total sales per country."})
print("Agent response:", response)

