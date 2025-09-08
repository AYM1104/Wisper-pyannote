"""
音声ファイルの変換ユーティリティ
ffmpegを使用して16kHzモノラルWAVに変換
"""

import os
import tempfile
import ffmpeg
from pathlib import Path


def to_wav_mono16k(src_path: str) -> str:
    """
    音声ファイルを16kHzモノラルWAVに変換
    
    Args:
        src_path: 入力音声ファイルのパス
        
    Returns:
        変換されたWAVファイルのパス
    """
    src_path = Path(src_path)
    
    # 出力ファイル名を生成（一時ファイル）
    output_path = tempfile.mktemp(suffix='.wav')
    
    try:
        # ffmpegで16kHzモノラルWAVに変換
        (
            ffmpeg
            .input(str(src_path))
            .output(
                output_path,
                acodec='pcm_s16le',  # 16bit PCM
                ac=1,                # モノラル
                ar=16000             # 16kHz
            )
            .overwrite_output()
            .run(quiet=True)
        )
        
        print(f"音声ファイルを変換しました: {src_path.name} -> {Path(output_path).name}")
        return output_path
        
    except ffmpeg.Error as e:
        # エラーが発生した場合は一時ファイルを削除
        if os.path.exists(output_path):
            os.remove(output_path)
        raise RuntimeError(f"音声ファイルの変換に失敗しました: {e}")
