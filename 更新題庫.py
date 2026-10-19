# 修改 questions.json 之後執行這個檔案，把題庫同步到 index.html 裡：
#   python 更新題庫.py
import io, json, os

here = os.path.dirname(os.path.abspath(__file__))
bank = json.load(io.open(os.path.join(here, 'questions.json'), encoding='utf-8'))
lst = bank['成語庫']

# 基本檢查
names = [x['成語'] for x in lst]
problems = []
for x in lst:
    if len(x['成語']) != 4:
        problems.append(f"{x['成語']}：不是四個字")
    if x.get('難度') not in (1, 2, 3, 4, 5):
        problems.append(f"{x['成語']}：難度要是 1～5")
    if not x.get('類別'):
        problems.append(f"{x['成語']}：沒有類別")
    for s in x.get('例句', []):
        if s.count('（　　　　）') != 1:
            problems.append(f"{x['成語']}：例句要有一個（　　　　）空格 → {s}")
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
print(f'已更新 index.html：共 {len(lst)} 個成語')
