"""
音声文字起こし＋話者分離のメインエントリーポイント
CLIインターフェースを提供
Colabでの実行もサポート
"""

import argparse
import os
import tempfile
from pathlib import Path

from app.utils_audio import to_wav_mono16k
from app.transcriber import transcribe, segments_to_srt
from app.diarizer import diarize, diarization_to_tsv


def run_colab_mode():
    """Colabモードでの実行"""
    try:
        from google.colab import files, drive
        print("Colab環境を検出しました。Colabモードで実行します。")
        
        # ファイルアップロード
        print("音声ファイルをアップロードしてください...")
        uploaded = files.upload()
        
        if not uploaded:
            print("エラー: ファイルがアップロードされませんでした。")
            return 1
        
        # アップロードしたファイル名を取得
        audio_file = list(uploaded.keys())[0]
        audio_path = f"/content/{audio_file}"
        
        print(f"アップロードしたファイル: {audio_file}")
        
        # 処理実行
        result = process_audio(audio_path, "large-v3", True)
        
        if result == 0:
            # 生成されたファイルをダウンロード
            base_name = Path(audio_file).stem
            srt_file = f"/content/{base_name}.srt"
            tsv_file = f"/content/{base_name}.diar.tsv"
            
            if os.path.exists(srt_file):
                files.download(srt_file)
                print(f"字幕ファイルをダウンロードしました: {base_name}.srt")
            
            if os.path.exists(tsv_file):
                files.download(tsv_file)
                print(f"話者分離ファイルをダウンロードしました: {base_name}.diar.tsv")
        
        return result
        
    except ImportError:
        print("Colab環境ではありません。通常モードで実行します。")
        return None


def process_audio(audio_path: str, model: str, do_diar: bool) -> int:
    """音声処理のメインロジック"""
    audio_path = Path(audio_path)
    
    # 入力ファイルの存在確認
    if not audio_path.exists():
        print(f"エラー: 音声ファイルが見つかりません: {audio_path}")
        return 1
    
    print(f"処理対象: {audio_path.name}")
    print(f"モデル: {model}")
    print(f"話者分離: {'有効' if do_diar else '無効'}")
    print("-" * 50)
    
    try:
        # 1. 音声ファイルを16kHzモノラルWAVに変換
        print("ステップ1: 音声ファイルの変換")
        wav_path = to_wav_mono16k(str(audio_path))
        
        # 2. 文字起こしを実行
        print("\nステップ2: 文字起こし")
        segments, info = transcribe(wav_path, model)
        
        # SRTファイルを生成・保存
        srt_content = segments_to_srt(segments)
        srt_path = audio_path.with_suffix('.srt')
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        print(f"字幕ファイルを保存しました: {srt_path}")
        
        # 3. 話者分離（オプション）
        if do_diar:
            print("\nステップ3: 話者分離")
            
            # Hugging Faceトークンの確認
            if not os.getenv("HUGGINGFACE_TOKEN"):
                print("警告: HUGGINGFACE_TOKENが設定されていません。話者分離をスキップします。")
            else:
                diarization_results = diarize(wav_path)
                
                # TSVファイルを生成・保存
                tsv_content = diarization_to_tsv(diarization_results)
                tsv_path = audio_path.with_suffix('.diar.tsv')
                
                with open(tsv_path, 'w', encoding='utf-8') as f:
                    f.write(tsv_content)
                
                print(f"話者分離ファイルを保存しました: {tsv_path}")
        
        print("\n処理完了!")
        print(f"生成ファイル:")
        print(f"  - 字幕: {srt_path}")
        if do_diar and os.getenv("HUGGINGFACE_TOKEN"):
            print(f"  - 話者分離: {tsv_path}")
        
        return 0
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    finally:
        # 一時ファイルを削除
        if 'wav_path' in locals() and os.path.exists(wav_path):
            os.remove(wav_path)
            print(f"一時ファイルを削除しました: {Path(wav_path).name}")


def main():
    """メイン関数"""
    # Colab環境かチェック
    colab_result = run_colab_mode()
    if colab_result is not None:
        return colab_result
    
    # 通常のCLIモード
    parser = argparse.ArgumentParser(
        description="音声文字起こし＋話者分離ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py --audio sample.m4a --model large-v3
  python main.py --audio sample.m4a --model large-v3 --do_diar
        """
    )
    
    parser.add_argument(
        "--audio",
        required=True,
        help="音声ファイルのパス（mp3/m4a/wav等）"
    )
    
    parser.add_argument(
        "--model",
        default="large-v3",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisperモデルサイズ（デフォルト: large-v3）"
    )
    
    parser.add_argument(
        "--do_diar",
        action="store_true",
        help="話者分離を実行する"
    )
    
    args = parser.parse_args()
    
    # 通常モードで処理実行
    return process_audio(args.audio, args.model, args.do_diar)


if __name__ == "__main__":
    exit(main())
