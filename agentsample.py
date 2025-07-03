from langchain_community.chat_models import ChatOllama # <<< IMPORTANT: Use ChatOllama
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool, BaseTool
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

class CalculatorInput(BaseModel):
   a: int = Field(..., description="The first number")
   b: int = Field(..., description="The second number")
   
# Option 1: Simplest and most common way to define a tool with a decorator
@tool("multiply_tool", args_schema=CalculatorInput)
def multiply(a: int, b: int) -> int:
    """A simple calculator tool that evaluates multiply expressions."""
    return a * b

# If you use the decorator as above, `multiply` itself is now a BaseTool instance.
tools: list[BaseTool] = [multiply] 

# Option 2 (Your previous approach, which also works but is slightly more verbose than Option 1):
# MultiplyTool = tool("multiply_tool", args_schema=CalculatorInput)
# def multiply_func(a: int, b: int) -> int:
#     """A simple calculator tool that evaluates multiply expressions."""
#     return a * b
# tools = [MultiplyTool(multiply_func)] # Here, MultiplyTool acts as a wrapper/decorator

# Corrected ChatPromptTemplate for create_tool_calling_agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can perform calculations using the provided tools. If you cannot answer the question, respond with \"I don't know\"."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ]
)

# --- CRUCIAL CHANGE HERE: Use ChatOllama ---
# Ensure you have 'llama3' (or 'llama3-tool-use' which is even better for this) pulled via Ollama.
llm = ChatOllama(base_url="http://localhost:11434", model="mixtral", temperature=0.1) 
llm_with_tools = llm.bind_tools(tools)
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True 
)

question = "What is the product of 5 and 6?"
response = agent_executor.invoke({"input": question})

print(response)

# IMPORTANT:
# 1. Make sure Ollama server is running: `ollama serve`
# 2. Pull the model: `ollama pull llama3` (or `ollama pull llama3-tool-use`)
# 3. If 'llama3' still gives `NotImplementedError`, try `llama3-tool-use` or `mixtral`.
#    The 'NotImplementedError' means the specific `ChatOllama` binding for the
#    model doesn't fully support the structured tool calling required by the agent.