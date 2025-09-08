"""
Colab用簡単セットアップ（トークン共有版）
このファイルをColabで実行してください
"""

# 1. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 2. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 3. トークンを自動設定
import base64
import os

def setup_shared_token():
    """共有トークンを設定"""
    # 暗号化されたトークン（管理者が設定）
    encrypted_token = "aGZfeW91cl90b2tlbl9oZXJl"  # 実際のトークンに置き換え
    
    try:
        # トークンを復号化
        token = base64.b64decode(encrypted_token).decode('utf-8')
        
        # 環境変数に設定
        os.environ["HUGGINGFACE_TOKEN"] = token
        
        print("✅ 共有トークンを設定しました")
        print("話者分離機能が使用可能になりました")
        return True
        
    except Exception as e:
        print(f"❌ トークンの設定に失敗しました: {e}")
        print("管理者に連絡してください")
        return False

# トークンを設定
token_set = setup_shared_token()

# 4. 手動でファイルをアップロード
from google.colab import files
uploaded = files.upload()

# 5. アップロードしたファイル名を確認
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 6. 実行
if token_set:
    # 話者分離付きで実行
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3 --do_diar
else:
    # 話者分離なしで実行
    !python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3

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
