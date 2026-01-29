# Auto-Redbook Skill V6.6

> 小红书笔记素材创作与批量发布工具

[![Version](https://img.shields.io/badge/version-6.6-blue.svg)](CHANGELOG_V6.6.md)
[![Python](https://img.shields.io/badge/python-3.14-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📖 简介

Auto-Redbook Skill 是一个专业的小红书笔记创作与发布工具，支持：

- ✅ 小红书风格内容创作
- ✅ 图片卡片智能渲染（7种样式）
- ✅ 批量发布笔记（GUI 图形界面）
- ✅ 自动间隔发布（防限流）
- ✅ 实时进度监控
- ✅ 发布记录管理

---

## 🚀 快速开始

### 1. 测试环境
```
双击运行: test_environment.bat
```

### 2. 配置 Cookie
创建 `.env` 文件，添加：
```
XHS_COOKIE=你的Cookie字符串
```

### 3. 开始发布
```
双击运行: start_publish.bat
```

**详细教程**: 查看 [使用指南.md](使用指南.md)

---

## 📦 目录结构

```
Auto-Redbook-Skills-main/
├── start_publish.bat          # 批量发布工具启动器
├── view_progress.bat          # 进度查看器启动器
├── test_environment.bat       # 环境测试工具
├── 使用指南.md                # 完整使用指南
├── SKILL.md                   # 技能文档
├── CHANGELOG_V6.6.md          # 版本说明
│
├── scripts/                   # Python 脚本
│   ├── publish_gui.py         # 批量发布 GUI
│   ├── progress_viewer_gui.py # 进度查看器 GUI
│   ├── render_xhs_v2.py      # 图片渲染脚本
│   └── ...
│
├── docs/                      # 文档目录
│   ├── 快速使用指南.md
│   ├── GUI工具使用说明.md
│   ├── Cookie获取指南.md
│   └── 常见问题解答.md
│
└── assets/                    # 资源文件
    ├── cover.html
    ├── card.html
    └── styles.css
```

---

## 🎨 核心功能

### 1. 内容创作
- 小红书风格标题和正文
- Markdown 格式支持
- 智能分页渲染
- 7种样式主题

### 2. 图片渲染
- 自动生成封面和卡片
- 智能内容分页
- 多种样式循环使用
- 高质量图片输出

### 3. 批量发布（GUI）
- 图形界面操作
- 实时进度显示
- 支持暂停/继续/停止
- 自动间隔发布（10分钟）
- 不会超时，稳定运行

### 4. 进度监控
- 实时查看发布进度
- 已发布笔记列表
- 双击打开笔记链接
- 自动刷新（每5秒）

---

## 🎯 V6.6 新特性

### 新增功能
- ✅ 批量发布 GUI 工具
- ✅ 进度查看器 GUI 工具
- ✅ 环境测试工具
- ✅ 自动保存发布记录

### 问题修复
- ✅ 修复批处理文件编码问题
- ✅ 修复 Python 语法错误
- ✅ 修复批量发布超时问题
- ✅ 修复批处理文件闪退问题

### 改进
- ✅ 图形界面更直观
- ✅ 实时显示发布进度
- ✅ 支持暂停/继续操作
- ✅ 不会因运行时间长而超时

**详细说明**: 查看 [CHANGELOG_V6.6.md](CHANGELOG_V6.6.md)

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [使用指南.md](使用指南.md) | 完整使用指南 |
| [SKILL.md](SKILL.md) | 技能文档 |
| [快速使用指南.md](docs/快速使用指南.md) | 快速上手 |
| [GUI工具使用说明.md](docs/GUI工具使用说明.md) | GUI 工具详解 |
| [Cookie获取指南.md](docs/Cookie获取指南.md) | Cookie 获取方法 |
| [常见问题解答.md](docs/常见问题解答.md) | FAQ |
| [CHANGELOG_V6.6.md](CHANGELOG_V6.6.md) | 版本更新说明 |

---

## 🛠️ 环境要求

### 必需
- Windows 操作系统
- Python 3.14
- 依赖库：xhs, python-dotenv

### 安装依赖
```bash
# 方法1：使用环境测试工具（推荐）
双击运行: test_environment.bat

# 方法2：手动安装
C:\Python314\python.exe -m pip install xhs python-dotenv
```

---

## ⚙️ 配置

### Cookie 配置（必需）

创建 `.env` 文件：
```
XHS_COOKIE=你的完整Cookie字符串
```

**获取方法**: 查看 [Cookie获取指南.md](docs/Cookie获取指南.md)

### 发布参数配置（可选）

编辑 `start_publish.bat`：
```batch
--start-from 1        # 从第几篇开始
--wait-minutes 10     # 发布间隔（分钟）
```

---

## 💻 使用方法

### 批量发布
```
1. 双击运行: start_publish.bat
2. 点击"开始发布"按钮
3. 等待任务完成
```

### 查看进度
```
1. 双击运行: view_progress.bat
2. 查看已发布笔记列表
3. 双击笔记打开链接
```

### 测试环境
```
1. 双击运行: test_environment.bat
2. 查看测试结果
3. 自动安装缺失依赖
```

---

## 📊 工作流程

```
创作内容 → 渲染图片 → 配置Cookie → 批量发布 → 查看进度
   ↓           ↓           ↓            ↓           ↓
Markdown    PNG图片     .env文件    GUI工具    进度查看器
```

### 完整流程

1. **创作笔记内容**
   - 撰写小红书风格内容
   - 生成 Markdown 文件

2. **渲染图片卡片**
   ```bash
   python scripts/render_xhs_v2.py note.md -o output --style purple
   ```

3. **配置 Cookie**
   - 获取小红书 Cookie
   - 创建 `.env` 文件

4. **批量发布**
   - 运行 `start_publish.bat`
   - 点击"开始发布"

5. **查看进度**
   - 运行 `view_progress.bat`
   - 查看发布结果

---

## ⚠️ 注意事项

1. **Cookie 管理**
   - Cookie 会过期，需定期更新
   - 不要分享 Cookie 给他人

2. **发布规则**
   - 默认间隔：10分钟/篇
   - 避免频繁发布被限流

3. **窗口管理**
   - 发布时不要关闭窗口
   - 可以最小化

4. **网络要求**
   - 确保网络稳定
   - 上传图片需要时间

---

## 🐛 故障排查

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| 双击后没反应 | 运行 `test_environment.bat` 检查环境 |
| 提示"未找到 Cookie" | 检查 `.env` 文件是否存在 |
| 发布失败 | 检查 Cookie 是否失效 |
| 进度查看器无数据 | 等待第一篇笔记发布完成 |

**详细解答**: 查看 [常见问题解答.md](docs/常见问题解答.md)

---

## 📈 版本历史

### V6.6 (2026-01-27) - 当前版本
- ✅ 新增批量发布 GUI 工具
- ✅ 新增进度查看器 GUI 工具
- ✅ 修复批处理文件问题
- ✅ 修复超时问题

### V6.5 (2026-01-27)
- ✅ 支持批量创作多篇笔记
- ✅ 图片样式自动循环
- ✅ 发布间隔机制

**完整历史**: 查看 [CHANGELOG_V6.6.md](CHANGELOG_V6.6.md)

---

## 🤝 贡献

欢迎提交问题和建议！

---

## 📞 获取帮助

- 📖 查看 [使用指南.md](使用指南.md)
- ❓ 查看 [常见问题解答.md](docs/常见问题解答.md)
- 📝 查看 [SKILL.md](SKILL.md)

---

## 📄 许可证

MIT License

---

## 🎉 开始使用

```
1. 运行 test_environment.bat 测试环境
2. 配置 .env 文件（Cookie）
3. 运行 start_publish.bat 开始发布
```

**祝你使用愉快！** 🚀

---

**版本**: V6.6  
**更新日期**: 2026-01-27  
**维护者**: StepFun AI Team
