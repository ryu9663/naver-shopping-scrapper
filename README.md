# 네이버 쇼핑 검색 수집기

네이버 Open API를 사용하여 쇼핑 상품을 검색하고 CSV로 저장하는 도구입니다.
CLI와 Streamlit 웹 앱 두 가지 방식으로 사용할 수 있습니다.

## 사전 준비

1. [네이버 개발자센터](https://developers.naver.com)에 가입
2. 애플리케이션 등록 → **검색** API 선택
3. 환경: WEB 설정 → URL에 `http://localhost` 입력
4. 프로젝트 루트에 `.env` 파일 생성:

```
NAVER_CLIENT_ID=발급받은ID
NAVER_CLIENT_SECRET=발급받은SECRET
```

## 설치

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 사용법

### 웹 앱 (Streamlit)

```bash
streamlit run app.py
```

사이드바에서 검색어, 수집 개수, 정렬 기준을 설정하고 검색하면 결과를 테이블로 확인하고 CSV로 다운로드할 수 있습니다.

### CLI

```bash
python coupang_scraper.py
```

검색어와 수집 개수를 입력하면 결과를 터미널에 미리보기로 출력하고 CSV 파일로 저장합니다.

## 주요 기능

- 상품명, 최저가, 쇼핑몰, 카테고리, 링크 수집
- 정렬 옵션: 정확도순, 날짜순, 가격 낮은순, 가격 높은순
- 최대 100개 상품 한 번에 수집
- UTF-8-SIG 인코딩 CSV 저장 (Excel 한글 깨짐 방지)
