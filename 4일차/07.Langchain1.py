import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Load environment variables from .env file
load_dotenv()


messages = [{"role": "system", "content": "You are a helpful assistant."}]
llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
            api_key=os.getenv("OPENAI_API_KEY"),
            streaming=True # stream 형태로 출력하기 위해서
        )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}"),
])

chain = prompt | llm  | StrOutputParser() # stream 형태로 출력하기 위해서 

# answer = chain.invoke({"question": "서울의 인구는?"})
for chunk in chain.stream({"question": "서울의 인구는?"}):
    print(chunk, end="", flush=True)


