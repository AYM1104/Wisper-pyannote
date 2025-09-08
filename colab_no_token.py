"""
Colab用セットアップ（トークン不要版）
このコードをColabのセルにコピー&ペーストして実行してください
"""

# 1. セットアップ
!git clone https://github.com/AYM1104/Wisper-pyannote.git
%cd Wisper-pyannote
!pip install -r requirements.txt
!pip install --upgrade torch torchaudio torchvision

# 2. ファイルをアップロード
from google.colab import files
uploaded = files.upload()
audio_file = list(uploaded.keys())[0]
print(f"アップロードしたファイル: {audio_file}")

# 3. 実行（話者分離なし）
print("🚀 文字起こしを実行します...")
!python main.py --audio "/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{audio_file}" --model large-v3

# 4. 結果をダウンロード
base_name = audio_file.split('.')[0]
srt_file = f"/content/Wisper-pyannote/Wisper-pyannote/Wisper-pyannote/{base_name}.srt"

if os.path.exists(srt_file):
    files.download(srt_file)
    print(f"✅ 字幕ファイルをダウンロードしました: {base_name}.srt")
else:
    print("❌ 字幕ファイルが見つかりません")

print("")
print("📝 話者分離機能を使用したい場合は:")
print("1. https://huggingface.co/settings/tokens でトークンを取得")
print("2. 以下のコードを実行:")
print("   import os")
print("   os.environ['HUGGINGFACE_TOKEN'] = 'あなたのトークン'")
print("3. 再度実行: !python main.py --audio 'ファイル' --model large-v3 --do_diar")
