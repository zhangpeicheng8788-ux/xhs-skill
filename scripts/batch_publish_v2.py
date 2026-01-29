#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记批量发布脚本 - 升级版 V2.0
支持手动指定发布资源文件夹路径

功能特性：
1. 交互式输入资源文件夹路径
2. 自动检测笔记结构（支持多种格式）
3. 智能识别图片和内容
4. 批量发布，支持间隔设置
5. 断点续传，跳过已发布笔记

使用方法:
    python batch_publish_v2.py
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import argparse

# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 导入发布辅助模块
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from publish_helper import publish_note, get_user_info
except ImportError:
    print("Error: Cannot import publish_helper module")
    print("Please make sure publish_helper.py exists in the scripts directory")
    sys.exit(1)


def print_banner():
    """打印横幅"""
    print("\n" + "=" * 80)
    print("XHS Batch Publish Tool V2.0 - Upgraded Version")
    print("=" * 80)
    print("\nFeatures:")
    print("  - Manually specify resource folder path")
    print("  - Auto detect note structure")
    print("  - Smart image and content recognition")
    print("  - Batch publish with interval settings")
    print("  - Resume from breakpoint, skip published notes")
    print("\n" + "=" * 80 + "\n")


def get_resource_path():
    """交互式获取资源文件夹路径"""
    print("Please enter the resource folder path:")
    print("  Tip: You can drag and drop the folder into this window")
    print("  Example: D:\\jieyue_work\\note_1")
    print("  Or: D:\\jieyue_work (parent directory containing multiple notes)")
    print()
    
    while True:
        path_input = input("Path > ").strip()
        
        # 移除可能的引号
        path_input = path_input.strip('"').strip("'")
        
        if not path_input:
            print("Error: Path cannot be empty, please re-enter")
            continue
        
        resource_path = Path(path_input)
        
        if not resource_path.exists():
            print(f"Error: Path does not exist: {resource_path}")
            retry = input("Re-enter? (y/n): ").strip().lower()
            if retry != 'y':
                return None
            continue
        
        if not resource_path.is_dir():
            print(f"Error: Not a valid folder: {resource_path}")
            retry = input("Re-enter? (y/n): ").strip().lower()
            if retry != 'y':
                return None
            continue
        
        print(f"\nOK Selected path: {resource_path}")
        confirm = input("Confirm this path? (y/n): ").strip().lower()
        if confirm == 'y':
            return resource_path
        else:
            print("Re-enter path...\n")


def detect_note_structure(resource_path):
    """
    检测笔记结构
    支持两种结构：
    1. 单个笔记：resource_path 直接包含 cover.png 和 card_*.png
    2. 多个笔记：resource_path 包含多个子文件夹（note_01, note_02 等）
    """
    resource_path = Path(resource_path)
    
    # 检查是否是单个笔记
    cover = resource_path / 'cover.png'
    if cover.exists():
        print(f"\nDetected single note structure")
        return 'single', [resource_path]
    
    # 检查是否包含多个笔记子文件夹
    note_dirs = []
    for item in resource_path.iterdir():
        if item.is_dir():
            cover = item / 'cover.png'
            if cover.exists():
                note_dirs.append(item)
    
    if note_dirs:
        print(f"\nDetected multiple note structure, total {len(note_dirs)} notes")
        return 'multiple', sorted(note_dirs)
    
    print(f"\nError: No valid note structure detected")
    print("   Please ensure the folder contains:")
    print("   - cover.png (cover image)")
    print("   - card_1.png, card_2.png... (content cards)")
    return None, []


def load_note_info(note_dir):
    """加载笔记信息"""
    note_dir = Path(note_dir)
    note_info = {
        'note_dir': note_dir,
        'note_id': note_dir.name,
        'title': '',
        'desc': '',
        'images': [],
        'published': False,
        'metadata': {}
    }
    
    # 尝试读取元数据
    meta_file = note_dir / 'metadata.json'
    if meta_file.exists():
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            note_info['metadata'] = metadata
            note_info['title'] = metadata.get('title', '')
            note_info['published'] = bool(metadata.get('published_at'))
        except Exception as e:
            print(f"Warning: Failed to read metadata: {e}")
    
    # 尝试读取发布记录
    publish_record = note_dir / 'publish_record.json'
    if publish_record.exists():
        try:
            with open(publish_record, 'r', encoding='utf-8') as f:
                record = json.load(f)
            note_info['published'] = True
            note_info['publish_record'] = record
        except Exception as e:
            print(f"Warning: Failed to read publish record: {e}")
    
    # 收集图片（最多9张）
    images = []
    cover = note_dir / 'cover.png'
    if cover.exists():
        images.append(str(cover.absolute()))
    
    for i in range(1, 20):
        card = note_dir / f'card_{i}.png'
        if card.exists():
            images.append(str(card.absolute()))
        else:
            break
    
    # 小红书最多9张图
    note_info['images'] = images[:9]
    
    # 尝试读取 Markdown 文件获取标题
    if not note_info['title']:
        md_files = list(note_dir.glob('*.md'))
        if md_files:
            try:
                with open(md_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                # 简单提取标题（第一个 # 标题）
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# '):
                        note_info['title'] = line[2:].strip()
                        break
            except Exception as e:
                print(f"Warning: Failed to read Markdown: {e}")
    
    # 如果还是没有标题，使用文件夹名
    if not note_info['title']:
        note_info['title'] = note_dir.name
    
    return note_info


def get_note_content(note_info):
    """获取笔记内容（标题和正文）"""
    print(f"\nNote: {note_info['note_id']}")
    print(f"   Current title: {note_info['title']}")
    print(f"   Image count: {len(note_info['images'])}")
    print()
    
    # 输入标题
    print("Enter note title (leave empty to use default):")
    title_input = input("Title > ").strip()
    if title_input:
        title = title_input
    else:
        title = note_info['title']
    
    # 输入正文
    print("\nEnter note content (multi-line supported, type END to finish):")
    print("Tip: Can include Emoji, tags, etc.")
    print()
    
    desc_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        desc_lines.append(line)
    
    desc = '\n'.join(desc_lines).strip()
    
    if not desc:
        print("\nError: Content cannot be empty")
        return None, None
    
    return title, desc


def publish_notes_batch(notes_info, interval_minutes=20, skip_published=True):
    """批量发布笔记"""
    
    # 检查登录状态
    print("\nChecking login status...")
    user_info = get_user_info()
    
    if not user_info['success']:
        print(f"Error: Not logged in or Cookie expired")
        print("Please run login script first:")
        print("   python scripts/login_xhs.py")
        return
    
    print(f"OK Logged in, current user: {user_info['info'].get('nickname', 'Unknown')}")
    
    # 过滤待发布的笔记
    if skip_published:
        pending_notes = [n for n in notes_info if not n['published']]
        published_count = len(notes_info) - len(pending_notes)
        
        if published_count > 0:
            print(f"\nStatistics:")
            print(f"   Total notes: {len(notes_info)}")
            print(f"   Published: {published_count}")
            print(f"   Pending: {len(pending_notes)}")
    else:
        pending_notes = notes_info
    
    if not pending_notes:
        print("\nAll notes have been published")
        return
    
    # 显示发布计划
    print(f"\nPublish plan:")
    print(f"   Note count: {len(pending_notes)}")
    print(f"   Publish interval: {interval_minutes} minutes")
    
    total_time = (len(pending_notes) - 1) * interval_minutes
    end_time = datetime.now() + timedelta(minutes=total_time)
    print(f"   Estimated time: {total_time} minutes")
    print(f"   Estimated completion: {end_time.strftime('%H:%M:%S')}")
    
    # 确认发布
    print("\n" + "=" * 80)
    confirm = input("Confirm to start publishing? (type yes to continue): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled")
        return
    
    print("\n" + "=" * 80)
    
    # 开始发布
    published_count = 0
    
    for i, note_info in enumerate(pending_notes):
        print(f"\n{'='*80}")
        print(f"Publishing note {i+1}/{len(pending_notes)}")
        print(f"{'='*80}")
        
        # 获取笔记内容
        title, desc = get_note_content(note_info)
        
        if not title or not desc:
            print(f"Warning: Skipping note {note_info['note_id']}")
            continue
        
        # 发布笔记
        print(f"\nStarting publish...")
        print(f"   Title: {title}")
        print(f"   Images: {len(note_info['images'])} images")
        
        result = publish_note(title, desc, note_info['images'])
        
        if result['success']:
            print(f"OK Published successfully!")
            print(f"   Note ID: {result['note_id']}")
            print(f"   Link: {result['link']}")
            
            # 保存发布记录
            publish_record = {
                'note_id': note_info['note_id'],
                'title': title,
                'published_at': datetime.now().isoformat(),
                'note_id_xhs': result['note_id'],
                'link': result['link']
            }
            
            record_file = note_info['note_dir'] / 'publish_record.json'
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(publish_record, f, ensure_ascii=False, indent=2)
            
            # 更新元数据
            if note_info['metadata']:
                note_info['metadata']['published_at'] = datetime.now().isoformat()
                note_info['metadata']['note_id_xhs'] = result['note_id']
                note_info['metadata']['link'] = result['link']
                
                meta_file = note_info['note_dir'] / 'metadata.json'
                with open(meta_file, 'w', encoding='utf-8') as f:
                    json.dump(note_info['metadata'], f, ensure_ascii=False, indent=2)
            
            published_count += 1
            
            # 如果不是最后一篇，等待间隔时间
            if i < len(pending_notes) - 1:
                wait_seconds = interval_minutes * 60
                next_time = datetime.now() + timedelta(seconds=wait_seconds)
                
                print(f"\nWaiting {interval_minutes} minutes...")
                print(f"   Next publish time: {next_time.strftime('%H:%M:%S')}")
                print(f"   Remaining notes: {len(pending_notes) - i - 1}")
                
                # 倒计时显示
                for remaining in range(wait_seconds, 0, -60):
                    mins = remaining // 60
                    print(f"   Countdown: {mins:02d}:00", end='\r')
                    time.sleep(60)
                
                print()  # 换行
        else:
            print(f"Error: Publish failed: {result.get('error', 'Unknown error')}")
            print(f"Suggestion: Check network connection and login status")
            
            retry = input("\nContinue to next note? (y/n): ").strip().lower()
            if retry != 'y':
                break
    
    # 发布完成
    print("\n" + "=" * 80)
    print("Publish completed!")
    print("=" * 80)
    print(f"OK Successfully published: {published_count}/{len(pending_notes)} notes")
    
    if published_count < len(pending_notes):
        print(f"Warning: Failed/Skipped: {len(pending_notes) - published_count} notes")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='XHS Batch Publish Tool V2.0')
    parser.add_argument('--path', type=str, help='Resource folder path (optional, interactive input if not specified)')
    parser.add_argument('--interval', type=int, default=20, help='Publish interval (minutes), default 20')
    parser.add_argument('--include-published', action='store_true', help='Include already published notes')
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 获取资源路径
    if args.path:
        resource_path = Path(args.path)
        if not resource_path.exists():
            print(f"Error: Specified path does not exist: {resource_path}")
            return
        print(f"OK Using specified path: {resource_path}")
    else:
        resource_path = get_resource_path()
        if not resource_path:
            print("\nNo valid path selected, exiting")
            return
    
    # 检测笔记结构
    structure_type, note_dirs = detect_note_structure(resource_path)
    
    if not note_dirs:
        print("\nNo valid notes found, exiting")
        return
    
    # 加载笔记信息
    print(f"\nLoading note information...")
    notes_info = []
    for note_dir in note_dirs:
        note_info = load_note_info(note_dir)
        if note_info['images']:
            notes_info.append(note_info)
            status = "Published" if note_info['published'] else "Pending"
            print(f"   OK {note_info['note_id']}: {note_info['title']} ({len(note_info['images'])} images) [{status}]")
        else:
            print(f"   Warning {note_dir.name}: No images, skipping")
    
    if not notes_info:
        print("\nNo publishable notes found")
        return
    
    # 批量发布
    skip_published = not args.include_published
    publish_notes_batch(notes_info, args.interval, skip_published)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser interrupted, exiting")
    except Exception as e:
        print(f"\n\nProgram error: {e}")
        import traceback
        traceback.print_exc()
