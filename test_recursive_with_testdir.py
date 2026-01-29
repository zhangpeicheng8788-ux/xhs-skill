# -*- coding: utf-8 -*-
"""
测试递归检测 - 使用测试目录
"""
import os
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("Recursive Note Detection Test - Test Directory")
print("=" * 80)

def find_notes_recursive(root_path, depth=0, max_depth=10):
    """递归查找包含 cover.png 的文件夹"""
    note_dirs = []
    
    def scan(path, d):
        if d > max_depth:
            return
        
        try:
            # 检查当前目录是否包含 cover.png
            if os.path.exists(os.path.join(path, 'cover.png')):
                note_dirs.append(path)
                rel_path = os.path.relpath(path, root_path)
                print(f"  [Found] {rel_path if rel_path != '.' else '(root)'} (depth: {d})")
                return  # 找到笔记后不再深入此目录
            
            # 遍历子目录
            try:
                items = os.listdir(path)
            except PermissionError:
                print(f"  [Skip] No permission: {os.path.relpath(path, root_path)}")
                return
            
            for item in sorted(items):  # 排序以便有序输出
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # 跳过隐藏文件夹和系统文件夹
                    if item.startswith('.') or item.startswith('__'):
                        continue
                    # 跳过常见的非笔记文件夹
                    if item.lower() in ['node_modules', 'venv', '.git', '.vscode', 'dist', 'build']:
                        continue
                    # 递归检查子文件夹
                    scan(item_path, d + 1)
        except Exception as e:
            print(f"  [Error] {path}: {str(e)}")
    
    scan(root_path, depth)
    return sorted(note_dirs)

# 测试路径
test_path = r"D:\jieyue_work\test_recursive"

print(f"\nTest path: {test_path}")
print(f"Path exists: {os.path.exists(test_path)}")
print()

if os.path.exists(test_path):
    print("Starting recursive scan...")
    print()
    
    note_dirs = find_notes_recursive(test_path)
    
    print()
    print("=" * 80)
    print(f"Scan completed! Found {len(note_dirs)} notes")
    print("=" * 80)
    
    if note_dirs:
        print()
        for i, note_dir in enumerate(note_dirs, 1):
            rel_path = os.path.relpath(note_dir, test_path)
            
            # 统计图片
            try:
                images = [f for f in os.listdir(note_dir) if f.endswith('.png')]
                cover_count = 1 if 'cover.png' in images else 0
                card_count = len([f for f in images if f.startswith('card_')])
                total_images = min(cover_count + card_count, 9)
                
                print(f"[{i:02d}] {rel_path}")
                print(f"     Images: {total_images} (cover:{cover_count}, cards:{card_count})")
            except Exception as e:
                print(f"[{i:02d}] {rel_path} - Error: {str(e)}")
    else:
        print("\nNo notes found!")
else:
    print(f"Test path does not exist: {test_path}")
    print("Run create_test_structure.py first to create test directory")

print()
print("=" * 80)
