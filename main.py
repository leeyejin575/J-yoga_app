import streamlit as st
import openai
from dotenv import load_dotenv
import os
import io
import csv

# 1. 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2. 페이지 설정
st.set_page_config(page_title="J YOGA ChatGPT 챗봇 💬")
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧘‍♀️ J YOGA ChatGPT 챗봇 <span style='font-size:24px;'>💬</span></h1>", unsafe_allow_html=True)

# 3. 닉네임 입력
if "nickname" not in st.session_state:
    st.session_state.nickname = st.text_input("닉네임을 입력해주세요:")
    if not st.session_state.nickname:
        st.stop()

# 4. 메시지 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. 사용자 입력
user_input = st.chat_input("요가, 명상, 몸 상태 등 무엇이든 물어보세요")
if user_input:
    nickname = st.session_state.nickname
    user_msg = f"{nickname}: {user_input}"
    st.session_state.messages.append({"role": "user", "content": user_msg})

    with st.chat_message("user"):
        st.markdown(user_msg)

    # 7. 시스템 메시지 추가 (요가 전문가 역할)
    system_prompt = {
        "role": "system",
        "content": (
            "당신은 요가 전문가이자 마음을 돌보는 명상 안내자입니다."
            " 사용자에게 친절하고 따뜻하게 요가 동작 추천, 명상 유도, 몸과 마음의 긴장을 푸는 방법을 알려주세요."
        )
    }

    with st.chat_message("assistant"):
        with st.spinner("챗봇이 응답을 준비 중이에요..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[system_prompt] + st.session_state.messages
            )
            bot_reply = response.choices[0].message.content
            st.markdown(f"🧘‍♀️ {bot_reply}")

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# 8. 대화 내용 저장 - TXT
txt_buffer = io.StringIO()
for m in st.session_state.messages:
    txt_buffer.write(f"{m['role']}: {m['content']}\n\n")
st.download_button(
    label="📄 대화내용 TXT 저장",
    data=txt_buffer.getvalue(),
    file_name="j_yoga_chat_history.txt",
    mime="text/plain"
)

# 9. 대화 내용 저장 - CSV
csv_buffer = io.StringIO()
writer = csv.writer(csv_buffer)
writer.writerow(["Role", "Content"])
for m in st.session_state.messages:
    writer.writerow([m["role"], m["content"]])
st.download_button(
    label="📊 대화내용 CSV 저장",
    data=csv_buffer.getvalue(),
    file_name="j_yoga_chat_history.csv",
    mime="text/csv"
)
