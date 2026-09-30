# -*- coding: utf-8 -*-
"""
승인된 자료를 data.json에 추가하는 스크립트 (표준 라이브러리만 사용)

사용법
  python scripts/add_items.py approved.json
  python scripts/add_items.py approved.json --dry-run   # 검증만, 저장 안 함

approved.json 형식: 아래 키를 가진 객체의 배열
  cat      카테고리 (CATEGORIES 중 하나, 필수)
  sub      하부카테고리 (선택, 없으면 "")
  type     논문 | 리포트 | 기사  또는 paper | report | news (필수)
  en       원제목 (필수)
  ko       번역제목 (필수)
  summary  핵심내용 (필수)
  source   출처 (필수)
  date     게재일 "YYYY.M.D" (필수)
  url      원본링크 (필수)
  file     저장소 내 PDF 상대 경로 "docs/02/xxx.pdf" 또는 "" (선택)
  added    등록일 (선택, 생략 시 오늘 KST)

규칙
  - url 또는 en 이 기존 항목과 같으면 중복으로 건너뜀
  - file 이 지정되면 해당 파일이 저장소에 실제로 있어야 함
  - lastUpdate 는 실행일(KST)로 갱신
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

CATEGORIES = [
    "01_선수_평가_체계", "02_선수_발굴_체계", "03_아카데미_운영_사례",
    "04_훈련_방법", "05_선수_교육(지도)", "06_육성_정책·제도", "07_선수_성장·발달",
]
TYPE_MAP = {"논문": "paper", "리포트": "report", "기사": "news", "기사·보고서": "news",
            "paper": "paper", "report": "report", "news": "news"}
REQUIRED = ["cat", "type", "en", "ko", "summary", "source", "date", "url"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")


def kst_today():
    return (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y.%m.%d")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src, dry = sys.argv[1], "--dry-run" in sys.argv
    new_items = json.load(open(src, encoding="utf-8"))
    if isinstance(new_items, dict):
        new_items = new_items.get("items", [])

    d = json.load(open(DATA, encoding="utf-8"))
    items = d["items"]
    seen_url = {it["url"].strip().lower() for it in items if it.get("url")}
    seen_en = {it["en"].strip().lower() for it in items}

    added, errors, skipped = [], [], []
    for i, it in enumerate(new_items, 1):
        g = lambda k: str(it.get(k) or "").strip()
        miss = [k for k in REQUIRED if not g(k)]
        if miss:
            errors.append(f"{i}번: 필수 항목 누락 {miss} ({g('en')[:40]})"); continue
        if g("cat") not in CATEGORIES:
            errors.append(f"{i}번: 카테고리 '{g('cat')}' 미인식"); continue
        t = TYPE_MAP.get(g("type"))
        if not t:
            errors.append(f"{i}번: 유형 '{g('type')}' 미인식"); continue
        if g("url").lower() in seen_url or g("en").lower() in seen_en:
            skipped.append(f"{i}번: 중복 ({g('en')[:50]})"); continue
        f = g("file")
        if f and not os.path.exists(os.path.join(ROOT, f)):
            errors.append(f"{i}번: 파일 없음 {f}"); continue
        rec = {"cat": g("cat"), "sub": g("sub"), "type": t, "added": g("added") or kst_today(),
               "en": g("en"), "ko": g("ko"), "summary": g("summary"), "source": g("source"),
               "date": g("date"), "url": g("url"), "file": f}
        items.append(rec); seen_url.add(g("url").lower()); seen_en.add(g("en").lower()); added.append(rec)

    for m in errors: print("오류:", m)
    for m in skipped: print("건너뜀:", m)
    print(f"추가 {len(added)}건 / 오류 {len(errors)}건 / 중복 {len(skipped)}건 / 총 {len(items)}건")
    if errors:
        sys.exit("중단: 오류 항목을 수정한 뒤 다시 실행")
    if dry or not added:
        return
    d["lastUpdate"] = kst_today()
    json.dump(d, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장 완료: data.json (lastUpdate {d['lastUpdate']})")


if __name__ == "__main__":
    main()
