# 🚀 部署指南

本文档将指导你完成从GitHub到Streamlit Community Cloud的完整部署流程。

## 📋 前置准备

在开始部署前，请确保：

- ✅ 已有GitHub账号（如无，请访问 https://github.com 注册）
- ✅ 已有OpenAI API密钥
- ✅ 本地代码已完成Git初始化和提交（已完成✓）

## 步骤一：创建GitHub仓库并推送代码

### 1. 创建GitHub仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `tcm-assistant` 或 `medical` （你可以自定义）
   - **Description**: "中医智能小助手 - AI驱动的中医养生建议应用"
   - **Public/Private**: 选择 Public（公开仓库）
   - ⚠️ **不要勾选** "Initialize this repository with a README" （我们已经有了）
3. 点击 "Create repository"

### 2. 推送代码到GitHub

创建完仓库后，GitHub会显示推送代码的命令。在项目目录执行：

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/tcm-assistant.git

# 推送代码
git branch -M main
git push -u origin main
```

**示例**：
```bash
git remote add origin https://github.com/zhangsan/tcm-assistant.git
git branch -M main
git push -u origin main
```

执行后，刷新GitHub页面，你应该能看到所有项目文件。

## 步骤二：部署到Streamlit Community Cloud

### 1. 访问Streamlit Cloud

访问：https://share.streamlit.io

### 2. 登录账号

- 点击右上角 "Sign in"
- 选择 "Continue with GitHub"
- 授权Streamlit访问你的GitHub仓库

### 3. 创建新应用

1. 点击 "New app" 按钮
2. 填写部署信息：

   **Repository**:
   - 选择你刚创建的仓库（如 `YOUR_USERNAME/tcm-assistant`）

   **Branch**:
   - 选择 `main`

   **Main file path**:
   - 填写 `app.py`

   **App URL (可选)**:
   - 自定义应用URL，如 `tcm-assistant`
   - 最终URL将是：`https://tcm-assistant.streamlit.app`

3. 点击 "Advanced settings" （高级设置）

### 4. 配置Secrets（重要！）

在 Advanced settings 中，找到 "Secrets" 部分，添加以下内容：

```toml
OPENAI_API_KEY = "sk-proj-你的完整API密钥"
```

**注意**：
- 直接粘贴你的OpenAI API密钥
- 保持TOML格式（键值对用 = 连接，字符串用双引号）
- 不要分享这个密钥给他人

### 5. 开始部署

1. 确认所有设置正确
2. 点击 "Deploy!" 按钮
3. 等待部署完成（通常1-3分钟）

### 6. 部署状态监控

部署过程中，你会看到：

- 🟡 **Building** - 正在构建环境和安装依赖
- 🟢 **Running** - 应用正在运行
- 🔴 **Error** - 部署出错（查看日志排查）

## 步骤三：验证部署

### 1. 访问应用

部署成功后，点击应用URL访问你的应用。

### 2. 测试功能

测试基本功能：
1. 输入症状描述
2. 填写补充信息
3. 点击"开始分析"
4. 查看AI生成的养生建议

### 3. 检查日志

如果遇到问题：
- 点击应用管理界面的 "Manage app"
- 查看 "Logs" 标签
- 检查错误信息

## 常见问题排查

### ❌ 问题1：API密钥错误

**错误信息**：
```
ValueError: 未找到OPENAI_API_KEY
```

**解决方法**：
1. 进入应用设置
2. 检查 Secrets 配置
3. 确保格式正确：`OPENAI_API_KEY = "your-key"`
4. 点击 "Save" 并重启应用

### ❌ 问题2：依赖安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决方法**：
1. 检查 `requirements.txt` 格式
2. 确保版本号正确
3. 可以去掉版本限制，如 `streamlit` 而不是 `streamlit>=1.28.0`

### ❌ 问题3：应用启动超时

**可能原因**：
- 依赖包太多或太大
- OpenAI API调用超时

**解决方法**：
1. 检查网络连接
2. 查看日志获取详细错误
3. 尝试重新部署

## 部署后的管理

### 更新应用

修改代码后推送到GitHub：
```bash
git add .
git commit -m "更新说明"
git push
```

Streamlit Cloud会自动检测并重新部署（1-2分钟）。

### 查看分析数据

在Streamlit Cloud控制台：
- 查看应用访问量
- 监控资源使用
- 查看错误日志

### 暂停/删除应用

在应用管理页面：
- **Pause app** - 暂停应用（节省资源）
- **Delete app** - 删除应用

## 🎉 完成部署检查清单

- [ ] GitHub仓库已创建
- [ ] 代码已推送到GitHub
- [ ] Streamlit Cloud账号已创建
- [ ] 应用已成功部署
- [ ] Secrets已正确配置
- [ ] 应用可以正常访问
- [ ] 核心功能测试通过
- [ ] 获得公开访问URL

## 📝 后续步骤

1. **更新README**：
   - 将部署URL添加到README.md中
   - 更新作者信息和联系方式

2. **分享应用**：
   - 将URL分享给朋友测试
   - 收集反馈持续改进

3. **持续优化**：
   - 根据使用情况优化Prompt
   - 改进UI/UX
   - 添加新功能

## 🆘 需要帮助？

如果在部署过程中遇到问题：

1. **查看官方文档**：
   - Streamlit Cloud文档：https://docs.streamlit.io/streamlit-community-cloud

2. **社区支持**：
   - Streamlit论坛：https://discuss.streamlit.io

3. **检查日志**：
   - 应用管理界面 → Logs 标签

---

**祝你部署顺利！🚀**