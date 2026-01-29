#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查小红书笔记发布进度
通过检查已发布的笔记来判断进度
"""

import json
import os
import sys
from pathlib import Path


def check_published_notes(notes_dir: str):
    """检查哪些笔记已经发布"""
    
    print("="*60)
    print("小红书笔记发布进度检查")
    print("="*60)
    print()
    
    # 获取所有笔记目录
    note_dirs = sorted([d for d in Path(notes_dir).glob('note_*') if d.is_dir()])
    
    if not note_dirs:
        print(f"[ERROR] No note directories found in {notes_dir}")
        return
    
    print(f"[INFO] Found {len(note_dirs)} notes")
    print()
    
    published_count = 0
    
    for note_dir in note_dirs:
        note_name = note_dir.name
        metadata_file = note_dir / 'metadata.json'
        
        if not metadata_file.exists():
            print(f"[WARNING] {note_name}: No metadata.json")
            continue
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            title = metadata.get('title', 'Unknown')
            note_num = metadata.get('note_num', 0)
            
            # 检查是否有发布记录（这里简单检查，实际可能需要其他方式）
            # 由于我们没有保存发布状态，这里只能显示笔记信息
            
            print(f"[{note_num:2d}] {note_name}")
            print(f"     Title: {title}")
            print(f"     Status: Waiting for manual check")
            print()
            
        except Exception as e:
            print(f"[ERROR] {note_name}: {e}")
            print()
    
    print("="*60)
    print("[INFO] Progress check completed")
    print("="*60)
    print()
    print("[NOTE] To check actual publish status:")
    print("  1. Check terminal output where batch_publish_xhs.py is running")
    print("  2. Visit https://creator.xiaohongshu.com to see published notes")
    print("  3. Check the note URLs printed during publishing")
    print()


def main():
    notes_dir = r"D:\jieyue_work\drivingschool_notes"
    
    if not os.path.isdir(notes_dir):
        print(f"[ERROR] Directory not found: {notes_dir}")
        sys.exit(1)
    
    check_published_notes(notes_dir)


if __name__ == '__main__':
    main()
