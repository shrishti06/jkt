from langchain.chains.sql_database.query  import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.llms.ollama import Ollama

llm = Ollama(base_url="http://localhost:11434",model="llama4", temperature=0.1 )
db = SQLDatabase.from_uri("sqlite:///data/olympics.db")
print(db.dialect)  # This will print the dialect of the database, e.g., 'sqlite'
print(db.get_usable_table_names())  # This will print the list of tables in the database
chain = create_sql_query_chain(llm, db)
question = "What is the total number of medals won by India in the Olympics?"
response = chain.invoke({"input": question})
print(response)

