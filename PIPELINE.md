# 운영 파이프라인 (2026.09.30 전환)

## 구조

```
월·수·금 09:00 KST  조이스 예약 작업 실행
   ↓  해외 유소년 축구 자료 검색·선별·번역·요약
   ↓  후보 목록 통지 (게시 없음)
사용자 승인 ("1, 3번 올려" / 문구 수정 지시)
   ↓
조이스가 승인분만 처리
   ↓  PDF 확보 → docs/<카테고리번호>/ 에 저장
   ↓  scripts/add_items.py 로 data.json 에 행 추가
   ↓  git commit & push
GitHub Pages 자동 반영 (수 분 내)
```

## 원천 데이터

- **원천은 `data.json` 하나.** 구글 시트 「자료목록_마스터」는 2026.09.28 갱신분(95건)을 마지막으로 동결, 보관용.
- 시트 기반 자동 갱신 워크플로(`.github/workflows/update-data.yml`)는 폐지. 스크립트는 `scripts/legacy_update_from_sheet.py`로 보관하며 실행 시 즉시 중단되도록 잠금.
- `index.html` 안의 내장 백업 `DATA`는 `data.json` 로드 실패 시에만 쓰이는 폴백. 전환 시점(95건)으로 동기화했으며 이후에는 분기별 정도로 `data.json` 내용으로 다시 맞추면 된다.

## 자료 등록 절차 (조이스 실행 기준)

1. 승인된 항목을 `approved.json`(배열)로 작성. 키는 `scripts/add_items.py` 상단 설명 참조.
2. PDF가 오픈액세스이면 `docs/<카테고리번호>/` 규칙 경로에 저장하고 `file`에 상대 경로 기입. 구독·유료 자료는 `file`을 `""`로 두고 `url`만 등록.
3. `python scripts/add_items.py approved.json --dry-run` 으로 검증 → 오류 0건 확인 후 `--dry-run` 없이 실행.
4. `git add data.json docs && git commit -m "feat: 자료 N건 추가 (YYYY-MM-DD)" && git push`.

## 검증 규칙 (add_items.py가 자동 차단)

- 필수 항목 누락, 미인식 카테고리·유형
- `url` 또는 `en`이 기존 항목과 동일한 중복
- `file`에 지정한 경로에 파일이 실제로 없는 경우

## 데이터 정합 기록

- 2026.09.30 전수 점검: 시트 95건 = data.json 95건 일치, 필수 열 공란 0건.
- Fortune·AFP(2건)가 같은 드라이브 파일을 가리키는 것은 두 기사를 함께 분석한 더이룸 브리프 1건이므로 정상.
- IJSSC 「What does research tell us about scouting in football?」의 드라이브 링크가 JSSM 논문 파일을 잘못 가리키고 있어 링크 제거. 오픈액세스(CC BY 4.0) 논문이므로 PDF 확보 후 `docs/02/`에 등록 예정.
