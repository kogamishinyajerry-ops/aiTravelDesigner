# AI旅行规划软件 - 项目初始化指南

## 🚀 快速开始

### 1. 环境准备

#### 系统要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker（可选）

#### 安装依赖

```bash
# Python依赖
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis celery \
            openai scrapy playwright jieba sentry-sdk prometheus-client

# Node.js依赖（前端）
npm install -g create-react-app

# Playwright浏览器
playwright install chromium
```

### 2. 项目初始化脚本

```bash
#!/bin/bash

echo "=========================================="
echo "AI旅行规划软件 - 项目初始化"
echo "=========================================="

# 创建项目目录
mkdir -p ai_travel_planner
cd ai_travel_planner

# 创建子目录
mkdir -p backend/api/v1/endpoints
mkdir -p backend/services/{ai,planning,crawler,data}
mkdir -p backend/models
mkdir -p backend/schemas
mkdir -p backend/core
mkdir -p frontend/src/{components,pages,services,hooks,utils}
mkdir -p frontend/public
mkdir -p crawler/{spiders,pipelines,middlewares}
mkdir -p ml/{recommendation,nlp,route_opt}
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs/{api,deployment}
mkdir -p scripts
mkdir -p logs

# 初始化Git
git init

# 创建.gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Node.js
node_modules/
npm-debug.log
yarn-error.log
.pnpm-debug.log

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Database
*.db
*.sqlite

# Redis
dump.rdb

# Scrapy
.scrapy/

# Playwright
playwright-report/
test-results/

# OS
.DS_Store
Thumbs.db
EOF

# 创建Python虚拟环境
python3 -m venv backend/venv
source backend/venv/bin/activate

# 安装Python依赖
cat > backend/requirements.txt << 'EOF'
# Web框架
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# 缓存
redis==5.0.1
hiredis==2.2.3

# 消息队列
celery==5.3.6

# AI
openai==1.10.0
tiktoken==0.5.2

# NLP
jieba==0.42.1
transformers==4.37.2
torch==2.1.2

# 爬虫
scrapy==2.11.0
playwright==1.40.0
beautifulsoup4==4.12.3
requests==2.31.0
selenium==4.17.2

# 数据处理
pandas==2.2.0
numpy==1.26.3

# 地理
geopy==2.4.1
pyproj==3.6.1

# 工具
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
httpx==0.26.0
aiohttp==3.9.1

# 监控
prometheus-client==0.19.0
sentry-sdk==1.40.0

# 测试
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
EOF

pip install -r backend/requirements.txt

# 初始化前端
cd frontend
npm init -y
npm install react react-dom react-router-dom
npm install @reduxjs/toolkit react-redux
npm install axios
npm install @mui/material @emotion/react @emotion/styled
npm install leaflet react-leaflet
cd ..

# 创建Docker配置
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/travel_planner
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=travel_planner
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
EOF

# 创建环境变量模板
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/travel_planner

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Services
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Maps
AMAP_API_KEY=your_amap_api_key_here

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
EOF

# 创建README
cat > README.md << 'EOF'
# AI旅行规划软件

## 项目简介

基于AI的智能旅行规划平台，深度理解用户需求，结合真实数据源，生成个性化行程方案。

## 功能特色

- 🤖 AI深度需求理解
- 🌍 多源实时数据爬取
- 🗺️ 智能路线规划
- 💰 精准预算计算
- 📱 全平台支持

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 安装步骤

1. 克隆项目
```bash
git clone <repository>
cd ai_travel_planner
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入配置
```

3. 启动数据库
```bash
docker-compose up -d db redis
```

4. 安装依赖
```bash
# 后端
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 前端
cd ../frontend
npm install
```

5. 初始化数据库
```bash
cd backend
alembic upgrade head
```

6. 启动服务
```bash
# 后端
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端
cd frontend
npm start
```

7. 访问应用
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 项目结构

```
ai_travel_planner/
├── backend/          # 后端服务
├── frontend/         # 前端应用
├── crawler/          # 爬虫服务
├── ml/              # 机器学习模型
└── docs/            # 文档
```

## 开发指南

详细的开发文档请参考：
- [需求分析](REQUIREMENT_ANALYSIS.md)
- [技术实现](TECHNICAL_IMPLEMENTATION.md)
- [API文档](docs/api/README.md)

## 贡献指南

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License
EOF

echo "=========================================="
echo "✅ 项目初始化完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，配置环境变量"
echo "2. 启动数据库: docker-compose up -d db redis"
echo "3. 初始化数据库: cd backend && alembic upgrade head"
echo "4. 启动后端: uvicorn main:app --reload"
echo "5. 启动前端: cd frontend && npm start"
echo ""
```

## 使用初始化脚本

```bash
# 复制上面的脚本内容，保存为 init_project.sh
chmod +x init_project.sh
./init_project.sh
```

## 开发工具推荐

### 后端开发
- **IDE**: PyCharm Professional / VS Code
- **API测试**: Postman / Insomnia
- **数据库**: DBeaver / pgAdmin
- **Redis客户端**: RedisInsight

### 前端开发
- **IDE**: VS Code
- **调试**: React Developer Tools
- **UI库**: Material UI / Ant Design

### 爬虫开发
- **调试**: Scrapy Shell
- **代理**: 亮数据 / 快代理
- **验证码识别**: 2Captcha / 打码兔

## 学习资源

### FastAPI
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [FastAPI实战教程](https://www.fastapicn.com/)

### React
- [React官方文档](https://react.dev/)
- [React中文文档](https://zh-hans.react.dev/)

### Scrapy
- [Scrapy官方文档](https://docs.scrapy.org/)
- [Scrapy中文文档](https://scrapy-chs.readthedocs.io/)

### AI/LLM
- [OpenAI API文档](https://platform.openai.com/docs)
- [LangChain文档](https://python.langchain.com/)

## 常见问题

### Q: 如何测试爬虫？
```bash
# 进入爬虫目录
cd crawler

# 运行单个爬虫
scrapy crawl ctrip_attraction

# 调试爬虫
scrapy shell "https://you.ctrip.com/sight/beijing"
```

### Q: 如何查看日志？
```bash
# 后端日志
tail -f logs/app.log

# 爬虫日志
tail -f logs/crawler.log

# Celery日志
tail -f logs/celery.log
```

### Q: 如何重启服务？
```bash
# 使用脚本
./scripts/restart.sh

# 或手动
docker-compose restart
```

## 下一步计划

### Week 1-4: MVP开发
- [ ] 后端框架搭建
- [ ] 用户认证系统
- [ ] 对话接口实现
- [ ] 基础爬虫
- [ ] 简单路线生成
- [ ] 前端基础UI

### Week 5-10: 功能完善
- [ ] 多方案对比
- [ ] 行程调整
- [ ] 价格追踪
- [ ] 用户账户
- [ ] 移动端适配

### Week 11+: 深度智能化
- [ ] 个性化推荐
- [ ] 动态调整
- [ ] 社交功能
- [ ] 商业化

## 联系方式

- 项目负责人: [待定]
- 技术支持: [待定]
- 问题反馈: [GitHub Issues]

---

**祝你开发顺利！🚀**
```

## 📝 核心文件快速创建

### 1. 后端main.py

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import router as api_v1_router

app = FastAPI(
    title="AI Travel Planner API",
    description="AI智能旅行规划平台API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Travel Planner API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 2. 前端App.tsx

```tsx
// frontend/src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import Home from './pages/Home';
import Planner from './pages/Planner';
import Search from './pages/Search';
import Profile from './pages/Profile';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/planner" element={<Planner />} />
          <Route path="/search" element={<Search />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
```

### 3. 爬虫基础类

```python
# crawler/spiders/base_spider.py
import scrapy
from scrapy.http import Request
import random
import time

class BaseSpider(scrapy.Spider):
    name = 'base'
    
    def __init__(self):
        super().__init__()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        ]
    
    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml',
        }
    
    def start_requests(self):
        urls = self.get_start_urls()
        for url in urls:
            yield Request(url, headers=self.get_headers())
    
    def get_start_urls(self):
        return []
```

---

**文档版本**：v1.0
**创建时间**：2026-02-18
