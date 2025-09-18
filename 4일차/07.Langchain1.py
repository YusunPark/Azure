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

post_format = ChatPromptTemplate.from_template(
    """
    답변을 할때 항상 안녕하세요 주인님 하고 시작해줘.
    그리고 다음 조건을 반드시 지켜줘.
    답변을 발표 슬라이드 형태로 작성해줘.
    - 각 슬라이드는 번호로 구분해줘.
    - 슬라이드 제목을 포함해줘.
    - 슬라이드 내용은 3줄 이내로 작성해줘.
    - 슬라이드 내용은 bullet point로 작성해줘.
    - 슬라이드가 여러개일 경우, 슬라이드 사이에 빈 줄을 하나 넣어줘.
    - 슬라이드 번호는 1, 2, 3 ... 형태로 작성해줘.
    - 슬라이드 제목은 "## "로 시작해줘.
    - 슬라이드 내용은 "-"로 시작해줘.
    - 슬라이드 예시는 다음과 같아.
    1. ## 슬라이드 제목
       - 슬라이드 내용 1
       - 슬라이드 내용 2
       - 슬라이드 내용 3
    2. ## 슬라이드 제목
         - 슬라이드 내용 1
         - 슬라이드 내용 2
         - 슬라이드 내용 3

     예시를 참고해서 다음 질문에 답변을 슬라이드 형태로 작성해줘.
     '''
    {raw}
    '''

    """
)

parser = StrOutputParser()
chain = prompt | llm  | parser
polished_chain = ({"raw": chain}) | post_format | llm | parser


# answer = chain.invoke({"question": "서울의 인구는?"})
for chunk in chain.stream({"question": "서울의 인구는?"}):
    print(chunk, end="", flush=True)

for chunk in polished_chain.stream({"question": "경기도 안양시의 인구는?"}):
    print(chunk, end="", flush=True)
