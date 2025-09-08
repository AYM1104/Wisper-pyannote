"""
Colab用手動トークン設定版（最も確実）
このコードをColabのセルにコピー&ペーストして実行してください
"""

# 1. セットアップ
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 2. トークンを手動設定
import os

print("🔐 Hugging Faceトークンの設定")
print("")
print("📋 以下の手順でトークンを取得してください:")
print("1. https://github.com/AYM1104/Wisper-pyannote/actions にアクセス")
print("2. 'Setup Token for Colab' ワークフローを実行")
print("3. 表示されたトークンをコピー")
print("4. 以下のコードを実行:")
print("")
print("import os")
print("os.environ['HUGGINGFACE_TOKEN'] = 'コピーしたトークン'")
print("")

# トークンが設定されているかチェック
if os.getenv("HUGGINGFACE_TOKEN"):
    print("✅ トークンが設定されています")
    token_set = True
else:
    print("⚠️  トークンが設定されていません")
    print("上記の手順でトークンを設定してから再実行してください")
    token_set = False

# 3. ファイルをアップロード
from google.colab import files
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 4. 実行
if token_set:
    print("🚀 話者分離付きで実行します...")
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3 --do_diar
else:
    print("🚀 話者分離なしで実行します...")
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3

# 5. 結果をダウンロード
base_name = audio_file.split('.')[0]
srt_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.srt"
tsv_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.diar.tsv"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"✅ 字幕ファイルをダウンロードしました: {base_name}.srt")

if os.path.exists(tsv_file):
    files.download(tsv_file)
    print(f"✅ 話者分離ファイルをダウンロードしました: {base_name}.diar.tsv")
