"""
Colab用超簡単セットアップ
このコードをColabのセルにコピー&ペーストして実行してください
"""

# 1. セットアップ
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 2. トークンを自動取得
import requests
import os
import re

def auto_get_token():
    """GitHub Actionsからトークンを自動取得"""
    print("🔐 GitHub Actionsからトークンを自動取得中...")
    
    try:
        url = "https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/workflows/setup_token.yml/runs"
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Wisper-Colab-Setup"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            runs = response.json()
            if runs.get("workflow_runs"):
                latest_run = runs["workflow_runs"][0]
                
                if latest_run["status"] == "completed" and latest_run["conclusion"] == "success":
                    logs_url = f"https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/runs/{latest_run['id']}/logs"
                    logs_response = requests.get(logs_url, headers=headers)
                    
                    if logs_response.status_code == 200:
                        logs = logs_response.text
                        token_pattern = r"os\.environ\['HUGGINGFACE_TOKEN'\] = '([^']+)'"
                        match = re.search(token_pattern, logs)
                        
                        if match:
                            token = match.group(1)
                            if token.startswith("hf_"):
                                os.environ["HUGGINGFACE_TOKEN"] = token
                                print("✅ トークンを自動取得しました")
                                return True
                    
                    print("⚠️  ログからトークンを抽出できませんでした")
                else:
                    print("⚠️  最新のワークフローが完了していません")
            else:
                print("⚠️  ワークフローの実行履歴が見つかりません")
        else:
            print(f"⚠️  GitHub APIエラー: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  自動取得に失敗しました: {e}")
    
    return False

# トークンを自動取得
token_set = auto_get_token()

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
