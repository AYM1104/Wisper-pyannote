"""
音声文字起こし＋話者分離のメインエントリーポイント
CLIインターフェースを提供
"""

import argparse
import os
import tempfile
from pathlib import Path

from app.utils_audio import to_wav_mono16k
from app.transcriber import transcribe, segments_to_srt
from app.diarizer import diarize, diarization_to_tsv


def main():
    """メイン関数"""
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
    
    # 入力ファイルの存在確認
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"エラー: 音声ファイルが見つかりません: {audio_path}")
        return 1
    
    print(f"処理対象: {audio_path.name}")
    print(f"モデル: {args.model}")
    print(f"話者分離: {'有効' if args.do_diar else '無効'}")
    print("-" * 50)
    
    try:
        # 1. 音声ファイルを16kHzモノラルWAVに変換
        print("ステップ1: 音声ファイルの変換")
        wav_path = to_wav_mono16k(str(audio_path))
        
        # 2. 文字起こしを実行
        print("\nステップ2: 文字起こし")
        segments, info = transcribe(wav_path, args.model)
        
        # SRTファイルを生成・保存
        srt_content = segments_to_srt(segments)
        srt_path = audio_path.with_suffix('.srt')
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        print(f"字幕ファイルを保存しました: {srt_path}")
        
        # 3. 話者分離（オプション）
        if args.do_diar:
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
        if args.do_diar and os.getenv("HUGGINGFACE_TOKEN"):
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


if __name__ == "__main__":
    exit(main())
