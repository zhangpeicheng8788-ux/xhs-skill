# 📕 Auto-Redbook-Skills

> 一个自动撰写笔记、生成图片、自动发布小红书的 Skills

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🆕 v2.0 版本更新

### ✨ 新增功能

- **🔐 扫码登录** - 自动弹出浏览器窗口，扫码登录，无需手动复制 Cookie（新增 🆕）
- **💾 自动保存 Cookie** - 登录成功后自动保存，下次使用无需重新登录（新增 🆕）
- **🔄 智能检测** - 自动检测 Cookie 是否有效，失效时提示重新登录（新增 🆕）
- **🚀 智能分页渲染** - 自动检测内容高度，超出时自动拆分到多张卡片，彻底解决文字溢出问题
- **🎨 7种可选样式** - 新增多种主题风格，一键切换不同视觉效果
- **⚡ V2 渲染脚本** - 全新 `render_xhs_v2.py` / `render_xhs_v2.js`，推荐升级使用

### 📋 可用样式列表

| 样式 | 名称 | 预览 |
|------|------|------|
| `purple` | 紫韵（默认）| 蓝紫色渐变 |
| `xiaohongshu` | 小红书红 | 品牌红色系 |
| `mint` | 清新薄荷 | 绿色自然调 |
| `sunset` | 日落橙 | 粉橙浪漫调 |
| `ocean` | 深海蓝 | 海洋蓝色调 |
| `elegant` | 优雅白 | 灰白简约调 |
| `dark` | 暗黑模式 | 深色高对比 |

### 🎯 使用 V2 脚本

```bash
# Python 版本
python scripts/render_xhs_v2.py note.md --style sunset

# Node.js 版本
node scripts/render_xhs_v2.js note.md --style ocean

# 查看所有样式
python scripts/render_xhs_v2.py --list-styles
```

### 📁 v2.0 新增文件

```
scripts/
├── render_xhs_v2.py    # 新增：Python 智能分页版（推荐）
├── render_xhs_v2.js    # 新增：Node.js 智能分页版（推荐）
├── login_xhs.py        # 新增：Python 扫码登录脚本 🆕
├── login_xhs.js        # 新增：Node.js 扫码登录脚本 🆕
├── render_xhs.py       # 旧版：保留兼容
├── render_xhs.js       # 旧版：保留兼容
└── publish_xhs.py      # 发布脚本（已优化）
STYLES.md               # 新增：样式选择指南
LOGIN_GUIDE.md          # 新增：扫码登录使用指南 🆕
```

**注：V1 旧版脚本保留兼容，V2 版本完全向下兼容 Markdown 格式。**

---

## ✨ 功能特性

- 📝 **撰写笔记** - 根据既定主题，撰写小红书笔记（提示词自己调整，在 `SKILL.md`里）
- 🎨 **生成卡片** - 根据内容自动渲染生成图片，包含 cover 和内容详情，支持 Markdown 渲染
- 🐍 **双语言脚本** - 提供 Python 和 Node.js 两种渲染方案
- 📤 **一键发布** - 支持直接发布到小红书（需配置 Cookie）


## 🚀 快速开始

### Clone 项目

Clone 项目到本地

```bash

git clone https://github.com/comeonzhj/Auto-Redbook-Skills.git					 

```

移动到支持 Skills 的客户端对应文件夹里：

- For Claude ： `~/.claude/skills/`
- For Alma： `~/.config/Alma/skills/`
- For TRAE： `/your-path/.trae/skills/`

### 安装依赖

**Python 版本：**

```bash
pip install markdown pyyaml playwright python-dotenv xhs
playwright install chromium
```

**Node.js 版本：**

```bash
cd Auto-Redbook-Skills
npm install
npx playwright install chromium
```

## 🎨 渲染图片

### V2 渲染（推荐）

```bash
# 使用默认样式
python scripts/render_xhs_v2.py note.md

# 指定样式主题
python scripts/render_xhs_v2.py note.md --style sunset

# 指定输出目录
python scripts/render_xhs_v2.py note.md -o ./output --style xiaohongshu

# 查看所有样式
python scripts/render_xhs_v2.py --list-styles
```

**V2 特性：**
- 智能分页：自动检测内容高度，自动拆分卡片
- 固定尺寸：所有卡片固定 1080×1440px
- 多种样式：7种预设主题风格

### V1 渲染（旧版）

```bash
# Python 版本
python scripts/render_xhs.py note.md

# Node.js 版本
node scripts/render_xhs.js note.md
```

**注意：** V1 版本当内容过长时可能出现溢出，建议手动使用 `---` 分隔内容。

## 📤 发布到小红书

### 方式一：扫码登录（推荐 🆕）

使用全新的扫码登录功能，无需手动复制 Cookie：

**Python 版本：**
```bash
# 1. 首次使用：扫码登录
python scripts/login_xhs.py

# 2. 发布笔记
python scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述内容" \
  --images cover.png card_1.png card_2.png
```

**Node.js 版本：**
```bash
# 1. 首次使用：扫码登录
node scripts/login_xhs.js

# 2. 发布笔记（使用 Python 发布脚本）
python scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述内容" \
  --images cover.png card_1.png card_2.png
```

**扫码登录特点：**
- ✅ 自动弹出浏览器窗口
- ✅ 扫码后自动保存 Cookie
- ✅ 智能检测 Cookie 有效性
- ✅ 失效时自动提示重新登录

详细使用说明请查看 [LOGIN_GUIDE.md](./LOGIN_GUIDE.md)

### 方式二：手动配置 Cookie（备选）

如果扫码登录遇到问题，也可以手动配置：

复制 `env.example.txt` 为 `.env`，填入小红书 Cookie：

```bash
cp env.example.txt .env
```

编辑 `.env` 文件：

```
XHS_COOKIE=your_cookie_string_here
```

**获取 Cookie 方法：**

1. 在浏览器中登录 [小红书创作者中心](https://creator.xiaohongshu.com)
2. 打开开发者工具（F12）
3. 在 Network 标签中查看任意请求的 Cookie 头
4. 复制完整的 cookie 字符串

### 发布参数说明

| 参数 | 说明 |
|------|------|
| `--private` | 设为私密笔记 |
| `--post-time "2024-01-01 12:00:00"` | 定时发布 |
| `--dry-run` | 仅验证，不实际发布 |

## 🎨 自定义样式

### 修改背景渐变（V1）

编辑 `assets/card.html` 中的 `.card-container`：

```css
.card-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**预设渐变色：**

| 名称 | 渐变值 |
|------|--------|
| 紫蓝 | `#667eea → #764ba2` |
| 粉红 | `#f093fb → #f5576c` |
| 青蓝 | `#4facfe → #00f2fe` |
| 绿色 | `#43e97b → #38f9d7` |
| 橙黄 | `#fa709a → #fee140` |

### 更多样式选择（V2）

V2 版本提供 7 种内置样式，通过 `--style` 参数快速切换：

```bash
python scripts/render_xhs_v2.py note.md --style dark   # 暗黑模式
python scripts/render_xhs_v2.py note.md --style mint   # 清新薄荷
```

详见 [STYLES.md](./STYLES.md)

## 📁 项目结构

```
md2Redbook/
├── SKILL.md              # 技能描述（AI Agent 使用）
├── README.md             # 项目文档
├── STYLES.md             # 样式选择指南
├── LOGIN_GUIDE.md        # 扫码登录使用指南 🆕
├── requirements.txt      # Python 依赖
├── package.json          # Node.js 依赖
├── env.example.txt       # Cookie 配置示例
├── .env                  # Cookie 配置文件（自动生成）
├── assets/
│   ├── cover.html        # 封面 HTML 模板
│   ├── card.html         # 正文卡片 HTML 模板
│   ├── styles.css        # 共用样式表
│   └── example.md        # 示例 Markdown
└── scripts/
    ├── render_xhs_v2.py  # Python 渲染脚本 V2（推荐）
    ├── render_xhs_v2.js  # Node.js 渲染脚本 V2（推荐）
    ├── render_xhs.py     # Python 渲染脚本 V1
    ├── render_xhs.js     # Node.js 渲染脚本 V1
    ├── login_xhs.py      # Python 扫码登录脚本 🆕
    ├── login_xhs.js      # Node.js 扫码登录脚本 🆕
    └── publish_xhs.py    # 小红书发布脚本
```


## ⚠️ 注意事项

1. **扫码登录** - 推荐使用 `login_xhs.py` 或 `login_xhs.js` 进行扫码登录，自动管理 Cookie
2. **Cookie 安全** - `.env` 文件包含登录凭证，请勿泄露或提交到版本控制（已添加到 .gitignore）
3. **Cookie 有效期** - Cookie 会过期，失效时登录脚本会自动提示重新登录
4. **发布频率** - 避免频繁发布，以免触发平台限制
5. **图片尺寸** - 渲染的图片为 1080×1440px，符合小红书推荐比例
6. **浏览器依赖** - 首次使用需要运行 `playwright install chromium` 安装浏览器

## 🙏 致谢

- [Playwright](https://playwright.dev/) - 浏览器自动化渲染
- [Marked](https://marked.js.org/) - Markdown 解析
- [Madopic](https://github.com/xiaolinbaba/Madopic) - Markdown 渲染  
- [xhs](https://github.com/ReaJason/xhs) - 小红书 API 客户端

## 📄 License

MIT License © 2026
