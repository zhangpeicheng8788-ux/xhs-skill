#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布辅助模块
提供统一的发布接口
"""

import sys
import os
from pathlib import Path

try:
    from xhs import XhsClient
    from xhs.help import sign as local_sign
except ImportError:
    print("Please install xhs library: pip install xhs")
    sys.exit(1)


def load_cookie():
    """从 .env 文件加载 Cookie"""
    # 优先使用项目根目录的 .env
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    
    if not env_file.exists():
        return None
    
    cookie = None
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('XHS_COOKIE=') and 'your_cookie_string_here' not in line:
                cookie = line.replace('XHS_COOKIE=', '').strip()
                # 移除引号
                cookie = cookie.strip("'\"")
                if cookie:
                    break
    
    return cookie


def create_client():
    """创建小红书客户端"""
    cookie = load_cookie()
    
    if not cookie:
        raise Exception("No valid Cookie found, please run login_xhs.py first")
    
    def sign_func(uri, data=None, a1="", web_session=""):
        return local_sign(uri, data, a1=a1)
    
    try:
        client = XhsClient(cookie=cookie, sign=sign_func)
        return client
    except Exception as e:
        raise Exception(f"Failed to create client: {e}")


def publish_note(title, desc, images, is_private=False):
    """
    发布笔记
    
    Args:
        title: 笔记标题
        desc: 笔记描述/正文
        images: 图片路径列表
        is_private: 是否私密笔记
    
    Returns:
        dict: 发布结果
            {
                'success': bool,
                'note_id': str,
                'link': str,
                'error': str (if failed)
            }
    """
    try:
        client = create_client()
        
        # 验证图片
        valid_images = []
        for img_path in images:
            img_file = Path(img_path)
            if img_file.exists() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                valid_images.append(str(img_file.absolute()))
        
        if not valid_images:
            return {
                'success': False,
                'error': 'No valid image files'
            }
        
        # 发布笔记
        result = client.create_image_note(
            title=title,
            desc=desc,
            files=valid_images,
            is_private=is_private
        )
        
        # 解析结果
        if isinstance(result, dict):
            note_id = result.get('id') or result.get('note_id')
            if note_id:
                return {
                    'success': True,
                    'note_id': note_id,
                    'link': f'https://www.xiaohongshu.com/explore/{note_id}',
                    'result': result
                }
        
        return {
            'success': False,
            'error': 'Publish failed, no note ID returned',
            'result': result
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_user_info():
    """获取当前用户信息"""
    try:
        client = create_client()
        info = client.get_self_info()
        return {
            'success': True,
            'info': info
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
