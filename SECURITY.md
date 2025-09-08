# セキュリティガイド

## Hugging Faceトークンについて

### ⚠️ 重要な注意事項
- **トークンを公開リポジトリにコミットしないでください**
- **トークンを他人と共有しないでください**
- **トークンは個人のHugging Faceアカウントで取得してください**

### 安全な使用方法

#### 1. 個人でトークンを取得
1. [Hugging Face](https://huggingface.co/settings/tokens)にアクセス
2. 無料アカウントを作成
3. 個人用のトークンを生成

#### 2. Colabでの安全な設定
```python
# トークンを直接コードに書かない
import os
os.environ["HUGGINGFACE_TOKEN"] = "hf_your_actual_token"

# 実行
!python main.py --audio "file.m4a" --model large-v3 --do_diar
```

#### 3. トークンの管理
- トークンは定期的に更新する
- 不要になったら削除する
- 漏洩した場合は即座に再生成する

### 基本機能（トークン不要）
話者分離が不要な場合は、トークン設定なしで文字起こしのみを使用できます：

```python
# トークン設定なしで実行
!python main.py --audio "file.m4a" --model large-v3
```

## サポート
トークンに関する問題がある場合は、Hugging Faceの公式ドキュメントを参照してください。
