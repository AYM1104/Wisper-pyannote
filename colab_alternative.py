"""
Colab用代替セットアップ（ログアクセス問題の解決版）
このコードをColabのセルにコピー&ペーストして実行してください
"""

# 1. セットアップ
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 2. トークンを自動取得（代替方法）
import requests
import os
import re
import json

def auto_get_token_alternative():
    """GitHub Actionsからトークンを自動取得（代替方法）"""
    print("🔐 GitHub Actionsからトークンを自動取得中...")
    
    try:
        # 方法1: GitHub Actions APIから最新のワークフロー実行を取得
        url = "https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/workflows/setup_token.yml/runs"
        headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Wisper-Colab-Setup"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            runs = response.json()
            if runs.get("workflow_runs"):
                latest_run = runs["workflow_runs"][0]
                
                print(f"📋 最新のワークフロー実行ID: {latest_run['id']}")
                print(f"📋 実行時刻: {latest_run['created_at']}")
                print(f"📋 ステータス: {latest_run['status']} - {latest_run['conclusion']}")
                
                if latest_run["status"] == "completed" and latest_run["conclusion"] == "success":
                    # 方法2: ワークフローのログを取得
                    logs_url = f"https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/runs/{latest_run['id']}/logs"
                    logs_response = requests.get(logs_url, headers=headers)
                    
                    if logs_response.status_code == 200:
                        logs = logs_response.text
                        print(f"📋 ログサイズ: {len(logs)} 文字")
                        
                        # 複数のパターンでトークンを検索
                        patterns = [
                            r"os\.environ\['HUGGINGFACE_TOKEN'\] = '([^']+)'",
                            r"HUGGINGFACE_TOKEN.*?=.*?'([^']+)'",
                            r"hf_[a-zA-Z0-9_]+",
                            r"'hf_[^']+'"
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, logs)
                            for match in matches:
                                if isinstance(match, str) and match.startswith("hf_"):
                                    os.environ["HUGGINGFACE_TOKEN"] = match
                                    print("✅ トークンを自動取得しました")
                                    return True
                        
                        # デバッグ用: ログの一部を表示
                        print("📋 ログの一部:")
                        lines = logs.split('\n')
                        for i, line in enumerate(lines):
                            if "HUGGINGFACE_TOKEN" in line or "hf_" in line:
                                print(f"  {i}: {line}")
                                if i > 10:  # 最初の10行だけ表示
                                    break
                    
                    else:
                        print(f"⚠️  ログ取得エラー: {logs_response.status_code}")
                        print("📋 ログアクセスに問題があります。手動設定に切り替えます。")
                else:
                    print(f"⚠️  最新のワークフローが完了していません")
            else:
                print("⚠️  ワークフローの実行履歴が見つかりません")
        else:
            print(f"⚠️  GitHub APIエラー: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  自動取得に失敗しました: {e}")
    
    return False

# トークンを自動取得
token_set = auto_get_token_alternative()

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
