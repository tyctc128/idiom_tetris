# 修改題庫之後執行這個檔案，把題庫同步到 index.html 裡：
#   python 更新題庫.py                  → 使用 question2.json（目前遊戲用的題庫）
#   python 更新題庫.py questions.json   → 改用其他題庫檔
import io, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else 'question2.json'
bank = json.load(io.open(os.path.join(here, src), encoding='utf-8'))
lst = bank['成語庫']

# 基本檢查
names = [x['成語'] for x in lst]
problems = []
for x in lst:
    w = x['成語']
    if len(w) != 4:
        problems.append(f"{w}：不是四個字")
    if x.get('難度') not in (1, 2, 3, 4, 5):
        problems.append(f"{w}：難度要是 1～5")
    if not x.get('類別'):
        problems.append(f"{w}：沒有類別")
    for s in x.get('例句', []):
        if s.count('（　　　　）') != 1:
            problems.append(f"{w}：例句要有一個（　　　　）空格 → {s}")
    for o in x.get('選項', []):
        if o and o[0] != w:
            problems.append(f"{w}：選項的第一個要是正解 → {o}")
    for g in x.get('干擾字', []):
        bad = [c for c in g if c in w]
        if bad:
            problems.append(f"{w}：干擾字不能用到答案裡的字 → {''.join(bad)}")
dups = {n for n in names if names.count(n) > 1}
if dups:
    problems.append('重複的成語：' + '、'.join(dups))
if problems:
    print('題庫有問題，請先修正：')
    print('\n'.join(problems))
    raise SystemExit(1)

path = os.path.join(here, 'index.html')
h = io.open(path, encoding='utf-8').read()
start = h.index('window.QUESTION_BANK = ')
end = h.index(';\n', start)
h = h[:start] + 'window.QUESTION_BANK = ' + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + h[end:]
io.open(path, 'w', encoding='utf-8', newline='\n').write(h)
print(f'已用 {src} 更新 index.html：共 {len(lst)} 個成語')
if len(lst) < 40:
    print(f'提醒：一局有 40 題，題庫只有 {len(lst)} 個成語，同一局會有成語重複出現（會換題型或例句）。')
