"""네이버 쇼핑 검색 수집기 - Streamlit 웹 앱"""

import streamlit as st
import pandas as pd
from coupang_scraper import search_naver_shopping, CLIENT_ID, CLIENT_SECRET

st.set_page_config(page_title="네이버 쇼핑 검색기", page_icon="🛒")
st.title("네이버 쇼핑 검색 수집기")

if not CLIENT_ID or not CLIENT_SECRET:
    st.error(
        "`.env` 파일에 네이버 API 키를 설정해주세요.\n\n"
        "```\nNAVER_CLIENT_ID=발급받은ID\nNAVER_CLIENT_SECRET=발급받은SECRET\n```"
    )
    st.stop()

SORT_OPTIONS = {
    "정확도순": "sim",
    "날짜순": "date",
    "가격 낮은순": "asc",
    "가격 높은순": "dsc",
}

with st.sidebar:
    keyword = st.text_input("검색어")
    count = st.slider("수집 개수", 1, 100, 20)
    sort_label = st.selectbox("정렬", list(SORT_OPTIONS.keys()))
    search = st.button("검색", type="primary", disabled=not keyword)

if search and keyword:
    with st.spinner("검색 중..."):
        try:
            sort_value = SORT_OPTIONS[sort_label]
            results, total = search_naver_shopping(keyword, display=count, sort=sort_value)
        except Exception as e:
            st.error(f"API 요청 실패: {e}")
            st.stop()

    st.info(f"전체 {total:,}개 중 {len(results)}개 수집")

    if results:
        df = pd.DataFrame(results)
        st.dataframe(
            df,
            column_config={"링크": st.column_config.LinkColumn("링크")},
            use_container_width=True,
        )

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "CSV 다운로드",
            csv,
            file_name=f"네이버쇼핑_{keyword}.csv",
            mime="text/csv",
        )
    else:
        st.warning("검색 결과가 없습니다.")
