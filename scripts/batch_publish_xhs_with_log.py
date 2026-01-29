#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量发布小红书笔记脚本 - 带日志记录版本
每篇笔记发布后等待10分钟
"""

import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    from xhs import XhsClient
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install xhs python-dotenv")
    sys.exit(1)


# 日志文件路径
LOG_FILE = None


def log(message: str, to_console: bool = True, to_file: bool = True):
    """记录日志到控制台和文件"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    
    if to_console:
        print(message)
    
    if to_file and LOG_FILE:
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"[WARNING] Failed to write log: {e}")


def load_cookie():
    """从 .env 文件加载 Cookie"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    cookie = os.getenv('XHS_COOKIE')
    if not cookie:
        log("[ERROR] XHS_COOKIE not found in .env file")
        log("[INFO] Please run login_xhs_simple.py first to get cookie")
        sys.exit(1)
    
    return cookie


def create_client(cookie: str) -> XhsClient:
    """创建小红书客户端"""
    try:
        from xhs.help import sign as local_sign
        
        def sign_func(uri, data=None, a1="", web_session=""):
            return local_sign(uri, data, a1=a1)
        
        client = XhsClient(cookie=cookie, sign=sign_func)
        return client
    except Exception as e:
        log(f"[ERROR] Failed to create client: {e}")
        sys.exit(1)


def get_note_info(note_dir: str):
    """从笔记目录获取元数据"""
    metadata_file = os.path.join(note_dir, 'metadata.json')
    
    if not os.path.exists(metadata_file):
        log(f"[WARNING] metadata.json not found in {note_dir}")
        return None
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        log(f"[ERROR] Failed to read metadata: {e}")
        return None


def get_note_images(note_dir: str):
    """获取笔记的所有图片"""
    images = []
    cover = os.path.join(note_dir, 'cover.png')
    if os.path.exists(cover):
        images.append(cover)
    
    card_pattern = os.path.join(note_dir, 'card_*.png')
    cards = sorted(glob.glob(card_pattern), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    images.extend(cards)
    
    return images


def publish_note(client: XhsClient, title: str, desc: str, images: list, note_name: str):
    """发布单篇笔记"""
    try:
        log(f"\n[INFO] Publishing: {title}")
        log(f"  Images: {len(images)} files")
        
        result = client.create_image_note(
            title=title,
            desc=desc,
            files=images,
            is_private=False
        )
        
        log("[SUCCESS] Published!")
        if isinstance(result, dict):
            note_id = result.get('note_id') or result.get('id') or result.get('data', {}).get('id')
            if note_id:
                log(f"  Note ID: {note_id}")
                log(f"  URL: https://www.xiaohongshu.com/explore/{note_id}")
                
                # 保存发布记录
                save_publish_record(note_name, note_id, title)
        
        return True
        
    except Exception as e:
        log(f"[ERROR] Publish failed: {e}")
        return False


def save_publish_record(note_name: str, note_id: str, title: str):
    """保存发布记录到文件"""
    record_file = Path(__file__).parent.parent / 'publish_records.json'
    
    try:
        # 读取现有记录
        if record_file.exists():
            with open(record_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
        else:
            records = {}
        
        # 添加新记录
        records[note_name] = {
            'note_id': note_id,
            'title': title,
            'published_at': datetime.now().isoformat(),
            'url': f'https://www.xiaohongshu.com/explore/{note_id}'
        }
        
        # 保存记录
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        log(f"  Saved publish record to {record_file}")
        
    except Exception as e:
        log(f"[WARNING] Failed to save publish record: {e}")


def create_description(metadata: dict):
    """根据元数据创建描述"""
    theme = metadata.get('theme', '')
    subtitle = metadata.get('subtitle', '')
    
    desc = f"{subtitle}\n\n"
    
    tags = [
        "#德安驾校",
        "#学车",
        "#驾校推荐",
        "#学车攻略"
    ]
    
    if "价格" in theme or "费用" in theme:
        tags.extend(["#3280元学车", "#无隐形消费"])
    elif "快速" in theme or "拿证" in theme:
        tags.extend(["#35天拿证", "#快速拿证"])
    elif "先学后付" in theme:
        tags.extend(["#先学后付", "#0首付"])
    elif "教练" in theme:
        tags.extend(["#女教练", "#温柔教练"])
    elif "女生" in theme:
        tags.extend(["#女生学车", "#姐妹推荐"])
    
    desc += " ".join(tags)
    
    return desc


def batch_publish(notes_dir: str, start_from: int = 1, wait_minutes: int = 10, dry_run: bool = False):
    """批量发布笔记"""
    global LOG_FILE
    
    # 设置日志文件
    LOG_FILE = Path(notes_dir) / f'publish_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    log(f"[INFO] Log file: {LOG_FILE}")
    
    # 获取所有笔记目录
    note_dirs = sorted([d for d in glob.glob(os.path.join(notes_dir, 'note_*')) if os.path.isdir(d)])
    
    if not note_dirs:
        log(f"[ERROR] No note directories found in {notes_dir}")
        sys.exit(1)
    
    log(f"\n[INFO] Found {len(note_dirs)} notes")
    
    # 过滤起始位置
    note_dirs = [d for d in note_dirs if int(os.path.basename(d).split('_')[1]) >= start_from]
    
    if not note_dirs:
        log(f"[ERROR] No notes to publish (start_from={start_from})")
        sys.exit(1)
    
    log(f"[INFO] Will publish {len(note_dirs)} notes (starting from note_{start_from:02d})")
    
    if dry_run:
        log("\n[DRY-RUN MODE] Not actually publishing")
    
    # 加载 Cookie 并创建客户端
    cookie = load_cookie()
    client = create_client(cookie)
    
    # 逐个发布
    for i, note_dir in enumerate(note_dirs, 1):
        note_name = os.path.basename(note_dir)
        log(f"\n{'='*60}")
        log(f"[{i}/{len(note_dirs)}] Processing {note_name}")
        log('='*60)
        
        # 获取元数据
        metadata = get_note_info(note_dir)
        if not metadata:
            log(f"[ERROR] Skipping {note_name} - no metadata")
            continue
        
        title = metadata.get('title', 'Untitled')
        desc = create_description(metadata)
        
        # 获取图片
        images = get_note_images(note_dir)
        if not images:
            log(f"[ERROR] Skipping {note_name} - no images")
            continue
        
        log(f"  Title: {title}")
        log(f"  Description: {desc[:100]}...")
        log(f"  Images: {len(images)} files")
        
        if dry_run:
            log("[DRY-RUN] Would publish here")
        else:
            # 发布笔记
            success = publish_note(client, title, desc, images, note_name)
            
            if not success:
                log(f"[ERROR] Failed to publish {note_name}")
                log("[INFO] Stopping batch publish due to error")
                break
        
        # 如果不是最后一篇，等待指定时间
        if i < len(note_dirs):
            wait_seconds = wait_minutes * 60
            log(f"\n[INFO] Waiting {wait_minutes} minutes before next publish...")
            
            if not dry_run:
                # 显示倒计时
                for remaining in range(wait_seconds, 0, -30):
                    mins = remaining // 60
                    secs = remaining % 60
                    log(f"  Remaining: {mins:02d}:{secs:02d}", to_file=False)
                    time.sleep(30)
                log("")  # 换行
    
    log(f"\n{'='*60}")
    log("[SUCCESS] Batch publish completed!")
    log('='*60)
    log(f"\n[INFO] Log saved to: {LOG_FILE}")


def main():
    parser = argparse.ArgumentParser(description='Batch publish Xiaohongshu notes with logging')
    parser.add_argument(
        'notes_dir',
        help='Directory containing note_XX folders'
    )
    parser.add_argument(
        '--start-from',
        type=int,
        default=1,
        help='Start from note number (default: 1)'
    )
    parser.add_argument(
        '--wait-minutes',
        type=int,
        default=10,
        help='Wait time between publishes in minutes (default: 10)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate only, do not actually publish'
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.notes_dir):
        print(f"[ERROR] Directory not found: {args.notes_dir}")
        sys.exit(1)
    
    batch_publish(args.notes_dir, args.start_from, args.wait_minutes, args.dry_run)


if __name__ == '__main__':
    main()
