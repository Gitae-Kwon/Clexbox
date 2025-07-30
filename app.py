# -*- coding: utf-8 -*-
import http.client
import json
import streamlit as st
import uuid


class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = "clovastudio.stream.ntruss.com"
        self._api_key = "nv-0fcd9ac140a84743bc048135c96363c3lEvD"  # 여긴 순수 API 키만 (Bearer 제거)
        self._request_id = str(uuid.uuid4())

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self._api_key}',  # 여기서만 Bearer 붙이기
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
            return res  # 전체 에러 반환


# ✅ Streamlit 앱
st.set_page_config(page_title="네이버 Clova 요약기", layout="centered")
st.title("✂️ 네이버 Clova 요약기 (Studio API v2)")

input_text = st.text_area("요약할 내용을 입력하세요", height=200)

if st.button("요약하기"):
    if not input_text.strip():
        st.warning("요약할 내용을 입력해주세요.")
    else:
        with st.spinner("요약 중입니다..."):
            executor = CompletionExecutor(
                host="clovastudio.stream.ntruss.com",
                api_key="nv-여기에_발급받은_API_KEY만_입력하세요",  # Bearer 없이!
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

                if (
                    isinstance(result, dict)
                    and "result" in result
                    and "summaries" in result["result"]
                    and len(result["result"]["summaries"]) > 0
                ):
                    st.success("✅ 요약 결과:")
                    st.write(result["result"]["summaries"][0]["summary"])
                else:
                    st.error("❌ 요약 실패:")
                    st.json(result)
