# 小红书 Cookie 获取详细指南

## 问题说明

当前 `.env` 文件中的 Cookie 格式不正确。Cookie 只有 52 个字符，但完整的小红书 Cookie 应该包含多个键值对，通常有几百到上千个字符。

**当前 Cookie（不正确）：**
```
19a10437e01eyo1c5fcngw9lk3n89ybf5cwu2pwzo50000236914
```

**正确的 Cookie 格式示例：**
```
a1=xxx; webId=xxx; web_session=xxx; xsecappid=xxx; acw_tc=xxx; ...
```

## 正确获取 Cookie 的步骤

### 步骤 1：打开浏览器并登录

1. 打开 **Chrome** 或 **Edge** 浏览器
2. 访问小红书创作者中心：
   ```
   https://creator.xiaohongshu.com
   ```
3. 使用小红书 APP 扫码登录

### 步骤 2：打开开发者工具

登录成功后，按 **F12** 键打开开发者工具（或右键点击页面 → 检查）

### 步骤 3：切换到 Network 标签

在开发者工具中，点击顶部的 **Network**（网络）标签

### 步骤 4：刷新页面

按 **F5** 或点击浏览器的刷新按钮，刷新页面

### 步骤 5：找到请求

在 Network 标签中，你会看到很多网络请求。找到任意一个发送到 `xiaohongshu.com` 的请求，例如：
- `creator.xiaohongshu.com` 开头的请求
- `edith.xiaohongshu.com` 开头的请求

点击这个请求

### 步骤 6：查看请求头

在右侧面板中：
1. 点击 **Headers**（请求头）标签
2. 向下滚动找到 **Request Headers**（请求标头）部分
3. 找到 **Cookie:** 这一行

### 步骤 7：复制完整的 Cookie

**重要**：必须复制 **整个** Cookie 字符串，包括所有的键值对。

Cookie 看起来像这样（很长的一串）：
```
a1=19bff173bf6elsavheaotccd1rd7ubi60ci4u85e650000393850; webId=06d5b08b2580e43cdcc2d0c03304067f; web_session=040069b43c8e6e2c1234567890abcdef; xsecappid=ugc; acw_tc=0a0d0eb817695112720681265e2eb9ff0564a02a04820a29bd2b025afe5bde; ...（还有更多）
```

**复制方法：**
- 方法1：点击 Cookie 值，会自动全选，然后 Ctrl+C 复制
- 方法2：右键点击 Cookie 值 → Copy value（复制值）

### 步骤 8：更新 .env 文件

1. 打开文件：`D:\20260127XHS\Auto-Redbook-Skills-main\.env`
2. 找到 `XHS_COOKIE=` 这一行
3. 将等号后面的内容替换为刚才复制的完整 Cookie
4. 保存文件

**更新后的 .env 文件应该看起来像这样：**
```
# 小红书Cookie配置
# 更新时间: 2026-01-27 19:30:00
XHS_COOKIE=a1=19bff173bf6elsavheaotccd1rd7ubi60ci4u85e650000393850; webId=06d5b08b2580e43cdcc2d0c03304067f; web_session=040069b43c8e6e2c1234567890abcdef; xsecappid=ugc; acw_tc=0a0d0eb817695112720681265e2eb9ff0564a02a04820a29bd2b025afe5bde; ...（很长的一串）
```

## 验证 Cookie

更新 Cookie 后，运行验证脚本检查是否正确：

```powershell
cd "D:\20260127XHS\Auto-Redbook-Skills-main"
C:\Python314\python.exe scripts/validate_cookie.py
```

如果看到以下输出，说明 Cookie 有效：
```
[SUCCESS] Cookie is valid!
  Nickname: 你的昵称
  User ID: 你的用户ID
```

## 常见问题

### Q1: 找不到 Cookie 在哪里？
**A:** 确保你在 Network 标签中点击了一个请求，然后在右侧的 Headers 标签中向下滚动，Cookie 通常在 Request Headers 部分的底部。

### Q2: Cookie 太长了，复制不完整？
**A:** 不要手动选择，直接点击 Cookie 值会自动全选，或者右键选择 "Copy value"。

### Q3: 复制后发现 Cookie 还是很短？
**A:** 可能复制错了位置。确保复制的是 **Request Headers** 中的 Cookie，不是 Response Headers。

### Q4: Cookie 多久会失效？
**A:** 小红书的 Cookie 通常在几小时到几天后失效，失效后需要重新获取。

## 截图示例位置

```
开发者工具 (F12)
├── Network (网络) 标签  ← 点击这里
│   ├── 请求列表
│   │   └── creator.xiaohongshu.com  ← 点击任意请求
│   └── 右侧面板
│       ├── Headers (请求头) 标签  ← 点击这里
│       └── Request Headers (请求标头)
│           └── Cookie: ...  ← 复制这里的完整值
```

## 下一步

Cookie 更新并验证成功后，就可以运行批量发布脚本了：

```powershell
cd "D:\20260127XHS\Auto-Redbook-Skills-main"
C:\Python314\python.exe scripts/batch_publish_xhs.py "D:\jieyue_work\drivingschool_notes"
```
