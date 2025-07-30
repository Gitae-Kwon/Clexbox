import requests
import streamlit as st

st.title("✂️ 네이버 Clova 요약기 (Studio용)")

text = st.text_area("요약할 내용을 입력하세요")

if st.button("요약하기"):
    api_key = "nv-eb29729ac74043cfbc34216d21d848a0QwLw"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "messages": [
            {"role": "system", "content": "다음 글을 3문장으로 요약해줘."},
            {"role": "user", "content": text}
        ],
        "topP": 0.8,
        "topK": 0,
        "temperature": 0.7,
        "maxTokens": 500,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeAiFilters": False
    }

    response = requests.post(
        "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        answer = result["result"]["message"]["content"]
        st.success(answer)
    else:
        st.error(f"요약 실패: {response.status_code}")
        st.code(response.text)
