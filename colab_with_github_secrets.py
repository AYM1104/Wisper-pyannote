"""
Colab用セットアップ（GitHub Secrets版）
このファイルをColabで実行してください
"""

import subprocess
import os

# 1. リポジトリのクローン
subprocess.run(["git", "clone", "https://github.com/AYM1104/Wisper-pyannote.git"])
os.chdir("Wisper-pyannote")

# 2. 依存関係のインストール
subprocess.run(["pip", "install", "-r", "requirements.txt"])
subprocess.run(["pip", "install", "--upgrade", "torch", "torchaudio", "torchvision"])

# 3. GitHub Actionsからトークンを自動取得
import requests
import os
import json

def get_token_from_github():
    """GitHub Actionsからトークンを自動取得"""
    print("🔐 GitHub Actionsからトークンを自動取得中...")
    
    try:
        # GitHub Actions APIから最新のワークフロー実行を取得
        url = "https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/workflows/setup_token.yml/runs"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Wisper-Colab-Setup"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            runs = response.json()
            if runs.get("workflow_runs"):
                latest_run = runs["workflow_runs"][0]
                
                if latest_run["status"] == "completed" and latest_run["conclusion"] == "success":
                    # ワークフローのログを取得
                    logs_url = f"https://api.github.com/repos/AYM1104/Wisper-pyannote/actions/runs/{latest_run['id']}/logs"
                    logs_response = requests.get(logs_url, headers=headers)
                    
                    if logs_response.status_code == 200:
                        logs = logs_response.text
                        # ログからトークンを抽出
                        lines = logs.split('\n')
                        for line in lines:
                            if "os.environ['HUGGINGFACE_TOKEN']" in line and "hf_" in line:
                                # トークンを抽出
                                token_start = line.find("'") + 1
                                token_end = line.rfind("'")
                                token = line[token_start:token_end]
                                
                                if token and token.startswith("hf_"):
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
    
    # 自動取得に失敗した場合の手動設定
    print("")
    print("📋 手動でトークンを設定してください:")
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
    subprocess.run([
        "python", "main.py", 
        "--audio", f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}", 
        "--model", "large-v3", 
        "--do_diar"
    ])
else:
    # 話者分離なしで実行
    print("🚀 話者分離なしで実行します...")
    subprocess.run([
        "python", "main.py", 
        "--audio", f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}", 
        "--model", "large-v3"
    ])

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
