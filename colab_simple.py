"""
Colab用超簡単セットアップ（文字起こしのみ）
このコードをColabのセルにコピー&ペーストして実行してください
"""

# 1. セットアップ
import os
os.environ['COLAB_MODE'] = 'false'

print("🚀 Wisper-pyannote セットアップ開始...")
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision
print("✅ セットアップ完了")

# 2. ファイルをアップロード
print("\n📁 音声ファイルをアップロードしてください...")
from google.colab import files
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]
print(f"✅ アップロード完了: {audio_file}")

# 3. 文字起こし実行
print(f"\n🎤 文字起こしを開始します...")
print(f"ファイル: {audio_file}")
print(f"モデル: large-v3")
print(f"出力: テキストのみ（タイムスタンプなし）")

!python main.py --audio "/content/{audio_file}" --model large-v3

# 4. テキスト抽出（進捗バー付き）
from tqdm import tqdm
print(f"\n📝 テキストを抽出中...")
base_name = audio_file.split('.')[0]
srt_path = f"/content/Wisper-pyannote/{base_name}.srt"

with open(srt_path, 'r', encoding='utf-8') as f:
    srt_content = f.read()

lines = srt_content.strip().split('\n')
text_lines = []

print("テキスト行を抽出中...")
for i, line in enumerate(tqdm(lines, desc="テキスト抽出")):
    line = line.strip()
    if line.isdigit() or '-->' in line or not line:
        continue
    text_lines.append(line)

text_content = '\n'.join(text_lines)
text_file = f"/content/Wisper-pyannote/{base_name}.txt"
with open(text_file, 'w', encoding='utf-8') as f:
    f.write(text_content)

print(f"✅ テキスト抽出完了: {len(text_lines)}行")

# 5. ダウンロード
print(f"\n📥 ファイルをダウンロード中...")
files.download(text_file)
print("✅ テキストファイルをダウンロードしました")