# 小红书扫码登录功能使用指南

## 🆕 新功能说明

为了简化小红书笔记发布流程，我们新增了**扫码登录**功能，无需手动复制 Cookie，一键完成登录配置。

## ✨ 功能特点

- 🔐 **自动弹窗登录**：运行脚本后自动打开小红书登录页面
- 📱 **扫码即登录**：使用小红书 APP 扫码，安全便捷
- 💾 **自动保存 Cookie**：登录成功后自动保存到 `.env` 文件
- 🔄 **智能检测**：自动检测 Cookie 是否有效，失效时提示重新登录
- ⏰ **记录时间**：记录 Cookie 更新时间，方便管理

## 📦 依赖安装

### Python 版本

```bash
# 安装依赖
pip install playwright python-dotenv

# 安装浏览器
playwright install chromium
```

### Node.js 版本

```bash
# 安装依赖
npm install playwright dotenv

# 安装浏览器
npx playwright install chromium
```

## 🚀 快速开始

### 第一步：扫码登录

**Python 版本：**
```bash
python scripts/login_xhs.py
```

**Node.js 版本：**
```bash
node scripts/login_xhs.js
```

运行后会：
1. 自动打开浏览器窗口
2. 显示小红书登录页面
3. 使用小红书 APP 扫描二维码
4. 登录成功后自动保存 Cookie

### 第二步：发布笔记

登录完成后，就可以使用发布脚本了：

```bash
python scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述内容" \
  --images cover.png card_1.png card_2.png
```

## 📝 使用示例

### 示例 1：基本使用

```bash
# 1. 首次登录
python scripts/login_xhs.py

# 2. 发布笔记
python scripts/publish_xhs.py \
  --title "春节学车3280元" \
  --desc "德安驾校春节特惠，立省1000元！" \
  --images cover.png card_1.png card_2.png card_3.png
```

### 示例 2：重新登录

如果 Cookie 失效，重新运行登录脚本即可：

```bash
python scripts/login_xhs.py
```

脚本会自动检测现有 Cookie 是否有效：
- ✅ 如果有效，会提示是否要重新登录
- ❌ 如果失效，会直接进入登录流程

### 示例 3：发布私密笔记

```bash
python scripts/publish_xhs.py \
  --title "测试笔记" \
  --desc "这是一条测试笔记" \
  --images cover.png card_1.png \
  --private
```

### 示例 4：定时发布

```bash
python scripts/publish_xhs.py \
  --title "定时发布测试" \
  --desc "这条笔记将在指定时间发布" \
  --images cover.png card_1.png \
  --post-time "2024-02-01 10:00:00"
```

### 示例 5：验证模式（不实际发布）

```bash
python scripts/publish_xhs.py \
  --title "验证测试" \
  --desc "仅验证，不会实际发布" \
  --images cover.png card_1.png \
  --dry-run
```

## 🔧 高级功能

### 检查 Cookie 状态

登录脚本会自动检测 Cookie 是否有效：

```bash
python scripts/login_xhs.py
```

输出示例：
```
🔍 检测到现有 Cookie，正在验证...
✅ 现有 Cookie 有效
✨ 您已经登录，Cookie 仍然有效
```

### 查看 Cookie 信息

Cookie 保存在项目根目录的 `.env` 文件中：

```bash
# 查看 .env 文件内容
cat .env
```

文件内容示例：
```
XHS_COOKIE=web_session=xxx; a1=xxx; webId=xxx; ...
# Cookie 更新时间: 2024-01-27 15:30:00
```

### 手动删除 Cookie

如需重新登录，可以删除 `.env` 文件：

```bash
# Windows
del .env

# macOS/Linux
rm .env
```

然后重新运行登录脚本。

## ⚠️ 注意事项

1. **Cookie 有效期**
   - Cookie 有过期时间，通常为几天到几周
   - 失效后需要重新扫码登录
   - 登录脚本会自动检测并提示

2. **安全性**
   - `.env` 文件包含敏感信息，不要分享给他人
   - 建议将 `.env` 添加到 `.gitignore`，避免提交到代码仓库
   - 定期更新 Cookie，提高安全性

3. **浏览器窗口**
   - 登录时会弹出浏览器窗口，请不要关闭
   - 扫码完成后，窗口会自动关闭
   - 如果窗口无响应，可以关闭后重新运行

4. **网络要求**
   - 需要稳定的网络连接
   - 确保能够访问小红书网站
   - 扫码时手机和电脑需要联网

5. **多账号管理**
   - 一个 `.env` 文件只能保存一个账号的 Cookie
   - 如需切换账号，重新运行登录脚本即可
   - 旧 Cookie 会被新 Cookie 覆盖

## 🐛 常见问题

### Q1: 登录超时怎么办？

**A:** 默认等待时间为 2 分钟，如果超时：
1. 检查网络连接
2. 重新运行登录脚本
3. 确保及时扫码

### Q2: Cookie 验证失败怎么办？

**A:** 可能的原因：
1. Cookie 已过期 → 重新登录
2. 网络问题 → 检查网络连接
3. 小红书更新 → 更新脚本

### Q3: 发布失败怎么办？

**A:** 检查以下几点：
1. Cookie 是否有效 → 运行 `login_xhs.py` 验证
2. 图片文件是否存在 → 检查文件路径
3. 标题是否超过 20 字 → 缩短标题
4. 网络是否正常 → 检查网络连接

### Q4: 如何切换账号？

**A:** 重新运行登录脚本：
```bash
python scripts/login_xhs.py
```
选择 "y" 重新登录，新 Cookie 会覆盖旧 Cookie。

### Q5: 支持哪些浏览器？

**A:** 脚本使用 Playwright，自动下载 Chromium 浏览器，无需手动安装。

## 📞 技术支持

如遇到问题，请检查：
1. 依赖是否正确安装
2. 浏览器是否正确安装
3. 网络连接是否正常
4. Python/Node.js 版本是否符合要求

## 🔄 更新日志

### v2.0 (2024-01-27)
- 🆕 新增扫码登录功能
- 🆕 自动保存和管理 Cookie
- 🆕 智能检测 Cookie 有效性
- 🆕 支持 Python 和 Node.js 双版本
- ✨ 优化用户体验
- ✨ 添加详细的日志输出

### v1.0
- ✅ 基础渲染功能
- ✅ 手动配置 Cookie 发布

## 📄 许可证

MIT License

---

**享受更便捷的小红书笔记发布体验！** 🎉
