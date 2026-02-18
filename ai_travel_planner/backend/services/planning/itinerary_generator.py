"""
行程生成器 - 核心规划算法
实现智能路线规划，优化时间安排和体验
"""
import json
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import numpy as np
from loguru import logger


@dataclass
class Attraction:
    """景点数据类"""
    id: int
    name: str
    category: str
    latitude: float
    longitude: float
    rating: float
    recommended_duration: int  # 建议游览时长（分钟）
    opening_hours: Dict[str, List[Tuple[int, int]]]
    ticket_price: float
    best_time_to_visit: str
    tags: List[str]


@dataclass
class Restaurant:
    """餐厅数据类"""
    id: int
    name: str
    cuisine_type: str
    price_level: int  # 1-5
    avg_price_per_person: float
    rating: float
    latitude: float
    longitude: float
    opening_hours: Dict[str, List[Tuple[int, int]]]


class ItineraryGenerator:
    """行程生成器"""
    
    def __init__(self):
        self.attractions_db = self._load_sample_attractions()
        self.restaurants_db = self._load_sample_restaurants()
        
    def _load_sample_attractions(self) -> Dict[str, List[Attraction]]:
        """加载示例景点数据库"""
        # 模拟数据 - 生产环境应从数据库读取
        return {
            "京都": [
                Attraction(1, "清水寺", "历史文化", 34.9949, 135.7850, 4.5, 120,
                          {"mon": [(6, 18)], "tue": [(6, 18)]}, 30.0,
                          "清晨", ["历史", "建筑", "摄影"]),
                Attraction(2, "伏见稻荷大社", "历史文化", 34.9671, 135.7727, 4.6, 180,
                          {"mon": [(0, 24)]}, 0.0, "全天", ["自然", "摄影", "徒步"]),
                Attraction(3, "金阁寺", "历史文化", 35.0394, 135.7292, 4.4, 60,
                          {"mon": [(9, 17)]}, 40.0, "上午", ["历史", "建筑"]),
                Attraction(4, "二条城", "历史文化", 35.0140, 135.7481, 4.3, 90,
                          {"mon": [(8.75, 17)]}, 50.0, "上午", ["历史", "文化"]),
                Attraction(5, "岚山竹林", "自然风光", 35.0094, 135.6719, 4.5, 90,
                          {"mon": [(8, 17)]}, 0.0, "下午", ["自然", "摄影"]),
                Attraction(6, "锦市场", "美食购物", 35.0047, 135.7636, 4.2, 120,
                          {"mon": [(9, 18)]}, 0.0, "上午", ["美食", "购物"]),
            ],
            "东京": [
                Attraction(11, "浅草寺", "历史文化", 35.7148, 139.7967, 4.3, 90,
                          {"mon": [(6, 17)]}, 0.0, "上午", ["历史", "文化"]),
                Attraction(12, "东京塔", "观光", 35.6586, 139.7454, 4.2, 60,
                          {"mon": [(9, 23)]}, 30.0, "傍晚", ["观光", "夜景"]),
                Attraction(13, "明治神宫", "历史文化", 35.6764, 139.6993, 4.4, 60,
                          {"mon": [(5, 18)]}, 0.0, "上午", ["历史", "自然"]),
                Attraction(14, "新宿御苑", "自然风光", 35.6851, 139.7104, 4.3, 120,
                          {"mon": [(9, 16)]}, 5.0, "上午", ["自然", "散步"]),
                Attraction(15, "银座", "购物", 35.6717, 139.7640, 4.4, 180,
                          {"mon": [(10, 20)]}, 0.0, "下午", ["购物", "美食"]),
            ],
        }
    
    def _load_sample_restaurants(self) -> Dict[str, List[Restaurant]]:
        """加载示例餐厅数据库"""
        return {
            "京都": [
                Restaurant(1, "怀石料理 某某店", "日式", 5, 300.0, 4.5, 35.0085, 135.7726,
                          {"mon": [(11, 14), (17, 21)]}),
                Restaurant(2, "拉面店", "日式", 1, 15.0, 4.2, 35.0112, 135.7681,
                          {"mon": [(11, 22)]}),
                Restaurant(3, "居酒屋", "日式", 2, 40.0, 4.3, 35.0058, 135.7650,
                          {"mon": [(17, 23)]}),
            ],
            "东京": [
                Restaurant(11, "寿司店", "日式", 4, 200.0, 4.6, 35.6580, 139.7454,
                          {"mon": [(11, 14), (17, 21)]}),
                Restaurant(12, "拉面店", "日式", 1, 12.0, 4.1, 35.7023, 139.7744,
                          {"mon": [(11, 23)]}),
            ],
        }
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        计算两点之间的距离（Haversine公式）
        返回：公里数
        """
        from math import radians, cos, sin, sqrt, atan2
        
        R = 6371  # 地球半径（公里）
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        
        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def solve_tsp(self, attractions: List[Attraction]) -> List[Attraction]:
        """
        解决旅行商问题（TSP）- 使用贪心算法
        优化路线，减少往返时间
        """
        if len(attractions) <= 2:
            return attractions
        
        # 使用贪心算法：每次选择最近的下一个景点
        visited = [attractions[0]]
        remaining = attractions[1:]
        
        while remaining:
            current = visited[-1]
            # 找到最近的景点
            next_attraction = min(
                remaining,
                key=lambda a: self.calculate_distance(
                    current.latitude, current.longitude,
                    a.latitude, a.longitude
                )
            )
            visited.append(next_attraction)
            remaining.remove(next_attraction)
        
        return visited
    
    def filter_attractions_by_preferences(
        self,
        attractions: List[Attraction],
        preferences: Dict[str, Any]
    ) -> List[Attraction]:
        """根据偏好筛选景点"""
        filtered = attractions
        
        # 根据兴趣标签筛选
        if "interests" in preferences and preferences["interests"]:
            filtered = [
                a for a in filtered
                if any(tag in a.tags for tag in preferences["interests"])
            ]
        
        # 根据评分筛选
        min_rating = preferences.get("min_rating", 4.0)
        filtered = [a for a in filtered if a.rating >= min_rating]
        
        return filtered
    
    def recommend_attractions_for_day(
        self,
        destination: str,
        day_index: int,
        preferences: Dict[str, Any]
    ) -> List[Attraction]:
        """为某天推荐景点"""
        attractions = self.attractions_db.get(destination, [])
        
        # 筛选景点
        filtered = self.filter_attractions_by_preferences(attractions, preferences)
        
        # 如果筛选后景点太少，返回所有景点
        if len(filtered) < 3:
            filtered = attractions
        
        # 根据天数轮换景点
        attractions_per_day = min(len(filtered), 3)
        start_idx = (day_index * attractions_per_day) % len(filtered)
        day_attractions = filtered[start_idx:start_idx + attractions_per_day]
        
        # 优化路线
        if len(day_attractions) > 1:
            day_attractions = self.solve_tsp(day_attractions)
        
        return day_attractions
    
    def recommend_restaurant(
        self,
        destination: str,
        meal_type: str,  # lunch/dinner
        price_level: int = None
    ) -> Optional[Restaurant]:
        """推荐餐厅"""
        restaurants = self.restaurants_db.get(destination, [])
        
        if not restaurants:
            return None
        
        # 根据价格等级筛选
        if price_level:
            restaurants = [r for r in restaurants if r.price_level <= price_level]
        
        if not restaurants:
            return None
        
        # 根据用餐类型选择（午餐选择便宜的，晚餐选择好的）
        if meal_type == "lunch":
            candidates = [r for r in restaurants if r.price_level <= 2]
        else:  # dinner
            candidates = [r for r in restaurants if r.price_level >= 2]
        
        if not candidates:
            candidates = restaurants
        
        # 随机选择一个（生产环境可以用更复杂的推荐算法）
        return random.choice(candidates)
    
    def generate_daily_plan(
        self,
        destination: str,
        day_index: int,
        date: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成单日行程"""
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday = date_obj.strftime("%a").lower()
        
        # 推荐景点
        attractions = self.recommend_attractions_for_day(destination, day_index, preferences)
        
        # 推荐餐厅
        lunch = self.recommend_restaurant(destination, "lunch", preferences.get("price_level"))
        dinner = self.recommend_restaurant(destination, "dinner", preferences.get("price_level"))
        
        # 生成时间安排
        timeline = []
        current_time = 9  # 9:00开始
        
        # 上午景点
        if attractions:
            attraction = attractions[0]
            end_time = current_time + attraction.recommended_duration / 60
            timeline.append({
                "time": f"{current_time:02d}:00-{int(end_time):02d}:{(end_time%1)*60:02.0f}",
                "activity": "景点游览",
                "location": attraction.name,
                "category": attraction.category,
                "ticket_price": attraction.ticket_price,
                "tips": f"建议游览{attraction.recommended_duration}分钟"
            })
            current_time = end_time + 0.5  # 30分钟转场
            
            # 午餐
            if lunch:
                timeline.append({
                    "time": f"{int(current_time):02d}:00-{int(current_time+1.5):02d}:00",
                    "activity": "午餐",
                    "location": lunch.name,
                    "cuisine": lunch.cuisine_type,
                    "estimated_cost": lunch.avg_price_per_person,
                    "tips": "推荐尝试当地特色"
                })
                current_time += 1.5
        
        # 下午景点
        if len(attractions) > 1:
            attraction = attractions[1]
            end_time = current_time + attraction.recommended_duration / 60
            timeline.append({
                "time": f"{int(current_time):02d}:00-{int(end_time):02d}:{(end_time%1)*60:02.0f}",
                "activity": "景点游览",
                "location": attraction.name,
                "category": attraction.category,
                "ticket_price": attraction.ticket_price,
                "tips": "下午光线适合拍照"
            })
            current_time = end_time + 0.5
        
        # 晚餐
        if dinner:
            timeline.append({
                "time": f"{int(current_time):02d}:00-{int(current_time+2):02d}:00",
                "activity": "晚餐",
                "location": dinner.name,
                "cuisine": dinner.cuisine_type,
                "estimated_cost": dinner.avg_price_per_person,
                "tips": "享受当地美食"
            })
        
        return {
            "day": day_index + 1,
            "date": date,
            "weekday": weekday,
            "attractions": [a.__dict__ for a in attractions],
            "restaurants": {
                "lunch": lunch.__dict__ if lunch else None,
                "dinner": dinner.__dict__ if dinner else None
            },
            "timeline": timeline,
            "estimated_cost": sum(
                item.get("estimated_cost", 0) or item.get("ticket_price", 0)
                for item in timeline
            )
        }
    
    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        start_date: str,
        travelers: int,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成完整行程
        
        Args:
            destination: 目的地
            days: 天数
            start_date: 开始日期
            travelers: 人数
            preferences: 偏好设置
        
        Returns:
            完整行程
        """
        logger.info(f"Generating itinerary: {destination}, {days} days")
        
        # 验证目的地
        if destination not in self.attractions_db:
            available = ", ".join(self.attractions_db.keys())
            raise ValueError(
                f"暂不支持目的地 '{destination}'。"
                f"目前支持：{available}"
            )
        
        # 生成每日行程
        daily_plans = []
        total_cost = 0
        
        for day in range(days):
            date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)).strftime("%Y-%m-%d")
            
            try:
                daily_plan = self.generate_daily_plan(
                    destination, day, date, preferences
                )
                daily_plans.append(daily_plan)
                total_cost += daily_plan["estimated_cost"]
            except Exception as e:
                logger.warning(f"Failed to generate plan for day {day + 1}: {e}")
        
        # 生成住宿建议
        accommodation = self._recommend_accommodation(destination, days, preferences)
        
        # 生成交通建议
        transportation = self._recommend_transportation(destination, days)
        
        return {
            "destination": destination,
            "title": f"{destination}{days}日深度游",
            "days": days,
            "start_date": start_date,
            "end_date": (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=days-1)).strftime("%Y-%m-%d"),
            "travelers": travelers,
            "daily_plans": daily_plans,
            "accommodation": accommodation,
            "transportation": transportation,
            "budget": {
                "total": total_cost * travelers + accommodation.get("total_cost", 0) + transportation.get("total_cost", 0),
                "per_person": (total_cost + accommodation.get("total_cost", 0)/travelers + transportation.get("total_cost", 0)/travelers),
                "breakdown": {
                    "attractions": total_cost * travelers,
                    "food": sum(d.get("estimated_cost", 0) for d in daily_plans) * travelers,
                    "accommodation": accommodation.get("total_cost", 0),
                    "transportation": transportation.get("total_cost", 0),
                    "other": 0
                }
            },
            "tips": self._generate_tips(destination, days),
            "generated_at": datetime.now().isoformat()
        }
    
    def _recommend_accommodation(
        self,
        destination: str,
        days: int,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """推荐住宿"""
        # 简化实现，生产环境应从数据库读取
        avg_price = {
            "京都": 500,
            "东京": 700,
            "大阪": 450,
        }.get(destination, 500)
        
        return {
            "type": preferences.get("accommodation_type", "酒店"),
            "suggestion": "选择市中心交通便利的酒店",
            "estimated_price_per_night": avg_price,
            "total_cost": avg_price * days,
            "tips": "提前预订可享受优惠"
        }
    
    def _recommend_transportation(
        self,
        destination: str,
        days: int
    ) -> Dict[str, Any]:
        """推荐交通方式"""
        # 简化实现
        transport_options = {
            "京都": {
                "local": "巴士/地铁通票",
                "cost": 50,
                "description": "京都市内交通推荐购买一日通票"
            },
            "东京": {
                "local": "地铁/电车",
                "cost": 80,
                "description": "推荐购买Suica卡或一日通票"
            },
        }
        
        option = transport_options.get(destination, {
            "local": "公共交通",
            "cost": 60,
            "description": "当地公共交通便利"
        })
        
        return {
            "to_destination": f"前往{destination}（请根据出发地选择交通方式）",
            "local": option["local"],
            "cost": option["cost"] * days,
            "total_cost": option["cost"] * days,
            "description": option["description"]
        }
    
    def _generate_tips(self, destination: str, days: int) -> List[str]:
        """生成旅行贴士"""
        tips = [
            "建议提前预订热门景点门票",
            "准备现金，部分小店不支持信用卡",
            "学习几句基本的当地问候语",
            "随身携带充电宝",
        ]
        
        if days >= 5:
            tips.append("行程较长，注意合理安排休息时间")
        
        if destination == "京都":
            tips.extend([
                "京都很多景点需要脱鞋，建议穿舒适的鞋子",
                "清水寺和金阁寺早上人少，建议早去"
            ])
        
        return tips


# 单例
_itinerary_generator = None

def get_itinerary_generator() -> ItineraryGenerator:
    """获取行程生成器单例"""
    global _itinerary_generator
    if _itinerary_generator is None:
        _itinerary_generator = ItineraryGenerator()
    return _itinerary_generator
