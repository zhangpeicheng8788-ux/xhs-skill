#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记发布脚本 - 简化版
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    from xhs import XhsClient
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install xhs python-dotenv")
    sys.exit(1)


def load_cookie():
    """从 .env 文件加载 Cookie"""
    env_path = Path.cwd() / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    script_env = Path(__file__).parent.parent / '.env'
    if script_env.exists():
        load_dotenv(script_env)
    
    cookie = os.getenv('XHS_COOKIE')
    if not cookie:
        print("[ERROR] XHS_COOKIE not found in .env file")
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
        print(f"[ERROR] Failed to create client: {e}")
        sys.exit(1)


def validate_images(image_paths: list) -> list:
    """验证图片文件是否存在"""
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(os.path.abspath(path))
        else:
            print(f"[WARNING] Image not found: {path}")
    
    if not valid_images:
        print("[ERROR] No valid images found")
        sys.exit(1)
    
    return valid_images


def publish_note(client: XhsClient, title: str, desc: str, images: list, 
                 is_private: bool = False, post_time: str = None):
    """发布图文笔记"""
    try:
        print(f"\n[INFO] Publishing note...")
        print(f"  Title: {title}")
        print(f"  Images: {len(images)} files")
        
        result = client.create_image_note(
            title=title,
            desc=desc,
            files=images,
            is_private=is_private,
            post_time=post_time
        )
        
        print("\n[SUCCESS] Note published!")
        if isinstance(result, dict):
            note_id = result.get('note_id') or result.get('id')
            if note_id:
                print(f"  Note ID: {note_id}")
                print(f"  URL: https://www.xiaohongshu.com/explore/{note_id}")
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] Publish failed: {e}")
        sys.exit(1)


def get_user_info(client: XhsClient):
    """获取当前登录用户信息"""
    try:
        info = client.get_self_info()
        print(f"\n[INFO] Current user: {info.get('nickname', 'Unknown')}")
        return info
    except Exception as e:
        print(f"[WARNING] Cannot get user info: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Publish note to Xiaohongshu')
    parser.add_argument('--title', '-t', required=True, help='Note title (max 20 chars)')
    parser.add_argument('--desc', '-d', default='', help='Note description')
    parser.add_argument('--images', '-i', nargs='+', required=True, help='Image file paths')
    parser.add_argument('--private', action='store_true', help='Set as private note')
    parser.add_argument('--post-time', default=None, help='Scheduled publish time')
    parser.add_argument('--dry-run', action='store_true', help='Validate only, do not publish')
    
    args = parser.parse_args()
    
    # 验证标题长度
    if len(args.title) > 20:
        print(f"[WARNING] Title too long, truncating to 20 chars")
        args.title = args.title[:20]
    
    # 加载 Cookie
    cookie = load_cookie()
    
    # 验证图片
    valid_images = validate_images(args.images)
    
    # 创建客户端
    client = create_client(cookie)
    
    # 获取用户信息
    get_user_info(client)
    
    if args.dry_run:
        print("\n[DRY-RUN] Validation passed, not publishing")
        print(f"  Title: {args.title}")
        print(f"  Images: {valid_images}")
        return
    
    # 发布笔记
    publish_note(
        client=client,
        title=args.title,
        desc=args.desc,
        images=valid_images,
        is_private=args.private,
        post_time=args.post_time
    )


if __name__ == '__main__':
    main()
