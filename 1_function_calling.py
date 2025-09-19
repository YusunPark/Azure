from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
import os

load_dotenv()

llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=1  # Explicitly set temperature to the supported default value
        )


# tool을 만들때 llm이 잘 이해할 수 있도록 description을 잘 작성하는 것이 중요, 변수별로 설명도 적을 수 있음
def get_weather(city):
    """ 주어진 도시의 날씨 정보를 반환 합니다."""
    return f"{city}의 날씨는 맑음, 기온은 25도 입니다."  # 실제 API 호출로 대체 가능

def recommand_outfit(temp: int):
    """ 주어진 기온에 맞는 옷차림을 추천합니다. 
    temp: 기온 (섭씨)
    """
    if temp >= 25:
        return "반팔 티셔츠와 반바지를 추천합니다."
    elif 15 <= temp < 25:
        return "긴팔 셔츠와 청바지를 추천합니다."
    elif 5 <= temp < 15:
        return "스웨터와 코트를 추천합니다."
    else:
        return "두꺼운 코트와 목도리를 추천합니다."


weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="주어진 도시의 날씨 정보를 반환합니다. 예: 서울, 뉴욕"
)

outfit_tool = Tool(
    name="recommand_outfit",
    func=recommand_outfit,
    description="주어진 기온에 맞는 옷차림을 추천합니다. 예 temp: 기온 (섭씨)")



# ZERO_SHOT_REACT_DESCRIPTION : 도구 설명을 보고 어떤 도구를 사용할지 결정
tools = [weather_tool, outfit_tool]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


response = agent.run("서울과 뉴욕의 날씨를 알려줘")
print(response)




