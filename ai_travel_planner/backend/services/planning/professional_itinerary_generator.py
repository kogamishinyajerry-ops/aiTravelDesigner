"""
专业行程生成器 V2
基于专业旅行规划师标准，提供规范化、标准化的行程规划服务
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import numpy as np
from loguru import logger

from .professional_standards import (
    TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType,
    TravelRequirements, ProfessionalItinerary, ProfessionalPlanningStandards,
    SeasonalGuidelines, QualityChecklist
)
from .itinerary_generator import Attraction, Restaurant


@dataclass
class ProfessionalAttraction(Attraction):
    """专业景点数据 - 扩展版"""
    # 专业属性
    best_seasons: List[str] = field(default_factory=list)
    crowd_level: str = "medium"  # low/medium/high
    photography_quality: int = 3  # 1-5
    family_friendly: bool = True
    accessibility: str = "good"  # excellent/good/poor
    nearby_restaurants: int = 0
    ticket_booking_required: bool = False
    indoor_outdoor: str = "mixed"  # indoor/outdoor/mixed
    weather_dependency: bool = False
    minimum_time_needed: int = 60  # 最少需要时间（分钟）
    
    # 装备要求
    equipment_needed: List[str] = field(default_factory=list)
    clothing_suggestions: List[str] = field(default_factory=list)


@dataclass
class ProfessionalRestaurant(Restaurant):
    """专业餐厅数据 - 扩展版"""
    # 专业属性
    must_try_dishes: List[str] = field(default_factory=list)
    advance_booking_required: bool = False
    dress_code: str = "casual"  # casual/smart_casual/formal
    seating_options: List[str] = field(default_factory=list)  # indoor/outdoor/private
    noise_level: str = "moderate"  # quiet/moderate/loud
    family_friendly: bool = True
    special_dietary_options: List[str] = field(default_factory=list)
    average_wait_time: int = 15  # 分钟
    michelin_starred: bool = False
    local_favorite: bool = True


@dataclass
class TimeSlot:
    """时间槽 - 标准化时间管理"""
    start_time: float  # 9.0 表示9:00
    end_time: float
    activity_type: str  # attraction/meal/transit/rest
    activity_name: str
    location: str
    duration: float  # 小时
    notes: str = ""
    cost: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "time_range": f"{int(self.start_time):02d}:{int((self.start_time % 1) * 60):02d} - "
                         f"{int(self.end_time):02d}:{int((self.end_time % 1) * 60):02d}",
            "activity_type": self.activity_type,
            "activity_name": self.activity_name,
            "location": self.location,
            "duration_hours": self.duration,
            "notes": self.notes,
            "cost": self.cost
        }


class ProfessionalItineraryGenerator:
    """专业行程生成器 V2"""
    
    def __init__(self):
        self.standards = ProfessionalPlanningStandards()
        self.attractions_db = self._load_professional_attractions()
        self.restaurants_db = self._load_professional_restaurants()
        logger.info("Professional Itinerary Generator initialized")
    
    def _load_professional_attractions(self) -> Dict[str, List[ProfessionalAttraction]]:
        """加载专业景点数据库"""
        return {
            "京都": [
                ProfessionalAttraction(
                    id=1, name="清水寺", category="历史文化",
                    latitude=34.9949, longitude=135.7850, rating=4.5,
                    recommended_duration=120, opening_hours={"mon": [(6, 18)]},
                    ticket_price=30.0, best_time_to_visit="清晨",
                    tags=["历史", "建筑", "摄影"],
                    best_seasons=["spring", "autumn"],
                    crowd_level="high", photography_quality=5,
                    family_friendly=True, accessibility="moderate",
                    nearby_restaurants=10, ticket_booking_required=True,
                    indoor_outdoor="mixed", weather_dependency=False,
                    minimum_time_needed=90,
                    equipment_needed=["相机"], clothing_suggestions=["舒适鞋"]
                ),
                ProfessionalAttraction(
                    id=2, name="伏见稻荷大社", category="历史文化",
                    latitude=34.9671, longitude=135.7727, rating=4.6,
                    recommended_duration=180, opening_hours={"mon": [(0, 24)]},
                    ticket_price=0.0, best_time_to_visit="清晨",
                    tags=["自然", "摄影", "徒步"],
                    best_seasons=["all"], crowd_level="high",
                    photography_quality=5, family_friendly=True,
                    accessibility="poor", nearby_restaurants=5,
                    ticket_booking_required=False, indoor_outdoor="outdoor",
                    weather_dependency=True, minimum_time_needed=120,
                    equipment_needed=[], clothing_suggestions=["舒适鞋", "防晒"]
                ),
                ProfessionalAttraction(
                    id=3, name="金阁寺", category="历史文化",
                    latitude=35.0394, longitude=135.7292, rating=4.4,
                    recommended_duration=60, opening_hours={"mon": [(9, 17)]},
                    ticket_price=40.0, best_time_to_visit="上午",
                    tags=["历史", "建筑"],
                    best_seasons=["all"], crowd_level="high",
                    photography_quality=5, family_friendly=True,
                    accessibility="good", nearby_restaurants=3,
                    ticket_booking_required=False, indoor_outdoor="outdoor",
                    weather_dependency=True, minimum_time_needed=60,
                    equipment_needed=["相机"], clothing_suggestions=[]
                ),
            ],
            "东京": [
                ProfessionalAttraction(
                    id=11, name="浅草寺", category="历史文化",
                    latitude=35.7148, longitude=139.7967, rating=4.3,
                    recommended_duration=90, opening_hours={"mon": [(6, 17)]},
                    ticket_price=0.0, best_time_to_visit="上午",
                    tags=["历史", "文化"],
                    best_seasons=["all"], crowd_level="high",
                    photography_quality=4, family_friendly=True,
                    accessibility="good", nearby_restaurants=15,
                    ticket_booking_required=False, indoor_outdoor="mixed",
                    weather_dependency=False, minimum_time_needed=60,
                    equipment_needed=[], clothing_suggestions=["得体着装"]
                ),
                ProfessionalAttraction(
                    id=12, name="东京塔", category="观光",
                    latitude=35.6586, longitude=139.7454, rating=4.2,
                    recommended_duration=60, opening_hours={"mon": [(9, 23)]},
                    ticket_price=30.0, best_time_to_visit="傍晚",
                    tags=["观光", "夜景"],
                    best_seasons=["all"], crowd_level="medium",
                    photography_quality=5, family_friendly=True,
                    accessibility="excellent", nearby_restaurants=8,
                    ticket_booking_required=False, indoor_outdoor="mixed",
                    weather_dependency=False, minimum_time_needed=45,
                    equipment_needed=["相机"], clothing_suggestions=[]
                ),
            ],
        }
    
    def _load_professional_restaurants(self) -> Dict[str, List[ProfessionalRestaurant]]:
        """加载专业餐厅数据库"""
        return {
            "京都": [
                ProfessionalRestaurant(
                    id=1, name="怀石料理 某某店", cuisine_type="日式",
                    price_level=5, avg_price_per_person=300.0, rating=4.5,
                    latitude=35.0085, longitude=135.7726,
                    opening_hours={"mon": [(11, 14), (17, 21)]},
                    must_try_dishes=["怀石料理套餐", "抹茶甜点"],
                    advance_booking_required=True, dress_code="smart_casual",
                    seating_options=["indoor", "private"], noise_level="quiet",
                    family_friendly=False, special_dietary_options=["素食"],
                    average_wait_time=0, michelin_starred=True,
                    local_favorite=True
                ),
                ProfessionalRestaurant(
                    id=2, name="拉面店", cuisine_type="日式",
                    price_level=1, avg_price_per_person=15.0, rating=4.2,
                    latitude=35.0112, longitude=135.7681,
                    opening_hours={"mon": [(11, 22)]},
                    must_try_dishes=["豚骨拉面", "煎饺"],
                    advance_booking_required=False, dress_code="casual",
                    seating_options=["indoor"], noise_level="moderate",
                    family_friendly=True, special_dietary_options=[],
                    average_wait_time=15, michelin_starred=False,
                    local_favorite=True
                ),
            ],
            "东京": [
                ProfessionalRestaurant(
                    id=11, name="寿司店", cuisine_type="日式",
                    price_level=4, avg_price_per_person=200.0, rating=4.6,
                    latitude=35.6580, longitude=139.7454,
                    opening_hours={"mon": [(11, 14), (17, 21)]},
                    must_try_dishes=["握寿司", "刺身"],
                    advance_booking_required=True, dress_code="smart_casual",
                    seating_options=["indoor", "counter"], noise_level="quiet",
                    family_friendly=False, special_dietary_options=[],
                    average_wait_time=0, michelin_starred=True,
                    local_favorite=True
                ),
            ],
        }
    
    async def generate_professional_itinerary(
        self,
        requirements: TravelRequirements
    ) -> ProfessionalItinerary:
        """
        生成专业行程 - 核心方法
        
        Args:
            requirements: 旅行需求（标准化）
        
        Returns:
            专业行程对象
        """
        logger.info(f"Generating professional itinerary for {requirements.destination}")
        
        # 验证需求
        is_valid, errors = requirements.validate()
        if not is_valid:
            raise ValueError(f"需求验证失败: {', '.join(errors)}")
        
        # 生成每日行程
        daily_plans = []
        for day in range(requirements.days):
            date = (datetime.strptime(requirements.start_date, "%Y-%m-%d") + 
                   timedelta(days=day)).strftime("%Y-%m-%d")
            
            daily_plan = await self._generate_professional_daily_plan(
                requirements, day, date
            )
            daily_plans.append(daily_plan)
        
        # 生成住宿建议
        accommodation = self._recommend_professional_accommodation(requirements)
        
        # 生成交通建议
        transportation = self._recommend_professional_transportation(requirements)
        
        # 计算预算
        from .budget_calculator import get_budget_calculator
        budget_calculator = get_budget_calculator()
        budget = await budget_calculator.calculate_total_budget(
            departure=requirements.departure_city,
            destination=requirements.destination,
            days=requirements.days,
            travelers=requirements.total_travelers(),
            preferences={
                "room_type": requirements.budget_level.value,
                "meal_level": requirements.budget_level.value
            }
        )
        
        # 质量检查
        quality_results = self._perform_quality_check(daily_plans)
        
        # 创建专业行程对象
        itinerary = ProfessionalItinerary(
            itinerary_id=f"ITIN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            requirements=requirements,
            created_at=datetime.now(),
            status="draft",
            daily_plans=daily_plans,
            accommodation=accommodation,
            transportation=transportation,
            budget_breakdown=budget,
            planning_notes=quality_results.get("notes", []),
            recommendations=quality_results.get("recommendations", []),
            warnings=quality_results.get("warnings", []),
            version=1,
            last_modified=datetime.now()
        )
        
        logger.info(f"Professional itinerary generated: {itinerary.itinerary_id}")
        return itinerary
    
    async def _generate_professional_daily_plan(
        self,
        requirements: TravelRequirements,
        day_index: int,
        date: str
    ) -> Dict[str, Any]:
        """生成单日专业行程"""
        # 获取日期信息
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday = date_obj.strftime("%a").lower()
        month = date_obj.month
        
        # 获取季节性建议
        seasonal_tips = SeasonalGuidelines.get_seasonal_tips(
            requirements.destination, month
        )
        
        # 推荐景点
        attractions = self._recommend_professional_attractions(
            requirements, day_index
        )
        
        # 推荐餐厅
        lunch = self._recommend_professional_restaurant(
            requirements, "lunch"
        )
        dinner = self._recommend_professional_restaurant(
            requirements, "dinner"
        )
        
        # 生成时间轴
        timeline = self._generate_professional_timeline(
            requirements, attractions, lunch, dinner
        )
        
        # 计算当日成本
        daily_cost = sum(slot.cost for slot in timeline)
        
        return {
            "day": day_index + 1,
            "date": date,
            "weekday": weekday,
            "season": SeasonalGuidelines.get_season(month),
            "seasonal_tips": seasonal_tips,
            "attractions": [a.__dict__ for a in attractions],
            "restaurants": {
                "lunch": lunch.__dict__ if lunch else None,
                "dinner": dinner.__dict__ if dinner else None
            },
            "timeline": [slot.to_dict() for slot in timeline],
            "total_activities": len([t for t in timeline if t.activity_type == "attraction"]),
            "daily_cost": round(daily_cost * requirements.total_travelers(), 2),
            "pace": self._calculate_daily_pace(timeline),
            "walk_distance_estimate": self._estimate_daily_walk_distance(attractions)
        }
    
    def _recommend_professional_attractions(
        self,
        requirements: TravelRequirements,
        day_index: int
    ) -> List[ProfessionalAttraction]:
        """推荐专业景点"""
        attractions = self.attractions_db.get(requirements.destination, [])
        
        # 根据兴趣筛选
        if requirements.interests:
            filtered = [
                a for a in attractions
                if any(tag in a.tags for tag in requirements.interests)
            ]
        else:
            filtered = attractions
        
        # 根据评分筛选
        min_rating = 4.0
        filtered = [a for a in filtered if a.rating >= min_rating]
        
        # 根据旅行风格调整
        if requirements.travel_style == TravelStyle.FAMILY:
            filtered = [a for a in filtered if a.family_friendly]
        elif requirements.travel_style == TravelStyle.FOODIE:
            filtered = [a for a in filtered if a.nearby_restaurants >= 5]
        
        # 确定每日景点数量
        activities_per_day = self.standards.get_activities_per_day(
            requirements.activity_intensity
        )
        
        # 轮换景点
        start_idx = (day_index * activities_per_day) % len(filtered)
        day_attractions = filtered[start_idx:start_idx + activities_per_day]
        
        # 路线优化
        if len(day_attractions) > 1:
            day_attractions = self._optimize_attraction_route(day_attractions)
        
        return day_attractions
    
    def _recommend_professional_restaurant(
        self,
        requirements: TravelRequirements,
        meal_type: str
    ) -> Optional[ProfessionalRestaurant]:
        """推荐专业餐厅"""
        restaurants = self.restaurants_db.get(requirements.destination, [])
        
        if not restaurants:
            return None
        
        # 根据预算等级筛选
        budget_level_map = {
            BudgetLevel.BUDGET: 1,
            BudgetLevel.STANDARD: 2,
            BudgetLevel.COMFORT: 3,
            BudgetLevel.PREMIUM: 4,
            BudgetLevel.LUXURY: 5
        }
        max_price_level = budget_level_map.get(requirements.budget_level, 3)
        
        filtered = [r for r in restaurants if r.price_level <= max_price_level]
        
        # 根据特殊需求筛选
        if "vegetarian" in requirements.dietary_restrictions:
            filtered = [r for r in filtered if "素食" in r.special_dietary_options]
        
        if requirements.travelers_children > 0:
            filtered = [r for r in filtered if r.family_friendly]
        
        if not filtered:
            filtered = restaurants
        
        # 用餐类型选择
        if meal_type == "lunch":
            candidates = [r for r in filtered if r.price_level <= 2]
        else:
            candidates = [r for r in filtered if r.price_level >= 2]
        
        if not candidates:
            candidates = filtered
        
        # 评分优先
        candidates.sort(key=lambda r: r.rating, reverse=True)
        return candidates[0] if candidates else None
    
    def _generate_professional_timeline(
        self,
        requirements: TravelRequirements,
        attractions: List[ProfessionalAttraction],
        lunch: Optional[ProfessionalRestaurant],
        dinner: Optional[ProfessionalRestaurant]
    ) -> List[TimeSlot]:
        """生成专业时间轴"""
        timeline = []
        current_time = self.standards.DAILY_START_TIME
        
        # 早餐建议
        timeline.append(TimeSlot(
            start_time=8.0,
            end_time=9.0,
            activity_type="meal",
            activity_name="早餐",
            location="酒店/当地早餐店",
            duration=1.0,
            notes="建议品尝当地特色早餐",
            cost=0
        ))
        
        # 上午景点
        for attraction in attractions[:2]:
            end_time = current_time + attraction.recommended_duration / 60
            timeline.append(TimeSlot(
                start_time=current_time,
                end_time=end_time,
                activity_type="attraction",
                activity_name=f"游览{attraction.name}",
                location=attraction.name,
                duration=attraction.recommended_duration / 60,
                notes=f"{attraction.best_time_to_visit}最佳",
                cost=attraction.ticket_price
            ))
            current_time = end_time + self.standards.TRANSIT_TIME_BUFFER
        
        # 午餐
        if lunch and current_time < 14.0:
            timeline.append(TimeSlot(
                start_time=current_time,
                end_time=current_time + self.standards.MEAL_DURATION,
                activity_type="meal",
                activity_name="午餐",
                location=lunch.name,
                duration=self.standards.MEAL_DURATION,
                notes=f"推荐尝试{lunch.must_try_dishes[0] if lunch.must_try_dishes else ''}",
                cost=lunch.avg_price_per_person
            ))
            current_time += self.standards.MEAL_DURATION
        
        # 下午景点
        for attraction in attractions[2:]:
            end_time = current_time + attraction.recommended_duration / 60
            timeline.append(TimeSlot(
                start_time=current_time,
                end_time=end_time,
                activity_type="attraction",
                activity_name=f"游览{attraction.name}",
                location=attraction.name,
                duration=attraction.recommended_duration / 60,
                notes="下午光线适合拍照",
                cost=attraction.ticket_price
            ))
            current_time = end_time + self.standards.TRANSIT_TIME_BUFFER
        
        # 晚餐
        if dinner and current_time < 20.0:
            timeline.append(TimeSlot(
                start_time=current_time,
                end_time=current_time + 2.0,
                activity_type="meal",
                activity_name="晚餐",
                location=dinner.name,
                duration=2.0,
                notes=f"品尝当地美食{dinner.must_try_dishes[0] if dinner.must_try_dishes else ''}",
                cost=dinner.avg_price_per_person
            ))
        
        return timeline
    
    def _optimize_attraction_route(
        self,
        attractions: List[ProfessionalAttraction]
    ) -> List[ProfessionalAttraction]:
        """优化景点路线 - TSP贪心算法"""
        if len(attractions) <= 2:
            return attractions
        
        def calculate_distance(a1: ProfessionalAttraction, a2: ProfessionalAttraction) -> float:
            from math import radians, cos, sin, sqrt, atan2
            R = 6371
            lat1, lon1, lat2, lon2 = map(radians, [a1.latitude, a1.longitude, a2.latitude, a2.longitude])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return R * c
        
        visited = [attractions[0]]
        remaining = attractions[1:]
        
        while remaining:
            current = visited[-1]
            next_attraction = min(
                remaining,
                key=lambda a: calculate_distance(current, a)
            )
            visited.append(next_attraction)
            remaining.remove(next_attraction)
        
        return visited
    
    def _recommend_professional_accommodation(
        self,
        requirements: TravelRequirements
    ) -> Dict[str, Any]:
        """推荐专业住宿"""
        base_prices = {
            "京都": 500,
            "东京": 700,
            "大阪": 450,
        }
        
        base_price = base_prices.get(requirements.destination, 500)
        
        # 根据住宿类型调整
        type_multiplier = {
            AccommodationType.BUDGET_HOTEL: 0.6,
            AccommodationType.STANDARD_HOTEL: 1.0,
            AccommodationType.BOUTIQUE_HOTEL: 1.3,
            AccommodationType.RESORT: 2.0,
            AccommodationType.RYOKAN: 1.8,
            AccommodationType.APARTMENT: 0.8,
            AccommodationType.HOSTEL: 0.4,
            AccommodationType.GUESTHOUSE: 0.6,
        }
        
        multiplier = type_multiplier.get(requirements.accommodation_type, 1.0)
        price_per_night = base_price * multiplier
        
        # 计算房间数
        rooms_needed = (requirements.total_travelers() + 1) // 2
        
        total_cost = price_per_night * rooms_needed * (requirements.days - 1)
        
        return {
            "type": requirements.accommodation_type.value,
            "name": f"精选{requirements.accommodation_type.value}",
            "rooms_needed": rooms_needed,
            "price_per_night": round(price_per_night, 2),
            "total_cost": round(total_cost, 2),
            "location_preference": "市中心",
            "amenities": ["WiFi", "空调", "浴室"],
            "booking_tip": "建议提前2周预订",
            "meal_plan": requirements.meal_plan.value
        }
    
    def _recommend_professional_transportation(
        self,
        requirements: TravelRequirements
    ) -> Dict[str, Any]:
        """推荐专业交通"""
        transport_info = {
            "京都": {
                "local": "巴士/地铁一日券",
                "daily_cost": 50,
                "recommendation": "购买京都巴士一日券最划算",
                "options": ["巴士一日券", "地铁一日券", "IC卡"]
            },
            "东京": {
                "local": "地铁/电车",
                "daily_cost": 80,
                "recommendation": "推荐购买Suica/PASMO卡",
                "options": ["都营地铁一日券", "Tokyo Metro一日券", "IC卡"]
            }
        }
        
        info = transport_info.get(requirements.destination, {
            "local": "公共交通",
            "daily_cost": 60,
            "recommendation": "使用当地公共交通",
            "options": ["一日通票", "单程票"]
        })
        
        total_local_cost = info["daily_cost"] * requirements.days
        
        # 航班舱位
        flight_class_map = {
            "economy": "经济舱",
            "premium_economy": "超级经济舱",
            "business": "商务舱",
            "first": "头等舱"
        }
        
        return {
            "departure": requirements.departure_city,
            "destination": requirements.destination,
            "flight_class": flight_class_map[requirements.flight_class],
            "flight_recommendation": f"选择{flight_class_map[requirements.flight_class]}航班",
            "local_transport": info["local"],
            "local_cost_per_day": info["daily_cost"],
            "total_local_cost": total_local_cost,
            "total_transport_cost": total_local_cost,
            "recommendations": info["options"],
            "main_tip": info["recommendation"]
        }
    
    def _calculate_daily_pace(self, timeline: List[TimeSlot]) -> str:
        """计算当日节奏"""
        total_hours = sum(t.duration for t in timeline)
        
        if total_hours < 6:
            return "relaxed"
        elif total_hours < 8:
            return "moderate"
        elif total_hours < 10:
            return "active"
        else:
            return "intense"
    
    def _estimate_daily_walk_distance(self, attractions: List) -> float:
        """估算每日步行距离"""
        if not attractions:
            return 0.0
        return len(attractions) * 2.0  # 每个景点约2km步行
    
    def _perform_quality_check(
        self,
        daily_plans: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """执行质量检查"""
        notes = []
        recommendations = []
        warnings = []
        
        for plan in daily_plans:
            # 检查活动数量
            activities = plan.get("total_activities", 0)
            if activities > 4:
                warnings.append(f"第{plan['day']}天活动较多({activities}个)，注意休息")
            elif activities < 1:
                notes.append(f"第{plan['day']}天活动较少，可考虑增加景点")
            
            # 检查季节性
            if "seasonal_tips" in plan:
                recommendations.extend(plan["seasonal_tips"])
        
        return {
            "notes": notes,
            "recommendations": list(set(recommendations)),
            "warnings": warnings
        }


# 单例
_professional_generator = None

def get_professional_generator() -> ProfessionalItineraryGenerator:
    """获取专业行程生成器单例"""
    global _professional_generator
    if _professional_generator is None:
        _professional_generator = ProfessionalItineraryGenerator()
    return _professional_generator
