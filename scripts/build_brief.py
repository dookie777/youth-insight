# -*- coding: utf-8 -*-
"""구단별 정리본 HTML을 A4 가로 PDF로 변환
사용법: python scripts/build_brief.py templates/club-brief/<구단>.html docs/00/<파일명>.pdf
필요: playwright(chromium), Noto Sans CJK KR 글꼴
"""
import os, sys
from playwright.sync_api import sync_playwright
src, out = os.path.abspath(sys.argv[1]), sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + src); pg.wait_for_timeout(400)
    pg.pdf(path=out, width="297mm", height="210mm", print_background=True,
           margin=dict(top="0", bottom="0", left="0", right="0"))
    b.close()
