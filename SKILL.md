---
name: Auto-Redbook
description: 小红书笔记素材创作技能。当用户需要创建小红书笔记素材时使用这个技能。技能包含：根据用户的需求和提供的资料，撰写小红书笔记内容（标题+正文），生成图片卡片（封面+正文卡片，支持多种样式主题）。
---

# 小红书笔记创作技能

这个技能用于创建专业的小红书笔记素材，包括内容撰写、图片卡片生成（支持7种样式主题）和智能分页渲染。

## 使用场景

- 用户需要创建小红书笔记时
- 用户提供资料需要转化为小红书风格内容时
- 用户需要生成精美的图片卡片用于发布时
- 用户需要多种风格样式选择时

## 工作流程

### 第一步：撰写小红书笔记内容

根据用户需求和提供的资料，创作符合小红书风格的内容：

#### 标题要求
- 不超过 20 字
- 吸引眼球，制造好奇心
- 可使用数字、疑问句、感叹号增强吸引力
- 示例：「5个让效率翻倍的神器推荐！」「震惊！原来这样做才对」

#### 正文要求
- 使用良好的排版，段落清晰
- 点缀少量 Emoji 增加可读性（每段 1-2 个即可）
- 使用简短的句子和段落
- 结尾给出 SEO 友好的 Tags 标签（5-10 个相关标签）

### 第二步：生成 Markdown 文档

**注意：这里生成的 Markdown 文档是用于渲染卡片的，必须专门生成，禁止直接使用上一步的笔记正文内容。**

Markdown 文件，文件应包含：

1. YAML 头部元数据（封面信息）：
```yaml
---
emoji: "🚀"           # 封面装饰 Emoji
title: "大标题"        # 封面大标题（不超过15字）
subtitle: "副标题文案"  # 封面副标题（不超过15字）
---
```

2. 用于渲染卡片的 Markdown 文本内容：
   - 使用 `---` 分割线将正文分隔为多个卡片段落
   - 每个分段的文字控制在 200 字左右
   - 脚本会自动检测内容高度并智能分页

完整示例：
```markdown
---
emoji: "💡"
title: "5个效率神器让工作效率翻倍"
subtitle: "对着抄作业就好了，一起变高效"
---

# 神器一：Notion 📝

> 全能型笔记工具，支持数据库、看板、日历等多种视图...

## 特色功能

- 特色一
- 特色二

---

# 神器二：Raycast ⚡

可使用代码块来增加渲染后图片的视觉丰富度

## 推荐原因

- 原因一
- 原因二
- ……

---

# 神器三：Arc 🌈

全新理念的浏览器，侧边栏标签管理...

...

#效率工具 #生产力 #Mac软件
```

### 第三步：渲染图片卡片

将 Markdown 文档渲染为图片卡片。**推荐使用 V2 版本脚本**，支持智能分页和多种样式。

#### V2 渲染脚本（推荐）

V2 版本新增特性：
- ✅ **智能分页**：自动检测内容高度，超出时自动拆分到多张卡片
- ✅ **多种样式**：支持 7 种预设样式主题
- ✅ **字数预估**：基于字数预分配内容，减少渲染次数

**Python 版本：**

```bash
# 基本用法
python scripts/render_xhs_v2.py <markdown_file>

# 指定输出目录
python scripts/render_xhs_v2.py <markdown_file> -o <output_directory>

# 指定样式主题
python scripts/render_xhs_v2.py <markdown_file> --style xiaohongshu

# 查看所有可用样式
python scripts/render_xhs_v2.py --list-styles
```

**Node.js 版本：**

```bash
# 基本用法
node scripts/render_xhs_v2.js <markdown_file>

# 指定输出目录和样式
node scripts/render_xhs_v2.js <markdown_file> -o ./output --style mint

# 查看所有可用样式
node scripts/render_xhs_v2.js --list-styles
```

#### 可用样式主题

| 样式键 | 名称 | 描述 |
|--------|------|------|
| `purple` | 紫韵 | 默认样式，紫蓝色渐变 |
| `xiaohongshu` | 小红书红 | 小红书品牌色系 |
| `mint` | 清新薄荷 | 绿色/自然调 |
| `sunset` | 日落橙 | 粉色/日落渐变 |
| `ocean` | 深海蓝 | 蓝绿色海洋调 |
| `elegant` | 优雅白 | 简约灰白调 |
| `dark` | 暗黑模式 | 深色背景，高对比度 |

#### 旧版渲染脚本（保留）

如需使用旧版（不支持自动分页）：

```bash
# Python 版本
python scripts/render_xhs.py <markdown_file> [--output-dir <output_directory>]

# Node.js 版本
node scripts/render_xhs.js <markdown_file> [--output-dir <output_directory>]
```

**旧版已知问题**：单张卡片内容过多时可能出现文字溢出，需手动用 `---` 分隔。

### 第四步：发布小红书笔记（可选）

#### 4.1 首次使用：扫码登录

**推荐方式**：使用扫码登录脚本，自动保存 Cookie，无需手动配置。

**Python 版本：**
```bash
python scripts/login_xhs.py
```

**Node.js 版本：**
```bash
node scripts/login_xhs.js
```

**登录流程**：
1. 运行登录脚本，自动弹出小红书登录页面
2. 使用小红书 APP 扫描二维码登录
3. 登录成功后，Cookie 自动保存到 `.env` 文件
4. 下次发布时自动使用保存的 Cookie

**功能特点**：
- ✅ 自动检测现有 Cookie 是否有效
- ✅ Cookie 失效时提示重新登录
- ✅ 支持重新登录覆盖旧 Cookie
- ✅ 记录 Cookie 更新时间

#### 4.2 发布笔记

登录完成后，使用发布脚本将生成的图片发布到小红书：

**Python 版本：**
```bash
python scripts/publish_xhs.py --title "笔记标题" --desc "笔记描述" --images cover.png card_1.png card_2.png
```

**Node.js 版本（如果有）：**
```bash
node scripts/publish_xhs.js --title "笔记标题" --desc "笔记描述" --images cover.png card_1.png card_2.png
```

**发布参数说明**：
- `--title` / `-t`: 笔记标题（不超过20字）
- `--desc` / `-d`: 笔记描述/正文内容
- `--images` / `-i`: 图片文件路径（可以多个，建议封面放第一张）
- `--private`: 设为私密笔记（可选）
- `--post-time`: 定时发布时间（可选，格式：2024-01-01 12:00:00）
- `--dry-run`: 仅验证，不实际发布（可选）

**示例**：
```bash
# 基本发布
python scripts/publish_xhs.py --title "春节学车3280元" --desc "德安驾校春节特惠" --images cover.png card_1.png card_2.png

# 私密笔记
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --private

# 定时发布
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --post-time "2024-02-01 10:00:00"

# 验证模式（不实际发布）
python scripts/publish_xhs.py --title "标题" --desc "描述" --images cover.png --dry-run
```

#### 4.3 手动配置 Cookie（备选方案）

如果扫码登录遇到问题，也可以手动配置 Cookie：

1. 在项目根目录创建 `.env` 文件
2. 添加以下内容：
```
XHS_COOKIE=your_cookie_string_here
```

3. Cookie 获取方式：
   - 在浏览器中登录小红书（https://creator.xiaohongshu.com）
   - 打开开发者工具（F12）
   - 在 Network 标签中查看请求头的 Cookie
   - 复制完整的 Cookie 字符串

## 图片规格说明

### 封面卡片
- 尺寸比例：3:4（小红书推荐比例）
- 基准尺寸：1080×1440px
- 包含：Emoji 装饰、大标题、副标题
- 样式：渐变背景 + 圆角内容区（根据所选主题变化）

### 正文卡片
- 尺寸比例：3:4
- 基准尺寸：1080×1440px
- 支持：标题、段落、列表、引用、代码块、图片
- 样式：白色卡片 + 渐变背景边框（根据所选主题变化）
- V2 版本：自动分页，单张卡片内容不会溢出

## 技能资源

### 脚本文件
- `scripts/render_xhs.py` - Python V1 渲染脚本（旧版）
- `scripts/render_xhs.js` - Node.js V1 渲染脚本（旧版）
- `scripts/render_xhs_v2.py` - Python V2 渲染脚本（推荐 ✅）
- `scripts/render_xhs_v2.js` - Node.js V2 渲染脚本（推荐 ✅）
- `scripts/login_xhs.py` - Python 扫码登录脚本（新增 🆕）
- `scripts/login_xhs.js` - Node.js 扫码登录脚本（新增 🆕）
- `scripts/publish_xhs.py` - 小红书发布脚本

### 资源文件
- `assets/cover.html` - 封面 HTML 模板（旧版）
- `assets/card.html` - 正文卡片 HTML 模板（旧版）
- `assets/styles.css` - 共用样式表（旧版）
- `assets/example.md` - 示例 Markdown 文件

## 注意事项

1. **V2 版本推荐**：V2 版本支持智能分页，可自动处理内容溢出问题
2. **样式选择**：根据内容风格选择合适的样式主题
3. **Markdown 位置**：Markdown 文件应保存在工作目录，渲染后的图片也保存在工作目录
4. **内容长度**：建议每个 `---` 分隔的内容块控制在 200 字以内
5. **扫码登录**：首次发布前需要运行 `login_xhs.py` 或 `login_xhs.js` 进行扫码登录
6. **Cookie 有效期**：Cookie 有过期限制，失效后登录脚本会自动提示重新登录
7. **发布依赖**：发布功能依赖 xhs 库（Python）或相应的 npm 包（Node.js）
   - Python: `pip install xhs python-dotenv`
   - Node.js: `npm install dotenv`

## 智能分页说明

V2 版本的智能分页机制：

1. **预估阶段**：基于字数、元素类型预估内容高度
2. **预渲染阶段**：使用 Playwright 预渲染并测量实际高度
3. **拆分阶段**：如果内容超出，按段落/行智能拆分内容
4. **固定输出**：每张卡片固定为 1080×1440px，确保一致性

这种机制确保无论内容多长，都不会出现文字溢出问题。
