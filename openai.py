from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2023-05-15",
    azure_endpoint="https://your-openai-api-endpoint"
)

completion = client.chat.completions.create(
    model="gpt-35-turbo",   
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},      
        
        {"role": "user", "content": "What is the capital of France?"}
    ],
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=None,
    temperature=0.7
)

response = completion.choices[0].message.content
print(response)  # This will print the response from the model