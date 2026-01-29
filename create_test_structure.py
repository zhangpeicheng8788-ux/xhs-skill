# -*- coding: utf-8 -*-
"""
创建测试目录结构
"""
import os
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("Creating test directory structure...")

# 创建测试根目录
test_root = Path(r"D:\jieyue_work\test_recursive")
test_root.mkdir(exist_ok=True)

# 创建多层嵌套的笔记结构
structures = [
    "batch_1/note_01",
    "batch_1/note_02",
    "batch_2/group_a/note_03",
    "batch_2/group_b/note_04",
    "special/deep/nested/note_05",
]

for structure in structures:
    note_dir = test_root / structure
    note_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 cover.png 标记文件
    cover_file = note_dir / "cover.png"
    if not cover_file.exists():
        cover_file.write_text("test")
    
    # 创建几个 card 文件
    for i in range(1, 4):
        card_file = note_dir / f"card_{i}.png"
        if not card_file.exists():
            card_file.write_text("test")
    
    print(f"Created: {structure}")

print()
print(f"Test directory created: {test_root}")
print()
print("Now you can test recursive detection with this path:")
print(f"  {test_root}")
