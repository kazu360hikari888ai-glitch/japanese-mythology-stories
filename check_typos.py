import os
import glob
import re
from collections import Counter
import difflib

def check_files(directory):
    md_files = glob.glob(os.path.join(directory, "*.md"))
    
    katakana_pattern = re.compile(r'[ア-ンー]{3,}')
    all_katakana = Counter()
    
    suspicious_patterns = [
        (re.compile(r'をを'), "「をを」の連続"),
        (re.compile(r'にに'), "「にに」の連続"),
        (re.compile(r'でで'), "「でで」の連続"),
        (re.compile(r'てて'), "「てて」の連続"),
        (re.compile(r'とと'), "「とと」の連続"),
        (re.compile(r'。。'), "「。。」の連続"),
        (re.compile(r'、、'), "「、、」の連続"),
        (re.compile(r'？！'), "「？！」（！？が一般的）"),
    ]

    typos_found = []

    for path in md_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Extract Katakana
            words = katakana_pattern.findall(content)
            all_katakana.update(words)
            
            # Check suspicious patterns
            for line_idx, line in enumerate(lines):
                for pattern, desc in suspicious_patterns:
                    if pattern.search(line):
                        if desc == "「てて」の連続" and any(x in line for x in ["見捨てて", "立てて", "隔てて", "果てて", "棄てて", "勝てて", "満ちてて"]):
                            continue
                        if desc == "「とと」の連続" and any(x in line for x in ["いとと", "人とと", "事とと", "命とと"]):
                            continue
                        typos_found.append((os.path.basename(path), line_idx + 1, desc, line.strip()))

    with open("typo_report.txt", "w", encoding="utf-8") as out:
        out.write("=== Suspicious Katakana (Potential God Name Typos) ===\n")
        unique_words = list(all_katakana.keys())
        for i in range(len(unique_words)):
            for j in range(i + 1, len(unique_words)):
                w1 = unique_words[i]
                w2 = unique_words[j]
                if len(w1) > 3 and len(w2) > 3 and abs(len(w1) - len(w2)) <= 1:
                    ratio = difflib.SequenceMatcher(None, w1, w2).ratio()
                    if ratio > 0.8:
                        f1 = all_katakana[w1]
                        f2 = all_katakana[w2]
                        if f1 > 5 and f2 <= 2:
                            out.write(f"Possible typo: {w2} (Count: {f2}) -> meant {w1}? (Count: {f1})\n")
                        elif f2 > 5 and f1 <= 2:
                            out.write(f"Possible typo: {w1} (Count: {f1}) -> meant {w2}? (Count: {f2})\n")

        out.write("\n=== Rare Katakana Words (Occurs 1-2 times, please manually check) ===\n")
        rare_words = [w for w, c in all_katakana.items() if c <= 2]
        out.write(", ".join(rare_words) + "\n")

        out.write("\n=== Text Pattern Warnings ===\n")
        for path_name, line_num, desc, line_content in typos_found:
            out.write(f"{path_name} (Line {line_num}): {desc} -> {line_content}\n")

if __name__ == "__main__":
    target_dir = r"c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文"
    check_files(target_dir)
