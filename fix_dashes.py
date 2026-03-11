import os, glob, re

target_dir = r"c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文"
md_files = glob.glob(os.path.join(target_dir, "*.md"))

for path in md_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # "一" or "ー" がダッシュ "──" と繋がってしまう問題の修正
    original_content = content
    content = re.sub(r'──一', '── 一', content)
    content = re.sub(r'一──', '一 ──', content)
    content = re.sub(r'──ー', '── ー', content)
    content = re.sub(r'ー──', 'ー ──', content)

    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed dashes in {os.path.basename(path)}")

print("Done fixing markdown dashes.")
