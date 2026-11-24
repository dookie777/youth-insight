# -*- coding: utf-8 -*-
"""정리본 HTML의 헤드 메시지 불릿을 계측 (기준: 문장당 75~90자, 한글·공백 1자, 숫자·영문·기호 0.5자)
사용법: python scripts/check_head_length.py templates/club-brief/<구단>.html
"""
import re, sys
def eff_len(s): return sum(1 if ('가' <= c <= '힣' or c == ' ') else 0.5 for c in s)
html = open(sys.argv[1], encoding="utf-8").read()
bad = 0
for blk in re.findall(r'<div class="head"><ul>(.*?)</ul></div>', html, flags=re.S):
    for li in re.findall(r'<li>(.*?)</li>', blk, flags=re.S):
        n = eff_len(li); end = li.strip()[-1]
        ok = 75 <= n <= 90 and end not in ".함됨임음짐"
        bad += not ok
        print(f"{n:5.1f} {'통과' if ok else '수정 필요'} | ...{li[-12:]}")
sys.exit(1 if bad else 0)
