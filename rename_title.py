import os

base_dir = r'c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文'
count = 0
for fname in sorted(os.listdir(base_dir)):
    if fname.endswith('.md'):
        fpath = os.path.join(base_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace('# 神々の黄昏 ～日本神話物語～', '# 不完全な神々 ～日本神話物語～')
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f'OK: {fname}')
print(f'\n{count} files updated')
