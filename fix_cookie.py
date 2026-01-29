# -*- coding: utf-8 -*-
"""
一键修复"无登录信息"问题
"""
import os
import sys
from pathlib import Path
import subprocess

os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 80)
print("XHS Cookie Fix Tool")
print("=" * 80)
print()
print("This tool will help you fix the 'No login info' error")
print()

# 步骤 1：检查 .env 文件
print("[Step 1] Check .env file...")
env_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\.env")

if env_file.exists():
    print(f"OK .env file exists: {env_file}")
    
    # 询问是否删除
    print()
    print("Do you want to delete the old Cookie file and re-login?")
    print("1. Yes - Delete and re-login (Recommended)")
    print("2. No - Keep existing Cookie and test")
    print()
    
    choice = input("Enter choice (1/2): ").strip()
    
    if choice == '1':
        print()
        print("Deleting old .env file...")
        try:
            env_file.unlink()
            print("OK Old .env file deleted")
        except Exception as e:
            print(f"FAIL Failed to delete: {e}")
            input("\nPress Enter to exit...")
            sys.exit(1)
    else:
        print()
        print("Keeping existing Cookie...")
else:
    print(f"WARN .env file not found: {env_file}")
    print("Will create new Cookie file after login")

# 步骤 2：运行登录脚本
print()
print("[Step 2] Run login script...")
print()
print("A browser window will open for QR code login")
print("Please scan the QR code with your XHS app")
print()

login_script = r"D:\20260127XHS\Auto-Redbook-Skills-main\scripts\login_xhs.py"

if not Path(login_script).exists():
    print(f"FAIL Login script not found: {login_script}")
    input("\nPress Enter to exit...")
    sys.exit(1)

input("Press Enter to start login...")
print()

try:
    result = subprocess.run(
        [sys.executable, login_script],
        cwd=r"D:\20260127XHS\Auto-Redbook-Skills-main"
    )
    
    if result.returncode == 0:
        print()
        print("=" * 80)
        print("Login completed!")
        print("=" * 80)
    else:
        print()
        print("=" * 80)
        print("Login may have failed, please check the output above")
        print("=" * 80)
        
except Exception as e:
    print(f"FAIL Error running login script: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

# 步骤 3：测试 Cookie
print()
print("[Step 3] Test Cookie...")
print()

test_script = r"D:\20260127XHS\Auto-Redbook-Skills-main\test_cookie_loading.py"

if Path(test_script).exists():
    try:
        subprocess.run([sys.executable, test_script])
    except Exception as e:
        print(f"WARN Test script error: {e}")
else:
    print(f"WARN Test script not found: {test_script}")

# 完成
print()
print("=" * 80)
print("Fix process completed!")
print("=" * 80)
print()
print("Next steps:")
print("1. Run start_publish.bat to start the GUI")
print("2. Select your notes folder")
print("3. Click 'Detect Notes' button")
print("4. Click 'Start Publish' button")
print()

input("Press Enter to exit...")
