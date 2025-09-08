# Wisper - 音声文字起こし＋話者分離

Google Colabで動作する音声文字起こし（Whisper/faster-whisper）＋話者分離（pyannote）の最小構成です。

## 機能

- **音声文字起こし**: faster-whisperを使用してmp3/m4a/wavファイルを文字起こし
- **話者分離**: pyannote.audioを使用して話者を識別（オプション）
- **出力形式**: 
  - 字幕ファイル（.srt）
  - 話者分離ファイル（.diar.tsv）

## Google Colabでの実行手順

### 1. リポジトリのクローン
```bash
!git clone https://github.com/your-username/Wisper.git
%cd Wisper
```

### 2. 依存関係のインストール
```bash
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision
```

### 3. Hugging Faceトークンの設定（話者分離を使用する場合）
```python
import os
os.environ["HUGGINGFACE_TOKEN"] = "hf_your_token_here"
```

### 4. 実行
```bash
# 文字起こしのみ
!python main.py --audio "/content/drive/MyDrive/audio/sample.m4a" --model large-v3

# 文字起こし＋話者分離
!python main.py --audio "/content/drive/MyDrive/audio/sample.m4a" --model large-v3 --do_diar
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