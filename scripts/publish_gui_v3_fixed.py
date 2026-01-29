#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记批量发布 GUI - V3.0 修复版

修复内容:
1. 修复Cookie验证逻辑,正确处理登录失败情况
2. 优化递归遍历子目录功能
3. 完善发布记录系统
4. 改进错误提示和日志记录

使用方法:
    python publish_gui_v3_fixed.py
"""

import glob
import json
import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime
from pathlib import Path
from threading import Thread
import hashlib

try:
    from dotenv import load_dotenv
    from xhs import XhsClient
    from xhs.help import sign as local_sign
    from PIL import Image, ImageTk  # 用于显示二维码
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install xhs python-dotenv pillow")
    input("Press Enter to exit...")
    sys.exit(1)


class PublishRecordManager:
    """发布记录管理器"""
    
    def __init__(self, record_file=None):
        if record_file is None:
            # 默认记录文件位置
            script_dir = Path(__file__).parent.parent
            self.record_file = script_dir / 'publish_records.json'
        else:
            self.record_file = Path(record_file)
        
        self.records = self.load_records()
    
    def load_records(self):
        """加载发布记录"""
        if self.record_file.exists():
            try:
                with open(self.record_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load records: {e}")
                return {}
        return {}
    
    def save_records(self):
        """保存发布记录"""
        try:
            # 确保目录存在
            self.record_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.record_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error: Failed to save records: {e}")
            return False
    
    def get_note_hash(self, note_dir):
        """计算笔记的唯一标识（基于路径和内容）"""
        note_dir = str(Path(note_dir).absolute())
        
        # 使用绝对路径作为基础
        hash_str = note_dir
        
        # 添加 cover.png 的修改时间（如果存在）
        cover_file = Path(note_dir) / 'cover.png'
        if cover_file.exists():
            mtime = cover_file.stat().st_mtime
            hash_str += f"_{mtime}"
        
        # 计算 MD5
        return hashlib.md5(hash_str.encode('utf-8')).hexdigest()
    
    def is_published(self, note_dir):
        """检查笔记是否已发布"""
        note_hash = self.get_note_hash(note_dir)
        return note_hash in self.records
    
    def add_record(self, note_dir, title, note_id_xhs, link):
        """添加发布记录"""
        note_hash = self.get_note_hash(note_dir)
        
        record = {
            'note_dir': str(Path(note_dir).absolute()),
            'note_name': os.path.basename(note_dir),
            'title': title,
            'note_id_xhs': note_id_xhs,
            'link': link,
            'published_at': datetime.now().isoformat(),
            'hash': note_hash
        }
        
        self.records[note_hash] = record
        
        # 同时在笔记目录创建标记文件
        self.create_marker_file(note_dir, record)
        
        return self.save_records()
    
    def create_marker_file(self, note_dir, record):
        """在笔记目录创建发布标记文件"""
        marker_file = Path(note_dir) / '.published'
        
        try:
            with open(marker_file, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: Failed to create marker file: {e}")
    
    def get_record(self, note_dir):
        """获取笔记的发布记录"""
        note_hash = self.get_note_hash(note_dir)
        return self.records.get(note_hash)
    
    def get_all_records(self):
        """获取所有发布记录"""
        return list(self.records.values())
    
    def get_statistics(self):
        """获取统计信息"""
        total = len(self.records)
        
        # 按日期统计
        today = datetime.now().date()
        today_count = 0
        
        for record in self.records.values():
            try:
                pub_date = datetime.fromisoformat(record['published_at']).date()
                if pub_date == today:
                    today_count += 1
            except:
                pass
        
        return {
            'total': total,
            'today': today_count
        }


class PublishGUI:
    def __init__(self, default_notes_dir=None, start_from=1, wait_minutes=20):
        self.notes_dir = default_notes_dir or ""
        self.start_from = start_from
        self.wait_minutes = wait_minutes
        self.is_running = False
        self.is_paused = False
        
        # 初始化发布记录管理器
        self.record_manager = PublishRecordManager()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("小红书笔记批量发布工具 V3.0 修复版")
        self.root.geometry("950x800")
        
        self.setup_ui()
        
        # 显示统计信息
        self.update_statistics()
        
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#FF2442', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="小红书笔记批量发布工具 V3.0 修复版",
            font=("Microsoft YaHei", 16, "bold"),
            bg='#FF2442',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # ===== 作者信息区域（新增）=====
        author_frame = tk.Frame(self.root, padx=20, pady=10, bg='#FFF8DC')
        author_frame.pack(fill=tk.X)
        
        # 左侧：作者信息
        author_left = tk.Frame(author_frame, bg='#FFF8DC')
        author_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            author_left,
            text="👤 作者公众号：小鱼儿AIGC",
            font=("Microsoft YaHei", 10, "bold"),
            bg='#FFF8DC',
            fg='#FF6347',
            anchor='w'
        ).pack(fill=tk.X)
        
        tk.Label(
            author_left,
            text="感谢使用本工具！如果觉得好用，欢迎赞赏支持 →",
            font=("Microsoft YaHei", 8),
            bg='#FFF8DC',
            fg='#666666',
            anchor='w'
        ).pack(fill=tk.X, pady=(2, 0))
        
        # 右侧：赞赏按钮
        author_right = tk.Frame(author_frame, bg='#FFF8DC')
        author_right.pack(side=tk.RIGHT)
        
        tk.Button(
            author_right,
            text="💰 赞赏作者",
            font=("Microsoft YaHei", 10, "bold"),
            bg='#FFD700',
            fg='#8B4513',
            width=12,
            height=1,
            cursor='hand2',
            command=self.show_donation_qrcode
        ).pack(pady=5)
        
        # ===== 统计信息区域 =====
        stats_frame = tk.Frame(self.root, padx=20, pady=10, bg='#F0F8FF')
        stats_frame.pack(fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Microsoft YaHei", 9),
            bg='#F0F8FF',
            fg='#333333',
            anchor='w'
        )
        self.stats_label.pack(fill=tk.X)
        
        # ===== 资源路径选择区域 =====
        path_frame = tk.Frame(self.root, padx=20, pady=15, bg='#F5F5F5')
        path_frame.pack(fill=tk.X)
        
        tk.Label(
            path_frame,
            text="📂 发布资源路径:",
            font=("Microsoft YaHei", 10, "bold"),
            bg='#F5F5F5',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        
        path_input_frame = tk.Frame(path_frame, bg='#F5F5F5')
        path_input_frame.pack(fill=tk.X)
        
        self.path_entry = tk.Entry(
            path_input_frame,
            font=("Microsoft YaHei", 9),
            width=60
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        if self.notes_dir:
            self.path_entry.insert(0, self.notes_dir)
        
        tk.Button(
            path_input_frame,
            text="浏览...",
            font=("Microsoft YaHei", 9),
            width=10,
            command=self.browse_path
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            path_input_frame,
            text="检测笔记",
            font=("Microsoft YaHei", 9),
            width=10,
            bg='#4CAF50',
            fg='white',
            command=self.detect_notes
        ).pack(side=tk.LEFT)
        
        # 路径提示
        self.path_hint_label = tk.Label(
            path_frame,
            text="提示：选择包含笔记的文件夹，支持递归检测所有子文件夹",
            font=("Microsoft YaHei", 8),
            bg='#F5F5F5',
            fg='#666666',
            anchor='w'
        )
        self.path_hint_label.pack(fill=tk.X, pady=(5, 0))
        
        # ===== 配置信息区域 =====
        config_frame = tk.Frame(self.root, padx=20, pady=10)
        config_frame.pack(fill=tk.X)
        
        config_left = tk.Frame(config_frame)
        config_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.notes_count_label = tk.Label(
            config_left,
            text="笔记数量: 未检测",
            font=("Microsoft YaHei", 9),
            anchor='w',
            fg='#666666'
        )
        self.notes_count_label.pack(fill=tk.X)
        
        # 新增：显示新笔记数量
        self.new_notes_label = tk.Label(
            config_left,
            text="",
            font=("Microsoft YaHei", 9),
            anchor='w',
            fg='#4CAF50'
        )
        self.new_notes_label.pack(fill=tk.X)
        
        config_right = tk.Frame(config_frame)
        config_right.pack(side=tk.RIGHT)
        
        tk.Label(
            config_right,
            text="起始笔记:",
            font=("Microsoft YaHei", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_from_var = tk.IntVar(value=self.start_from)
        tk.Spinbox(
            config_right,
            from_=1,
            to=100,
            textvariable=self.start_from_var,
            font=("Microsoft YaHei", 9),
            width=5
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            config_right,
            text="发布间隔(分钟):",
            font=("Microsoft YaHei", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.wait_minutes_var = tk.IntVar(value=self.wait_minutes)
        tk.Spinbox(
            config_right,
            from_=5,
            to=120,
            textvariable=self.wait_minutes_var,
            font=("Microsoft YaHei", 9),
            width=5
        ).pack(side=tk.LEFT)
        
        # 进度信息
        progress_frame = tk.Frame(self.root, padx=20, pady=10)
        progress_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="准备就绪，请先选择资源路径并检测笔记",
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
            height=12
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
        
        # 新增：查看发布记录按钮
        tk.Button(
            button_frame,
            text="发布记录",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            command=self.show_publish_records
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="退出",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            command=self.quit_app
        ).pack(side=tk.RIGHT, padx=5)
    
    def update_statistics(self):
        """更新统计信息"""
        stats = self.record_manager.get_statistics()
        self.stats_label.config(
            text=f"📊 发布统计: 总计 {stats['total']} 篇 | 今日 {stats['today']} 篇"
        )
    
    def show_publish_records(self):
        """显示发布记录"""
        records = self.record_manager.get_all_records()
        
        if not records:
            messagebox.showinfo("发布记录", "暂无发布记录")
            return
        
        # 创建新窗口显示记录
        record_window = tk.Toplevel(self.root)
        record_window.title("发布记录")
        record_window.geometry("800x600")
        
        # 标题
        title_label = tk.Label(
            record_window,
            text=f"发布记录 (共 {len(records)} 篇)",
            font=("Microsoft YaHei", 12, "bold"),
            pady=10
        )
        title_label.pack()
        
        # 记录列表
        record_text = scrolledtext.ScrolledText(
            record_window,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        record_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 按发布时间倒序排列
        sorted_records = sorted(
            records,
            key=lambda x: x.get('published_at', ''),
            reverse=True
        )
        
        for i, record in enumerate(sorted_records, 1):
            pub_time = record.get('published_at', 'Unknown')
            try:
                pub_time = datetime.fromisoformat(pub_time).strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
            
            record_text.insert(tk.END, f"[{i:03d}] {record.get('title', 'Untitled')}\n")
            record_text.insert(tk.END, f"      发布时间: {pub_time}\n")
            record_text.insert(tk.END, f"      笔记路径: {record.get('note_name', 'Unknown')}\n")
            record_text.insert(tk.END, f"      笔记链接: {record.get('link', 'Unknown')}\n")
            record_text.insert(tk.END, "\n")
        
        record_text.config(state=tk.DISABLED)
        
        # 关闭按钮
        tk.Button(
            record_window,
            text="关闭",
            font=("Microsoft YaHei", 10),
            width=15,
            command=record_window.destroy
        ).pack(pady=10)
    
    def browse_path(self):
        """浏览选择路径"""
        initial_dir = self.path_entry.get() or os.path.expanduser("~")
        path = filedialog.askdirectory(
            title="选择笔记资源文件夹",
            initialdir=initial_dir
        )
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.log(f"已选择路径: {path}")
    
    def detect_notes(self):
        """检测笔记 - 递归遍历所有子文件夹"""
        path = self.path_entry.get().strip()
        if not path:
            messagebox.showwarning("提示", "请先输入或选择资源路径")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("错误", f"路径不存在: {path}")
            return
        
        self.notes_dir = path
        self.log("="*60)
        self.log(f"检测路径: {path}")
        self.log("正在递归遍历所有子文件夹...")
        
        # 递归检测笔记结构
        note_dirs = []
        
        def find_notes_recursive(root_path, depth=0, max_depth=10):
            """递归查找包含 cover.png 的文件夹"""
            if depth > max_depth:
                return
            
            try:
                # 检查当前目录是否包含 cover.png
                has_cover = os.path.exists(os.path.join(root_path, 'cover.png'))
                if has_cover:
                    note_dirs.append(root_path)
                    rel_path = os.path.relpath(root_path, path)
                    if rel_path == '.':
                        rel_path = os.path.basename(root_path)
                    self.log(f"  [发现] {rel_path}")
                
                # 继续遍历子目录（即使当前目录有cover.png，子目录也可能有笔记）
                try:
                    items = os.listdir(root_path)
                except PermissionError:
                    self.log(f"  [跳过] 无权限访问: {os.path.relpath(root_path, path)}")
                    return
                
                for item in items:
                    item_path = os.path.join(root_path, item)
                    if os.path.isdir(item_path):
                        # 跳过隐藏文件夹和系统文件夹
                        if item.startswith('.') or item.startswith('__'):
                            continue
                        # 跳过常见的非笔记文件夹
                        if item.lower() in ['node_modules', 'venv', '.git', '.vscode', 'dist', 'build']:
                            continue
                        # 递归检查子文件夹
                        find_notes_recursive(item_path, depth + 1, max_depth)
            except Exception as e:
                self.log(f"  [错误] 检测 {root_path} 时出错: {str(e)}")
        
        # 开始递归查找
        find_notes_recursive(path)
        
        if not note_dirs:
            self.log("错误: 未检测到有效的笔记结构")
            self.log("请确保文件夹或其子文件夹包含:")
            self.log("  - cover.png (封面)")
            self.log("  - card_1.png, card_2.png... (内容卡片)")
            self.notes_count_label.config(text="笔记数量: 0", fg='red')
            self.new_notes_label.config(text="")
            messagebox.showerror("错误", "未检测到有效的笔记结构\n\n请确保文件夹或其子文件夹包含:\n- cover.png (封面)\n- card_*.png (内容卡片)")
            return
        
        # 按路径排序
        note_dirs.sort()
        
        # 检查哪些是新笔记（未发布）
        new_notes = []
        published_notes = []
        
        for note_dir in note_dirs:
            if self.record_manager.is_published(note_dir):
                published_notes.append(note_dir)
            else:
                new_notes.append(note_dir)
        
        # 显示检测结果
        self.notes_count_label.config(
            text=f"笔记数量: {len(note_dirs)} 个 (已发布: {len(published_notes)}, 未发布: {len(new_notes)})",
            fg='green'
        )
        
        if new_notes:
            self.new_notes_label.config(
                text=f"✨ 发现 {len(new_notes)} 个新笔记待发布",
                fg='#4CAF50'
            )
        else:
            self.new_notes_label.config(
                text="ℹ️ 所有笔记都已发布",
                fg='#FF9800'
            )
        
        self.log("")
        self.log(f"检测完成！共找到 {len(note_dirs)} 个笔记:")
        self.log(f"  - 已发布: {len(published_notes)} 个")
        self.log(f"  - 未发布: {len(new_notes)} 个")
        self.log("")
        
        # 显示未发布的笔记
        if new_notes:
            self.log("未发布的笔记:")
            for i, note_dir in enumerate(new_notes, 1):
                note_name = os.path.basename(note_dir)
                rel_path = os.path.relpath(note_dir, path)
                
                try:
                    images = [f for f in os.listdir(note_dir) if f.endswith('.png')]
                    cover_count = 1 if 'cover.png' in images else 0
                    card_count = len([f for f in images if f.startswith('card_')])
                    total_images = min(cover_count + card_count, 9)
                    
                    self.log(f"  [{i:02d}] {rel_path}")
                    self.log(f"       └─ {total_images} 张图片 (封面:{cover_count}, 卡片:{card_count})")
                except Exception as e:
                    self.log(f"  [{i:02d}] {rel_path} - 读取失败: {str(e)}")
        
        # 显示已发布的笔记（简略）
        if published_notes:
            self.log("")
            self.log(f"已发布的笔记 ({len(published_notes)} 个):")
            for i, note_dir in enumerate(published_notes[:5], 1):  # 只显示前5个
                rel_path = os.path.relpath(note_dir, path)
                record = self.record_manager.get_record(note_dir)
                if record:
                    pub_time = record.get('published_at', '')
                    try:
                        pub_time = datetime.fromisoformat(pub_time).strftime('%Y-%m-%d %H:%M')
                    except:
                        pass
                    self.log(f"  [{i:02d}] {rel_path} (发布于: {pub_time})")
            
            if len(published_notes) > 5:
                self.log(f"  ... 还有 {len(published_notes) - 5} 个已发布笔记")
        
        self.log("="*60)
        self.log("检测完成！可以开始发布")
        
        if new_notes:
            self.progress_label.config(text=f"检测到 {len(new_notes)} 个新笔记待发布，点击[开始发布]按钮启动任务")
            messagebox.showinfo(
                "检测完成",
                f"递归检测完成！\n\n"
                f"总笔记数: {len(note_dirs)} 个\n"
                f"已发布: {len(published_notes)} 个\n"
                f"未发布: {len(new_notes)} 个\n\n"
                f"将只发布未发布的笔记！"
            )
        else:
            self.progress_label.config(text=f"所有 {len(note_dirs)} 个笔记都已发布")
            messagebox.showinfo(
                "检测完成",
                f"递归检测完成！\n\n"
                f"总笔记数: {len(note_dirs)} 个\n"
                f"所有笔记都已发布过\n\n"
                f"没有新笔记需要发布"
            )
    
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
        
        # 验证路径
        path = self.path_entry.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showwarning("提示", "请先选择有效的资源路径并检测笔记")
            return
        
        self.notes_dir = path
        self.start_from = self.start_from_var.get()
        self.wait_minutes = self.wait_minutes_var.get()
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.path_entry.config(state=tk.DISABLED)
        
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
            self.path_entry.config(state=tk.NORMAL)
            self.log("任务已停止")
    
    def show_donation_qrcode(self):
        """显示赞赏二维码"""
        # 创建新窗口
        donation_window = tk.Toplevel(self.root)
        donation_window.title("赞赏作者")
        donation_window.geometry("500x650")
        donation_window.resizable(False, False)
        
        # 设置窗口背景色
        donation_window.configure(bg='#FFF8DC')
        
        # 标题
        title_label = tk.Label(
            donation_window,
            text="💰 赞赏支持",
            font=("Microsoft YaHei", 18, "bold"),
            bg='#FFF8DC',
            fg='#FF6347'
        )
        title_label.pack(pady=20)
        
        # 作者信息
        author_label = tk.Label(
            donation_window,
            text="作者公众号：小鱼儿AIGC",
            font=("Microsoft YaHei", 12, "bold"),
            bg='#FFF8DC',
            fg='#333333'
        )
        author_label.pack(pady=5)
        
        # 感谢文字
        thanks_label = tk.Label(
            donation_window,
            text="感谢您使用本工具！\n如果觉得好用，欢迎扫码赞赏支持~",
            font=("Microsoft YaHei", 10),
            bg='#FFF8DC',
            fg='#666666',
            justify='center'
        )
        thanks_label.pack(pady=10)
        
        # 二维码图片
        try:
            # 获取二维码路径
            script_dir = Path(__file__).parent.parent
            qrcode_path = script_dir / 'sang.jpg'
            
            if qrcode_path.exists():
                # 加载并调整图片大小
                img = Image.open(qrcode_path)
                # 调整大小为300x300
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 显示图片
                img_label = tk.Label(donation_window, image=photo, bg='#FFF8DC')
                img_label.image = photo  # 保持引用，防止被垃圾回收
                img_label.pack(pady=10)
                
                # 提示文字
                tip_label = tk.Label(
                    donation_window,
                    text="扫描上方二维码进行赞赏",
                    font=("Microsoft YaHei", 9),
                    bg='#FFF8DC',
                    fg='#999999'
                )
                tip_label.pack(pady=5)
            else:
                # 如果二维码文件不存在
                error_label = tk.Label(
                    donation_window,
                    text=f"二维码文件未找到\n路径: {qrcode_path}",
                    font=("Microsoft YaHei", 10),
                    bg='#FFF8DC',
                    fg='#FF0000',
                    justify='center'
                )
                error_label.pack(pady=20)
        except Exception as e:
            # 加载图片失败
            error_label = tk.Label(
                donation_window,
                text=f"加载二维码失败\n错误: {str(e)}",
                font=("Microsoft YaHei", 10),
                bg='#FFF8DC',
                fg='#FF0000',
                justify='center'
            )
            error_label.pack(pady=20)
        
        # 关闭按钮
        close_button = tk.Button(
            donation_window,
            text="关闭",
            font=("Microsoft YaHei", 10),
            width=15,
            bg='#4CAF50',
            fg='white',
            command=donation_window.destroy
        )
        close_button.pack(pady=20)
    
    def quit_app(self):
        """退出应用"""
        if self.is_running:
            if not messagebox.askyesno("确认", "发布任务正在运行，确定要退出吗？"):
                return
        self.root.quit()
    
    def load_cookie(self):
        """加载 Cookie"""
        script_dir = Path(__file__).parent.parent
        env_file = script_dir / '.env'
        
        if not env_file.exists():
            return None
        
        cookie = None
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('XHS_COOKIE='):
                    cookie = line.replace('XHS_COOKIE=', '').strip()
                    cookie = cookie.strip("'\"")
                    if cookie and 'your_cookie_string_here' not in cookie:
                        break
        
        return cookie
    
    def create_client(self, cookie):
        """创建小红书客户端"""
        def sign_func(uri, data=None, a1="", web_session=""):
            return local_sign(uri, data, a1=a1)
        
        client = XhsClient(cookie=cookie, sign=sign_func)
        return client
    
    def verify_login(self, client):
        """验证登录状态 - 修复版"""
        try:
            self.log("正在验证登录状态...")
            user_info = client.get_self_info()
            
            # 打印原始响应用于调试
            self.log(f"DEBUG: 用户信息响应: {user_info}")
            
            # 检查响应类型和内容
            if not isinstance(user_info, dict):
                self.log(f"警告: 响应类型异常: {type(user_info)}")
                return False, "响应格式错误"
            
            # 检查错误码
            code = user_info.get('code')
            success = user_info.get('success', True)
            
            if code == -1 or code == -100:
                msg = user_info.get('msg', '无登录信息')
                self.log(f"错误: Cookie已失效 - {msg}")
                return False, msg
            
            if not success:
                msg = user_info.get('msg', '登录验证失败')
                self.log(f"错误: {msg}")
                return False, msg
            
            # 尝试获取用户昵称
            data = user_info.get('data', {})
            if isinstance(data, dict):
                nickname = data.get('nickname') or data.get('name') or data.get('basic_info', {}).get('nickname')
            else:
                nickname = user_info.get('nickname') or user_info.get('name')
            
            if nickname:
                self.log(f"✅ 登录验证成功！当前用户: {nickname}")
                return True, nickname
            else:
                self.log("警告: 无法获取用户昵称，但登录似乎成功")
                return True, "未知用户"
                
        except Exception as e:
            self.log(f"登录验证异常: {str(e)}")
            return False, str(e)
    
    def get_note_info(self, note_dir):
        """获取笔记信息"""
        metadata_file = os.path.join(note_dir, 'metadata.json')
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 如果没有 metadata，返回基本信息
        note_name = os.path.basename(note_dir)
        return {
            'title': note_name,
            'subtitle': '',
            'theme': ''
        }
    
    def get_note_images(self, note_dir):
        """获取笔记图片"""
        images = []
        
        # 封面
        cover = os.path.join(note_dir, 'cover.png')
        if os.path.exists(cover):
            images.append(cover)
        
        # 内容卡片（最多9张）
        for i in range(1, 20):
            card = os.path.join(note_dir, f'card_{i}.png')
            if os.path.exists(card):
                images.append(card)
            else:
                break
        
        return images[:9]  # 小红书最多9张图
    
    def publish_task(self):
        """发布任务主逻辑 - 修复版"""
        try:
            self.log("="*60)
            self.log("开始批量发布任务 (V3.0 修复版)")
            self.log("="*60)
            
            # 加载 Cookie
            self.log("正在加载 Cookie...")
            cookie = self.load_cookie()
            if not cookie:
                self.log("❌ 错误: 未找到 Cookie")
                self.log("")
                self.log("请先运行登录脚本:")
                self.log("  python scripts/login_xhs.py")
                self.log("")
                messagebox.showerror(
                    "Cookie未找到",
                    "未找到登录Cookie\n\n"
                    "请先运行登录脚本:\n"
                    "python scripts/login_xhs.py\n\n"
                    "或双击运行 fix_cookie.bat"
                )
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.path_entry.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                return
            
            self.log(f"✅ Cookie加载成功 (长度: {len(cookie)})")
            
            # 创建客户端
            self.log("正在创建小红书客户端...")
            try:
                client = self.create_client(cookie)
                self.log("✅ 客户端创建成功")
            except Exception as e:
                self.log(f"❌ 错误: 客户端创建失败 - {str(e)}")
                messagebox.showerror("错误", f"客户端创建失败\n\n{str(e)}\n\n请检查网络连接")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.path_entry.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                return
            
            # 验证登录状态 - 使用修复后的验证方法
            login_ok, login_msg = self.verify_login(client)
            
            if not login_ok:
                self.log("❌ Cookie验证失败")
                self.log("")
                self.log("Cookie可能已过期，请重新登录:")
                self.log("  1. 运行: python scripts/login_xhs.py")
                self.log("  2. 或双击运行: fix_cookie.bat")
                self.log("  3. 扫码登录后重试")
                self.log("")
                messagebox.showerror(
                    "Cookie已失效",
                    f"Cookie验证失败: {login_msg}\n\n"
                    "Cookie可能已过期，请重新登录:\n\n"
                    "方法1: 运行 python scripts/login_xhs.py\n"
                    "方法2: 双击运行 fix_cookie.bat\n\n"
                    "扫码登录后重试"
                )
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.path_entry.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                return
            
            # 获取笔记列表 - 递归扫描
            self.log("")
            self.log("正在递归扫描笔记...")
            note_dirs = []
            
            def find_notes_recursive(root_path, depth=0, max_depth=10):
                """递归查找包含 cover.png 的文件夹"""
                if depth > max_depth:
                    return
                
                try:
                    # 检查当前目录是否包含 cover.png
                    has_cover = os.path.exists(os.path.join(root_path, 'cover.png'))
                    if has_cover:
                        note_dirs.append(root_path)
                    
                    # 继续遍历子目录（即使当前目录有cover.png，子目录也可能有笔记）
                    try:
                        items = os.listdir(root_path)
                    except PermissionError:
                        return
                    
                    for item in items:
                        item_path = os.path.join(root_path, item)
                        if os.path.isdir(item_path):
                            # 跳过隐藏文件夹和系统文件夹
                            if item.startswith('.') or item.startswith('__'):
                                continue
                            # 跳过常见的非笔记文件夹
                            if item.lower() in ['node_modules', 'venv', '.git', '.vscode', 'dist', 'build']:
                                continue
                            # 递归检查子文件夹
                            find_notes_recursive(item_path, depth + 1, max_depth)
                except Exception:
                    pass
            
            # 开始递归查找
            find_notes_recursive(self.notes_dir)
            
            # 按路径排序
            note_dirs.sort()
            
            if not note_dirs:
                self.log("❌ 错误: 没有找到要发布的笔记")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.path_entry.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                return
            
            # 过滤已发布的笔记
            self.log("")
            self.log("正在检查发布记录...")
            
            new_notes = []
            skipped_notes = []
            
            for note_dir in note_dirs:
                if self.record_manager.is_published(note_dir):
                    skipped_notes.append(note_dir)
                else:
                    new_notes.append(note_dir)
            
            self.log(f"总笔记数: {len(note_dirs)}")
            self.log(f"已发布: {len(skipped_notes)} 个 (将跳过)")
            self.log(f"未发布: {len(new_notes)} 个 (将发布)")
            
            if not new_notes:
                self.log("")
                self.log("✅ 所有笔记都已发布，没有新笔记需要发布")
                messagebox.showinfo("提示", "所有笔记都已发布过\n\n没有新笔记需要发布")
                self.is_running = False
                self.start_button.config(state=tk.NORMAL)
                self.path_entry.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                return
            
            # 开始发布
            self.log("")
            self.log("="*60)
            self.log(f"开始发布 {len(new_notes)} 个新笔记")
            self.log("="*60)
            
            published_count = 0
            failed_count = 0
            
            for idx, note_dir in enumerate(new_notes, 1):
                if not self.is_running:
                    self.log("任务已停止")
                    break
                
                # 暂停检查
                while self.is_paused and self.is_running:
                    time.sleep(1)
                
                if not self.is_running:
                    break
                
                note_name = os.path.basename(note_dir)
                rel_path = os.path.relpath(note_dir, self.notes_dir)
                
                self.log("")
                self.log(f"[{idx}/{len(new_notes)}] 正在发布: {rel_path}")
                
                try:
                    # 获取笔记信息
                    note_info = self.get_note_info(note_dir)
                    title = note_info.get('title', note_name)
                    subtitle = note_info.get('subtitle', '')
                    
                    # 构建描述
                    desc = f"{title}\n{subtitle}" if subtitle else title
                    
                    # 获取图片
                    images = self.get_note_images(note_dir)
                    
                    if not images:
                        self.log(f"  ⚠️ 跳过: 没有找到图片")
                        failed_count += 1
                        continue
                    
                    self.log(f"  标题: {title}")
                    self.log(f"  图片: {len(images)} 张")
                    
                    # 上传图片
                    self.log(f"  正在上传图片...")
                    image_ids = []
                    
                    for img_idx, img_path in enumerate(images, 1):
                        try:
                            with open(img_path, 'rb') as f:
                                img_data = f.read()
                            
                            result = client.upload_image_file(img_data)
                            
                            if isinstance(result, dict) and result.get('success'):
                                image_id = result.get('data', {}).get('image_id')
                                if image_id:
                                    image_ids.append(image_id)
                                    self.log(f"    [{img_idx}/{len(images)}] 上传成功")
                                else:
                                    self.log(f"    [{img_idx}/{len(images)}] 上传失败: 未获取到image_id")
                            else:
                                self.log(f"    [{img_idx}/{len(images)}] 上传失败: {result}")
                        except Exception as e:
                            self.log(f"    [{img_idx}/{len(images)}] 上传异常: {str(e)}")
                    
                    if not image_ids:
                        self.log(f"  ❌ 发布失败: 所有图片上传失败")
                        failed_count += 1
                        continue
                    
                    # 发布笔记
                    self.log(f"  正在发布笔记...")
                    
                    result = client.create_image_note(
                        title=title,
                        desc=desc,
                        image_ids=image_ids,
                        is_private=False
                    )
                    
                    if isinstance(result, dict) and result.get('success'):
                        note_id = result.get('data', {}).get('note_id')
                        link = f"https://www.xiaohongshu.com/explore/{note_id}" if note_id else "Unknown"
                        
                        self.log(f"  ✅ 发布成功!")
                        self.log(f"  笔记ID: {note_id}")
                        self.log(f"  链接: {link}")
                        
                        # 记录发布
                        self.record_manager.add_record(note_dir, title, note_id, link)
                        published_count += 1
                        
                        # 更新统计
                        self.update_statistics()
                        
                    else:
                        self.log(f"  ❌ 发布失败: {result}")
                        failed_count += 1
                    
                except Exception as e:
                    self.log(f"  ❌ 发布异常: {str(e)}")
                    failed_count += 1
                
                # 更新进度
                self.update_progress(idx, len(new_notes))
                
                # 等待间隔（最后一个不等待）
                if idx < len(new_notes) and self.is_running:
                    wait_seconds = self.wait_minutes * 60
                    self.log(f"  等待 {self.wait_minutes} 分钟后发布下一篇...")
                    
                    for i in range(wait_seconds):
                        if not self.is_running:
                            break
                        while self.is_paused and self.is_running:
                            time.sleep(1)
                        if not self.is_running:
                            break
                        time.sleep(1)
            
            # 完成
            self.log("")
            self.log("="*60)
            self.log("发布任务完成!")
            self.log(f"成功: {published_count} 篇")
            self.log(f"失败: {failed_count} 篇")
            self.log("="*60)
            
            messagebox.showinfo(
                "发布完成",
                f"发布任务完成！\n\n"
                f"成功: {published_count} 篇\n"
                f"失败: {failed_count} 篇"
            )
            
        except Exception as e:
            self.log(f"❌ 任务异常: {str(e)}")
            messagebox.showerror("错误", f"任务执行异常\n\n{str(e)}")
        
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.path_entry.config(state=tk.NORMAL)
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书笔记批量发布工具 V3.0 修复版')
    parser.add_argument('--path', type=str, help='笔记资源路径')
    parser.add_argument('--start-from', type=int, default=1, help='起始笔记序号')
    parser.add_argument('--wait-minutes', type=int, default=20, help='发布间隔(分钟)')
    
    args = parser.parse_args()
    
    # 创建并运行GUI
    app = PublishGUI(
        default_notes_dir=args.path,
        start_from=args.start_from,
        wait_minutes=args.wait_minutes
    )
    app.run()


if __name__ == '__main__':
    main()
