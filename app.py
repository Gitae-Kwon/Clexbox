import requests
import streamlit as st

st.title("✂️ 네이버 Clova 요약기")

text = st.text_area("요약할 내용을 입력하세요")

if st.button("요약하기"):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "YOUR_CLIENT_ID",
        "X-NCP-APIGW-API-KEY": "YOUR_CLIENT_SECRET",
        "Content-Type": "application/json"
    }
    data = {
        "document": {
            "content": text
        },
        "option": {
            "language": "ko",
            "model": "general",
            "tone": 2,
            "summaryCount": 3
        }
    }

    response = requests.post(
        "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        st.success(response.json()['summary'])
    else:
        st.error("요약 실패! 에러 코드: " + str(response.status_code))
