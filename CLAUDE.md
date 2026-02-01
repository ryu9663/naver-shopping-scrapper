# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

네이버 쇼핑 검색 수집기 — Naver Shopping API를 사용하여 상품을 검색하고 CSV로 저장하는 도구. CLI(`coupang_scraper.py`)와 Streamlit 웹 앱(`app.py`) 두 가지 인터페이스를 제공한다.

## Commands

```bash
# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# Streamlit 웹 앱 실행
streamlit run app.py

# CLI로 직접 실행
python coupang_scraper.py
```

## Architecture

- **`coupang_scraper.py`**: 핵심 모듈. `search_naver_shopping()` 함수가 네이버 Open API(`/v1/search/shop.json`)를 호출하여 상품 데이터를 반환. `save_to_csv()`로 CSV 저장. `main()`은 CLI 인터페이스.
- **`app.py`**: Streamlit 웹 UI. `coupang_scraper`에서 `search_naver_shopping`을 임포트하여 사용. 사이드바에서 검색 조건 입력, 결과를 DataFrame으로 표시 및 CSV 다운로드 제공.
- **`.env`**: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 저장. 네이버 개발자센터에서 발급.

## Hooks

`.claude/hooks/protect-env.sh` 훅이 `.env` 파일에 대한 모든 읽기/쓰기/실행 접근을 차단한다. `.env` 파일을 직접 조작하지 말 것.

## Environment

- Python 3.14, venv 기반
- 주요 의존성: requests, beautifulsoup4, python-dotenv, streamlit, pandas
