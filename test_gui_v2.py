# -*- coding: utf-8 -*-
"""
GUI 批量发布工具 V2.0 - 快速测试
"""
import os
import sys
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("GUI Batch Publish Tool V2.0 - Quick Test")
print("=" * 80)

# 测试 1：检查 GUI 脚本
print("\n[Test 1] Check GUI script...")
gui_script = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts\publish_gui_v2.py")
if gui_script.exists():
    print(f"OK GUI script exists: {gui_script}")
    size = gui_script.stat().st_size
    print(f"   File size: {size} bytes")
else:
    print(f"FAIL GUI script not found: {gui_script}")

# 测试 2：检查启动文件
print("\n[Test 2] Check start batch file...")
bat_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\start_publish.bat")
if bat_file.exists():
    print(f"OK Batch file exists: {bat_file}")
else:
    print(f"FAIL Batch file not found: {bat_file}")

# 测试 3：检查文档
print("\n[Test 3] Check documentation...")
doc_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\GUI批量发布工具_V2_使用说明.md")
if doc_file.exists():
    print(f"OK Documentation exists: {doc_file}")
    size = doc_file.stat().st_size
    print(f"   File size: {size} bytes")
else:
    print(f"FAIL Documentation not found: {doc_file}")

# 测试 4：检查依赖
print("\n[Test 4] Check dependencies...")
try:
    import tkinter
    print("OK tkinter module available")
except ImportError:
    print("FAIL tkinter module not found")

try:
    from xhs import XhsClient
    print("OK xhs module available")
except ImportError:
    print("WARN xhs module not found (run: pip install xhs)")

try:
    from dotenv import load_dotenv
    print("OK dotenv module available")
except ImportError:
    print("WARN dotenv module not found (run: pip install python-dotenv)")

# 测试 5：检查 Cookie
print("\n[Test 5] Check Cookie file...")
cookie_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\.env")
if cookie_file.exists():
    print(f"OK Cookie file exists: {cookie_file}")
else:
    print(f"WARN Cookie file not found (run login_xhs.py first)")

# 测试 6：检查测试数据
print("\n[Test 6] Check test data...")
test_dir = Path(r"D:\jieyue_work")
if test_dir.exists():
    print(f"OK Test directory exists: {test_dir}")
    note_dirs = [d for d in test_dir.iterdir() if d.is_dir() and d.name.startswith('note_')]
    if note_dirs:
        print(f"   Found {len(note_dirs)} note folders")
    else:
        print(f"   WARN No note folders found")
else:
    print(f"WARN Test directory not found: {test_dir}")

# 总结
print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
print("\nUsage:")
print("1. Double click: start_publish.bat")
print("2. Command line: python scripts/publish_gui_v2.py")
print("3. With default path: python scripts/publish_gui_v2.py --path D:\\jieyue_work")
print("\nFeatures:")
print("- Select resource path in GUI")
print("- Detect notes structure")
print("- Batch publish with interval")
print("- Pause/Resume/Stop controls")
print()
