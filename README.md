# Wisper-pyannote

音声文字起こし（Whisper/faster-whisper）＋話者分離（pyannote）の最小構成

## 機能

- ✅ **音声文字起こし**: faster-whisperを使用した高精度な文字起こし
- ✅ **話者分離**: pyannote.audioを使用した話者識別（オプション）
- ✅ **Google Colab対応**: GPU環境での高速処理
- ✅ **複数出力形式**: SRT、TSV、テキストファイル

## セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/AYM1104/Wisper-pyannote.git
cd Wisper-pyannote
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 使用方法

### 文字起こしのみ
```bash
python main.py --audio "音声ファイル.wav" --model large-v3
```

### 話者分離付き
```bash
# Hugging Faceトークンを設定
export HUGGINGFACE_TOKEN="hf_your_token_here"

# 実行
python main.py --audio "音声ファイル.wav" --model large-v3 --do_diar
```

## Google Colabでの実行

### 文字起こしのみ（推奨）
```python
# 1. セットアップ
import os
os.environ['COLAB_MODE'] = 'false'

!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 2. ファイルをアップロード
from google.colab import files
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]

# 3. 文字起こし実行
!python main.py --audio "/content/{audio_file}" --model large-v3

# 4. テキスト抽出
base_name = audio_file.split('.')[0]
srt_path = f"/content/Wisper-pyannote/{base_name}.srt"

with open(srt_path, 'r', encoding='utf-8') as f:
    srt_content = f.read()

lines = srt_content.strip().split('\n')
text_lines = []

for i, line in enumerate(lines):
    line = line.strip()
    if line.isdigit() or '-->' in line or not line:
        continue
    text_lines.append(line)

text_content = '\n'.join(text_lines)
text_file = f"/content/Wisper-pyannote/{base_name}.txt"
with open(text_file, 'w', encoding='utf-8') as f:
    f.write(text_content)

# 5. ダウンロード
files.download(text_file)
```

### 話者分離付き
```python
# 1. トークン設定
import os
os.environ["HUGGINGFACE_TOKEN"] = "hf_your_token_here"
os.environ['COLAB_MODE'] = 'false'

# 2-3. セットアップとファイルアップロード（上記と同じ）

# 4. 話者分離付き実行
!python main.py --audio "/content/{audio_file}" --model large-v3 --do_diar

# 5. 結果をダウンロード
files.download(f"/content/Wisper-pyannote/{base_name}.srt")
files.download(f"/content/Wisper-pyannote/{base_name}.diar.tsv")
```

## 出力ファイル

- **`.srt`**: 字幕ファイル（タイムスタンプ付き）
- **`.diar.tsv`**: 話者分離ファイル（話者分離実行時のみ）
- **`.txt`**: テキストファイル（タイムスタンプなし）

## 必要なトークン

話者分離機能を使用する場合は、Hugging Faceトークンが必要です：

1. [Hugging Face](https://huggingface.co/settings/tokens)でトークンを取得
2. `HUGGINGFACE_TOKEN`環境変数に設定

## ライセンス

MIT License