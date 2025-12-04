#!/usr/bin/env python3
"""
YouTube 字幕清理工具
解析 VTT 格式字幕并提取纯文本
"""

import re
import sys
from pathlib import Path


def clean_vtt_subtitle(vtt_content):
    """
    清理 VTT 格式字幕，提取纯文本

    Args:
        vtt_content: VTT 字幕文件内容

    Returns:
        清理后的纯文本
    """
    lines = vtt_content.split('\n')
    text_lines = []
    seen_lines = set()  # 用于去重

    for line in lines:
        # 跳过 VTT 头部
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        # 跳过时间戳行
        if '-->' in line:
            continue

        # 跳过空行
        if not line.strip():
            continue

        # 去除 HTML 标签
        clean_line = re.sub(r'<[^>]+>', '', line)

        # 去除标签标记（如 <c> </c>）
        clean_line = re.sub(r'</?\w+>', '', clean_line)

        # 去除多余空格
        clean_line = ' '.join(clean_line.split())

        # 去重（避免重复的字幕行）
        if clean_line and clean_line not in seen_lines:
            text_lines.append(clean_line)
            seen_lines.add(clean_line)

    return '\n'.join(text_lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 clean_subtitles.py <字幕文件路径>", file=sys.stderr)
        print("示例: python3 clean_subtitles.py subtitle.zh.vtt", file=sys.stderr)
        sys.exit(1)

    subtitle_file = Path(sys.argv[1])

    if not subtitle_file.exists():
        print(f"错误: 文件 {subtitle_file} 不存在", file=sys.stderr)
        sys.exit(1)

    # 读取字幕文件
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            vtt_content = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 - {e}", file=sys.stderr)
        sys.exit(1)

    # 清理字幕
    cleaned_text = clean_vtt_subtitle(vtt_content)

    # 输出清理后的文本
    print(cleaned_text)

    # 输出统计信息到 stderr
    line_count = len(cleaned_text.split('\n'))
    char_count = len(cleaned_text)
    print(f"\n--- 统计 ---", file=sys.stderr)
    print(f"行数: {line_count}", file=sys.stderr)
    print(f"字符数: {char_count}", file=sys.stderr)


if __name__ == '__main__':
    main()
