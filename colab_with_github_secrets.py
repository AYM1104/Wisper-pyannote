"""
Colab用セットアップ（GitHub Secrets版）
このファイルをColabで実行してください
"""

# 1. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 2. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 3. GitHub Actionsからトークンを取得
import requests
import os

def get_token_from_github():
    """GitHub Actionsからトークンを取得"""
    print("🔐 GitHub Actionsからトークンを取得中...")
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
    
    # ユーザーにトークン設定を促す
    token = input("トークンを設定しましたか？ (y/n): ")
    if token.lower() == 'y':
        if os.getenv("HUGGINGFACE_TOKEN"):
            print("✅ トークンが設定されています")
            return True
        else:
            print("❌ トークンが設定されていません")
            return False
    else:
        print("⚠️  トークンが設定されていません")
        return False

# トークンを確認
token_set = get_token_from_github()

# 4. 手動でファイルをアップロード
from google.colab import files
uploaded = files.upload()

# 5. アップロードしたファイル名を確認
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 6. 実行
if token_set:
    # 話者分離付きで実行
    print("🚀 話者分離付きで実行します...")
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3 --do_diar
else:
    # 話者分離なしで実行
    print("🚀 話者分離なしで実行します...")
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3

# 7. 生成されたファイルをダウンロード
base_name = audio_file.split('.')[0]
srt_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.srt"
tsv_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.diar.tsv"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"✅ 字幕ファイルをダウンロードしました: {base_name}.srt")

if os.path.exists(tsv_file):
    files.download(tsv_file)
    print(f"✅ 話者分離ファイルをダウンロードしました: {base_name}.diar.tsv")
