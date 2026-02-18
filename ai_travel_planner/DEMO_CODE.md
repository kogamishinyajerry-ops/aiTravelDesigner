# AI旅行规划软件 - 核心代码演示

## 🎯 演示概述

本文档展示核心功能的代码实现，包括：
1. AI需求理解
2. 智能路线规划
3. 多源数据爬取
4. 预算计算
5. 前端交互

---

## 1. AI需求理解模块

### 1.1 对话式需求采集

```python
# backend/services/ai/llm_service.py
import json
from openai import AsyncOpenAI
from typing import Dict, List, Optional
from loguru import logger

class LLMService:
    """LLM调用服务"""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        
        self.system_prompt = """你是一位专业的旅行规划师，拥有15年经验。
你的任务是深度理解用户的旅行需求，提取关键信息。

理解原则：
1. 识别显性信息（明确提及的）
2. 推断隐性信息（可以合理推测的）
3. 识别冲突点（矛盾的需求）
4. 提出澄清问题（信息不足时）"""
    
    async def understand_travel_need(
        self,
        user_input: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        理解旅行需求
        
        Args:
            user_input: 用户输入
            conversation_history: 对话历史
            
        Returns:
            提取的需求信息
        """
        
        # 构建消息
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        
        # 添加对话历史
        if conversation_history:
            messages.extend(conversation_history)
        
        # 添加用户输入
        user_prompt = f"""
用户需求：
{user_input}

请提取以下信息（JSON格式）：
{{
    "destination": "目的地（城市/国家）",
    "departure_city": "出发城市",
    "duration_days": "行程天数",
    "travel_date": "出行时间（YYYY-MM-DD）",
    "flexible_date": "日期是否灵活（true/false）",
    "travelers": {{
        "count": "人数",
        "type": "类型（情侣/家庭/朋友/独自）",
        "age_groups": ["年龄段1", "年龄段2"]
    }},
    "budget": {{
        "total": "总预算（元）",
        "per_person": "人均预算（元）",
        "flexible": "预算是否灵活（true/false）"
    }},
    "preferences": {{
        "pace": "节奏（悠闲/适中/充实）",
        "accommodation": "住宿偏好（经济型/舒适型/奢华型）",
        "transport": "交通偏好（公共交通/自驾/包车）",
        "activities": ["活动类型1", "活动类型2"],
        "food": "饮食偏好（当地特色/中餐/素食等）"
    }},
    "constraints": {{
        "must_include": ["必去景点1", "必去景点2"],
        "must_avoid": ["避免的景点/活动"],
        "special_requirements": ["特殊要求"]
    }},
    "missing_info": ["缺少的信息1", "缺少的信息2"],
    "need_clarification": "是否需要进一步澄清（true/false）"
}}

如果某项信息未提及，设为null。"""
        
        messages.append({"role": "user", "content": user_prompt})
        
        try:
            # 调用LLM
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # 解析响应
            result = json.loads(response.choices[0].message.content)
            
            logger.info(f"需求理解成功: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"需求理解失败: {e}")
            raise
    
    async def generate_clarification_questions(
        self,
        missing_info: List[str],
        context: Dict
    ) -> List[str]:
        """
        生成澄清问题
        
        Args:
            missing_info: 缺失的信息列表
            context: 已知信息上下文
            
        Returns:
            澄清问题列表
        """
        
        prompt = f"""
用户已经提供的信息：
{json.dumps(context, ensure_ascii=False, indent=2)}

缺失的信息：
{', '.join(missing_info)}

请生成自然、友好的澄清问题，引导用户补充这些信息。
要求：
1. 问题要自然，不要像问卷调查
2. 一次只问1-2个问题
3. 根据已有信息，推测最可能的答案并提问
4. 保持对话的连贯性

返回JSON格式：
{{
    "questions": ["问题1", "问题2"]
}}"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位专业的旅行规划师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result["questions"]
```

### 1.2 使用示例

```python
# 示例：理解用户需求
llm_service = LLMService(api_key="your-api-key")

user_input = """
我想和女朋友3月份去云南玩5天，预算5000左右，
不想太赶，喜欢拍照打卡，对美食感兴趣
"""

result = await llm_service.understand_travel_need(user_input)

# 输出示例：
{
    "destination": "云南",
    "departure_city": null,
    "duration_days": 5,
    "travel_date": "2024-03",
    "travelers": {
        "count": 2,
        "type": "情侣",
        "age_groups": ["青年"]
    },
    "budget": {
        "total": 10000,
        "per_person": 5000,
        "flexible": true
    },
    "preferences": {
        "pace": "悠闲",
        "accommodation": null,
        "transport": null,
        "activities": ["拍照打卡", "美食体验"],
        "food": "当地特色"
    },
    "missing_info": [
        "departure_city",
        "specific_date",
        "accommodation_preference",
        "transport_preference"
    ],
    "need_clarification": true
}

# 生成澄清问题
questions = await llm_service.generate_clarification_questions(
    missing_info=result["missing_info"],
    context=result
)

# 输出：
[
    "你们是从哪个城市出发呢？这样我可以帮你们推荐最合适的交通方式。",
    "有没有具体的时间安排？比如3月几号出发，方便我查一下当时的天气和优惠活动。"
]
```

---

## 2. 智能路线规划模块

### 2.1 景点筛选与排序

```python
# backend/services/planning/attraction_selector.py
from typing import List, Dict
from geopy.distance import geodesic

class AttractionSelector:
    """景点选择器"""
    
    def __init__(self, attraction_db):
        self.attraction_db = attraction_db
    
    async def select_attractions(
        self,
        destination: str,
        interests: List[str],
        days: int,
        pace: str = "适中"
    ) -> List[Dict]:
        """
        选择适合的景点
        
        Args:
            destination: 目的地
            interests: 兴趣点
            days: 天数
            pace: 节奏（悠闲/适中/充实）
            
        Returns:
            景点列表
        """
        
        # 每天推荐的景点数量
        attractions_per_day = {
            "悠闲": 2,
            "适中": 3,
            "充实": 4
        }
        
        target_count = attractions_per_day.get(pace, 3) * days
        
        # 1. 从数据库获取候选景点
        candidates = await self.attraction_db.get_by_destination(
            destination=destination,
            limit=target_count * 3  # 获取3倍候选
        )
        
        # 2. 根据兴趣点打分
        scored_attractions = []
        for attraction in candidates:
            score = self._calculate_attraction_score(
                attraction=attraction,
                interests=interests
            )
            scored_attractions.append({
                **attraction,
                "match_score": score
            })
        
        # 3. 排序并选择top
        scored_attractions.sort(
            key=lambda x: (x["match_score"], x["rating"], -x["popularity_score"]),
            reverse=True
        )
        
        selected = scored_attractions[:target_count]
        
        # 4. 地理位置平衡（避免同一天都在一个地方）
        balanced = self._balance_by_location(
            attractions=selected,
            days=days,
            pace=pace
        )
        
        return balanced
    
    def _calculate_attraction_score(
        self,
        attraction: Dict,
        interests: List[str]
    ) -> float:
        """计算景点匹配分数"""
        
        score = 0.0
        
        # 兴趣匹配（权重0.4）
        attraction_tags = set(attraction.get("tags", []))
        interest_tags = set(interests)
        
        if attraction_tags & interest_tags:
            overlap = len(attraction_tags & interest_tags)
            score += (overlap / len(interest_tags)) * 0.4
        
        # 评分（权重0.3）
        if attraction.get("rating"):
            score += (attraction["rating"] / 5) * 0.3
        
        # 热度（权重0.2）
        if attraction.get("popularity_score"):
            max_popularity = 1000
            score += (attraction["popularity_score"] / max_popularity) * 0.2
        
        # 价格合理（权重0.1）
        if attraction.get("ticket_price"):
            # 假设合理范围是0-200元
            reasonable_price = min(attraction["ticket_price"] / 200, 1)
            score += reasonable_price * 0.1
        
        return score
    
    def _balance_by_location(
        self,
        attractions: List[Dict],
        days: int,
        pace: str
    ) -> List[Dict]:
        """地理位置平衡"""
        
        # 按地理位置聚类
        clusters = self._cluster_by_location(attractions)
        
        # 每天从不同区域选择
        balanced = []
        clusters.sort(key=lambda x: len(x), reverse=True)
        
        for day in range(days):
            for cluster_idx, cluster in enumerate(clusters):
                if len(balanced) < len(attractions) and cluster:
                    balanced.append(cluster.pop(0))
        
        return balanced
    
    def _cluster_by_location(
        self,
        attractions: List[Dict]
    ) -> List[List[Dict]]:
        """按位置聚类"""
        
        clusters = []
        used = set()
        
        for i, attr1 in enumerate(attractions):
            if i in used:
                continue
                
            cluster = [attr1]
            used.add(i)
            
            for j, attr2 in enumerate(attractions):
                if j in used:
                    continue
                    
                # 计算距离（假设在5公里内算同一区域）
                dist = geodesic(
                    (attr1["latitude"], attr1["longitude"]),
                    (attr2["latitude"], attr2["longitude"])
                ).kilometers
                
                if dist <= 5:
                    cluster.append(attr2)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
```

### 2.2 路线优化算法

```python
# backend/services/planning/route_optimizer.py
from typing import List, Dict, Tuple
import numpy as np

class RouteOptimizer:
    """路线优化器（TSP变种）"""
    
    def __init__(self, transport_db):
        self.transport_db = transport_db
    
    async def optimize_daily_route(
        self,
        attractions: List[Dict],
        day: int,
        start_point: Tuple[float, float],
        constraints: Dict
    ) -> List[Dict]:
        """
        优化单日路线
        
        Args:
            attractions: 景点列表
            day: 第几天
            start_point: 起始点坐标
            constraints: 约束条件（时间、预算等）
            
        Returns:
            优化后的景点顺序
        """
        
        if len(attractions) <= 1:
            return attractions
        
        # 1. 构建距离矩阵
        distance_matrix = await self._build_distance_matrix(
            attractions=attractions,
            start_point=start_point
        )
        
        # 2. 使用贪心算法求解TSP
        route_indices = self._solve_tsp_greedy(
            distance_matrix=distance_matrix,
            attractions=attractions,
            constraints=constraints
        )
        
        # 3. 按优化后的顺序返回景点
        optimized_route = [attractions[i] for i in route_indices]
        
        return optimized_route
    
    async def _build_distance_matrix(
        self,
        attractions: List[Dict],
        start_point: Tuple[float, float]
    ) -> np.ndarray:
        """构建距离矩阵"""
        
        # 包含起始点
        all_points = [start_point] + [
            (a["latitude"], a["longitude"])
            for a in attractions
        ]
        
        n = len(all_points)
        distance_matrix = np.zeros((n, n))
        
        # 计算所有点之间的距离
        for i in range(n):
            for j in range(n):
                if i != j:
                    # 使用高德地图API获取实际距离
                    real_distance = await self.transport_db.get_distance(
                        from_point=all_points[i],
                        to_point=all_points[j]
                    )
                    distance_matrix[i][j] = real_distance
        
        return distance_matrix
    
    def _solve_tsp_greedy(
        self,
        distance_matrix: np.ndarray,
        attractions: List[Dict],
        constraints: Dict
    ) -> List[int]:
        """
        使用贪心算法求解TSP
        
        策略：每次选择距离最近的未访问节点
        """
        
        n = len(attractions)
        visited = [False] * (n + 1)  # 包含起始点
        route = [0]  # 从起始点开始（索引0）
        visited[0] = True
        
        current = 0
        
        while len(route) <= n:
            # 找到最近的未访问节点
            nearest = None
            min_distance = float('inf')
            
            for i in range(1, n + 1):
                if not visited[i]:
                    # 检查约束条件
                    if self._check_constraints(
                        current=i,
                        attractions=attractions,
                        constraints=constraints
                    ):
                        dist = distance_matrix[current][i]
                        if dist < min_distance:
                            min_distance = dist
                            nearest = i
            
            if nearest is not None:
                route.append(nearest)
                visited[nearest] = True
                current = nearest
            else:
                break
        
        # 去掉起始点
        return route[1:]
    
    def _check_constraints(
        self,
        current: int,
        attractions: List[Dict],
        constraints: Dict
    ) -> bool:
        """检查约束条件"""
        
        # 检查时间约束
        if "max_attractions_per_day" in constraints:
            if len(attractions) >= constraints["max_attractions_per_day"]:
                return False
        
        # 检查景点开放时间
        attraction = attractions[current - 1]
        if "opening_hours" in attraction:
            # 这里可以添加更复杂的逻辑
            pass
        
        return True
```

### 2.3 完整行程生成

```python
# backend/services/planning/itinerary_generator.py
from datetime import datetime, timedelta
from typing import List, Dict
import asyncio

class ItineraryGenerator:
    """行程生成器"""
    
    def __init__(self, attraction_selector, route_optimizer, restaurant_service):
        self.attraction_selector = attraction_selector
        self.route_optimizer = route_optimizer
        self.restaurant_service = restaurant_service
    
    async def generate(
        self,
        destination: str,
        days: int,
        interests: List[str],
        pace: str,
        start_date: str,
        travelers: int
    ) -> Dict:
        """
        生成完整行程
        
        Returns:
            完整行程数据
        """
        
        itinerary = {
            "destination": destination,
            "days": days,
            "start_date": start_date,
            "end_date": self._calculate_end_date(start_date, days),
            "daily_plans": []
        }
        
        # 1. 选择景点
        all_attractions = await self.attraction_selector.select_attractions(
            destination=destination,
            interests=interests,
            days=days,
            pace=pace
        )
        
        # 2. 按天分组
        attractions_per_day = len(all_attractions) // days
        for day in range(days):
            start_idx = day * attractions_per_day
            end_idx = start_idx + attractions_per_day
            
            day_attractions = all_attractions[start_idx:end_idx]
            
            # 3. 优化单日路线
            start_point = await self._get_day_start_point(
                destination=destination,
                day=day
            )
            
            optimized_attractions = await self.route_optimizer.optimize_daily_route(
                attractions=day_attractions,
                day=day + 1,
                start_point=start_point,
                constraints={"pace": pace}
            )
            
            # 4. 生成详细日程
            day_plan = await self._generate_day_plan(
                day=day + 1,
                date=self._calculate_day_date(start_date, day),
                attractions=optimized_attractions,
                pace=pace
            )
            
            itinerary["daily_plans"].append(day_plan)
        
        # 5. 计算总预算
        itinerary["budget"] = await self._calculate_budget(
            itinerary=itinerary,
            travelers=travelers
        )
        
        return itinerary
    
    async def _generate_day_plan(
        self,
        day: int,
        date: str,
        attractions: List[Dict],
        pace: str
    ) -> Dict:
        """生成单日详细计划"""
        
        activities = []
        
        # 设置开始时间
        if pace == "悠闲":
            start_hour = 9
        elif pace == "适中":
            start_hour = 8
        else:
            start_hour = 7
        
        current_time = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=start_hour, minute=0
        )
        
        for i, attraction in enumerate(attractions):
            # 添加交通时间
            if i > 0:
                transport_time = await self._get_transport_time(
                    from_location=attractions[i-1],
                    to_location=attraction
                )
                current_time += timedelta(minutes=transport_time)
                
                activities.append({
                    "type": "transport",
                    "from": attractions[i-1]["name"],
                    "to": attraction["name"],
                    "duration": transport_time,
                    "start_time": current_time.strftime("%H:%M"),
                    "estimated_cost": self._estimate_transport_cost(transport_time)
                })
                
                current_time += timedelta(minutes=transport_time)
            
            # 添加景点活动
            visit_duration = attraction.get("suggested_duration", 120)
            
            activities.append({
                "type": "attraction",
                "name": attraction["name"],
                "address": attraction["address"],
                "duration": visit_duration,
                "ticket_price": attraction.get("ticket_price", 0),
                "rating": attraction.get("rating"),
                "description": attraction.get("description"),
                "start_time": current_time.strftime("%H:%M"),
                "end_time": (current_time + timedelta(minutes=visit_duration)).strftime("%H:%M"),
                "tips": attraction.get("tips", [])
            })
            
            current_time += timedelta(minutes=visit_duration)
            
            # 添加用餐
            if current_time.hour in [12, 13]:
                meal = await self.restaurant_service.suggest_nearby(
                    location=attraction,
                    meal_type="lunch"
                )
                if meal:
                    activities.append({
                        "type": "meal",
                        "name": meal["name"],
                        "cuisine": meal["cuisine"],
                        "average_price": meal["average_price"],
                        "rating": meal["rating"],
                        "duration": 60,
                        "start_time": current_time.strftime("%H:%M")
                    })
                    current_time += timedelta(minutes=60)
        
        return {
            "day": day,
            "date": date,
            "activities": activities,
            "summary": {
                "total_attractions": len(attractions),
                "total_activities": len(activities),
                "estimated_cost": sum(
                    a.get("ticket_price", 0) + a.get("estimated_cost", 0)
                    for a in activities
                )
            }
        }
```

---

## 3. 多源数据爬取模块

### 3.1 爬虫调度器

```python
# backend/services/crawler/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class CrawlerScheduler:
    """爬虫调度器"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.crawlers = {}
        
    def register_crawler(
        self,
        name: str,
        crawler_class,
        schedule: str,
        params: Dict
    ):
        """注册爬虫"""
        
        crawler = crawler_class(**params)
        self.crawlers[name] = crawler
        
        # 添加定时任务
        if schedule == "hourly":
            self.scheduler.add_job(
                self._run_crawler,
                'interval',
                hours=1,
                args=[name],
                id=f"{name}_hourly"
            )
        elif schedule == "daily":
            self.scheduler.add_job(
                self._run_crawler,
                'interval',
                days=1,
                args=[name],
                id=f"{name}_daily"
            )
        elif schedule == "weekly":
            self.scheduler.add_job(
                self._run_crawler,
                'interval',
                weeks=1,
                args=[name],
                id=f"{name}_weekly"
            )
        
        logger.info(f"Registered crawler: {name} (schedule: {schedule})")
    
    async def _run_crawler(self, name: str):
        """运行爬虫"""
        
        logger.info(f"Starting crawler: {name}")
        
        try:
            crawler = self.crawlers[name]
            data = await crawler.run()
            
            # 存储数据
            await self._store_data(name, data)
            
            logger.info(f"Crawler {name} completed: {len(data)} items")
            
        except Exception as e:
            logger.error(f"Crawler {name} failed: {e}")
    
    async def _store_data(self, crawler_name: str, data: List[Dict]):
        """存储爬取的数据"""
        # 实现数据存储逻辑
        pass
    
    def start(self):
        """启动调度器"""
        self.scheduler.start()
        logger.info("Crawler scheduler started")
    
    def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        logger.info("Crawler scheduler stopped")
```

### 3.2 景点数据爬取示例

```python
# crawler/spiders/attraction_spider.py
import scrapy
from typing import Dict, List
import json
from datetime import datetime

class CtripAttractionSpider(scrapy.Spider):
    """携程景点爬虫"""
    
    name = 'ctrip_attraction'
    
    def __init__(self, cities: List[str] = None):
        super().__init__()
        self.cities = cities or ['北京', '上海', '广州']
        self.base_url = "https://you.ctrip.com/sight"
    
    def start_requests(self):
        """生成初始请求"""
        
        for city in self.cities:
            url = f"{self.base_url}/{city}"
            yield scrapy.Request(
                url=url,
                callback=self.parse_city,
                meta={'city': city}
            )
    
    def parse_city(self, response):
        """解析城市景点列表"""
        
        city = response.meta['city']
        
        # 提取景点列表
        attractions = response.css('.sight-item')
        
        for attraction in attractions:
            # 提取基本信息
            item = {
                'name': self._clean_text(attraction.css('.title::text').get()),
                'rating': self._extract_rating(attraction),
                'price': self._extract_price(attraction),
                'address': self._clean_text(attraction.css('.address::text').get()),
                'description': self._clean_text(attraction.css('.desc::text').get()),
                'image_url': self._extract_image(attraction),
                'tags': self._extract_tags(attraction),
                'source': 'ctrip',
                'crawl_time': datetime.now().isoformat()
            }
            
            # 提取详情链接
            detail_link = attraction.css('a::attr(href)').get()
            if detail_link:
                yield response.follow(
                    detail_link,
                    callback=self.parse_detail,
                    meta={'item': item}
                )
            else:
                yield item
    
    def parse_detail(self, response):
        """解析景点详情"""
        
        item = response.meta['item']
        
        # 提取详细信息
        item.update({
            'opening_hours': self._extract_opening_hours(response),
            'suggested_duration': self._extract_duration(response),
            'location': self._extract_location(response),
            'reviews_count': self._extract_reviews_count(response),
            'popularity_score': self._calculate_popularity(item, response)
        })
        
        yield item
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        return text.strip()
    
    def _extract_rating(self, attraction) -> float:
        """提取评分"""
        rating_text = attraction.css('.score::text').get()
        if rating_text:
            try:
                return float(rating_text)
            except ValueError:
                pass
        return 0.0
    
    def _extract_price(self, attraction) -> float:
        """提取价格"""
        price_text = attraction.css('.price::text').get()
        if price_text:
            # 提取数字
            import re
            match = re.search(r'\d+', price_text)
            if match:
                return float(match.group())
        return 0.0
    
    def _extract_image(self, attraction) -> str:
        """提取图片URL"""
        img_url = attraction.css('img::attr(src)').get()
        if img_url:
            # 处理URL
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            return img_url
        return ""
    
    def _extract_tags(self, attraction) -> List[str]:
        """提取标签"""
        tags = []
        tag_elements = attraction.css('.tag::text')
        for tag in tag_elements:
            tag_text = self._clean_text(tag.get())
            if tag_text:
                tags.append(tag_text)
        return tags
    
    def _extract_opening_hours(self, response) -> Dict:
        """提取开放时间"""
        # 实现开放时间提取逻辑
        return {}
    
    def _extract_duration(self, response) -> int:
        """提取建议游览时长"""
        # 实现时长提取逻辑
        return 120
    
    def _extract_location(self, response) -> Dict:
        """提取地理位置"""
        # 实现地理位置提取逻辑
        return {"latitude": 0.0, "longitude": 0.0}
    
    def _extract_reviews_count(self, response) -> int:
        """提取评论数量"""
        # 实现评论数提取逻辑
        return 0
    
    def _calculate_popularity(self, item: Dict, response) -> int:
        """计算热度分数"""
        # 基于评分、评论数、收藏数等计算
        score = item['rating'] * 100
        return int(score)
```

---

## 4. 预算计算模块

### 4.1 预算计算服务

```python
# backend/services/planning/budget_calculator.py
from typing import Dict
from datetime import datetime

class BudgetCalculator:
    """预算计算器"""
    
    def __init__(self, price_monitor, accommodation_service):
        self.price_monitor = price_monitor
        self.accommodation_service = accommodation_service
    
    async def calculate(
        self,
        itinerary: Dict,
        travelers: int,
        budget: float = None
    ) -> Dict:
        """
        计算行程预算
        
        Args:
            itinerary: 行程数据
            travelers: 人数
            budget: 用户预算（可选）
            
        Returns:
            详细预算分解
        """
        
        breakdown = {
            "transport": 0,
            "accommodation": 0,
            "food": 0,
            "tickets": 0,
            "other": 0,
            "total": 0,
            "per_person": 0,
            "details": {}
        }
        
        # 1. 交通费用
        transport_cost = await self._calculate_transport(
            itinerary=itinerary,
            travelers=travelers
        )
        breakdown["transport"] = transport_cost
        
        # 2. 住宿费用
        accommodation_cost = await self._calculate_accommodation(
            itinerary=itinerary,
            travelers=travelers
        )
        breakdown["accommodation"] = accommodation_cost
        
        # 3. 餐饮费用
        food_cost = await self._calculate_food(
            itinerary=itinerary,
            travelers=travelers
        )
        breakdown["food"] = food_cost
        
        # 4. 门票费用
        tickets_cost = await self._calculate_tickets(
            itinerary=itinerary,
            travelers=travelers
        )
        breakdown["tickets"] = tickets_cost
        
        # 5. 其他费用（预留20%）
        other_cost = (transport_cost + accommodation_cost + food_cost + tickets_cost) * 0.2
        breakdown["other"] = other_cost
        
        # 总计
        breakdown["total"] = (
            transport_cost +
            accommodation_cost +
            food_cost +
            tickets_cost +
            other_cost
        )
        
        breakdown["per_person"] = breakdown["total"] / travelers
        
        # 预算对比
        if budget:
            breakdown["budget"] = budget
            breakdown["budget_per_person"] = budget / travelers
            breakdown["over_budget"] = breakdown["total"] > budget
            breakdown["diff"] = breakdown["total"] - budget
            breakdown["diff_percentage"] = (
                (breakdown["total"] - budget) / budget * 100
            )
        
        return breakdown
    
    async def _calculate_transport(
        self,
        itinerary: Dict,
        travelers: int
    ) -> float:
        """计算交通费用"""
        
        total = 0.0
        
        for day_plan in itinerary["daily_plans"]:
            for activity in day_plan["activities"]:
                if activity["type"] == "transport":
                    cost = activity.get("estimated_cost", 0)
                    total += cost * travelers
        
        # 添加往返大交通（从出发地到目的地）
        # 这里简化处理，实际应该调用价格监控服务
        round_trip_cost = await self.price_monitor.get_transport_price(
            from_city="出发城市",
            to_city=itinerary["destination"],
            date=itinerary["start_date"]
        )
        total += round_trip_cost * travelers
        
        return total
    
    async def _calculate_accommodation(
        self,
        itinerary: Dict,
        travelers: int
    ) -> float:
        """计算住宿费用"""
        
        nights = itinerary["days"] - 1
        
        # 获取平均住宿价格
        avg_price = await self.accommodation_service.get_average_price(
            destination=itinerary["destination"],
            date=itinerary["start_date"],
            guests=travelers
        )
        
        # 需要的房间数（假设每间房最多住2人）
        rooms = max(1, travelers // 2)
        
        return avg_price * nights * rooms
    
    async def _calculate_food(
        self,
        itinerary: Dict,
        travelers: int
    ) -> float:
        """计算餐饮费用"""
        
        total = 0.0
        
        for day_plan in itinerary["daily_plans"]:
            for activity in day_plan["activities"]:
                if activity["type"] == "meal":
                    price = activity.get("average_price", 0)
                    total += price * travelers
        
        return total
    
    async def _calculate_tickets(
        self,
        itinerary: Dict,
        travelers: int
    ) -> float:
        """计算门票费用"""
        
        total = 0.0
        
        for day_plan in itinerary["daily_plans"]:
            for activity in day_plan["activities"]:
                if activity["type"] == "attraction":
                    price = activity.get("ticket_price", 0)
                    total += price * travelers
        
        return total
```

---

## 5. 前端交互演示

### 5.1 对话组件

```tsx
// frontend/src/components/Chat/ChatInterface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { apiService } from '../../services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '你好！我是你的AI旅行规划师。请告诉我你想去哪里玩？',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // 调用AI接口
      const response = await apiService.chat({
        message: input,
        history: messages.map(m => ({
          role: m.role,
          content: m.content
        }))
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '抱歉，我遇到了一些问题。请稍后再试。',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* 消息列表 */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </Box>

      {/* 输入框 */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="告诉我你想去哪里玩..."
            disabled={loading}
            variant="outlined"
          />
          <Button
            variant="contained"
            onClick={handleSend}
            disabled={loading || !input.trim()}
            endIcon={<SendIcon />}
          >
            发送
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2
      }}
    >
      <Paper
        elevation={1}
        sx={{
          p: 2,
          maxWidth: '70%',
          bgcolor: isUser ? 'primary.main' : 'grey.100',
          color: isUser ? 'white' : 'text.primary',
          borderRadius: 2
        }}
      >
        <Typography variant="body1">{message.content}</Typography>
        <Typography variant="caption" sx={{ opacity: 0.7, mt: 1, display: 'block' }}>
          {message.timestamp.toLocaleTimeString()}
        </Typography>
      </Paper>
    </Box>
  );
};
```

---

## 总结

以上代码展示了AI旅行规划软件的核心功能实现：

1. **AI需求理解**：使用GPT-4o深度理解用户需求
2. **智能路线规划**：基于TSP算法优化路线
3. **多源数据爬取**：Scrapy + Playwright爬取实时数据
4. **预算计算**：详细的费用分解
5. **前端交互**：React实现友好的对话界面

这些代码可以直接用于项目开发，后续可以根据实际需求进行调整和优化。

---

**文档版本**：v1.0
**创建时间**：2026-02-18
