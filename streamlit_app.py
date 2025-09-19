s# streamlit run streamlit_app.py

import streamlit as st
import openai
import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os

# Load environment variables from .env file
load_dotenv()



weather_data = """
| 날짜       | 도시     | 날씨      | 최고기온(°C) | 최저기온(°C) | 강수확률(%) |
|------------|----------|-----------|--------------|--------------|------------|
| 2025-09-18 | 서울     | 맑음      | 28           | 19           | 10         |
| 2025-09-18 | 부산     | 흐림      | 26           | 21           | 30         |
| 2025-09-18 | 대구     | 소나기    | 27           | 20           | 60         |
| 2025-09-18 | 광주     | 구름많음  | 25           | 18           | 20         |
| 2025-09-18 | 제주     | 비        | 24           | 22           | 80         |
"""

st.write("Hello, Streamlit!")
st.markdown("## This is a **markdown** text.")
st.markdown(weather_data)

# Streamlit 세션 상태에 대화 이력(messages), 입력값, assistant 응답 저장
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
if 'assistant_response' not in st.session_state:
    st.session_state['assistant_response'] = ''

# 대화 초기화 버튼
if st.button('대화 초기화'):
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['user_input'] = ''
    st.session_state['assistant_response'] = ''
    st.success('대화 이력이 초기화되었습니다.')

st.session_state['user_input'] = st.text_input("Enter some text:", value=st.session_state['user_input'])
if st.session_state['user_input']:
    st.write("You entered:", st.session_state['user_input'])
    # 마지막 메시지가 user가 아니면 추가
    if not (len(st.session_state['messages']) > 1 and st.session_state['messages'][-1]['role'] == 'user' and st.session_state['messages'][-1]['content'] == st.session_state['user_input']):
        st.session_state['messages'].append({"role": "user", "content": st.session_state['user_input']})

    model = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response = model.invoke(st.session_state['messages'])
    st.session_state['messages'].append({"role": "assistant", "content": response.content})
    st.session_state['assistant_response'] = response.content
    
if st.session_state['assistant_response']:
    st.write("assistant: ")
    st.write(st.session_state['assistant_response'])
    st.write("=" * 100)