# -*- coding: utf-8 -*-
import streamlit as st
import http.client
import json
import uuid


class CompletionExecutor:
    def __init__(self, host: str, api_key: str, request_id: str):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self._api_key}',
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/v1/api-tools/summarization/v2',
                     json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        return res


def extract_summary(result):
    try:
        # 요약 결과가 summaries 배열에 담겨있는 경우
        return result["result"]["summaries"][0]["summary"]
    except (KeyError, TypeError):
        try:
            # fallback: 단일 text 필드에 담겨있는 경우
            return result["result"]["text"]
        except (KeyError, TypeError):
            return None


# ✅ Streamlit 앱 시작
st.set_page_config(page_title="네이버 Clova 요약기", layout="centered")
st.title("✂️ 네이버 Clova 요약기 (Studio API v2)")

input_text = st.text_area("요약할 내용을 입력하세요", height=200)

# 요약하기 버튼 클릭 시
if st.button("요약하기"):
    if not input_text.strip():
        st.warning("요약할 내용을 입력해주세요.")
    else:
        with st.spinner("요약 중입니다..."):

            # ✅ 여기에 본인의 실제 서비스용 API 키를 넣으세요 (Bearer 제거!)
            API_KEY = "nv-0fcd9ac140a84743bc048135c96363c3lEvD"  
            HOST = "clovastudio.stream.ntruss.com"

            executor = CompletionExecutor(
                host=HOST,
                api_key=API_KEY,
                request_id=str(uuid.uuid4())
            )

            request_data = {
                "texts": [input_text],
                "segMinSize": 300,
                "includeAiFilters": False,
                "autoSentenceSplitter": True,
                "segCount": -1,
                "segMaxSize": 1000
            }

            try:
                result = executor.execute(request_data)
                summary_text = extract_summary(result)

                if summary_text:
                    st.success("✅ 요약 결과:")
                    st.write(summary_text)
                else:
                    st.error("❌ 요약 실패:")
                    st.json(result)
            except Exception as e:
                st.error(f"❌ 예외 발생: {str(e)}")
