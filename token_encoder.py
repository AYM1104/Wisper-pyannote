"""
トークンエンコーダー（管理者用）
実際のトークンを暗号化して配布用に変換
"""

import base64

def encode_token(token):
    """トークンをbase64でエンコード"""
    encoded = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    return encoded

def decode_token(encoded_token):
    """base64でエンコードされたトークンをデコード"""
    decoded = base64.b64decode(encoded_token.encode('utf-8')).decode('utf-8')
    return decoded

# 使用例
if __name__ == "__main__":
    # 実際のトークンをここに設定
    actual_token = "hf_your_actual_token_here"
    
    # エンコード
    encoded = encode_token(actual_token)
    print(f"エンコードされたトークン: {encoded}")
    
    # デコード（確認用）
    decoded = decode_token(encoded)
    print(f"デコードされたトークン: {decoded}")
