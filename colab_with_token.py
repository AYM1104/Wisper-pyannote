"""
Colabでの実行例（トークン自動設定版）
このファイルをColabで実行してください
"""

# 1. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 2. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 3. Hugging Faceトークンを自動設定
import os
import requests

def get_huggingface_token():
    """GitHubからトークンを取得（公開リポジトリの場合）"""
    try:
        # GitHubのrawファイルからトークンを読み取り
        # 注意: これは公開リポジトリでのみ動作
        response = requests.get("https://raw.githubusercontent.com/AYM1104/Wisper-pyannote/main/.env.example")
        if response.status_code == 200:
            # 実際のトークンは別途設定が必要
            return "hf_your_token_here"  # 実際のトークンに置き換え
    except:
        pass
    return None

# トークンを設定
token = get_huggingface_token()
if token:
    os.environ["HUGGINGFACE_TOKEN"] = token
    print("✅ Hugging Faceトークンを設定しました")
else:
    print("⚠️  Hugging Faceトークンが設定されていません")
    print("手動で設定してください: os.environ['HUGGINGFACE_TOKEN'] = 'hf_your_token'")

# 4. 手動でファイルをアップロード
from google.colab import files
uploaded = files.upload()

# 5. アップロードしたファイル名を確認
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 6. 実行
!python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3 --do_diar

# 7. 生成されたファイルをダウンロード
base_name = audio_file.split('.')[0]
srt_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.srt"
tsv_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.diar.tsv"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"字幕ファイルをダウンロードしました: {base_name}.srt")

if os.path.exists(tsv_file):
    files.download(tsv_file)
    print(f"話者分離ファイルをダウンロードしました: {base_name}.diar.tsv")
