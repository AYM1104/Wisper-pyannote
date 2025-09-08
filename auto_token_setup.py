"""
自動トークン取得スクリプト
Colabで実行してください
"""

import requests
import os
import re

def auto_get_token():
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
                        
                        # 正規表現でトークンを抽出
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

# 実行
if __name__ == "__main__":
    success = auto_get_token()
    if success:
        print("🎉 トークンが設定されました！話者分離機能が使用可能です。")
    else:
        print("❌ 自動取得に失敗しました。手動でトークンを設定してください。")
