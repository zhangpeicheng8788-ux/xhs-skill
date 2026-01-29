#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记发布进度查看器 - GUI版本
"""

import json
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from pathlib import Path
import webbrowser


class ProgressViewer:
    def __init__(self):
        self.record_file = Path(r"D:\20260127XHS\Auto-Redbook-Skills-main\publish_records.json")
        self.notes_dir = Path(r"D:\jieyue_work\drivingschool_notes")
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("小红书笔记发布进度查看器")
        self.root.geometry("1000x700")
        
        self.setup_ui()
        self.refresh_data()
        
        # 自动刷新
        self.auto_refresh()
        
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#FF2442', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="小红书笔记发布进度查看器",
            font=("Microsoft YaHei", 16, "bold"),
            bg='#FF2442',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # 进度信息
        info_frame = tk.Frame(self.root, padx=20, pady=15)
        info_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            info_frame,
            text="正在加载...",
            font=("Microsoft YaHei", 12, "bold"),
            fg='#FF2442'
        )
        self.progress_label.pack()
        
        self.time_label = tk.Label(
            info_frame,
            text="",
            font=("Microsoft YaHei", 9),
            fg='#666666'
        )
        self.time_label.pack()
        
        # 笔记列表
        list_frame = tk.Frame(self.root, padx=20, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            list_frame,
            text="已发布笔记列表:",
            font=("Microsoft YaHei", 10, "bold"),
            anchor='w'
        ).pack(fill=tk.X)
        
        # 创建表格
        columns = ('序号', '笔记名称', '标题', '发布时间', '操作')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列
        self.tree.heading('序号', text='序号')
        self.tree.heading('笔记名称', text='笔记名称')
        self.tree.heading('标题', text='标题')
        self.tree.heading('发布时间', text='发布时间')
        self.tree.heading('操作', text='操作')
        
        self.tree.column('序号', width=50, anchor='center')
        self.tree.column('笔记名称', width=100, anchor='center')
        self.tree.column('标题', width=300, anchor='w')
        self.tree.column('发布时间', width=150, anchor='center')
        self.tree.column('操作', width=100, anchor='center')
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # 按钮区域
        button_frame = tk.Frame(self.root, padx=20, pady=15)
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame,
            text="刷新",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            command=self.refresh_data
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="打开创作者中心",
            font=("Microsoft YaHei", 10),
            width=15,
            height=2,
            command=lambda: webbrowser.open('https://creator.xiaohongshu.com')
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="退出",
            font=("Microsoft YaHei", 10),
            width=12,
            height=2,
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)
        
    def refresh_data(self):
        """刷新数据"""
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 更新时间
        self.time_label.config(
            text=f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # 读取发布记录
        if self.record_file.exists():
            try:
                with open(self.record_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                
                published_count = len(records)
                self.progress_label.config(
                    text=f"已发布: {published_count} / 10 篇"
                )
                
                # 添加到表格
                for idx, (note_name, info) in enumerate(sorted(records.items()), 1):
                    title = info.get('title', 'Unknown')
                    published_at = info.get('published_at', '')
                    if published_at:
                        try:
                            dt = datetime.fromisoformat(published_at)
                            published_at = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass
                    
                    self.tree.insert('', tk.END, values=(
                        idx,
                        note_name,
                        title,
                        published_at,
                        '查看笔记'
                    ), tags=(info.get('url', ''),))
                
            except Exception as e:
                self.progress_label.config(text=f"读取记录失败: {e}")
        else:
            self.progress_label.config(text="暂无发布记录")
    
    def on_double_click(self, event):
        """双击打开笔记链接"""
        item = self.tree.selection()[0]
        url = self.tree.item(item, 'tags')[0]
        if url:
            webbrowser.open(url)
    
    def auto_refresh(self):
        """自动刷新"""
        self.refresh_data()
        self.root.after(5000, self.auto_refresh)  # 每5秒刷新一次
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()


def main():
    app = ProgressViewer()
    app.run()


if __name__ == '__main__':
    main()
