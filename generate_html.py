"""
全50話のHTMLページを一括生成するスクリプト。
各話の Markdown 本文を読み込み、episode HTML テンプレートに当てはめて出力する。
"""
import os
import re
import glob

# === 各話のメタデータ ===
episodes = [
    # (話数, タイトル, 部番号, 部名, 概要)
    (1, "混沌の卵", 1, "天地開闢篇", "何もなかった──嘘だ。すべてが在りすぎたのだ。混沌の底で最初の「意志」が目覚める。"),
    (2, "神世七代", 1, "天地開闢篇", "独り神たちの孤独な誕生。最後に現れた男女神に、途方もない命令が下される。"),
    (3, "天の浮橋", 1, "天地開闢篇", "天沼矛で混沌の海をかき回し、世界最初の大地を創る。しかしイザナミが先に声をかけた。"),
    (4, "ヒルコの涙", 1, "天地開闢篇", "声も骨もない最初の子を、葦の舟に乗せて海へ流す。世界に「慟哭」が生まれた瞬間。"),
    (5, "国生み ─ 八つの島", 1, "天地開闢篇", "正しき順で結ばれた二柱が、八つの島を次々と生む。束の間の幸福が世界を満たしていく。"),
    (6, "火の神", 1, "天地開闢篇", "最後の子は──火だった。母の体を内から焼きながら生まれ、イザナミは目を閉じる。"),
    (7, "剣と涙", 1, "天地開闢篇", "妻を焼いた火の子を十拳剣で斬る。血から戦の神が生まれ、父は黄泉へと歩き出す。"),
    (8, "黄泉の国", 1, "天地開闢篇", "死者の国で妻の声を聞く。「私の姿を見ないで」──その約束は、守られなかった。"),
    (9, "腐乱の女神", 1, "天地開闢篇", "腐乱の姿を見られた女神の怒りと恥。黄泉醜女が闇を駆け、愛は呪いに変わる。"),
    (10, "千引の岩 ─ 永遠の別離", 1, "天地開闢篇", "岩の向こうで妻が静かに言う。「愛しい人、あなたの国の民を──毎日千人、殺してやる」。その言葉に、愛と憎しみの境界が消えた。"),

    (11, "月の裁き", 2, "高天原篇", "正しさだけを信じた月神は、食の女神を斬る。その刃が──昼と夜を永遠に引き裂いた。"),
    (12, "嵐の神", 2, "高天原篇", "母を知らぬ嵐神スサノオ、泣くことしかできない。姉へ向かうその足音は大地を震わす慟哭だった。"),
    (13, "誓約（うけい）", 2, "高天原篇", "剣と勾玉を噛み砕き、誓約で心の清さを示す。しかし「勝った」と叫ぶ不器用が災いの幕を開ける。"),
    (14, "天の斑馬", 2, "高天原篇", "斑馬の皮が機織殿に落ちた時、一人の織女が命を落とす。太陽の女神が初めて微笑みを止めた。"),
    (15, "天岩戸 ─ 太陽消失", 2, "高天原篇", "太陽が岩戸に隠れ、世界は闇に沈んだ。知恵の神が示した策は──絶望の中で、笑うこと。"),
    (16, "神々の祭り", 2, "高天原篇", "ウズメは闇の中で裸身を晒し、狂ったように舞う。八百万の大笑いが岩の向こうの太陽に届く。"),
    (17, "覗く太陽", 2, "高天原篇", "「あなたより尊い神が現れた」──嘘の誘いに覗いた太陽は、鏡の中に仮面を脱いだ己を見た。"),
    (18, "光の帰還", 2, "高天原篇", "タヂカラオの怪力が岩戸を引き開け、光が爆ぜた。太陽は──もう一人で背負わないと決めた。"),
    (19, "泣く乙女", 2, "高天原篇", "追放されたスサノオが出雲で出会ったのは、七人の姉を喪い声なく泣く末娘だった。"),
    (20, "八俣大蛇（ヤマタノオロチ）", 2, "高天原篇", "七回の別れの酒が、八つの首を眠らせる。初めて誰かを守るために剣を振るい──尾から神剣が現れた。"),

    (21, "須賀の宮 ─ 嵐神の贖罪", 3, "出雲篇", "大蛇を斬った嵐神が詠む、日本最初の歌。天叢雲剣を姉に贈り、贖罪の宮が建つ。"),
    (22, "因幡の白兎", 3, "出雲篇", "皮を剥がれた白兎に、荷物持ちの末っ子だけが手を差し伸べる。その優しさが運命を変えた。"),
    (23, "二度の死", 3, "出雲篇", "焼けた岩に潰され、大木に挟まれ──二度殺された末っ子を、母は命を削って蘇らせる。"),
    (24, "蛇の室屋", 3, "出雲篇", "蛇、ムカデ、蜂──根の国の試練の夜ごと、スセリビメの声が少しずつ愛に変わる。"),
    (25, "野火の試練", 3, "出雲篇", "四方から迫る野火。地の底で助けたのは、「大丈夫だよ」を覚えていた一匹のネズミだった。"),
    (26, "大脱走", 3, "出雲篇", "スサノオの髪を柱に結び、宝を奪い、二人は走る。背に届く怒声は──祝福だった。"),
    (27, "大国主の帰還", 3, "出雲篇", "根の国を越えた男が出雲に還る。八十の兄を退けたのは、大刀ではなく──静かな目だった。"),
    (28, "国造りの仲間たち", 3, "出雲篇", "手の平に乗る小さな知恵の神と、自らの魂の分身。国造りの果てに大国主が信じたのは己自身。"),
    (29, "恋多き神", 3, "出雲篇", "恋多き大国主に、スセリビメの声が氷点下に凍る。嫉妬の歌の底に、愛が燃えていた。"),
    (30, "国譲りの序曲", 3, "出雲篇", "豊かな出雲を高天原が欲する。稲佐の浜に剣を逆さに突き立て、雷神が降りてきた。"),

    (31, "国譲り", 4, "天孫降臨篇", "「大丈夫だよ」──口癖の主が、初めてその言葉を失う。砂浜に独り残る国譲りの夜。"),
    (32, "天孫ニニギ", 4, "天孫降臨篇", "「えっ」──それが天孫の第一声だった。三種の神器を抱え、不完全な若き神が雲を突き抜ける。"),
    (33, "猿田彦 ─ 道の守護者", 4, "天孫降臨篇", "異形の巨神に怯む一行の中、ウズメだけが笑って歩み寄る。天の八衢で始まる、鼻の長い恋。"),
    (34, "高千穂の降臨", 4, "天孫降臨篇", "雲を突き抜け、霧の山頂に降り立った天孫の最初の行為はくしゃみだった。冷たい土の感触に戸惑いながら、この男は思う──ここが、私が治めるべき地なのか、と。"),
    (35, "花の姫と岩の姫", 4, "天孫降臨篇", "花を選び、岩を「醜い」と返した。その一言で──人は永遠を失い、散る命を生きることになる。"),
    (36, "炎の産屋", 4, "天孫降臨篇", "疑うなら証明する──花の姫は自ら産屋に火を放つ。女の怒りが炎になる時、三つの命が燃え残る。"),
    (37, "海幸彦と山幸彦", 4, "天孫降臨篇", "たった一本の釣り針が返せない。兄の支配に泣く弟は、竹籠の舟で海の底へ沈んでいく。"),
    (38, "海神の宮殿", 4, "天孫降臨篇", "海底の宮殿で三年、愛に溺れて針を忘れた。ため息一つで現実が蘇り、山幸彦は海を発つ。"),
    (39, "兄の屈服", 4, "天孫降臨篇", "潮満珠が海を膨らませ、兄が膝をつく。しかし弟は踏みつけず──その手を取り、立たせた。"),
    (40, "産屋の秘密 ─ 鰐の姿", 4, "天孫降臨篇", "「見ないで」──また同じ禁忌。鰐の姿で泣く妻は海に帰り、残された子がやがて神武となる。"),

    (41, "日向を発つ", 5, "神武東征篇", "末弟は、まだ何も知らなかった。東に何があるかも、兄たちのうち何人が帰れないかも。ただ兄の手が肩に置かれた、最後の朝の話だ。"),
    (42, "十六年の航海", 5, "神武東征篇", "最初は泣いていた。十六年後、同じ男が血で濡れた剣を川で洗いながら、ただ前を見ていた。旅が人を作るのではない──喪失が作るのだ。"),
    (43, "孔舎衙坂の敗北", 5, "神武東征篇", "太陽に向かって攻めた愚かさ。兄の手が弟の肩に届かず落ちた時、東征の本当の代償が始まる。"),
    (44, "熊野の闇 ─ 毒気と八咫烏", 5, "神武東征篇", "三兄弟が海に消え、毒気が最後の一人を倒す。闇の底で霊剣が光り、三本足の烏が道を示す。"),
    (45, "兄宇迦斯の罠", 5, "神武東征篇", "罠の匂いを嗅ぎ分け、策士を己の策で殺す。酒宴の歌が合図に変わる時、祖先の血が繰り返す。"),
    (46, "長髄彦との再戦", 5, "神武東征篇", "もう一人の天孫が大和にいた。正義と正義がぶつかり、敗者の目に映ったのは──守りたかった空だった。"),
    (47, "橿原の宮", 5, "神武東征篇", "三人の兄を失った末弟が、震える声で最初の王となる。不完全だからこそ──始まる。"),
    (48, "ヒメタタライスズ ─ 皇后の秘密", 5, "神武東征篇", "自分の名前が嫌いだった。「タタラ」──炉の火。なぜ私の名に、そんな熱い言葉が入っているのか。その答えは、天と地の血が混ざる夜に明かされる。"),
    (49, "三輪山の影", 5, "神武東征篇", "三輪山から見えない糸を引く大国主。仮面を外した「大丈夫」が、初めて本物の声で響く。"),
    (50, "神代の終わり ─ 不完全さの中の美", 5, "神武東征篇", "不完全な神々の手は、いつも届かなかった。その届かなさが──祈りの始まりだった。"),
]

# 本文ファイルからHTMLの本文を読みこむためのマッピング
# (MDファイルの対応する話数の一覧)
def find_md_file(ep_num):
    """話数からMDファイルを探す"""
    base = r"c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\本文"
    # 個別ファイル
    patterns = [
        os.path.join(base, f"第{ep_num:02d}話_*.md"),
        os.path.join(base, f"第{ep_num}話_*.md"),
    ]
    for p in patterns:
        matches = glob.glob(p)
        if matches:
            return matches[0]
    # 複数話ファイル
    range_files = glob.glob(os.path.join(base, "第*話_第*話.md"))
    for f in range_files:
        fname = os.path.basename(f)
        m = re.search(r'第(\d+)話_第(\d+)話', fname)
        if m:
            start, end = int(m.group(1)), int(m.group(2))
            if start <= ep_num <= end:
                return f
    return None

def extract_episode_text_from_md(md_path, ep_num, ep_title):
    """MDファイルからエピソードのHTMLテキストを抽出"""
    if not md_path or not os.path.exists(md_path):
        return f'<p>（第{ep_num}話の本文は準備中です）</p>'

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 複数話ファイルの場合、該当話のセクションを抽出
    fname = os.path.basename(md_path)
    if re.search(r'第\d+話_第\d+話', fname):
        # "# 第XX話" で始まる部分を探す
        pattern = rf'# 第{ep_num}話[「：\s]'
        match = re.search(pattern, content)
        if match:
            start = match.start()
            # 次の "# 第" を探す
            next_match = re.search(r'\n# 第\d+話[「：\s]', content[start+1:])
            if next_match:
                end = start + 1 + next_match.start()
                content = content[start:end]
            else:
                # 最後の "---" or "*──" を探す
                last_sep = content.rfind('\n---\n')
                # 次の部完結マーカーまで
                next_part = re.search(r'\n\*──第.*部', content[start+1:])
                if next_part:
                    content = content[start:start+1+next_part.start()]
                else:
                    content = content[start:]
        else:
            return f'<p>（第{ep_num}話の本文は準備中です）</p>'

    # MD → HTML変換（簡易）
    lines = content.split('\n')
    html_parts = []
    for line in lines:
        line = line.rstrip()
        # ヘッダーをスキップ
        if line.startswith('#') or line.startswith('---') or line.startswith('*──'):
            continue
        if not line:
            continue
        # シーンブレイク
        if line.strip() in ['＊', '　　　　　　　　＊']:
            html_parts.append('    <p class="scene-break">＊</p>')
            continue
        # セリフ（「」を含む行）
        if '「' in line and '」' in line and line.strip().startswith('「'):
            text = line.strip().lstrip('　')
            html_parts.append(f'    <p class="dialogue">{text}</p>')
            continue
        # 通常テキスト
        text = line.strip().lstrip('　')
        if text:
            html_parts.append(f'    <p>{text}</p>')

    return '\n\n'.join(html_parts)


def generate_episode_html(ep_num, title, part_num, part_name, description):
    """エピソードHTMLを生成"""



    # 次話予告
    if ep_num < 50:
        next_ep = episodes[ep_num]
        part_num_next = next_ep[2]
        teaser = f'''
    <section class="next-episode-teaser" id="part{part_num_next}">
      <p class="next-episode-teaser__label">次回予告</p>
      <div class="episodes__grid next-teaser-grid">
        <a href="episode{ep_num+1}.html" class="episode-card episode-card--ep{ep_num+1}">
          <div class="episode-card__visual"><span class="episode-card__number">第 {ep_num+1} 話</span></div>
          <div class="episode-card__body">
            <h3 class="episode-card__title">{next_ep[1]}</h3>
            <p class="episode-card__synopsis">{next_ep[4]}</p>
            <span class="episode-card__cta">読む →</span>
          </div>
        </a>
      </div>
    </section>'''
    else:
        teaser = '''
    <section class="next-episode-teaser">
      <p class="next-episode-teaser__label">── 完 ──</p>
      <div class="episodes__grid next-teaser-grid">
        <div class="episode-card episode-card--final">
          <div class="episode-card__body" style="text-align: center;">
            <h3 class="episode-card__title">全50話 完結</h3>
            <p class="episode-card__synopsis">不完全な神々が紡いだ物語は、ここに幕を閉じる。しかし神々は消えたのではない──この国の隅々に息づいている。</p>
            <a href="index.html" class="episode-card__cta" style="justify-content: center; margin-top: 1.5rem;">目次へ戻る →</a>
          </div>
        </div>
      </div>
    </section>'''

    # 本文の取得
    md_path = find_md_file(ep_num)
    prose_content = extract_episode_text_from_md(md_path, ep_num, title)

    # 読了時間の推計（1分あたり約500文字）
    text_only = re.sub(r'<[^>]+>', '', prose_content)
    char_count = len(text_only)
    read_time = max(1, char_count // 500)

    img_src = f"images/ep{ep_num}.png"
    if not os.path.exists(os.path.join(output_dir, img_src)):
        img_src = f"images/part{part_num}.png"
    episode_img = f'\n  <div class="episode-top-image">\n    <img src="{img_src}" alt="第{ep_num}話 画像">\n  </div>'

    # シェアボタンのURLエンコード
    import urllib.parse
    share_text = f"第{ep_num}話「{title}」─ 不完全な神々 ～日本神話物語～"
    encoded_share_text = urllib.parse.quote(share_text)
    share_url = f"https://twitter.com/intent/tweet?text={encoded_share_text}&hashtags=不完全な神々,日本神話"


    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>第{ep_num}話「{title}」─ 不完全な神々 ～日本神話物語～</title>
  <meta name="description" content="{description}">

  <!-- Open Graph / Twitter Card -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="第{ep_num}話「{title}」─ 不完全な神々">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="images/ep{ep_num}.png">
  <meta name="twitter:card" content="summary_large_image">

  <!-- Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "第{ep_num}話「{title}」",
    "description": "{description}",
    "isPartOf": {{
      "@type": "CreativeWorkSeries",
      "name": "不完全な神々 ～日本神話物語～"
    }},
    "position": {ep_num}
  }}
  </script>

  <!-- Google Fonts (non-blocking) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Shippori+Mincho:wght@400;500;600;700;800&display=swap">

  <link rel="stylesheet" href="style.css?v=21">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2280%22>⛩️</text></svg>">
</head>
<body>

  <header class="reading-header" id="readingHeader">
    <div class="reading-header__inner">
      <a href="index.html" class="reading-header__back">← 目次へ</a>
      <span class="reading-header__title">第{ep_num}話「{title}」</span>
      <div class="reading-font-controls">
        <button class="font-size-btn" data-size="small">小</button>
        <button class="font-size-btn" data-size="medium">中</button>
        <button class="font-size-btn" data-size="large">大</button>
        <button class="theme-toggle" id="themeToggle" aria-label="テーマ切り替え" style="margin-left: var(--space-md);">
          <span class="theme-toggle__icon">🌞</span>
        </button>
      </div>
    </div>
    <div class="reading-header__progress" id="progressBar"></div>
  </header>

  <div class="episode-hero">
    <p class="episode-hero__part">第{part_num}部「{part_name}」</p>
    <p class="episode-hero__number">第 {ep_num} 話</p>
    <h1 class="episode-hero__title">{title}</h1>
    <p class="reading-time">読了目安：約{read_time}分</p>
  </div>
{episode_img}

  <article class="prose" id="proseContent">

{prose_content}

    <div class="episode-share reveal">
      <p class="episode-share__label">このエピソードをシェアする</p>
      <a href="{share_url}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--twitter">𝕏 (Twitter) でシェア</a>
    </div>

  </article>

{teaser}

  <footer class="site-footer">
    <p>不完全な神々 ～日本神話物語～</p>
    <p class="site-footer__copy">&copy; 2025-2026 All rights reserved.</p>
  </footer>

  <script src="reader.js" defer></script>

</body>
</html>'''

    return html


# === メイン処理 ===
output_dir = r"c:\Users\user\Desktop\Antigravity作成ファイル\日本神話\website"

for ep in episodes:
    ep_num, title, part_num, part_name, desc = ep
    # EP 1-3 は既存なのでスキップ（上書きする場合はコメントアウト）
    # if ep_num <= 3:
    #     continue
    html_content = generate_episode_html(ep_num, title, part_num, part_name, desc)
    filepath = os.path.join(output_dir, f"episode{ep_num}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ episode{ep_num}.html 生成完了")

print("\n🎉 全HTMLページ生成完了！")
