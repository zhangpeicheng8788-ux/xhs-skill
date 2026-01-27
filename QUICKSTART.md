# 🚀 快速开始指南

## 5分钟上手小红书笔记自动化

### 第一步：安装依赖（2分钟）

**Python 版本（推荐）：**
```bash
# 安装 Python 依赖
pip install markdown pyyaml playwright python-dotenv xhs

# 安装浏览器
playwright install chromium
```

**Node.js 版本：**
```bash
# 进入项目目录
cd Auto-Redbook-Skills

# 安装 Node.js 依赖
npm install

# 安装浏览器
npx playwright install chromium
```

---

### 第二步：扫码登录（1分钟）

**Python 版本：**
```bash
python scripts/login_xhs.py
```

**Node.js 版本：**
```bash
node scripts/login_xhs.js
```

**操作步骤：**
1. 运行命令后，会自动弹出浏览器窗口
2. 使用小红书 APP 扫描二维码
3. 登录成功后，Cookie 自动保存
4. 浏览器窗口自动关闭

✅ **完成！** 现在可以开始创作和发布了。

---

### 第三步：创作笔记（1分钟）

创建一个 Markdown 文件，例如 `my_note.md`：

```markdown
---
emoji: "🎉"
title: "我的第一篇笔记"
subtitle: "超级简单的教程"
---

# 第一部分 📝

这是我的第一篇小红书笔记内容。

**重点内容：**
- 要点一
- 要点二
- 要点三

---

# 第二部分 ✨

继续添加更多内容...

> 可以使用引用块

---

# 总结 🎯

记得添加标签哦！

#小红书 #笔记 #教程
```

---

### 第四步：渲染图片（30秒）

**使用默认样式：**
```bash
python scripts/render_xhs_v2.py my_note.md
```

**使用指定样式：**
```bash
# 小红书红色主题
python scripts/render_xhs_v2.py my_note.md --style xiaohongshu

# 清新薄荷主题
python scripts/render_xhs_v2.py my_note.md --style mint

# 暗黑模式
python scripts/render_xhs_v2.py my_note.md --style dark
```

**查看所有样式：**
```bash
python scripts/render_xhs_v2.py --list-styles
```

生成的图片会保存在当前目录：
- `cover.png` - 封面
- `card_1.png`, `card_2.png`, ... - 内容卡片

---

### 第五步：发布笔记（30秒）

```bash
python scripts/publish_xhs.py \
  --title "我的第一篇笔记" \
  --desc "这是我用自动化工具创作的第一篇笔记" \
  --images cover.png card_1.png card_2.png
```

**可选参数：**
```bash
# 发布为私密笔记（先测试）
python scripts/publish_xhs.py \
  --title "测试笔记" \
  --desc "测试内容" \
  --images cover.png card_1.png \
  --private

# 定时发布
python scripts/publish_xhs.py \
  --title "定时笔记" \
  --desc "明天早上发布" \
  --images cover.png card_1.png \
  --post-time "2024-02-01 09:00:00"

# 验证模式（不实际发布）
python scripts/publish_xhs.py \
  --title "验证测试" \
  --desc "仅验证" \
  --images cover.png card_1.png \
  --dry-run
```

---

## 🎨 样式选择指南

| 样式 | 适用场景 | 命令 |
|------|---------|------|
| `purple` | 科技、创意、通用 | `--style purple` |
| `xiaohongshu` | 时尚、美妆、生活 | `--style xiaohongshu` |
| `mint` | 健康、自然、环保 | `--style mint` |
| `sunset` | 浪漫、温暖、情感 | `--style sunset` |
| `ocean` | 清新、专业、商务 | `--style ocean` |
| `elegant` | 简约、高级、正式 | `--style elegant` |
| `dark` | 科技、编程、夜间 | `--style dark` |

详细说明请查看 [STYLES.md](./STYLES.md)

---

## 📋 完整工作流示例

### 示例 1：发布一篇产品推荐

```bash
# 1. 创建 Markdown 文件
cat > product_review.md << 'EOF'
---
emoji: "⭐"
title: "5款必买好物推荐"
subtitle: "闭眼入不踩雷"
---

# 好物一：智能手表 ⌚

功能强大，性价比超高！

**推荐理由：**
- 续航持久
- 功能丰富
- 颜值在线

---

# 好物二：蓝牙耳机 🎧

音质出色，佩戴舒适。

---

# 总结 🎯

这些好物都是我亲测好用的！

#好物推荐 #种草 #必买清单
EOF

# 2. 渲染图片（使用小红书红色主题）
python scripts/render_xhs_v2.py product_review.md --style xiaohongshu

# 3. 发布笔记
python scripts/publish_xhs.py \
  --title "5款必买好物推荐⭐" \
  --desc "闭眼入不踩雷！每一款都是我亲测好用的，快来看看有没有你需要的～" \
  --images cover.png card_1.png card_2.png card_3.png
```

### 示例 2：发布一篇教程

```bash
# 1. 创建教程 Markdown
cat > tutorial.md << 'EOF'
---
emoji: "📚"
title: "新手必看教程"
subtitle: "3分钟快速上手"
---

# 第一步：准备工作 🛠️

列出需要的工具和材料。

---

# 第二步：开始操作 ⚡

详细的操作步骤...

---

# 第三步：注意事项 ⚠️

重要提示和常见问题。

#教程 #新手必看 #干货分享
EOF

# 2. 渲染（使用优雅白主题）
python scripts/render_xhs_v2.py tutorial.md --style elegant

# 3. 发布
python scripts/publish_xhs.py \
  --title "新手必看教程📚" \
  --desc "3分钟快速上手，超详细步骤，小白也能学会！" \
  --images cover.png card_1.png card_2.png card_3.png
```

---

## 🔧 常见问题

### Q1: 如何重新登录？

```bash
# 直接运行登录脚本
python scripts/login_xhs.py

# 脚本会自动检测现有 Cookie 并询问是否重新登录
```

### Q2: 如何更换样式？

```bash
# 重新渲染即可，指定新的样式
python scripts/render_xhs_v2.py my_note.md --style ocean
```

### Q3: 如何批量发布？

```bash
# 创建一个 Shell 脚本
cat > batch_publish.sh << 'EOF'
#!/bin/bash

# 渲染多个笔记
python scripts/render_xhs_v2.py note1.md --style xiaohongshu -o ./output1
python scripts/render_xhs_v2.py note2.md --style mint -o ./output2

# 发布笔记（添加延迟避免频繁操作）
python scripts/publish_xhs.py --title "笔记1" --desc "内容1" --images ./output1/*.png
sleep 60  # 等待1分钟

python scripts/publish_xhs.py --title "笔记2" --desc "内容2" --images ./output2/*.png
EOF

chmod +x batch_publish.sh
./batch_publish.sh
```

### Q4: Cookie 失效怎么办？

登录脚本会自动检测，失效时会提示：
```
⚠️ 现有 Cookie 已失效
```
重新运行 `python scripts/login_xhs.py` 即可。

---

## 💡 进阶技巧

### 技巧 1：使用环境变量

```bash
# 设置默认样式
export XHS_DEFAULT_STYLE=xiaohongshu

# 设置默认输出目录
export XHS_OUTPUT_DIR=./output
```

### 技巧 2：自定义封面

修改 Markdown 文件的 YAML 头部：
```yaml
---
emoji: "🎨"           # 更换 emoji
title: "自定义标题"    # 修改标题
subtitle: "副标题"     # 修改副标题
---
```

### 技巧 3：内容分页控制

使用 `---` 分隔符控制分页：
```markdown
# 第一页内容

这里是第一页的内容...

---

# 第二页内容

这里是第二页的内容...
```

---

## 📞 获取帮助

- 查看完整文档：[README.md](./README.md)
- 样式选择指南：[STYLES.md](./STYLES.md)
- 登录详细说明：[LOGIN_GUIDE.md](./LOGIN_GUIDE.md)
- 技能使用说明：[SKILL.md](./SKILL.md)

---

**祝你创作愉快！** 🎉
