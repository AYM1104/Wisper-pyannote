"""
Colabでの実行例
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

# 4. 実行（自動でファイルアップロードとダウンロード）
!python main.py
