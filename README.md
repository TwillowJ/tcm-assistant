# 🏥 中医智能小助手

一个基于人工智能的中医养生建议应用，用户可以输入身体不适症状，应用会从中医角度进行辨证分析，并提供个性化的养生建议。

## ✨ 功能特点

- 🤖 **AI驱动分析**：集成OpenAI GPT模型，提供专业的中医辨证分析
- 📊 **个性化建议**：根据用户的年龄、性别、症状持续时间等信息，提供定制化养生方案
- 💊 **全面的养生指导**：包括饮食调理、生活起居、运动养生、穴位按摩等多方面建议
- ⚡ **实时流式输出**：分析结果实时显示，提供流畅的用户体验
- 🔒 **隐私保护**：用户输入数据不会被永久存储

## 🚀 在线演示

**部署链接**：[即将添加部署后的URL]

## 📋 功能模块

### 1. 症状输入
- 详细的症状描述输入框
- 补充信息收集（年龄、性别、症状持续时间）

### 2. 中医辨证分析
- 从中医角度分析可能的证型（气虚、血虚、阴虚、阳虚等）
- 解释症状与证型的对应关系

### 3. 养生建议
- **饮食调理**：推荐食物、食疗方、饮食习惯
- **生活起居**：作息时间、睡眠改善、情绪调节
- **运动养生**：适合的运动类型、传统养生功法
- **其他调理**：穴位按摩、外治方法、季节养生

### 4. 注意事项
- 症状变化监测提醒
- 就医建议
- 预期调理周期

## 🛠️ 技术栈

- **前端框架**：[Streamlit](https://streamlit.io/) - 快速构建数据应用
- **AI模型**：[OpenAI GPT-4o-mini](https://openai.com/) - 大语言模型
- **编程语言**：Python 3.8+
- **依赖管理**：pip + requirements.txt
- **部署平台**：Streamlit Community Cloud

## 📦 项目结构

```
medical/
├── app.py                          # Streamlit主应用
├── llm_service.py                  # LLM调用服务模块
├── requirements.txt                # Python依赖
├── .env                           # 环境变量配置（本地）
├── .env.example                   # 环境变量示例
├── .gitignore                     # Git忽略配置
├── .streamlit/
│   ├── config.toml                # Streamlit配置
│   └── secrets.toml.example       # Secrets配置示例
└── README.md                      # 项目文档
```

## 🔧 本地开发

### 前置要求

- Python 3.8 或更高版本
- OpenAI API密钥

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/你的用户名/medical.git
cd medical
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

复制 `.env.example` 为 `.env`，并填入你的OpenAI API密钥：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. **运行应用**
```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

## 🌐 部署到Streamlit Cloud

### 部署步骤

1. **将代码推送到GitHub**
   - 确保代码已提交到GitHub仓库
   - 不要提交 `.env` 文件（已在.gitignore中）

2. **登录Streamlit Community Cloud**
   - 访问 [share.streamlit.io](https://share.streamlit.io)
   - 使用GitHub账号登录

3. **创建新应用**
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 主文件路径：`app.py`
   - 点击 "Deploy"

4. **配置Secrets**
   - 在应用设置中找到 "Secrets"
   - 添加以下内容：
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

5. **完成部署**
   - 等待1-2分钟，应用将自动部署
   - 获得公开访问链接

### 更新部署

修改代码后，只需推送到GitHub：
```bash
git add .
git commit -m "更新说明"
git push
```

Streamlit Cloud会自动检测变更并重新部署。

## 📝 使用说明

1. **访问应用**：打开应用链接
2. **输入症状**：在文本框中详细描述你的身体不适症状
3. **补充信息**：填写年龄、性别、症状持续时间等信息
4. **开始分析**：点击"开始分析"按钮
5. **查看建议**：等待AI分析完成，查看中医养生建议

### 示例输入

```
症状描述：
最近经常感到疲劳乏力，特别是下午时段更明显。晚上睡眠质量不好，
容易醒来。还有轻微的头晕，偶尔会出汗。胃口一般，有时会有腹胀感。

年龄：35岁
性别：女
症状持续时间：2-4周
```

## ⚠️ 免责声明

本应用提供的建议仅供参考，不能替代专业医疗诊断。

- 本应用基于AI模型生成建议，可能存在不准确之处
- 建议仅为养生保健参考，不涉及具体药物治疗
- 如有严重或持续性症状，请及时就医咨询专业医师
- 用户输入的信息仅用于生成建议，不会被永久存储

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 开发建议

- 优化Prompt设计以提高分析准确性
- 添加更多养生知识库
- 改进UI/UX设计
- 添加用户反馈机制
- 支持多语言

## 📄 开源协议

本项目采用 MIT 协议开源。

## 👨‍💻 作者

**你的名字**

- GitHub: [@你的用户名](https://github.com/你的用户名)

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的Web应用框架
- [OpenAI](https://openai.com/) - 强大的AI模型支持
- 传统中医理论为本应用提供理论基础

## 📊 版本历史

### v1.0.0 (2025-10-17)
- ✨ 初始版本发布
- 🤖 集成OpenAI GPT-4o-mini模型
- 💊 实现中医辨证分析和养生建议
- ⚡ 支持流式输出
- 🚀 部署到Streamlit Community Cloud

## 📮 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/你的用户名/medical/issues)
- 发送邮件至：your.email@example.com

---

**⭐ 如果这个项目对你有帮助，欢迎给个Star！**