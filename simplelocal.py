from langchain.llms.ollama import Ollama


model = "llama4"

ollama = Ollama(base_url='http://localhost:11434',model=model)

print("getting or creating collection")

ollama_res = ollama.generate(prompts=[
    'content: what is the reason for Operation Sindoor'
    ])

print(ollama_res)