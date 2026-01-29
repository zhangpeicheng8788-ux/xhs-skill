# 更新日志 (CHANGELOG)

## [2.0.0] - 2024-01-27

### 🆕 新增功能

#### 扫码登录系统
- **Python 扫码登录脚本** (`scripts/login_xhs.py`)
  - 自动弹出浏览器窗口显示小红书登录页
  - 支持扫码登录，无需手动复制 Cookie
  - 自动保存 Cookie 到 `.env` 文件
  - 智能检测现有 Cookie 是否有效
  - 失效时自动提示重新登录
  - 记录 Cookie 更新时间

- **Node.js 扫码登录脚本** (`scripts/login_xhs.js`)
  - 与 Python 版本功能一致
  - 提供 Node.js 环境的完整支持
  - 交互式命令行界面

#### 智能分页渲染
- **V2 渲染脚本** (`render_xhs_v2.py` / `render_xhs_v2.js`)
  - 自动检测内容高度
  - 智能分页，避免内容溢出
  - 固定卡片尺寸（1080×1440px）
  - 基于字数预估，减少渲染次数

#### 多样式主题系统
- 新增 7 种预设样式主题：
  - `purple` - 紫韵（默认）
  - `xiaohongshu` - 小红书红
  - `mint` - 清新薄荷
  - `sunset` - 日落橙
  - `ocean` - 深海蓝
  - `elegant` - 优雅白
  - `dark` - 暗黑模式

- 通过 `--style` 参数快速切换
- 支持 `--list-styles` 查看所有样式

### 📝 文档更新

- **LOGIN_GUIDE.md** - 扫码登录详细使用指南
- **QUICKSTART.md** - 5分钟快速开始指南
- **STYLES.md** - 样式选择和预览指南
- **CHANGELOG.md** - 版本更新日志
- **.gitignore** - 保护敏感信息
- 更新 **README.md** - 添加新功能说明
- 更新 **SKILL.md** - 完善技能使用流程

### ✨ 优化改进

#### 发布脚本优化
- 优化 `publish_xhs.py` 与登录系统集成
- 自动从 `.env` 读取 Cookie
- 支持多种发布参数：
  - `--private` - 私密笔记
  - `--post-time` - 定时发布
  - `--dry-run` - 验证模式

#### 用户体验提升
- 更友好的命令行输出
- 详细的进度提示
- 彩色 emoji 标识
- 错误信息更清晰

#### 安全性增强
- Cookie 自动保存到 `.env`
- `.env` 添加到 `.gitignore`
- 记录 Cookie 更新时间
- 自动检测 Cookie 有效性

### 🔧 技术改进

- 使用 Playwright 实现浏览器自动化
- 支持 Python 和 Node.js 双版本
- 异步处理提升性能
- 更好的错误处理机制

### 📦 依赖更新

#### Python 依赖
- 新增 `playwright` - 浏览器自动化
- 新增 `python-dotenv` - 环境变量管理
- 保留 `markdown`, `pyyaml`, `xhs`

#### Node.js 依赖
- 新增 `playwright` - 浏览器自动化
- 新增 `dotenv` - 环境变量管理
- 保留 `marked`, `js-yaml`

### 🐛 Bug 修复

- 修复 V1 版本内容溢出问题（V2 版本）
- 修复 Cookie 过期未提示问题
- 优化图片渲染质量
- 修复部分样式显示异常

### ⚠️ 破坏性变更

无破坏性变更，完全向下兼容 V1 版本。

---

## [1.0.0] - 2024-01-15

### 初始版本

#### 核心功能
- Markdown 转小红书图片卡片
- 封面和内容卡片生成
- Python 和 Node.js 渲染脚本
- 基础发布功能

#### 支持特性
- 自定义封面（emoji、标题、副标题）
- Markdown 语法支持
- 代码块、引用、列表渲染
- 3:4 比例图片输出

#### 文档
- README.md - 基础文档
- SKILL.md - AI Agent 技能描述
- assets/example.md - 示例文件

---

## 版本规划

### [2.1.0] - 计划中

#### 计划功能
- [ ] Node.js 发布脚本
- [ ] 批量发布工具
- [ ] 模板库系统
- [ ] 自定义样式编辑器
- [ ] 图片水印功能
- [ ] 数据统计面板

#### 优化计划
- [ ] 渲染速度优化
- [ ] 更多样式主题
- [ ] 移动端适配
- [ ] 国际化支持

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Bug
- 描述问题现象
- 提供复现步骤
- 附上错误日志
- 说明运行环境

### 功能建议
- 描述功能需求
- 说明使用场景
- 提供参考案例

### 代码贡献
- Fork 项目
- 创建功能分支
- 提交 Pull Request
- 通过代码审查

---

## 致谢

感谢所有贡献者和用户的支持！

特别感谢：
- [Playwright](https://playwright.dev/) - 浏览器自动化
- [xhs](https://github.com/ReaJason/xhs) - 小红书 API
- [Marked](https://marked.js.org/) - Markdown 解析

---

**保持更新，关注最新版本！** 🚀
