import http.client
import json
import streamlit as st
import uuid


class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
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
        conn.request('POST', '/v1/api-tools/summarization/v2', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']
        else:
            return res  # 전체 에러 메시지를 반환


# Streamlit 앱 시작
st.title("✂️ 네이버 Clova 요약기 (Studio API v2)")

input_text = st.text_area("요약할 내용을 입력하세요", height=200)

if st.button("요약하기"):
    with st.spinner("요약 중입니다..."):
        executor = CompletionExecutor(
            host="clovastudio.stream.ntruss.com",
            api_key="여기에_발급받은_API_KEY_입력",  # Bearer 빼고 키 값만
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

        result = executor.execute(request_data)

        if isinstance(result, dict) and "summary" in result:
            st.success("✅ 요약 결과:")
            st.write(result["summary"])
        else:
            st.error("❌ 요약 실패:")
            st.json(result)
