import os

base = r'c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文'
f14 = os.path.join(base, '第14話_天の斑馬.md')
with open(f14, 'r', encoding='utf-8') as f:
    content = f.read()
print(f'14話: chars={len(content)}, lines={content.count(chr(10))+1}')

# Quick total
total_chars = 0
for fname in sorted(os.listdir(base)):
    if fname.endswith('.md'):
        with open(os.path.join(base, fname), 'r', encoding='utf-8') as f:
            c = f.read()
        total_chars += len(c)
print(f'Total chars: {total_chars}')
