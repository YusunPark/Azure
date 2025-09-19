# file: app_stream.py - 스트리밍 출력
# 설명: 스트리밍 출력 표시를 위해 sys.stdout을 사용합니다.

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


#chain.stream()은 토큰 단위로 부분 결과를 내보내며, UI에서 실시간 표시 UX를 구현할 때 유용합니다.

if __name__ == "__main__":
	for chunk in chain.stream({
		"question": "퇴근 후 30분 안에 만들 수 있는 건강한 저녁 메뉴 3가지를 추천해줘. 대략적인 재료비도 알려줘."
	}):
		sys.stdout.write(chunk)
		sys.stdout.flush()
	print()
	


