import os

base = r'c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文'
files = sorted([f for f in os.listdir(base) if f.endswith('.md')])

results = []
for f in files:
    fpath = os.path.join(base, f)
    sz = os.path.getsize(fpath)
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
    char_count = len(content)
    results.append((f, sz, char_count))

with open(r'c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\size_report.txt', 'w', encoding='utf-8') as out:
    out.write("=" * 80 + "\n")
    out.write("全50話 文字数一覧\n")
    out.write("=" * 80 + "\n\n")
    
    for f, sz, cc in results:
        flag = ""
        if cc < 2500:
            flag = " <<< NG"
        elif cc < 3500:
            flag = " << WARNING"
        out.write(f"{f:60s} {cc:>5d}字{flag}\n")
    
    chars = [c for _,_,c in results]
    out.write(f"\n総ファイル数: {len(results)}\n")
    out.write(f"平均: {sum(chars)//len(chars)}字\n")
    out.write(f"最小: {min(chars)}字\n")
    out.write(f"最大: {max(chars)}字\n")
    
    under = [(f,c) for f,_,c in results if c < 3500]
    out.write(f"\n3500字未満: {len(under)}件\n")
    for f,c in under:
        out.write(f"  {c:>5d}字 - {f}\n")

print("Done: size_report.txt")
