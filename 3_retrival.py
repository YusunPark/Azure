from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


import os
from dotenv import load_dotenv

load_dotenv()

embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=os.getenv('OPENAI_EMBEDDING_DEPLOYMENT'),
            api_key=os.getenv("OPENAI_API_KEY"),
        )



# 샘플 문서 추가
documents = [
    "서울의 날씨는 맑습니다.",
    "오늘은 흐리고 비가 올 예정입니다.",
    "서울의 기온은 25도입니다.",
    "내일은 맑고 따뜻할 것입니다.",
    "이번 주말에는 비가 예상됩니다.",
    "우리 할머니는 생일에 미역국을 끓여주십니다.",
    "할머니는 항상 건강을 챙기시고, 맛있는 음식을 만들어 주십니다.",
    "할머니와 함께 산책을 자주 다니며, 자연을 즐깁니다.",
    "할머니는 손주들에게 사랑과 지혜를 나눠주십니다.",
    "할머니의 따뜻한 미소는 가족 모두에게 큰 힘이 됩니다.",
    "우리 가족은 추석에 프랑스 음식을 먹습니다.",
    "프랑스 음식은 다양하고 풍부한 맛을 자랑합니다.",
    "내 방에는 라부부 인형이 있습니다.",
    "라부부 인형은 귀엽고 포근한 느낌을 줍니다.",
    "라부부 인형은 친구들에게도 인기가 많습니다.",
    "내습관은 매일 아침 조깅을 하는 것입니다.",
    "조깅은 건강에 좋고, 하루를 상쾌하게 시작할 수 있게 해줍니다.",
    "나는 물을 마십니다.",
    "물은 생명에 필수적인 요소입니다.",
]

vectorstore = FAISS.from_texts(documents, embeddings)

query = "프랑스 여행 계획"

results = vectorstore.similarity_search(query, k=5)


print("검색결과")
for r in results:
    print("-", r.page_content)



llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0  # Set temperature to 0 for deterministic responses
        )


retrival = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template("""
                                            다음은 문서의 일부입니다:
                                            {context}
                                            이 문서를 바탕으로 다음 질문에 답해 주세요:
                                            질문 : {input}""")


document_chain = create_stuff_documents_chain(llm, prompt)
retrival_chain = create_retrieval_chain(retrival,document_chain)
result = retrival_chain.invoke({"input":query})

print("질문", query)
print("답변", result['answer'])