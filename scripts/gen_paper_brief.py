# -*- coding: utf-8 -*-
"""논문 정리본 HTML 생성 (구단별 정리본 양식 기반, 회색·검정 표지)
사용법: python scripts/gen_paper_brief.py templates/paper-brief/<슬러그>.json templates/paper-brief/<슬러그>.html
json 키: cat_label, title_cover(표지 제목, <br> 허용), title(쪽 제목용), en, authors, journal, pub, link,
         h2~h5(헤드 메시지 3개씩), l_title, l_sub, l_items, r_title, r_sub, cards,
         p3_title, p3_sub, findings(최대 6개: [제목, 문단1, 문단2, 근거]),
         p4_title, p4_left, flow, p4_right, devices, p5_title, p5_left, table, imp, lim, src2~src5
"""
import re, sys, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = open(os.path.join(ROOT, 'templates/club-brief/manchester-united.html'), encoding='utf-8').read()
CSS = base.split('<style>')[1].split('</style>')[0]
LOGO = re.search(r'<img class="co" src="([^"]+)"', base).group(1)
GRAY, INK = '#1A1A1A', '#1A1A1A'
CSS = re.sub(r':root\{--club:[^}]*\}', f':root{{--club:{GRAY};--club2:#FFFFFF;--ink:{INK}}}', CSS)
CSS = re.sub(r':root\{--title:[^}]*\}', f':root{{--title:{INK};--bar:{GRAY}}}', CSS)
CSS += ('.imp{background:#f4f4f4!important;border-color:#dcdcdc!important}'
        '.cv .ttl{font-size:28pt!important;line-height:1.38!important}'
        '.cv .meta{font-size:10.5pt!important}'
        # 가독성: 논문 정리본의 글자는 모두 검정 계열로 통일
        'body,h1,.pc h3,.card .v,.pc p,.flow .d,td,.head li{color:#1A1A1A!important}'
        '.card .k,.pc h3 span,.imp h4{color:#1A1A1A!important}'
        '.top,h1 small,h2 small,.pc .s,td.m,.src,.no{color:#3A3A3A!important}')
TOP = '<div class="top"><span><b>더이룸 스포츠</b> &nbsp;|&nbsp; 논문 정리</span><span>{r}</span></div>'
def head(items): return '<div class="head"><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>'
def ul(items): return '<ul>' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in items) + '</ul>'

def build(d):
    P = []
    P.append(f'''<div class="pg cv">
 <div class="red"></div><div class="yel"></div>
 <div class="up">
  <div class="lab">논문 정리 &nbsp;|&nbsp; {d['cat_label']}</div>
  <div class="ttl">{d['title_cover']}</div>
  <div class="bar"></div>
  <div class="meta">원제 : {d['en']}<br>저자 : {d['authors']}<br>게재 : {d['journal']}, {d['pub']}<br>원문 : {d['link']}<br>정리일 : 2026.11.24</div>
 </div>
 <img class="co" src="{LOGO}" alt="">
</div>''')
    cards = ''.join(f'<div class="card"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in d['cards'])
    P.append(f'''<div class="pg">
 {TOP.format(r='2026. 11. 24')}
 <h1>{d['title']}<small>{d['journal']}</small></h1>
 {head(d['h2'])}
 <div class="cols">
  <div class="col"><h2>{d['l_title']}<small>{d['l_sub']}</small></h2>{ul(d['l_items'])}</div>
  <div class="col"><h2>{d['r_title']}<small>{d['r_sub']}</small></h2><div class="num">{cards}</div></div>
 </div>
 <div class="src">출처: {d['src2']}</div><div class="no">@@NO@@</div>
</div>''')
    pcs = ''.join(f'<div class="pc"><h3><span>{i+1}</span>{t}</h3><p>{a}</p><p>{b}</p><div class="s">{s}</div></div>' for i, (t, a, b, s) in enumerate(d['findings']))
    P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>{d['p3_title']}<small>{d['p3_sub']}</small></h1>
 {head(d['h3'])}
 <div class="grid6">{pcs}</div>
 <div class="src">출처: {d['src3']}</div><div class="no">@@NO@@</div>
</div>''')
    for e in d.get('extra_pages', []):
        ecs = ''.join(f'<div class="pc"><h3><span>{i+1}</span>{t}</h3><p>{a}</p><p>{b}</p><div class="s">{s}</div></div>' for i, (t, a, b, s) in enumerate(e['cards']))
        P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>{e['title']}<small>{e.get('sub', '')}</small></h1>
 {head(e['head'])}
 <div class="grid6">{ecs}</div>
 <div class="src">출처: {e['src']}</div><div class="no">@@NO@@</div>
</div>''')
    if d.get('flow'):
        fl = ''.join(f'<div{" class=\"a\"" if i == len(d["flow"]) - 1 else ""}><span class="t">{t}</span><div class="d">{x}</div></div>' for i, (t, x) in enumerate(d['flow']))
        P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>{d['p4_title']}</h1>
 {head(d['h4'])}
 <div class="cols">
  <div class="col" style="flex:0.92"><h2>{d['p4_left']}</h2><div class="flow">{fl}</div></div>
  <div class="col" style="flex:1.08"><h2>{d['p4_right']}</h2>{ul(d['devices'])}</div>
 </div>
 <div class="src">출처: {d['src4']}</div><div class="no">@@NO@@</div>
</div>''')
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td class="m">{c}</td></tr>' for a, b, c in d['table'])
    P.append(f'''<div class="pg">
 {TOP.format(r=d['short'])}
 <h1>{d['p5_title']}</h1>
 {head(d['h5'])}
 <div class="cols">
  <div class="col" style="flex:1.12"><h2>{d['p5_left']}</h2><table>{rows}</table></div>
  <div class="col" style="flex:0.88">
   <div class="imp" style="margin-top:0"><h4>시사점</h4><ul>{''.join(f'<li>{x}</li>' for x in d['imp'])}</ul></div>
   <div class="lim"><h4>확인 범위와 한계</h4><ul>{''.join(f'<li>{x}</li>' for x in d['lim'])}</ul></div>
  </div>
 </div>
 <div class="src">출처: {d['src5']}</div><div class="no">@@NO@@</div>
</div>''')
    title = re.sub('<[^>]+>', ' ', d['title'])
    tot = len(P)
    for k in range(1, tot):
        P[k] = P[k].replace('@@NO@@', f'{k + 1} / {tot}')
    html = f'<!doctype html><html lang="ko"><head><meta charset="utf-8">\n<title>{title}</title>\n<style>{CSS}</style></head><body>\n\n' + '\n\n'.join(P) + '\n</body></html>\n'
    body = html.split('</style>')[1].replace(LOGO, '')
    assert "'" not in body, 'straight quote'
    assert '—' not in html and '–' not in html
    return html

if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    open(sys.argv[2], 'w', encoding='utf-8').write(build(d))
