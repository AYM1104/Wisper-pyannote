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
    
    if not hf_token:
        raise ValueError(
            "Hugging Faceトークンが設定されていません。\n"
            "話者分離を使用する場合は、以下の手順でトークンを取得・設定してください：\n"
            "1. https://huggingface.co/settings/tokens でトークンを取得\n"
            "2. Colabで実行: os.environ['HUGGINGFACE_TOKEN'] = 'hf_your_token'\n"
            "3. または、話者分離なしで実行: --do_diar フラグを外す"
        )
    
    print("話者分離パイプラインをロード中...")
    
    # pyannote.audio 3.xの話者分離パイプラインをロード
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )
    
    # GPUが利用可能な場合はGPUを使用、そうでなければCPUを使用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline = pipeline.to(device)
    print(f"話者分離パイプラインを{device}に配置しました")
    
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
    
    # 音声ファイルの情報を取得
    try:
        import torchaudio
        info = torchaudio.info(wav_path)
        duration = info.num_frames / info.sample_rate
        print(f"📊 音声ファイル情報:")
        print(f"   - ファイル: {wav_path}")
        print(f"   - 長さ: {duration:.1f}秒 ({duration/60:.1f}分)")
        print(f"   - サンプルレート: {info.sample_rate}Hz")
        print(f"   - チャンネル数: {info.num_channels}")
    except Exception as e:
        print(f"⚠️ 音声ファイル情報の取得に失敗: {e}")
    
    # 話者分離を実行（進捗表示付き）
    try:
        from tqdm import tqdm
        import time
        
        print("\n🔄 音声ファイルを解析中...")
        print("   (この処理には時間がかかります。しばらくお待ちください)")
        
        start_time = time.time()
        
        # 進捗バー付きで話者分離を実行
        with tqdm(total=100, desc="話者分離処理", unit="%") as pbar:
            # パイプライン実行（進捗をシミュレート）
            pbar.set_description("音声を解析中...")
            pbar.update(20)
            
            diarization = pipeline(wav_path)
            
            pbar.set_description("話者を識別中...")
            pbar.update(30)
            
            # 結果をリストに変換
            results = []
            segments = list(diarization.itertracks(yield_label=True))
            
            pbar.set_description("結果を処理中...")
            pbar.update(20)
            
            for i, (turn, _, speaker) in enumerate(segments):
                results.append((turn.start, turn.end, speaker))
                # 進捗を更新
                if i % max(1, len(segments) // 10) == 0:
                    pbar.update(30 / max(1, len(segments) // 10))
            
            pbar.set_description("完了")
            pbar.update(100 - pbar.n)
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ 話者分離完了!")
        print(f"   - 処理時間: {elapsed_time:.1f}秒")
        print(f"   - セグメント数: {len(results)}")
        print(f"   - 話者数: {len(set(speaker for _, _, speaker in results))}")
        
    except ImportError:
        # tqdmが利用できない場合は通常処理
        print("音声ファイルを解析中...")
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
