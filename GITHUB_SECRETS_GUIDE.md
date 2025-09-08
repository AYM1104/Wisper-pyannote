# GitHub Secrets 使用方法ガイド

## 管理者向け設定手順

### 1. GitHub Secretsの設定
1. リポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. Name: `HUGGINGFACE_TOKEN`
4. Value: 実際のHugging Faceトークン
5. 「Add secret」をクリック

### 2. Actions ワークフローの実行
1. [Actions](https://github.com/AYM1104/Wisper-pyannote/actions)にアクセス
2. 「Setup Token for Colab」ワークフローを選択
3. 「Run workflow」をクリック
4. 表示されたトークンをコピー

## ユーザー向け使用方法

### 方法1: 手動設定
1. GitHub Actionsからトークンを取得
2. Colabで以下を実行:
```python
import os
os.environ["HUGGINGFACE_TOKEN"] = "取得したトークン"
```

### 方法2: 自動セットアップ
```python
!python colab_with_github_secrets.py
```

## セキュリティの特徴

- ✅ トークンはGitHub Secretsで安全に管理
- ✅ トークンは公開されない
- ✅ ユーザーは簡単にアクセス可能
- ✅ 管理者がトークンを一元管理

## トラブルシューティング

### トークンが取得できない場合
1. GitHub Actionsの実行権限を確認
2. Secretsが正しく設定されているか確認
3. ワークフローが正常に実行されているか確認

### トークンが無効な場合
1. Hugging Faceトークンの有効性を確認
2. 新しいトークンを生成してSecretsを更新
