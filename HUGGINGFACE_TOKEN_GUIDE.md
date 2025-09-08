# Hugging Faceトークン取得ガイド

## 話者分離機能を使用するために必要なトークンの取得方法

### ステップ1: Hugging Faceアカウントの作成
1. [Hugging Face](https://huggingface.co/)にアクセス
2. 「Sign Up」をクリック
3. 無料アカウントを作成（メールアドレスとパスワード）

### ステップ2: トークンの生成
1. [トークン設定ページ](https://huggingface.co/settings/tokens)にアクセス
2. 「New token」をクリック
3. 以下の設定を入力：
   - **Token name**: `wisper-colab` など適当な名前
   - **Token type**: `Read` を選択
4. 「Generate a token」をクリック
5. 生成されたトークンをコピー（`hf_`で始まる文字列）

### ステップ3: Colabでトークンを設定
```python
import os
os.environ["HUGGINGFACE_TOKEN"] = "コピーしたトークン"
```

### ステップ4: 確認
```python
if os.getenv("HUGGINGFACE_TOKEN"):
    print("✅ トークンが設定されました")
else:
    print("❌ トークンが設定されていません")
```

## 注意事項
- トークンは個人情報です。他人と共有しないでください
- トークンが漏洩した場合は、Hugging Faceで再生成してください
- 無料アカウントでも話者分離機能は使用可能です

## トラブルシューティング
- トークンが無効な場合は、新しいトークンを生成してください
- アカウントが制限されている場合は、Hugging Faceの利用規約を確認してください
