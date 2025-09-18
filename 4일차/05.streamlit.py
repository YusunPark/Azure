import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()


# Streamlit 세션 상태에 대화 이력(messages) 저장
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


# 대화 초기화 버튼
if st.button('대화 초기화', key="reset_button"):
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.success('대화 이력이 초기화되었습니다.')


model = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
            api_key=os.getenv("OPENAI_API_KEY"),
        )

user_input = st.text_input("user:  ")

if st.button("Send", key="send_button") and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    response = model.invoke(st.session_state['messages'])
    st.session_state['messages'].append({"role": "assistant", "content": response.content})

    st.write(f"Assistant: {response.content}")
    st.success("AI 응답이 생성되었습니다.")
