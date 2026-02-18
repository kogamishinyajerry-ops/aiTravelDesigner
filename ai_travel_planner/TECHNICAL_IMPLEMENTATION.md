# AI旅行规划软件 - 技术实施方案

## 🏗️ 项目结构

```
ai_travel_planner/
├── backend/                    # 后端服务
│   ├── api/                   # API层
│   │   ├── v1/              # API v1版本
│   │   │   ├── endpoints/   # 路由端点
│   │   │   │   ├── chat.py      # 对话接口
│   │   │   │   ├── plan.py      # 规划接口
│   │   │   │   ├── search.py    # 搜索接口
│   │   │   │   └── booking.py   # 预订接口
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/              # 业务逻辑层
│   │   ├── ai/            # AI服务
│   │   │   ├── llm_service.py      # LLM调用
│   │   │   ├── nlp_service.py      # NLP处理
│   │   │   └── recommendation.py  # 推荐算法
│   │   ├── planning/       # 规划服务
│   │   │   ├── route_optimizer.py # 路线优化
│   │   │   ├── schedule_generator.py # 行程生成
│   │   │   └── budget_calculator.py # 预算计算
│   │   ├── crawler/       # 爬虫服务
│   │   │   ├── base.py            # 基础爬虫
│   │   │   ├── transport.py        # 交通数据爬取
│   │   │   ├── accommodation.py   # 住宿数据爬取
│   │   │   ├── attraction.py       # 景点数据爬取
│   │   │   ├── restaurant.py      # 餐厅数据爬取
│   │   │   └── scheduler.py       # 任务调度
│   │   └── data/          # 数据服务
│   │       ├── destination.py      # 目的地数据
│   │       ├── price_monitor.py    # 价格监控
│   │       └── weather.py        # 天气数据
│   ├── models/               # 数据模型
│   │   ├── user.py         # 用户模型
│   │   ├── itinerary.py   # 行程模型
│   │   ├── destination.py  # 目的地模型
│   │   └── attraction.py  # 景点模型
│   ├── schemas/            # Pydantic模式
│   │   ├── chat.py
│   │   ├── plan.py
│   │   └── booking.py
│   ├── core/               # 核心配置
│   │   ├── config.py      # 配置
│   │   ├── database.py    # 数据库
│   │   └── cache.py       # 缓存
│   └── main.py            # 应用入口
│
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── components/     # React组件
│   │   │   ├── Chat/          # 对话组件
│   │   │   ├── Planner/       # 规划器组件
│   │   │   ├── Timeline/      # 时间轴组件
│   │   │   ├── Map/           # 地图组件
│   │   │   └── Budget/        # 预算组件
│   │   ├── pages/         # 页面
│   │   │   ├── Home.tsx
│   │   │   ├── Planner.tsx
│   │   │   ├── Search.tsx
│   │   │   └── Profile.tsx
│   │   ├── services/       # API服务
│   │   ├── hooks/         # React Hooks
│   │   ├── utils/         # 工具函数
│   │   └── App.tsx
│   ├── public/
│   └── package.json
│
├── crawler/               # 独立爬虫服务
│   ├── spiders/           # 爬虫脚本
│   │   ├── ctrip_spider.py
│   │   ├── qunar_spider.py
│   │   ├── meituan_spider.py
│   │   └── dianping_spider.py
│   ├── pipelines/         # 数据管道
│   ├── middlewares/       # 中间件
│   └── scrapy.cfg
│
├── ml/                   # 机器学习模型
│   ├── recommendation/    # 推荐模型
│   ├── nlp/             # NLP模型
│   └── route_opt/       # 路线优化模型
│
├── tests/                # 测试
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                # 文档
│   ├── api/            # API文档
│   └── deployment/     # 部署文档
│
├── scripts/             # 脚本
│   ├── start.sh        # 启动脚本
│   ├── deploy.sh       # 部署脚本
│   └── backup.sh       # 备份脚本
│
├── docker-compose.yml   # Docker编排
├── requirements.txt    # Python依赖
├── .env.example      # 环境变量示例
└── README.md         # 项目说明
```

## 🔧 技术栈详细说明

### 后端技术栈

#### 1. Web框架：FastAPI
```python
# 优势
- 高性能异步框架
- 自动API文档（Swagger/Redoc）
- 类型提示支持
- 依赖注入
- WebSocket支持
```

#### 2. 数据库：PostgreSQL + Redis

**PostgreSQL** (主数据库)
```python
# 存储数据
- 用户信息
- 行程数据
- 目的地信息
- 订单数据
- 评价数据

# 扩展
- PostGIS（地理数据）
- pgvector（向量搜索）
```

**Redis** (缓存)
```python
# 缓存策略
- 热门目的地（24小时）
- 搜索结果（1小时）
- 用户会话（30分钟）
- 价格数据（5分钟）
- 限流计数
```

#### 3. 消息队列：Celery + Redis

```python
# 异步任务
- 爬虫调度
- 价格监控
- 邮件发送
- 数据统计
- 报告生成
```

#### 4. AI服务

**LLM调用**
```python
# 主模型：GPT-4o
- 复杂需求理解
- 多轮对话
- 创意生成

# 备用模型：DeepSeek
- 简单任务
- 成本优化
- 容灾备份
```

**NLP处理**
```python
# 本地模型
- jieba分词（中文）
- BERT意图识别
- 命名实体识别
```

#### 5. 爬虫框架：Scrapy + Playwright

**Scrapy** (静态页面)
```python
# 高效爬取
- 异步IO
- 内置调度
- 数据管道
- 中间件系统
```

**Playwright** (动态页面)
```python
# 渲染JavaScript
- 单页应用
- 懒加载内容
- 反爬虫绕过
```

### 前端技术栈

#### 1. 框架：React Native

```typescript
// 跨平台开发
- iOS + Android
- 原生性能
- 热更新
```

#### 2. 状态管理：Redux Toolkit

```typescript
// 状态结构
interface RootState {
  user: UserState;
  chat: ChatState;
  planner: PlannerState;
  itinerary: ItineraryState;
}
```

#### 3. UI组件：React Native Paper

```typescript
// Material Design组件库
- 丰富的组件
- 自定义主题
- 无障碍支持
```

#### 4. 地图：高德地图SDK

```typescript
// 地图功能
- POI搜索
- 路径规划
- 实时导航
- 地图标注
```

## 🕷️ 爬虫详细方案

### 1. 爬虫架构

```python
class CrawlerManager:
    """爬虫管理器"""
    
    def __init__(self):
        self.schedulers = []
        self.proxies = ProxyPool(size=100)
        self.rate_limiter = RateLimiter(requests_per_minute=30)
    
    async def run_all_crawlers(self):
        """运行所有爬虫"""
        tasks = [
            self.crawl_transport(),
            self.crawl_accommodation(),
            self.crawl_attractions(),
            self.crawl_restaurants(),
            self.crawl_reviews(),
        ]
        await asyncio.gather(*tasks)
```

### 2. 数据源详细列表

#### 交通数据爬取
| 平台 | 数据类型 | 频率 | 优先级 |
|------|---------|------|--------|
| 12306 | 火车票 | 1小时 | ⭐⭐⭐⭐⭐ |
| 携程机票 | 机票 | 1小时 | ⭐⭐⭐⭐⭐ |
| 飞猪机票 | 机票 | 1小时 | ⭐⭐⭐⭐ |
| 去哪儿机票 | 机票 | 1小时 | ⭐⭐⭐ |
| 同程机票 | 机票 | 2小时 | ⭐⭐⭐ |

#### 住宿数据爬取
| 平台 | 数据类型 | 频率 | 优先级 |
|------|---------|------|--------|
| 携程酒店 | 价格、库存 | 1小时 | ⭐⭐⭐⭐⭐ |
| 美团酒店 | 价格、库存 | 1小时 | ⭐⭐⭐⭐⭐ |
| Airbnb | 价格、房源 | 2小时 | ⭐⭐⭐⭐ |
| 去哪儿酒店 | 价格 | 2小时 | ⭐⭐⭐ |
| 同程酒店 | 价格 | 2小时 | ⭐⭐⭐ |

#### 景点数据爬取
| 平台 | 数据类型 | 频率 | 优先级 |
|------|---------|------|--------|
| 景区官网 | 门票价格 | 12小时 | ⭐⭐⭐⭐⭐ |
| 携程门票 | 价格、评价 | 12小时 | ⭐⭐⭐⭐⭐ |
| 大众点评 | 评价 | 24小时 | ⭐⭐⭐⭐ |
| 穷游 | 攻略、评分 | 7天 | ⭐⭐⭐ |
| 马蜂窝 | 攻略、评分 | 7天 | ⭐⭐⭐ |

#### 餐厅数据爬取
| 平台 | 数据类型 | 频率 | 优先级 |
|------|---------|------|--------|
| 大众点评 | 价格、评价 | 24小时 | ⭐⭐⭐⭐⭐ |
| 小红书 | 图片、评价 | 24小时 | ⭐⭐⭐⭐ |
| 携程美食 | 价格、位置 | 24小时 | ⭐⭐⭐ |
| 美团美食 | 价格、位置 | 24小时 | ⭐⭐⭐ |

### 3. 爬虫核心代码示例

```python
import scrapy
from playwright.async_api import async_playwright
import random
import time

class BaseSpider(scrapy.Spider):
    """基础爬虫类"""
    
    name = 'base_spider'
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
            # 更多User-Agent
        ]
        
        self.proxies = ProxyPool().get_random()
    
    def get_random_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def delay(self):
        """随机延迟"""
        await asyncio.sleep(random.uniform(2, 10))


class CtripAttractionSpider(BaseSpider):
    """携程景点爬虫"""
    
    name = 'ctrip_attraction'
    
    async def start_requests(self):
        cities = ['北京', '上海', '广州', '深圳', '成都']
        for city in cities:
            url = f'https://you.ctrip.com/sight/{city}'
            yield scrapy.Request(
                url=url,
                headers=self.get_random_headers(),
                callback=self.parse_attraction_list
            )
            await self.delay()
    
    async def parse_attraction_list(self, response):
        """解析景点列表"""
        attractions = response.css('.sight-item')
        for attraction in attractions:
            yield {
                'name': attraction.css('.title::text').get(),
                'rating': attraction.css('.score::text').get(),
                'price': attraction.css('.price::text').get(),
                'address': attraction.css('.address::text').get(),
                'source': 'ctrip',
                'crawl_time': datetime.now().isoformat(),
            }


class PlaywrightSpider:
    """Playwright爬虫（用于动态页面）"""
    
    async def crawl(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # 设置User-Agent
            await page.set_extra_http_headers({
                'User-Agent': self.get_random_headers()['User-Agent']
            })
            
            # 访问页面
            await page.goto(url, wait_until='networkidle')
            
            # 等待内容加载
            await page.wait_for_selector('.content')
            
            # 提取数据
            data = await page.evaluate('''
                () => {
                    return {
                        title: document.querySelector('.title')?.textContent,
                        content: document.querySelector('.content')?.textContent,
                    }
                }
            ''')
            
            await browser.close()
            return data
```

### 4. 反爬虫策略

```python
class AntiScrapingMiddleware:
    """反爬虫中间件"""
    
    def __init__(self):
        self.request_count = 0
        self.last_request_time = None
    
    async def process_request(self, request, spider):
        """处理请求"""
        
        # 限制请求频率
        await self.rate_limit()
        
        # 随机User-Agent
        request.headers['User-Agent'] = self.get_random_ua()
        
        # 随机代理
        request.meta['proxy'] = self.proxy_pool.get_random()
        
        # Cookie管理
        if not request.cookies:
            request.cookies = self.get_cookies(request.url)
        
        # 验证码识别
        if self.is_captcha(request):
            return await self.handle_captcha(request)
        
        return request
    
    async def rate_limit(self):
        """限流"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            min_interval = random.uniform(2, 10)
            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
        
        self.last_request_time = time.time()
```

## 🧠 AI服务详细设计

### 1. 需求理解服务

```python
class RequirementUnderstandingService:
    """需求理解服务"""
    
    def __init__(self):
        self.llm = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_template = """
你是一位专业的旅行规划师。请理解用户的旅行需求，提取关键信息。

用户输入：{user_input}

请提取以下信息（JSON格式）：
{{
    "destination": "目的地",
    "duration_days": "行程天数",
    "budget": "预算",
    "travelers": "出行人数和对象",
    "travel_date": "出行时间",
    "pace_preference": "节奏偏好（悠闲/适中/充实）",
    "interests": ["兴趣点1", "兴趣点2"],
    "accommodation_preference": "住宿偏好",
    "transport_preference": "交通偏好",
    "special_requirements": ["特殊要求1", "特殊要求2"]
}}

如果某个信息未提及，请设为null。
"""
    
    async def understand(self, user_input: str) -> dict:
        """理解用户需求"""
        prompt = self.prompt_template.format(user_input=user_input)
        
        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是专业的旅行规划师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # 验证完整性
        missing_info = self.check_missing_info(result)
        if missing_info:
            return {
                "extracted": result,
                "missing": missing_info,
                "need_clarification": True
            }
        
        return {
            "extracted": result,
            "need_clarification": False
        }
```

### 2. 路线规划服务

```python
class RoutePlanningService:
    """路线规划服务"""
    
    def __init__(self):
        self.attraction_db = AttractionDB()
        self.transport_db = TransportDB()
        self.optimizer = RouteOptimizer()
    
    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        interests: List[str],
        budget: float
    ) -> Itinerary:
        """生成行程"""
        
        # 1. 获取候选景点
        attractions = await self.attraction_db.get_by_interests(
            destination=destination,
            interests=interests,
            limit=days * 3  # 每天3个候选
        )
        
        # 2. 获取交通信息
        transport_matrix = await self.transport_db.get_matrix(
            location_ids=[a.id for a in attractions]
        )
        
        # 3. 优化路线（TSP变种）
        optimized_routes = await self.optimizer.optimize(
            attractions=attractions,
            days=days,
            transport_matrix=transport_matrix,
            budget=budget
        )
        
        # 4. 生成详细行程
        itinerary = await self._generate_detailed_itinerary(
            routes=optimized_routes,
            days=days
        )
        
        return itinerary
    
    async def _generate_detailed_itinerary(
        self,
        routes: List[Route],
        days: int
    ) -> Itinerary:
        """生成详细行程"""
        itinerary = Itinerary()
        
        for day, route in enumerate(routes[:days], 1):
            day_plan = DayPlan(day=day)
            
            # 添加景点
            for i, attraction in enumerate(route.attractions):
                start_time = self._calculate_start_time(i, day)
                end_time = self._calculate_end_time(
                    start_time,
                    attraction.suggested_duration
                )
                
                activity = Activity(
                    type='attraction',
                    name=attraction.name,
                    start_time=start_time,
                    end_time=end_time,
                    location=attraction.address,
                    budget=attraction.ticket_price
                )
                
                day_plan.add_activity(activity)
            
            # 添加用餐
            meals = await self._suggest_meals(route)
            for meal in meals:
                day_plan.add_activity(meal)
            
            itinerary.add_day(day_plan)
        
        return itinerary
```

### 3. 预算计算服务

```python
class BudgetCalculatorService:
    """预算计算服务"""
    
    async def calculate_budget(
        self,
        itinerary: Itinerary,
        travelers: int
    ) -> BudgetBreakdown:
        """计算预算"""
        
        budget = BudgetBreakdown()
        
        # 1. 交通费用
        transport_cost = await self._calculate_transport_cost(
            itinerary,
            travelers
        )
        budget.transport = transport_cost
        
        # 2. 住宿费用
        accommodation_cost = await self._calculate_accommodation_cost(
            itinerary,
            travelers
        )
        budget.accommodation = accommodation_cost
        
        # 3. 餐饮费用
        food_cost = await self._calculate_food_cost(
            itinerary,
            travelers
        )
        budget.food = food_cost
        
        # 4. 门票费用
        ticket_cost = await self._calculate_ticket_cost(
            itinerary,
            travelers
        )
        budget.tickets = ticket_cost
        
        # 5. 其他费用
        other_cost = await self._calculate_other_cost(
            itinerary,
            travelers
        )
        budget.other = other_cost
        
        # 总计
        budget.total = (
            transport_cost +
            accommodation_cost +
            food_cost +
            ticket_cost +
            other_cost
        )
        
        return budget
```

## 📊 数据模型设计

### 核心数据表

#### users表
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    preferences JSONB,  -- 用户偏好
    travel_history JSONB  -- 历史行程
);
```

#### destinations表
```sql
CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    province VARCHAR(50),
    country VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    tags TEXT[],
    best_season VARCHAR(50),
    average_budget DECIMAL(10, 2),
    popularity_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 空间索引
CREATE INDEX idx_destinations_location ON destinations USING GIST (
    (point(longitude, latitude)::geometry)
);
```

#### attractions表
```sql
CREATE TABLE attractions (
    id SERIAL PRIMARY KEY,
    destination_id INTEGER REFERENCES destinations(id),
    name VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    type VARCHAR(50),  -- 自然风光、历史文化、娱乐休闲等
    description TEXT,
    address VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    ticket_price DECIMAL(10, 2),
    opening_hours JSONB,
    suggested_duration INTEGER,  -- 建议游览时长（分钟）
    rating DECIMAL(3, 2),
    review_count INTEGER,
    tags TEXT[],
    best_visit_time VARCHAR(50),
    images TEXT[],
    popularity_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attractions_location ON attractions USING GIST (
    (point(longitude, latitude)::geometry)
);
CREATE INDEX idx_attractions_type ON attractions(type);
CREATE INDEX idx_attractions_tags ON attractions USING GIN(tags);
```

#### itineraries表
```sql
CREATE TABLE itineraries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(200) NOT NULL,
    destination_id INTEGER REFERENCES destinations(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days INTEGER NOT NULL,
    travelers INTEGER DEFAULT 1,
    total_budget DECIMAL(10, 2),
    actual_cost DECIMAL(10, 2),
    status VARCHAR(20),  -- planning, booked, ongoing, completed
    itinerary_data JSONB,  -- 完整行程数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### prices表
```sql
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    item_type VARCHAR(50) NOT NULL,  -- transport, accommodation, attraction, restaurant
    item_id INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL,  -- ctrip, qunar, meituan等
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    available BOOLEAN DEFAULT TRUE,
    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_time TIMESTAMP
);

CREATE INDEX idx_prices_item ON prices(item_type, item_id, crawl_time DESC);
```

## 🚀 部署方案

### Docker Compose配置

```yaml
version: '3.8'

services:
  # 后端API
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/travel_planner
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
  
  # 爬虫服务
  crawler:
    build: ./crawler
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
    command: celery -A tasks worker -l info
  
  # PostgreSQL数据库
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=travel_planner
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  # Redis缓存
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  # 前端
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  # Nginx反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
      - frontend

volumes:
  postgres_data:
  redis_data:
```

## 📈 监控与日志

### 1. 性能监控

```python
# 使用Prometheus + Grafana
from prometheus_client import Counter, Histogram, start_http_server

# 定义指标
api_requests_total = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')
crawler_success_total = Counter('crawler_success_total', 'Successful crawls', ['source'])
crawler_error_total = Counter('crawler_error_total', 'Failed crawls', ['source', 'error_type'])

# 启动监控
start_http_server(9090)
```

### 2. 日志系统

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 文件日志
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=10
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# 控制台日志
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

## 🔒 安全措施

### 1. 数据加密

```python
from cryptography.fernet import Fernet

class EncryptionService:
    """加密服务"""
    
    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY)
    
    def encrypt(self, data: str) -> str:
        """加密"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### 2. 限流保护

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# 限制API调用
@app.post("/api/v1/chat")
@limiter.limit("10/minute")
async def chat(request: Request, message: str):
    ...
```

## 📋 开发检查清单

### Phase 1 MVP
- [ ] 后端框架搭建
- [ ] 数据库设计
- [ ] 用户认证系统
- [ ] 对话接口实现
- [ ] 基础爬虫（3个数据源）
- [ ] 简单路线生成算法
- [ ] 前端基础UI
- [ ] 部署到测试环境

### Phase 2 功能完善
- [ ] 多方案对比
- [ ] 行程拖拽调整
- [ ] 实时价格追踪
- [ ] 增加爬虫数据源
- [ ] 用户账户系统
- [ ] 行程保存分享
- [ ] 性能优化

### Phase 3 深度智能化
- [ ] 历史行为分析
- [ ] 个性化推荐
- [ ] 动态调整能力
- [ ] 移动端App
- [ ] 社交分享

---

**文档版本**：v1.0
**创建时间**：2026-02-18
