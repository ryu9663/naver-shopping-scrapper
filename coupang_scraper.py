"""
네이버 쇼핑 상품 검색 수집기
- 검색어를 입력하면 상품명, 가격, 쇼핑몰, 링크를 수집합니다.
- 결과를 CSV 파일로 저장합니다.
- 네이버 Open API를 사용합니다. (https://developers.naver.com)

[사용 전 준비]
1. https://developers.naver.com 에 가입
2. 애플리케이션 등록 → "검색" API 선택
3. 발급받은 Client ID / Client Secret을 아래에 입력
"""

import csv
import os

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def search_naver_shopping(keyword, display=20, start=1, sort="sim"):
    """네이버 쇼핑 API로 상품을 검색합니다."""
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    params = {
        "query": keyword,
        "display": display,  # 한 번에 가져올 개수 (최대 100)
        "start": start,      # 시작 위치
        "sort": sort,        # sim(정확도), date(날짜), asc(가격낮은순), dsc(가격높은순)
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "상품명": item["title"].replace("<b>", "").replace("</b>", ""),
            "최저가": f'{int(item["lprice"]):,}원',
            "쇼핑몰": item.get("mallName", "네이버"),
            "카테고리": " > ".join(filter(None, [
                item.get("category1", ""),
                item.get("category2", ""),
                item.get("category3", ""),
            ])),
            "링크": item["link"],
        })

    return results, data.get("total", 0)


def save_to_csv(results, filename="결과.csv"):
    """결과를 CSV 파일로 저장합니다."""
    if not results:
        print("저장할 데이터가 없습니다.")
        return

    fields = ["상품명", "최저가", "쇼핑몰", "카테고리", "링크"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"'{filename}' 파일로 저장 완료! ({len(results)}개 상품)")


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("=" * 50)
        print("⚠ .env 파일에 네이버 API 키를 설정해주세요!")
        print()
        print("1. https://developers.naver.com 접속 & 로그인")
        print("2. [Application] → [애플리케이션 등록]")
        print("3. 이름 입력, [검색] API 선택")
        print("4. 환경: [WEB 설정] → URL에 http://localhost 입력")
        print("5. .env 파일에 발급받은 키 입력:")
        print("   NAVER_CLIENT_ID=발급받은ID")
        print("   NAVER_CLIENT_SECRET=발급받은SECRET")
        print("=" * 50)
        return

    keyword = input("검색할 상품명을 입력하세요: ")
    count = input("몇 개 수집할까요? (기본 20, 최대 100): ").strip()
    count = min(int(count), 100) if count else 20

    print(f"'{keyword}' 검색 중...")
    results, total = search_naver_shopping(keyword, display=count)
    print(f"전체 {total:,}개 중 {len(results)}개 수집 완료")

    if results:
        filename = f"네이버쇼핑_{keyword}.csv"
        save_to_csv(results, filename)

        print(f"\n=== 수집 결과 미리보기 (상위 5개) ===")
        for i, item in enumerate(results[:5], 1):
            print(f"{i}. {item['상품명'][:40]}")
            print(f"   {item['최저가']}  |  {item['쇼핑몰']}  |  {item['카테고리']}")
    else:
        print("수집된 상품이 없습니다.")


if __name__ == "__main__":
    main()
