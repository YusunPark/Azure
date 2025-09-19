# file: app_basic.py
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .env 불러오기
load_dotenv()

# Azure OpenAI 설정
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

# 배포 이름: Foundry에서 만든 배포명과 동일해야 함
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-chat-yusun")

# Azure OpenAI LLM 초기화
llm = AzureChatOpenAI(
		azure_endpoint=endpoint,
		api_key=api_key,
		api_version=api_version,
		azure_deployment=DEPLOYMENT_NAME,
		temperature=0.4,
		max_retries=3,
		timeout=30,
)


# 프롬프트 템플릿과 체인 구성
prompt = ChatPromptTemplate.from_messages([
	("system", "너는 바쁜 사람들을 돕는 초간결 비서야. 핵심만 3~5문장으로, 가벼운 유머는 한 번만."),
	("user", "{question}"),
])

chain = prompt | llm | StrOutputParser()


# 질문 예시
if __name__ == "__main__":
	answer = chain.invoke({
		"question": "헬스장 초보를 위한 1주일 운동 루틴을 제안해줘. 주의사항 포함!"
	})
	print("\n[답변]\n" + answer)

