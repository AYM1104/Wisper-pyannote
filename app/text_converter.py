"""
SRT/TSVファイルをテキスト形式に変換
"""

import os
from typing import List, Tuple


def srt_to_text(srt_content: str) -> str:
    """
    SRTファイルの内容をテキストに変換
    
    Args:
        srt_content: SRTファイルの内容
        
    Returns:
        テキスト形式の文字列
    """
    lines = srt_content.strip().split('\n')
    text_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 数字の行（セグメント番号）をスキップ
        if line.isdigit():
            i += 1
            continue
            
        # 時間行をスキップ
        if '-->' in line:
            i += 1
            continue
            
        # 空行をスキップ
        if not line:
            i += 1
            continue
            
        # テキスト行を追加
        text_lines.append(line)
        i += 1
    
    return '\n'.join(text_lines)


def tsv_to_text(tsv_content: str) -> str:
    """
    TSVファイルの内容をテキストに変換
    
    Args:
        tsv_content: TSVファイルの内容
        
    Returns:
        テキスト形式の文字列
    """
    lines = tsv_content.strip().split('\n')
    text_lines = []
    
    for line in lines[1:]:  # ヘッダー行をスキップ
        if not line.strip():
            continue
            
        parts = line.split('\t')
        if len(parts) >= 3:
            start_time = float(parts[0])
            end_time = float(parts[1])
            speaker = parts[2]
            text = parts[3] if len(parts) > 3 else ""
            
            # 時間を分:秒形式に変換
            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)
            
            text_lines.append(f"[{start_min:02d}:{start_sec:02d}-{end_min:02d}:{end_sec:02d}] {speaker}: {text}")
    
    return '\n'.join(text_lines)


def srt_to_timestamped_text(srt_content: str) -> str:
    """
    SRTファイルをタイムスタンプ付きテキストに変換
    
    Args:
        srt_content: SRTファイルの内容
        
    Returns:
        タイムスタンプ付きテキスト
    """
    lines = srt_content.strip().split('\n')
    text_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 数字の行（セグメント番号）をスキップ
        if line.isdigit():
            i += 1
            continue
            
        # 時間行を処理
        if '-->' in line:
            time_line = line
            i += 1
            # 次の行がテキスト
            if i < len(lines):
                text_line = lines[i].strip()
                if text_line:
                    text_lines.append(f"[{time_line}] {text_line}")
            i += 1
            continue
            
        # 空行をスキップ
        if not line:
            i += 1
            continue
            
        i += 1
    
    return '\n'.join(text_lines)


def save_text_files(base_name: str, srt_content: str = None, tsv_content: str = None) -> List[str]:
    """
    テキストファイルを保存
    
    Args:
        base_name: ベースファイル名
        srt_content: SRTファイルの内容
        tsv_content: TSVファイルの内容
        
    Returns:
        保存されたファイルのリスト
    """
    saved_files = []
    
    # 1. SRTからテキスト変換
    if srt_content:
        # 通常のテキスト
        text_content = srt_to_text(srt_content)
        text_file = f"/content/Wisper-pyannote/{base_name}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        saved_files.append(text_file)
        print(f"✅ テキストファイルを保存: {base_name}.txt")
        
        # タイムスタンプ付きテキスト
        timestamped_content = srt_to_timestamped_text(srt_content)
        timestamped_file = f"/content/Wisper-pyannote/{base_name}_timestamped.txt"
        with open(timestamped_file, 'w', encoding='utf-8') as f:
            f.write(timestamped_content)
        saved_files.append(timestamped_file)
        print(f"✅ タイムスタンプ付きテキストファイルを保存: {base_name}_timestamped.txt")
    
    # 2. TSVからテキスト変換
    if tsv_content:
        tsv_text_content = tsv_to_text(tsv_content)
        tsv_text_file = f"/content/Wisper-pyannote/{base_name}_speakers.txt"
        with open(tsv_text_file, 'w', encoding='utf-8') as f:
            f.write(tsv_text_content)
        saved_files.append(tsv_text_file)
        print(f"✅ 話者分離テキストファイルを保存: {base_name}_speakers.txt")
    
    return saved_files
