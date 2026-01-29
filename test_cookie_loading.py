# -*- coding: utf-8 -*-
"""
测试 Cookie 加载和客户端创建
"""
import os
import sys
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("Cookie Loading Test")
print("=" * 80)

# 测试 1：加载 Cookie
print("\n[Test 1] Load Cookie from .env file...")
script_dir = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts")
project_root = script_dir.parent
env_file = project_root / '.env'

print(f"Project root: {project_root}")
print(f"Env file: {env_file}")
print(f"Env file exists: {env_file.exists()}")

if env_file.exists():
    cookie = None
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('XHS_COOKIE='):
                cookie = line.replace('XHS_COOKIE=', '').strip()
                cookie = cookie.strip("'\"")
                if cookie and 'your_cookie_string_here' not in cookie:
                    break
    
    if cookie:
        print(f"OK Cookie loaded (length: {len(cookie)})")
        print(f"Cookie preview: {cookie[:100]}...")
    else:
        print("FAIL Cookie not found in .env file")
else:
    print("FAIL .env file not found")

# 测试 2：创建客户端
print("\n[Test 2] Create XHS client...")
try:
    from xhs import XhsClient
    from xhs.help import sign as local_sign
    
    print("OK xhs module imported")
    
    if cookie:
        def sign_func(uri, data=None, a1="", web_session=""):
            return local_sign(uri, data, a1=a1)
        
        try:
            client = XhsClient(cookie=cookie, sign=sign_func)
            print("OK Client created")
            
            # 测试获取用户信息
            print("\n[Test 3] Get user info...")
            try:
                info = client.get_self_info()
                print(f"OK User info retrieved")
                print(f"   Nickname: {info.get('nickname', 'Unknown')}")
            except Exception as e:
                print(f"FAIL Get user info failed: {e}")
                print(f"   This might be a Cookie issue")
                
        except Exception as e:
            print(f"FAIL Client creation failed: {e}")
    else:
        print("SKIP No cookie to test")
        
except ImportError as e:
    print(f"FAIL xhs module not found: {e}")

print("\n" + "=" * 80)
print("Test completed!")
print("=" * 80)
