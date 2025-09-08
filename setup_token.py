"""
トークン設定用スクリプト
Colabで実行してください
"""

import base64
import os

def setup_token():
    """暗号化されたトークンを復号化して設定"""
    
    # 暗号化されたトークン（実際のトークンをbase64でエンコード）
    # 注意: 実際のトークンは管理者が設定してください
    encrypted_token = "aGZfeW91cl90b2tlbl9oZXJl"  # これは例です
    
    try:
        # トークンを復号化
        token = base64.b64decode(encrypted_token).decode('utf-8')
        
        # 環境変数に設定
        os.environ["HUGGINGFACE_TOKEN"] = token
        
        print("✅ Hugging Faceトークンを設定しました")
        print("話者分離機能が使用可能になりました")
        
        return True
        
    except Exception as e:
        print(f"❌ トークンの設定に失敗しました: {e}")
        print("管理者に連絡してください")
        return False

# 実行
if __name__ == "__main__":
    setup_token()
