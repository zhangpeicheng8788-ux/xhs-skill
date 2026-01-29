#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试递归遍历功能
"""
import os
from pathlib import Path

def test_recursive_detection(root_path):
    """测试递归检测笔记"""
    print("="*60)
    print(f"测试路径: {root_path}")
    print("="*60)
    
    note_dirs = []
    
    def find_notes_recursive(current_path, depth=0, max_depth=10):
        """递归查找包含 cover.png 的文件夹"""
        if depth > max_depth:
            return
        
        try:
            # 检查当前目录是否包含 cover.png
            cover_path = os.path.join(current_path, 'cover.png')
            has_cover = os.path.exists(cover_path)
            if has_cover:
                note_dirs.append(current_path)
                rel_path = os.path.relpath(current_path, root_path)
                print(f"  [发现笔记] 深度{depth}: {rel_path}")
            
            # 继续遍历子目录（即使当前目录有cover.png，子目录也可能有笔记）
            try:
                items = os.listdir(current_path)
            except PermissionError:
                print(f"  [跳过] 无权限: {os.path.relpath(current_path, root_path)}")
                return
            
            for item in items:
                item_path = os.path.join(current_path, item)
                if os.path.isdir(item_path):
                    # 跳过隐藏文件夹和系统文件夹
                    if item.startswith('.') or item.startswith('__'):
                        continue
                    # 跳过常见的非笔记文件夹
                    if item.lower() in ['node_modules', 'venv', '.git', '.vscode', 'dist', 'build']:
                        continue
                    # 递归检查子文件夹
                    find_notes_recursive(item_path, depth + 1, max_depth)
        except Exception as e:
            print(f"  [错误] {current_path}: {str(e)}")
    
    # 开始递归查找
    print("\n开始递归遍历...")
    find_notes_recursive(root_path)
    
    print("\n" + "="*60)
    print(f"检测完成！共找到 {len(note_dirs)} 个笔记")
    print("="*60)
    
    if note_dirs:
        print("\n笔记列表:")
        for i, note_dir in enumerate(sorted(note_dirs), 1):
            rel_path = os.path.relpath(note_dir, root_path)
            print(f"  [{i:02d}] {rel_path}")
    else:
        print("\n未找到笔记")
    
    return note_dirs


if __name__ == '__main__':
    # 测试路径
    test_path = r"D:\jieyue_work"
    
    if not os.path.exists(test_path):
        print(f"错误: 路径不存在 - {test_path}")
    else:
        notes = test_recursive_detection(test_path)
        
        print("\n" + "="*60)
        print("统计信息:")
        print(f"  总笔记数: {len(notes)}")
        print("="*60)
