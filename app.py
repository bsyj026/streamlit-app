import streamlit as st
from openai import OpenAI

# Upstage API 클라이언트 설정
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://api.upstage.ai/v1"
)

st.set_page_config(page_title="학생 심리상담 챗봇", page_icon="🧑‍🎓")
st.title("🧑‍🎓 학생 심리상담 챗봇")
st.write("안녕하세요! 저는 여러분의 고민을 들어주는 심리상담 챗봇입니다. 편하게 고민을 이야기해 주세요.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 학생들의 심리상담을 도와주는 친절한 상담사야. 공감과 위로, 실질적인 조언을 제공해줘."}
    ]

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

if prompt := st.chat_input("고민을 입력해 주세요..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        response = ""
        stream = client.chat.completions.create(
            model="solar-pro2",
            messages=st.session_state["messages"],
            stream=True,
        )
        msg_placeholder = st.empty()
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                msg_placeholder.markdown(response)
        st.session_state["messages"].append({"role": "assistant", "content": response})
