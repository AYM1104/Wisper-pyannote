# Wisper - 音声文字起こし＋話者分離

Google Colabで動作する音声文字起こし（Whisper/faster-whisper）＋話者分離（pyannote）の最小構成です。

## 機能

- **音声文字起こし**: faster-whisperを使用してmp3/m4a/wavファイルを文字起こし
- **話者分離**: pyannote.audioを使用して話者を識別（オプション）
- **出力形式**: 
  - 字幕ファイル（.srt）
  - 話者分離ファイル（.diar.tsv）

## Google Colabでの実行手順

### 方法1: 手動アップロード（推奨）
```python
# 1. Hugging Faceトークンの設定（話者分離を使用する場合のみ）
import os
# 以下の行のコメントを外して、あなたのトークンを設定してください
# os.environ["HUGGINGFACE_TOKEN"] = "hf_your_token_here"

# 2. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 3. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 4. 手動でファイルをアップロード
from google.colab import files
uploaded = files.upload()

# 5. アップロードしたファイル名を確認
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 6. 実行（話者分離なし）
!python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3

# 7. 生成されたファイルをダウンロード
base_name = audio_file.split('.')[0]
srt_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.srt"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"字幕ファイルをダウンロードしました: {base_name}.srt")
```

### 方法1b: 話者分離付き（GitHub Secrets版）

**🔐 共有トークンを使用して話者分離機能を利用できます**

#### トークンの取得方法：
1. [GitHub Actions](https://github.com/AYM1104/Wisper-pyannote/actions)にアクセス
2. 「Setup Token for Colab」ワークフローを実行
3. 表示されたトークンをコピー
4. Colabで以下のコードを実行

#### 実行コード：
```python
# 1. GitHub Actionsから取得したトークンを設定
import os
os.environ["HUGGINGFACE_TOKEN"] = "GitHub Actionsから取得したトークン"

# 2-5. 上記と同じ手順

# 6. 実行（話者分離付き）
!python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3 --do_diar

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
```

### 方法1c: 自動セットアップ（推奨）
```python
# このファイルを実行するだけで自動セットアップ
!python colab_with_github_secrets.py
```

### 方法2: 自動モード（エラーが発生する場合あり）
```python
# 1. Hugging Faceトークンの設定
import os
os.environ["HUGGINGFACE_TOKEN"] = "hf_your_token_here"

# 2. リポジトリのクローン
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote

# 3. 依存関係のインストール
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 4. 実行（自動でファイルアップロードとダウンロード）
!python main.py
```

### 方法3: ファイルパスを直接指定
```bash
# 文字起こしのみ
!python main.py --audio "/content/sample.m4a" --model large-v3

# 文字起こし＋話者分離
!python main.py --audio "/content/sample.m4a" --model large-v3 --do_diar
```

## 引数

- `--audio`: 音声ファイルのパス（必須）
- `--model`: Whisperモデルサイズ（デフォルト: large-v3）
- `--do_diar`: 話者分離を実行するフラグ

## 出力ファイル

### .srtファイル（字幕）
標準的なSRT形式で出力されます。
```
1
00:00:00,000 --> 00:00:03,500
こんにちは、今日は良い天気ですね。

2
00:00:03,500 --> 00:00:07,200
はい、本当に気持ちが良いです。
```

### .diar.tsvファイル（話者分離）
タブ区切り形式で話者の時間情報を出力します。
```
start	end	speaker
0.0	3.5	SPEAKER_00
3.5	7.2	SPEAKER_01
```

## よくあるハマりポイント

1. **pyannoteのデバイス指定**: `.to(torch.device("cpu"))`を使用（文字列"cpu"は不可）
2. **長時間ファイル**: Colabのセッションタイムアウトに注意
3. **Hugging Faceトークン**: 話者分離を使用する場合は必須
4. **音声形式**: 自動的に16kHzモノラルWAVに変換されます

## 対応音声形式

- MP3
- M4A
- WAV
- その他ffmpegが対応する形式

## モデルサイズ

- `tiny`: 最も高速、精度は低い
- `base`: バランス型
- `small`: 中程度の精度
- `medium`: 高精度
- `large-v3`: 最高精度（推奨）