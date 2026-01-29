#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量发布工具 V2.0 - 功能测试脚本
"""

import os
import sys
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("XHS Batch Publish Tool V2.0 - Function Test")
print("=" * 80)

# 测试 1：检查脚本文件
print("\n[Test 1] Check script file...")
script_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts\batch_publish_v2.py")
if script_file.exists():
    print(f"OK Script file exists: {script_file}")
else:
    print(f"FAIL Script file not found: {script_file}")

# 测试 2：检查辅助模块
print("\n[Test 2] Check helper module...")
helper_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts\publish_helper.py")
if helper_file.exists():
    print(f"OK Helper module exists: {helper_file}")
else:
    print(f"FAIL Helper module not found: {helper_file}")

# 测试 3：检查启动器
print("\n[Test 3] Check launcher...")
launcher_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\启动发布工具_V2.py")
if launcher_file.exists():
    print(f"OK Launcher exists: {launcher_file}")
else:
    print(f"FAIL Launcher not found: {launcher_file}")

# 测试 4：检查 Cookie 文件
print("\n[Test 4] Check Cookie file...")
cookie_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\.env")
if cookie_file.exists():
    print(f"OK Cookie file exists: {cookie_file}")
    size = cookie_file.stat().st_size
    print(f"   File size: {size} bytes")
else:
    print(f"WARN Cookie file not found: {cookie_file}")
    print("   Please run login_xhs.py first")

# 测试 5：检查测试数据
print("\n[Test 5] Check test data...")
test_dir = Path(r"D:\jieyue_work")
if test_dir.exists():
    print(f"OK Test directory exists: {test_dir}")
    
    # 检查笔记文件夹
    note_dirs = [d for d in test_dir.iterdir() if d.is_dir() and d.name.startswith('note_')]
    if note_dirs:
        print(f"   Found {len(note_dirs)} note folders")
        for note_dir in sorted(note_dirs)[:5]:  # 只显示前5个
            cover = note_dir / 'cover.png'
            if cover.exists():
                cards = len(list(note_dir.glob('card_*.png')))
                print(f"   OK {note_dir.name}: cover + {cards} cards")
            else:
                print(f"   WARN {note_dir.name}: missing cover")
    else:
        print(f"   WARN No note folders found")
else:
    print(f"WARN Test directory not found: {test_dir}")

# 测试 6：导入测试
print("\n[Test 6] Import test...")
sys.path.insert(0, r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts")
try:
    from publish_helper import load_cookie
    print("OK publish_helper module imported successfully")
    
    # 测试加载 Cookie
    cookie = load_cookie()
    if cookie:
        print(f"OK Cookie loaded (length: {len(cookie)})")
    else:
        print("WARN Cookie not loaded")
except ImportError as e:
    print(f"FAIL Module import failed: {e}")

# 总结
print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
print("\nUsage:")
print("1. Double click: 启动发布工具_V2.py")
print("2. Command line: python scripts/batch_publish_v2.py")
print("3. With path: python scripts/batch_publish_v2.py --path D:\\jieyue_work")
print()
