import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print("Azure OpenAI API Key:", os.getenv('OPENAI_API_KEY'))
print("Azure OpenAI Endpoint:", os.getenv('AZURE_ENDPOINT'))
print("Azure OpenAI API Type:", os.getenv('OPENAI_API_TYPE'))
print("Azure OpenAI API Version:", os.getenv('OPENAI_API_VERSION'))

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.azure_endpoint = os.getenv('AZURE_ENDPOINT')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_version = os.getenv('OPENAI_API_VERSION')
deployment_name = os.getenv('OPENAI_DEPLOYMENT')

messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 응답 반복, 히스토리 유지
while True:
    user_input = input("user:  ")
    messages.append({"role": "user", "content": user_input})


    response = openai.chat.completions.create(
                    model=deployment_name,  
                    messages=messages
                )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    print("=" * 100)
    print("히스토리")
    print(messages)
    print("-" * 100)
    print("assistant: ")
    print(response)
    print("=" * 100)


        