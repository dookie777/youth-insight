# -*- coding: utf-8 -*-
import re, sys, json
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = open(os.path.join(ROOT, 'templates/club-brief/manchester-united.html'), encoding='utf-8').read()
CSS = base.split('<style>')[1].split('</style>')[0]
LOGO = re.search(r'<img class="co" src="([^"]+)"', base).group(1)
TOP = '<div class="top"><span><b>더이룸 스포츠</b> &nbsp;|&nbsp; 구단별 유소년 비전·철학 정리</span><span>{r}</span></div>'
def head(items): return '<div class="head"><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
def ul(items): return '<ul>' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in items) + '</ul>'
def build(d):
    css = re.sub(r':root\{[^}]*\}', f":root{{--club:{d['club']};--club2:{d['club2']};--ink:{d['ink']}}}", CSS)
    n = 5
    P = []
    P.append(f'''<div class="pg cv">
 <div class="red"></div><div class="yel"></div>
 <div class="up">
  <div class="lab">구단별 유소년 비전·철학 정리 &nbsp;|&nbsp; 00 비전과 철학</div>
  <div class="ttl">{d['name']}<br>{d['cover2']}</div>
  <div class="bar"></div>
  <div class="meta">대상 : {d['target']}<br>출처 : {d['cover_src']}<br>정리일 : 2026.11.24</div>
 </div>
 <img class="co" src="{LOGO}" alt="">
</div>''')
    cards = ''.join(f'<div class="card"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in d['cards'])
    P.append(f'''<div class="pg">
 {TOP.format(r='2026. 11. 24')}
 <h1>{d['name']} {d['cover2']}<small>{d['league']}</small></h1>
 {head(d['h2'])}
 <div class="cols">
  <div class="col"><h2>{d['l_title']}<small>{d['l_sub']}</small></h2>{ul(d['l_items'])}</div>
  <div class="col"><h2>{d['r_title']}<small>{d['r_sub']}</small></h2><div class="num">{cards}</div></div>
 </div>
 <div class="src">출처: {d['src2']}</div><div class="no">2 / {n}</div>
</div>''')
    pcs = ''.join(f'<div class="pc"><h3><span>{i+1}</span>{t}</h3><p>{a}</p><p>{b}</p><div class="s">{s}</div></div>' for i, (t, a, b, s) in enumerate(d['principles']))
    P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>철학을 이루는 여섯 가지 원칙<small>{d['p_sub']}</small></h1>
 {head(d['h3'])}
 <div class="grid6">{pcs}</div>
 <div class="src">출처: {d['src3']}</div><div class="no">3 / {n}</div>
</div>''')
    fl = ''.join(f'<div{" class=\"a\"" if i == len(d["flow"]) - 1 else ""}><span class="t">{t}</span><div class="d">{x}</div></div>' for i, (t, x) in enumerate(d['flow']))
    P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>철학이 운영에 반영된 방식</h1>
 {head(d['h4'])}
 <div class="cols">
  <div class="col" style="flex:0.92"><h2>연령 단계별 운영</h2><div class="flow">{fl}</div></div>
  <div class="col" style="flex:1.08"><h2>철학을 뒷받침하는 운영 장치</h2>{ul(d['devices'])}</div>
 </div>
 <div class="src">출처: {d['src4']}</div><div class="no">4 / {n}</div>
</div>''')
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td class="m">{c}</td></tr>' for a, b, c in d['timeline'])
    P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>{d['t5']}</h1>
 {head(d['h5'])}
 <div class="cols">
  <div class="col" style="flex:1.12"><h2>주요 경과</h2><table>{rows}</table></div>
  <div class="col" style="flex:0.88">
   <div class="imp" style="margin-top:0"><h4>시사점</h4><ul>{''.join(f'<li>{x}</li>' for x in d['imp'])}</ul></div>
   <div class="lim"><h4>확인 범위와 한계</h4><ul>{''.join(f'<li>{x}</li>' for x in d['lim'])}</ul></div>
  </div>
 </div>
 <div class="src">출처: {d['src5']}</div><div class="no">5 / {n}</div>
</div>''')
    html = f'<!doctype html><html lang="ko"><head><meta charset="utf-8">\n<title>{d["name"]} {d["cover2"]}</title>\n<style>{css}</style></head><body>\n\n' + '\n\n'.join(P) + '\n</body></html>\n'
    assert "'" not in html.split('</style>')[1].replace(LOGO, ''), 'straight quote'
    assert '—' not in html and '–' not in html
    return html
if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    open(sys.argv[2], 'w', encoding='utf-8').write(build(d))
