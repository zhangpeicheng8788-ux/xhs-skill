#!/usr/bin/env python3
"""
小红书扫码登录脚本
弹出浏览器窗口，扫码登录后自动保存 Cookie

使用方法:
    python login_xhs.py

功能:
    1. 弹出小红书登录页面
    2. 用户扫码登录
    3. 自动保存 Cookie 到 .env 文件
    4. 下次发布时自动使用保存的 Cookie

依赖安装:
    pip install playwright python-dotenv
    playwright install chromium
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright
    from dotenv import load_dotenv, set_key
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip install playwright python-dotenv")
    print("然后运行: playwright install chromium")
    sys.exit(1)


# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent.parent
ENV_FILE = SCRIPT_DIR / '.env'


def load_existing_cookie():
    """加载现有的 Cookie"""
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
        return os.getenv('XHS_COOKIE')
    return None


def save_cookie(cookie_str: str):
    """保存 Cookie 到 .env 文件"""
    try:
        # 如果 .env 文件不存在，创建它
        if not ENV_FILE.exists():
            ENV_FILE.touch()
            print(f"✅ 创建配置文件: {ENV_FILE}")
        
        # 保存或更新 Cookie
        set_key(ENV_FILE, 'XHS_COOKIE', cookie_str)
        print(f"✅ Cookie 已保存到: {ENV_FILE}")
        
        # 添加备注信息
        with open(ENV_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n# Cookie 更新时间: {timestamp}\n")
        
        return True
    except Exception as e:
        print(f"❌ 保存 Cookie 失败: {e}")
        return False


async def wait_for_login(page):
    """等待用户登录完成"""
    print("\n📱 请使用小红书 APP 扫码登录...")
    print("⏳ 等待登录中...")
    
    # 等待登录成功的标志
    # 小红书登录成功后会跳转到首页或创作者中心
    try:
        # 方法1: 等待跳转到首页
        await page.wait_for_url("**/explore**", timeout=120000)
        return True
    except:
        try:
            # 方法2: 等待用户头像出现
            await page.wait_for_selector(".avatar, .user-avatar, [class*='avatar']", timeout=120000)
            return True
        except:
            try:
                # 方法3: 检查是否有用户相关的 Cookie
                cookies = await page.context.cookies()
                for cookie in cookies:
                    if cookie['name'] in ['web_session', 'a1', 'webId']:
                        return True
                return False
            except:
                return False


def format_cookie(cookies):
    """将 Cookie 列表格式化为字符串"""
    cookie_parts = []
    for cookie in cookies:
        cookie_parts.append(f"{cookie['name']}={cookie['value']}")
    return '; '.join(cookie_parts)


async def login_with_qrcode():
    """使用二维码登录小红书"""
    async with async_playwright() as p:
        # 启动浏览器（非无头模式，显示窗口）
        print("🌐 正在启动浏览器...")
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--window-size=800,900',
                '--window-position=400,100'
            ]
        )
        
        # 创建浏览器上下文
        context = await browser.new_context(
            viewport={'width': 800, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 创建新页面
        page = await context.new_page()
        
        try:
            # 访问小红书创作者平台登录页
            print("📄 正在打开小红书登录页面...")
            await page.goto('https://creator.xiaohongshu.com/login', wait_until='networkidle')
            
            # 等待二维码加载
            await asyncio.sleep(2)
            
            # 等待用户登录
            login_success = await wait_for_login(page)
            
            if not login_success:
                print("❌ 登录超时或失败")
                await browser.close()
                return False
            
            print("✅ 登录成功！")
            
            # 等待一下确保 Cookie 完全设置
            await asyncio.sleep(2)
            
            # 获取所有 Cookie
            cookies = await context.cookies()
            
            if not cookies:
                print("❌ 未能获取 Cookie")
                await browser.close()
                return False
            
            # 格式化并保存 Cookie
            cookie_str = format_cookie(cookies)
            
            print(f"\n📋 获取到 {len(cookies)} 个 Cookie")
            
            # 显示关键 Cookie
            key_cookies = ['web_session', 'a1', 'webId']
            found_keys = [c['name'] for c in cookies if c['name'] in key_cookies]
            if found_keys:
                print(f"🔑 关键 Cookie: {', '.join(found_keys)}")
            
            # 保存 Cookie
            if save_cookie(cookie_str):
                print("\n🎉 登录配置完成！")
                print("💡 现在可以使用 publish_xhs.py 发布笔记了")
                
                # 等待几秒让用户看到成功消息
                await asyncio.sleep(3)
                await browser.close()
                return True
            else:
                await browser.close()
                return False
                
        except Exception as e:
            print(f"❌ 登录过程出错: {e}")
            await browser.close()
            return False


async def verify_cookie():
    """验证现有 Cookie 是否有效"""
    existing_cookie = load_existing_cookie()
    
    if not existing_cookie:
        return False
    
    print("🔍 检测到现有 Cookie，正在验证...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        # 设置 Cookie
        cookies = []
        for item in existing_cookie.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.xiaohongshu.com',
                    'path': '/'
                })
        
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        try:
            # 访问创作者中心
            await page.goto('https://creator.xiaohongshu.com/', timeout=10000)
            await asyncio.sleep(2)
            
            # 检查是否登录成功（没有跳转到登录页）
            current_url = page.url
            if 'login' not in current_url:
                print("✅ 现有 Cookie 有效")
                await browser.close()
                return True
            else:
                print("⚠️ 现有 Cookie 已失效")
                await browser.close()
                return False
                
        except Exception as e:
            print(f"⚠️ Cookie 验证失败: {e}")
            await browser.close()
            return False


async def main():
    print("=" * 60)
    print("🔐 小红书扫码登录工具")
    print("=" * 60)
    
    # 检查现有 Cookie
    if ENV_FILE.exists():
        cookie_valid = await verify_cookie()
        
        if cookie_valid:
            print("\n✨ 您已经登录，Cookie 仍然有效")
            print("💡 如需重新登录，请删除 .env 文件后再运行此脚本")
            
            response = input("\n是否要重新登录？(y/N): ").strip().lower()
            if response != 'y':
                print("👋 保持现有登录状态")
                return
            
            print("\n🔄 开始重新登录...")
    
    # 执行登录
    success = await login_with_qrcode()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 登录成功！")
        print("=" * 60)
        print("\n📝 使用方法:")
        print("   python scripts/publish_xhs.py --title '标题' --desc '描述' --images cover.png card_1.png")
    else:
        print("\n" + "=" * 60)
        print("❌ 登录失败")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 用户取消登录")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        sys.exit(1)
