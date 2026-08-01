# -*- coding: utf-8 -*-
# 자료목록_마스터(구글 시트) → data.json 변환 스크립트
import csv
import io
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

SHEET_ID = "1quiYEUYWy0Eut_1ZAfDHnPiTnYktfkK60DgBaGKV6Ds"  # 자료목록_마스터
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

TYPE_MAP = {"논문": "paper", "리포트": "report", "기사": "news", "기사·보고서": "news"}
REQUIRED_HEADERS = ["카테고리", "유형", "원제목", "번역제목", "핵심내용", "출처", "게재일"]


def main():
    raw = urllib.request.urlopen(CSV_URL, timeout=30).read().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(raw)))

    if not rows:
        sys.exit("중단: 시트에서 행을 읽지 못함")
    missing = [h for h in REQUIRED_HEADERS if h not in rows[0]]
    if missing:
        sys.exit(f"중단: 필수 열 누락 {missing} — 시트 머리글 확인 필요")

    items = []
    for i, r in enumerate(rows, start=2):
        g = lambda k: (r.get(k) or "").strip()
        cat, en = g("카테고리"), g("원제목")
        if not cat and not en:
            continue
        if not cat or not en:
            print(f"경고: {i}행 카테고리/원제목 누락 — 건너뜀")
            continue
        t = TYPE_MAP.get(g("유형"))
        if t is None:
            print(f"경고: {i}행 유형 '{g('유형')}' 미인식 — '기사'로 처리")
            t = "news"
        items.append({
            "cat": cat,
            "sub": g("하부카테고리"),
            "type": t,
            "added": g("등록일"),
            "en": en,
            "ko": g("번역제목"),
            "summary": g("핵심내용"),
            "source": g("출처"),
            "date": g("게재일"),
            "url": g("원본링크"),
            "file": g("드라이브다운로드"),
        })

    if len(items) < 5:
        sys.exit(f"중단: 유효 자료 {len(items)}건 — 시트 이상 의심, 기존 data.json 유지")

    kst_now = datetime.now(timezone.utc) + timedelta(hours=9)
    out = {"lastUpdate": kst_now.strftime("%Y.%m.%d"), "items": items}
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"완료: {len(items)}건 → data.json (lastUpdate {out['lastUpdate']})")


if __name__ == "__main__":
    main()
