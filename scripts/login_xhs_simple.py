#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书扫码登录脚本 - 简化版
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv, set_key
    from playwright.async_api import async_playwright
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install python-dotenv playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)


async def get_cookie_from_browser():
    """通过浏览器扫码登录获取 Cookie"""
    print("\n[INFO] Starting Xiaohongshu login...")
    print("[INFO] Opening browser, please scan QR code with Xiaohongshu app")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 访问小红书创作者中心
            await page.goto('https://creator.xiaohongshu.com', wait_until='networkidle')
            
            print("\n[INFO] Please scan the QR code to login...")
            print("[INFO] Waiting for login completion (max 5 minutes)...")
            
            # 等待登录成功（检测页面跳转或特定元素）
            try:
                await page.wait_for_url('**/creator.xiaohongshu.com/**', timeout=300000)
                print("\n[SUCCESS] Login successful!")
            except Exception:
                print("\n[WARNING] Timeout or login failed, trying to get cookies anyway...")
            
            # 等待一下确保 Cookie 完全设置
            await asyncio.sleep(3)
            
            # 获取所有 Cookie
            cookies = await context.cookies()
            
            if not cookies:
                print("[ERROR] No cookies found")
                return None
            
            # 转换为字符串格式
            cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            
            print(f"\n[SUCCESS] Got {len(cookies)} cookies")
            return cookie_str
            
        finally:
            await browser.close()


def save_cookie_to_env(cookie: str):
    """保存 Cookie 到 .env 文件"""
    env_path = Path(__file__).parent.parent / '.env'
    
    # 添加更新时间注释
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 读取现有内容
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # 更新或添加 Cookie
        lines = content.split('\n')
        new_lines = []
        cookie_found = False
        
        for line in lines:
            if line.startswith('XHS_COOKIE='):
                new_lines.append(f"# Update time: {timestamp}")
                new_lines.append(f"XHS_COOKIE={cookie}")
                cookie_found = True
            elif not line.startswith('# Update time:'):
                new_lines.append(line)
        
        if not cookie_found:
            new_lines.append(f"# Xiaohongshu Cookie")
            new_lines.append(f"# Update time: {timestamp}")
            new_lines.append(f"XHS_COOKIE={cookie}")
        
        # 写入文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"\n[SUCCESS] Cookie saved to: {env_path}")
        print(f"[INFO] Update time: {timestamp}")
        
    except Exception as e:
        print(f"[ERROR] Failed to save cookie: {e}")
        sys.exit(1)


def check_existing_cookie():
    """检查现有 Cookie 是否存在"""
    env_path = Path(__file__).parent.parent / '.env'
    
    if not env_path.exists():
        return False
    
    load_dotenv(env_path)
    cookie = os.getenv('XHS_COOKIE')
    
    if cookie:
        print(f"\n[INFO] Found existing cookie in .env")
        return True
    
    return False


async def main(force=False):
    print("=" * 60)
    print("Xiaohongshu Login Tool")
    print("=" * 60)
    
    # 检查现有 Cookie
    has_cookie = check_existing_cookie()
    
    if has_cookie and not force:
        print("\n[INFO] Cookie already exists. Use --force to re-login")
        return
    
    # 获取 Cookie
    cookie = await get_cookie_from_browser()
    
    if not cookie:
        print("\n[ERROR] Failed to get cookie")
        sys.exit(1)
    
    # 保存 Cookie
    save_cookie_to_env(cookie)
    
    print("\n[SUCCESS] All done! You can now use publish_xhs.py to publish notes")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Xiaohongshu Login Tool')
    parser.add_argument('--force', action='store_true', help='Force re-login even if cookie exists')
    args = parser.parse_args()
    
    try:
        asyncio.run(main(force=args.force))
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
