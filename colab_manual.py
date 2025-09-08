"""
Colabでの手動実行例（ファイルアップロードエラー対策版）
このファイルをColabで実行してください
"""

# 1. Hugging Faceトークンの設定
import os
os.environ["HUGGINGFACE_TOKEN"] = "hf_your_token_here"

# 2. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 3. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 4. 手動でファイルをアップロード
from google.colab import files
uploaded = files.upload()

# 5. アップロードしたファイル名を確認
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 6. 実行
!python main.py --audio "/content/{audio_file}" --model large-v3 --do_diar

# 7. 生成されたファイルをダウンロード
import os
base_name = audio_file.split('.')[0]
srt_file = f"/content/{base_name}.srt"
tsv_file = f"/content/{base_name}.diar.tsv"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"字幕ファイルをダウンロードしました: {base_name}.srt")

if os.path.exists(tsv_file):
    files.download(tsv_file)
    print(f"話者分離ファイルをダウンロードしました: {base_name}.diar.tsv")
