#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证小红书 Cookie 是否有效
"""

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
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    cookie = os.getenv('XHS_COOKIE')
    if not cookie:
        print("[ERROR] XHS_COOKIE not found in .env file")
        sys.exit(1)
    
    return cookie


def validate_cookie(cookie: str):
    """验证 Cookie 格式"""
    print("\n[INFO] Validating cookie format...")
    print(f"  Cookie length: {len(cookie)} characters")
    
    # 检查是否包含多个键值对
    if ';' not in cookie:
        print("[WARNING] Cookie seems incomplete (no semicolons found)")
        print("[INFO] A valid cookie should contain multiple key=value pairs separated by semicolons")
        print("[INFO] Example: key1=value1; key2=value2; key3=value3")
        return False
    
    # 检查是否包含常见的小红书 Cookie 字段
    required_fields = ['a1', 'web_session']
    found_fields = []
    
    for field in required_fields:
        if f'{field}=' in cookie:
            found_fields.append(field)
    
    print(f"  Found fields: {found_fields}")
    
    if not found_fields:
        print("[WARNING] Cookie may be invalid (missing common fields like 'a1', 'web_session')")
        return False
    
    print("[SUCCESS] Cookie format looks valid")
    return True


def test_cookie(cookie: str):
    """测试 Cookie 是否可以正常使用"""
    print("\n[INFO] Testing cookie with Xiaohongshu API...")
    
    try:
        from xhs.help import sign as local_sign
        
        def sign_func(uri, data=None, a1="", web_session=""):
            return local_sign(uri, data, a1=a1)
        
        client = XhsClient(cookie=cookie, sign=sign_func)
        
        # 尝试获取用户信息
        print("[INFO] Fetching user info...")
        info = client.get_self_info()
        
        if info and isinstance(info, dict):
            nickname = info.get('nickname', 'Unknown')
            user_id = info.get('user_id', 'Unknown')
            print(f"\n[SUCCESS] Cookie is valid!")
            print(f"  Nickname: {nickname}")
            print(f"  User ID: {user_id}")
            return True
        else:
            print("[ERROR] Failed to get user info")
            return False
            
    except Exception as e:
        print(f"[ERROR] Cookie validation failed: {e}")
        return False


def main():
    print("="*60)
    print("Xiaohongshu Cookie Validator")
    print("="*60)
    
    # 加载 Cookie
    cookie = load_cookie()
    
    # 验证格式
    format_valid = validate_cookie(cookie)
    
    if not format_valid:
        print("\n[ERROR] Cookie format is invalid")
        print("\n[HELP] How to get a valid cookie:")
        print("  1. Open https://creator.xiaohongshu.com in browser")
        print("  2. Login with your account")
        print("  3. Press F12 to open DevTools")
        print("  4. Go to Network tab")
        print("  5. Refresh the page")
        print("  6. Click any request")
        print("  7. Find 'Cookie' in Request Headers")
        print("  8. Copy the ENTIRE cookie string")
        print("  9. Update XHS_COOKIE in .env file")
        sys.exit(1)
    
    # 测试 Cookie
    api_valid = test_cookie(cookie)
    
    if api_valid:
        print("\n"+"="*60)
        print("[SUCCESS] Cookie validation passed!")
        print("You can now use batch_publish_xhs.py to publish notes")
        print("="*60)
        sys.exit(0)
    else:
        print("\n"+"="*60)
        print("[ERROR] Cookie validation failed!")
        print("Please update your cookie in .env file")
        print("="*60)
        sys.exit(1)


if __name__ == '__main__':
    main()
