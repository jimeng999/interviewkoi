# 面试锦鲤 InterviewKoi 🐟

> 每场面试，都如鱼得水

AI驱动的智能面试助手，输入岗位和简历，AI帮你准备面试答案、模拟面试、预测考题。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ 功能特色

### 🎯 考题预测
- 基于岗位JD智能分析
- 预测10-15道最可能被问的面试题
- 按出现概率排序：必考/高频/中频/低频
- 分类：行为题/技术题/情景题/文化题

### 💬 答案生成
- STAR法则结构化答案
- 基于用户真实经历定制
- 口语化自然表达
- 量化成果突出价值

### 🎭 模拟面试
- AI扮演专业面试官
- 逐题追问深挖细节
- 即时评分与反馈
- 多轮实战演练

### 📦 岗位覆盖
- 🖥️ 技术岗（前端/后端/算法/数据）
- 📱 产品岗（产品经理/运营/增长）
- 👔 管理岗（项目管理/团队管理）
- 💼 通用岗（销售/市场/HR/行政）

### 🎨 面试风格
- 🔥 压力面试模式（追问+质疑）
- 😊 友善聊天模式（轻松引导）
- 📋 行为面试模式（STAR深挖）
- ⚙️ 技术深挖模式（追问底层原理）

## 🚀 快速开始

### 本地开发

```bash
# 克隆项目
git clone https://github.com/your-repo/AI-InterviewKoi.git
cd AI-InterviewKoi

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m app.main
# 或
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000 即可使用。

### Vercel 部署

```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
vercel --prod
```

## 💡 使用指南

### 1. 输入信息
- **目标岗位**：输入公司名称和职位（如"字节跳动 高级产品经理"）
- **岗位类型**：选择技术/产品/管理/通用
- **简历/经历**：粘贴你的简历或工作经历
- **面试风格**：选择你想要的面试模式

### 2. 选择功能
- **考题预测**：获取针对性面试题库
- **答案生成**：获取STAR结构化答案
- **模拟面试**：开始AI对话模拟

### 3. 获取结果
- 查看预测考题列表
- 复制和使用生成答案
- 与AI面试官互动练习

## 🛠️ 技术栈

- **后端**：Python FastAPI
- **前端**：原生 HTML/CSS/JavaScript
- **AI**：DeepSeek API（BYOK模式）
- **部署**：Vercel Serverless

## 📁 项目结构

```
AI-InterviewKoi/
├── api/
│   ├── __init__.py
│   └── index.py              # Vercel Serverless 函数入口
├── app/
│   ├── main.py               # FastAPI 主应用
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── interview.py      # 面试相关路由
│   │   └── user.py           # 用户相关路由
│   ├── services/
│   │   ├── __init__.py
│   │   ├── generator.py       # Prompt 核心生成逻辑
│   │   └── billing.py         # 计费服务
│   └── models/
│       ├── __init__.py
│       └── schemas.py         # Pydantic 数据模型
├── static/
│   └── index.html             # 前端页面
├── vercel.json                # Vercel 配置
├── requirements.txt            # Python 依赖
└── README.md
```

## 💰 定价

| 方案 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0/月 | 每月3次 |
| Pro | ¥49/月 | 无限次使用 |

## 🔧 环境变量

```env
# DeepSeek API Key（可选，未配置时使用演示模式）
DEEPSEEK_API_KEY=sk-xxxxx

# BYOK 模式（可选，允许用户使用自己的API Key）
BYOK_ENABLED=true
```

## 📝 API 接口

### 预测考题
```
POST /api/interview/predict
Body: { job_title, job_type, resume, style }
Response: { questions: [{ title, type, frequency, tips }] }
```

### 生成答案
```
POST /api/interview/answer
Body: { job_title, job_type, question, resume, style }
Response: { answer: { situation, task, action, result } }
```

### 模拟面试
```
POST /api/interview/simulate
Body: { job_title, job_type, resume, style, history[] }
Response: { response, next_question, score, feedback }
```

## 🎨 界面预览

深色主题配合金色渐变，锦鲤元素贯穿全站，带来好运祝福。

- 主色调：深色底 `#0a0a0b`
- 强调色：金色渐变 `#f59e0b → #eab308`
- 点缀色：红色 `#ef4444`

## 📄 License

MIT License © 2024 InterviewKoi

---

🐟 **祝您面试顺利，如鱼得水！**
