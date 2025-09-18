import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os

# Load environment variables from .env file
load_dotenv()

print("Azure OpenAI API Key:", os.getenv('OPENAI_API_KEY'))
print("Azure OpenAI Endpoint:", os.getenv('AZURE_ENDPOINT'))
print("Azure OpenAI API Type:", os.getenv('OPENAI_API_TYPE'))
print("Azure OpenAI API Version:", os.getenv('OPENAI_API_VERSION'))
deployment_name = os.getenv('OPENAI_DEPLOYMENT')


messages = [{"role": "system", "content": "You are a helpful assistant."}]

model = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=deployment_name,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

while True:
    user_input = input("user:  ")
    messages.append({"role": "user", "content": user_input})

    response = model.invoke(messages)
    messages.append({"role": "assistant", "content": response})

    print(f"Assistant: {response}")
