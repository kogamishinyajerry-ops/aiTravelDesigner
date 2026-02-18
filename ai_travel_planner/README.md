# AI旅行规划软件

> 基于AI的智能旅行规划平台，深度理解用户需求，结合真实数据源，生成个性化行程方案

## 🎯 项目简介

AI旅行规划软件是一款通过AI深度理解用户需求，结合多源实时数据爬取，智能生成个性化旅行方案的平台。

### 核心功能

- 🤖 **AI需求理解** - 自然语言对话式需求采集
- 🌍 **多源数据爬取** - 20+数据源实时更新
- 🗺️ **智能路线规划** - TSP算法优化路线
- 💰 **精准预算计算** - 详细费用分解
- 📱 **全平台支持** - Web + 移动端

## 📁 项目结构

```
ai_travel_planner/
├── backend/                    # 后端服务（FastAPI）
│   ├── api/                   # API层
│   ├── services/              # 业务逻辑层
│   ├── models/               # 数据模型
│   ├── schemas/              # Pydantic模式
│   └── core/                 # 核心配置
│
├── frontend/                  # 前端应用（React）
│   └── src/
│       ├── components/       # React组件
│       ├── pages/           # 页面
│       ├── services/        # API服务
│       ├── hooks/           # React Hooks
│       └── utils/           # 工具函数
│
├── crawler/                   # 爬虫服务（Scrapy）
│   ├── spiders/             # 爬虫脚本
│   ├── pipelines/           # 数据管道
│   └── middlewares/         # 中间件
│
├── ml/                       # 机器学习模型
│   ├── recommendation/      # 推荐模型
│   ├── nlp/                # NLP模型
│   └── route_opt/          # 路线优化模型
│
├── tests/                    # 测试
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── e2e/               # E2E测试
│
├── docs/                    # 文档
├── logs/                    # 日志
├── scripts/                # 脚本
├── TODO.md                 # 开发TODO List
└── README.md              # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker（可选）

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository>
cd ai_travel_planner
```

#### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件，填入配置
```

#### 3. 启动数据库

```bash
docker-compose up -d db redis
```

#### 4. 安装后端依赖

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. 初始化数据库

```bash
alembic upgrade head
```

#### 6. 启动后端服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 7. 安装前端依赖

```bash
cd frontend
npm install
```

#### 8. 启动前端服务

```bash
npm start
```

#### 9. 访问应用

- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📚 开发文档

- [需求分析](REQUIREMENT_ANALYSIS.md) - 详细的需求分析
- [技术实现](TECHNICAL_IMPLEMENTATION.md) - 技术实施方案
- [项目初始化](INIT_PROJECT.md) - 项目初始化指南
- [核心代码](DEMO_CODE.md) - 核心功能代码演示
- [TODO List](TODO.md) - 开发任务清单

## 🎯 开发进度

当前进度: **Phase 1** - 基础设施搭建

查看详细进度: [TODO.md](TODO.md)

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: PostgreSQL + Redis
- **AI**: OpenAI GPT-4o / DeepSeek
- **爬虫**: Scrapy + Playwright
- **消息队列**: Celery + Redis

### 前端
- **框架**: React 18
- **UI库**: Material UI
- **状态管理**: Redux Toolkit
- **地图**: 高德地图
- **路由**: React Router

## 📖 API文档

启动后端服务后访问: http://localhost:8000/docs

### 主要端点

- `POST /api/v1/chat` - AI对话
- `POST /api/v1/plan/generate` - 生成行程
- `GET /api/v1/plan/budget` - 计算预算
- `GET /api/v1/destinations` - 获取目的地列表
- `GET /api/v1/attractions` - 获取景点列表

## 🤝 贡献指南

欢迎贡献代码！

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📝 许可证

MIT License

## 👥 团队

- 产品负责人: 待定
- 技术负责人: 待定
- 开发团队: 待定

## 📧 联系方式

- 项目主页: [GitHub]
- 问题反馈: [GitHub Issues]
- 邮箱: [待定]

## 🌟 致谢

感谢所有贡献者和开源项目的支持！

---

**版本**: v0.1.0-alpha
**最后更新**: 2026-02-18
