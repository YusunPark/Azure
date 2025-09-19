import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os
import streamlit as st


# 채팅 누적 출력 + input 창 하단 고정

# Load environment variables from .env file
load_dotenv()

model = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_deployment=os.getenv('OPENAI_DEPLOYMENT'),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

# 대화 초기화 버튼을 상단 오른쪽에 예쁘게 배치
col1, col2 = st.columns([8, 1])
with col2:
    st.markdown("""
        <style>
        .reset-btn button {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: bold;
            font-size: 16px;
            padding: 0.5em 1.2em;
        }
        </style>
    """, unsafe_allow_html=True)
    if st.button('🧹 대화 초기화', key="reset_button", help="모든 대화 이력을 삭제합니다.", type="primary"):
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.toast('대화 이력이 초기화되었습니다.', icon="🧹")
        st.rerun()

    

# Streamlit 세션 상태에 대화 이력(messages) 저장
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 채팅 메시지 누적 출력
for msg in st.session_state['messages']:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input 창을 항상 하단에 고정
if prompt := st.chat_input("Enter some text"):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""

        # LangChain의 stream=True 옵션 사용
        for chunk in model.stream(st.session_state['messages']):
            if hasattr(chunk, "content"):
                response_text += chunk.content
                placeholder.markdown(response_text)


        st.session_state['messages'].append({"role": "assistant", "content": response_text})


