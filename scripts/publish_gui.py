#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记批量发布 - 独立运行版本
不依赖终端，直接在独立窗口中运行
"""

import argparse
import glob
import json
import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
from pathlib import Path
from threading import Thread

try:
    from dotenv import load_dotenv
    from xhs import XhsClient
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install xhs python-dotenv")
    input("Press Enter to exit...")
    sys.exit(1)


class PublishGUI:
    def __init__(self, notes_dir, start_from=1, wait_minutes=10):
        self.notes_dir = notes_dir
        self.start_from = start_from
        self.wait_minutes = wait_minutes
        self.is_running = False
        self.is_paused = False
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("小红书笔记批量发布工具")
        self.root.geometry("900x700")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#FF2442', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="小红书笔记批量发布工具",
            font=("Microsoft YaHei", 16, "bold"),
            bg='#FF2442',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # 配置信息
        config_frame = tk.Frame(self.root, padx=20, pady=10)
        config_frame.pack(fill=tk.X)
        
        tk.Label(
            config_frame,
            text=f"笔记目录: {self.notes_dir}",
            font=("Microsoft YaHei", 9),
            anchor='w'
        ).pack(fill=tk.X)
        
        tk.Label(
            config_frame,
            text=f"起始笔记: note_{self.start_from:02d}  |  发布间隔: {self.wait_minutes} 分钟/篇",
            font=("Microsoft YaHei", 9),
            anchor='w'
        ).pack(fill=tk.X)
        
        # 进度信息
        progress_frame = tk.Frame(self.root, padx=20, pady=10)
        progress_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="准备就绪，点击[开始发布]按钮启动任务",
            font=("Microsoft YaHei", 10),
            fg='#666666'
        )
        self.progress_label.pack()
        
        # 日志输出区域
        log_frame = tk.Frame(self.root, padx=20, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            log_frame,
            text="发布日志:",
            font=("Microsoft YaHei", 9, "bold"),
            anchor='w'
        ).pack(fill=tk.X)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            wrap=tk.WORD,
            height=20
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        button_frame = tk.Frame(self.root, padx=20, pady=15)
        button_frame.pack(fill=tk.X)
        
        self.start_button = tk.Button(
            button_frame,
            text="开始发布",
            font=("Microsoft YaHei", 10, "bold"),
            bg='#FF2442',
            fg='white',
            width=12,
            height=2,
            command=self.start_publish
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="暂停",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            state=tk.DISABLED,
            command=self.toggle_pause
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="停止",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            state=tk.DISABLED,
            command=self.stop_publish
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="退出",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            command=self.quit_app
        ).pack(side=tk.RIGHT, padx=5)
        
    def log(self, message, color='black'):
        """添加日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_progress(self, current, total):
        """更新进度"""
        self.progress_label.config(
            text=f"发布进度: {current}/{total} 篇已完成"
        )
        
    def start_publish(self):
        """开始发布"""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        
        # 在新线程中运行发布任务
        thread = Thread(target=self.publish_task, daemon=True)
        thread.start()
        
    def toggle_pause(self):
        """暂停/继续"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="继续")
            self.log("任务已暂停")
        else:
            self.pause_button.config(text="暂停")
            self.log("任务已继续")
            
    def stop_publish(self):
        """停止发布"""
        if messagebox.askyesno("确认", "确定要停止发布任务吗？"):
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.log("任务已停止")
            
    def quit_app(self):
        """退出应用"""
        if self.is_running:
            if not messagebox.askyesno("确认", "发布任务正在运行，确定要退出吗？"):
                return
        self.root.quit()
        
    def publish_task(self):
        """发布任务主逻辑"""
        try:
            self.log("="*60)
            self.log("开始批量发布任务")
            self.log("="*60)
            
            # 加载 Cookie
            self.log("正在加载 Cookie...")
            cookie = self.load_cookie()
            if not cookie:
                self.log("错误: 未找到 Cookie，请先配置 .env 文件")
                self.is_running = False
                return
            
            # 创建客户端
            self.log("正在创建小红书客户端...")
            client = self.create_client(cookie)
            
            # 获取笔记列表
            note_dirs = sorted([
                d for d in glob.glob(os.path.join(self.notes_dir, 'note_*'))
                if os.path.isdir(d)
            ])
            
            note_dirs = [
                d for d in note_dirs
                if int(os.path.basename(d).split('_')[1]) >= self.start_from
            ]
            
            if not note_dirs:
                self.log("错误: 没有找到要发布的笔记")
                self.is_running = False
                return
            
            total = len(note_dirs)
            self.log(f"找到 {total} 篇笔记待发布")
            self.log("")
            
            # 逐个发布
            for i, note_dir in enumerate(note_dirs, 1):
                if not self.is_running:
                    self.log("任务已被停止")
                    break
                
                # 等待暂停结束
                while self.is_paused and self.is_running:
                    time.sleep(1)
                
                if not self.is_running:
                    break
                
                note_name = os.path.basename(note_dir)
                self.log("="*60)
                self.log(f"[{i}/{total}] 处理 {note_name}")
                self.log("="*60)
                
                # 获取笔记信息
                metadata = self.get_note_info(note_dir)
                if not metadata:
                    self.log(f"跳过 {note_name} - 无法读取元数据")
                    continue
                
                title = metadata.get('title', 'Untitled')
                desc = self.create_description(metadata)
                
                # 获取图片
                images = self.get_note_images(note_dir)
                if not images:
                    self.log(f"跳过 {note_name} - 没有图片")
                    continue
                
                self.log(f"标题: {title}")
                self.log(f"图片数量: {len(images)}")
                
                # 发布笔记
                success = self.publish_note(client, title, desc, images)
                
                if success:
                    self.update_progress(i, total)
                else:
                    self.log("发布失败，停止任务")
                    break
                
                # 等待间隔
                if i < total and self.is_running:
                    self.log(f"等待 {self.wait_minutes} 分钟后发布下一篇...")
                    
                    wait_seconds = self.wait_minutes * 60
                    for remaining in range(wait_seconds, 0, -10):
                        if not self.is_running:
                            break
                        
                        while self.is_paused and self.is_running:
                            time.sleep(1)
                        
                        if not self.is_running:
                            break
                        
                        mins = remaining // 60
                        secs = remaining % 60
                        self.progress_label.config(
                            text=f"等待中... 剩余时间: {mins:02d}:{secs:02d}"
                        )
                        time.sleep(10)
                    
                    self.log("")
            
            if self.is_running:
                self.log("="*60)
                self.log("批量发布任务完成！")
                self.log("="*60)
                messagebox.showinfo("完成", "所有笔记发布完成！")
            
        except Exception as e:
            self.log(f"错误: {e}")
            messagebox.showerror("错误", f"发布过程中出现错误:\n{e}")
        
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
    
    def load_cookie(self):
        """加载 Cookie"""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        return os.getenv('XHS_COOKIE')
    
    def create_client(self, cookie):
        """创建客户端"""
        from xhs.help import sign as local_sign
        
        def sign_func(uri, data=None, a1="", web_session=""):
            return local_sign(uri, data, a1=a1)
        
        return XhsClient(cookie=cookie, sign=sign_func)
    
    def get_note_info(self, note_dir):
        """获取笔记信息"""
        metadata_file = os.path.join(note_dir, 'metadata.json')
        if not os.path.exists(metadata_file):
            return None
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def get_note_images(self, note_dir):
        """获取笔记图片"""
        images = []
        cover = os.path.join(note_dir, 'cover.png')
        if os.path.exists(cover):
            images.append(cover)
        
        card_pattern = os.path.join(note_dir, 'card_*.png')
        cards = sorted(
            glob.glob(card_pattern),
            key=lambda x: int(x.split('_')[-1].split('.')[0])
        )
        images.extend(cards)
        
        return images
    
    def create_description(self, metadata):
        """创建描述"""
        theme = metadata.get('theme', '')
        subtitle = metadata.get('subtitle', '')
        
        desc = f"{subtitle}\n\n"
        
        tags = ["#德安驾校", "#学车", "#驾校推荐", "#学车攻略"]
        
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
    
    def publish_note(self, client, title, desc, images):
        """发布笔记"""
        try:
            self.log("正在上传图片...")
            
            result = client.create_image_note(
                title=title,
                desc=desc,
                files=images,
                is_private=False
            )
            
            self.log("发布成功！")
            
            if isinstance(result, dict):
                note_id = result.get('note_id') or result.get('id') or \
                         result.get('data', {}).get('id')
                if note_id:
                    url = f"https://www.xiaohongshu.com/explore/{note_id}"
                    self.log(f"笔记ID: {note_id}")
                    self.log(f"链接: {url}")
            
            return True
            
        except Exception as e:
            self.log(f"发布失败: {e}")
            return False
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(description='小红书笔记批量发布工具（GUI版本）')
    parser.add_argument(
        '--notes-dir',
        default=r'D:\jieyue_work\drivingschool_notes',
        help='笔记目录路径'
    )
    parser.add_argument(
        '--start-from',
        type=int,
        default=1,
        help='从第几篇开始发布'
    )
    parser.add_argument(
        '--wait-minutes',
        type=int,
        default=10,
        help='每篇笔记之间的等待时间（分钟）'
    )
    
    args = parser.parse_args()
    
    # 创建并运行GUI
    app = PublishGUI(args.notes_dir, args.start_from, args.wait_minutes)
    app.run()


if __name__ == '__main__':
    main()
