# file: app_rag_like_skeleton.py - 후처리 체인
# 실제 RAG는 아님. LangChain의 조합(LCEL)로 후처리를 보여주는 예시
# LCEL 조합으로 “생성 → 후처리” 2단계 체인을 구성합니다.

import os, sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt5-chat")

llm = AzureChatOpenAI(
		azure_endpoint=endpoint,
		api_key=api_key,
		api_version=api_version,
		azure_deployment=DEPLOYMENT_NAME,
		temperature=0.5,
)


prompt = ChatPromptTemplate.from_messages([
	("system", "너는 실전형 요약 비서야. 답변은 번호 매긴 3~5단계로, 각 단계는 한 문장. 실행 가능한 동사로 시작하고 과장된 표현은 피해."),
	("user", "{question}"),
])

chain = prompt | llm | StrOutputParser()
