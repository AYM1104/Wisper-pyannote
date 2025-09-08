"""
pyannote.audioを使用した話者分離
CPUで安定動作するように設定
"""

import os
import torch
from typing import List, Tuple
from pyannote.audio import Pipeline


def load_diarization_pipeline() -> Pipeline:
    """
    話者分離パイプラインをロード
    
    Returns:
        話者分離パイプライン
    """
    # Hugging Faceトークンを取得
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    
    # デフォルトトークン（公開用）
    if not hf_token:
        # 注意: 実際のトークンは環境変数で設定してください
        hf_token = "hf_your_token_here"
        print("⚠️  デフォルトトークンを使用しています。")
        print("   話者分離を使用する場合は、HUGGINGFACE_TOKENを設定してください。")
    
    if hf_token == "hf_your_token_here":
        raise ValueError(
            "Hugging Faceトークンが設定されていません。"
            "環境変数 HUGGINGFACE_TOKEN を設定してください。"
        )
    
    print("話者分離パイプラインをロード中...")
    
    # pyannote.audio 3.xの話者分離パイプラインをロード
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )
    
    # CPUで安定動作するように設定（重要: 文字列"cpu"ではなくtorch.device("cpu")）
    pipeline = pipeline.to(torch.device("cpu"))
    
    print("話者分離パイプラインのロード完了")
    return pipeline


def diarize(wav_path: str) -> List[Tuple[float, float, str]]:
    """
    音声ファイルの話者分離を実行
    
    Args:
        wav_path: WAVファイルのパス
        
    Returns:
        話者分離結果のリスト [(start, end, speaker), ...]
    """
    # パイプラインをロード
    pipeline = load_diarization_pipeline()
    
    print("話者分離を開始します...")
    print("⚠️  警告メッセージは正常な動作です。処理は継続されます。")
    
    # 話者分離を実行（進捗表示付き）
    try:
        from tqdm import tqdm
        print("音声ファイルを解析中...")
        diarization = pipeline(wav_path)
        
        # 結果をリストに変換（進捗表示付き）
        results = []
        print("話者分離結果を処理中...")
        
        # セグメント数を事前に取得
        segments = list(diarization.itertracks(yield_label=True))
        
        for turn, _, speaker in tqdm(segments, desc="話者分離処理"):
            results.append((turn.start, turn.end, speaker))
        
        print(f"✅ 話者分離完了: {len(results)}セグメント")
        
    except ImportError:
        # tqdmが利用できない場合は通常処理
        diarization = pipeline(wav_path)
        results = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            results.append((turn.start, turn.end, speaker))
        print(f"✅ 話者分離完了: {len(results)}セグメント")
    
    return results


def diarization_to_tsv(diarization_results: List[Tuple[float, float, str]]) -> str:
    """
    話者分離結果をTSV形式の文字列に変換
    
    Args:
        diarization_results: 話者分離結果のリスト
        
    Returns:
        TSV形式の文字列
    """
    tsv_lines = ["start\tend\tspeaker"]
    
    for start, end, speaker in diarization_results:
        tsv_lines.append(f"{start:.3f}\t{end:.3f}\t{speaker}")
    
    return "\n".join(tsv_lines)
