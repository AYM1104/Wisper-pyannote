"""
faster-whisperを使用した音声文字起こし
SRT形式での字幕ファイル生成
"""

import torch
from faster_whisper import WhisperModel
from typing import List, Tuple, Any


def transcribe(wav_path: str, model_size: str = "large-v3") -> Tuple[List[Any], Any]:
    """
    音声ファイルを文字起こし
    
    Args:
        wav_path: WAVファイルのパス
        model_size: Whisperモデルサイズ
        
    Returns:
        (segments, info): セグメント情報とモデル情報
    """
    # デバイスとコンピュートタイプを決定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    print(f"文字起こしを開始します...")
    print(f"デバイス: {device}, コンピュートタイプ: {compute_type}")
    
    # Whisperモデルをロード
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    # 文字起こし実行
    segments, info = model.transcribe(
        wav_path,
        language="ja",  # 日本語
        beam_size=5,
        best_of=5,
        temperature=0.0,
        condition_on_previous_text=False
    )
    
    # セグメントをリストに変換
    segments_list = list(segments)
    
    print(f"文字起こし完了: {len(segments_list)}セグメント")
    print(f"検出言語: {info.language} (信頼度: {info.language_probability:.2f})")
    
    return segments_list, info


def segments_to_srt(segments: List[Any]) -> str:
    """
    セグメントをSRT形式の文字列に変換
    
    Args:
        segments: Whisperのセグメントリスト
        
    Returns:
        SRT形式の文字列
    """
    srt_content = []
    
    for i, segment in enumerate(segments, 1):
        # タイムスタンプをSRT形式に変換
        start_time = _seconds_to_srt_time(segment.start)
        end_time = _seconds_to_srt_time(segment.end)
        
        # SRTエントリを構築
        srt_entry = f"{i}\n{start_time} --> {end_time}\n{segment.text.strip()}\n"
        srt_content.append(srt_entry)
    
    return "\n".join(srt_content)


def _seconds_to_srt_time(seconds: float) -> str:
    """
    秒数をSRT形式のタイムスタンプに変換
    
    Args:
        seconds: 秒数
        
    Returns:
        SRT形式のタイムスタンプ (hh:mm:ss,mmm)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
