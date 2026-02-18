"""
专业旅行规划标准
基于专业旅行规划师的行业标准和最佳实践
"""
from typing import Dict, List, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class TravelStyle(Enum):
    """旅行风格分类 - 专业标准"""
    LEISURE = "leisure"  # 休闲度假
    ADVENTURE = "adventure"  # 户外探险
    CULTURAL = "cultural"  # 文化深度游
    FOODIE = "foodie"  # 美食之旅
    SHOPPING = "shopping"  # 购物之旅
    FAMILY = "family"  # 亲子游
    HONEYMOON = "honeymoon"  # 蜜月游
    BUSINESS = "business"  # 商务出行
    EDUCATIONAL = "educational"  # 游学研修
    WELLNESS = "wellness"  # 康养度假


class ActivityIntensity(Enum):
    """活动强度等级"""
    RELAXED = 1  # 轻松 - 每天1-2个景点
    MODERATE = 2  # 适中 - 每天2-3个景点
    ACTIVE = 3  # 活跃 - 每天3-4个景点
    INTENSE = 4  # 紧凑 - 每天4-5个景点


class BudgetLevel(Enum):
    """预算等级"""
    BUDGET = "budget"  # 经济型
    STANDARD = "standard"  # 标准型
    COMFORT = "comfort"  # 舒适型
    PREMIUM = "premium"  # 高端型
    LUXURY = "luxury"  # 奢华型


class AccommodationType(Enum):
    """住宿类型"""
    BUDGET_HOTEL = "budget_hotel"  # 经济酒店
    STANDARD_HOTEL = "standard_hotel"  # 标准酒店
    BOUTIQUE_HOTEL = "boutique_hotel"  # 精品酒店
    RESORT = "resort"  # 度假村
    RYOKAN = "ryokan"  # 日式旅馆
    APARTMENT = "apartment"  # 公寓
    HOSTEL = "hostel"  # 青年旅舍
    GUESTHOUSE = "guesthouse"  # 客栈


class MealPlan(Enum):
    """餐饮计划"""
    NONE = "none"  # 不含餐
    BREAKFAST_ONLY = "breakfast_only"  # 含早餐
    HALF_BOARD = "half_board"  # 半食宿
    FULL_BOARD = "full_board"  # 全食宿
    ALL_INCLUSIVE = "all_inclusive"  # 全包式


@dataclass
class TravelRequirements:
    """旅行需求标准数据结构"""
    # 基本信息
    destination: str
    departure_city: str
    start_date: str
    end_date: str
    days: int
    
    # 人员信息
    travelers_adults: int = 1
    travelers_children: int = 0
    travelers_infants: int = 0
    travelers_seniors: int = 0
    
    # 旅行偏好
    travel_style: TravelStyle = TravelStyle.LEISURE
    activity_intensity: ActivityIntensity = ActivityIntensity.MODERATE
    budget_level: BudgetLevel = BudgetLevel.STANDARD
    budget_limit: Optional[float] = None
    
    # 兴趣主题（最多5个）
    interests: List[str] = field(default_factory=list)
    
    # 住宿偏好
    accommodation_type: AccommodationType = AccommodationType.STANDARD_HOTEL
    accommodation_preferences: List[str] = field(default_factory=list)  # 如["市中心", "安静", "有电梯"]
    meal_plan: MealPlan = MealPlan.BREAKFAST_ONLY
    
    # 交通偏好
    flight_class: Literal["economy", "premium_economy", "business", "first"] = "economy"
    transport_preference: str = "convenience"  # convenience/budget/comfort
    
    # 特殊需求
    accessibility_needs: List[str] = field(default_factory=list)  # 无障碍需求
    dietary_restrictions: List[str] = field(default_factory=list)  # 饮食限制
    special_occasions: List[str] = field(default_factory=list)  # 特殊场合
    
    # 其他
    language_preference: str = "chinese"
    guide_required: bool = False
    notes: str = ""
    
    def validate(self) -> tuple[bool, List[str]]:
        """验证需求完整性"""
        errors = []
        
        if not self.destination:
            errors.append("目的地不能为空")
        
        if not self.start_date or not self.end_date:
            errors.append("出发日期和返回日期不能为空")
        
        if self.days <= 0:
            errors.append("旅行天数必须大于0")
        
        total_travelers = self.travelers_adults + self.travelers_children + \
                         self.travelers_infants + self.travelers_seniors
        
        if total_travelers == 0:
            errors.append("至少需要1名旅行者")
        
        if len(self.interests) > 5:
            errors.append("兴趣主题最多选择5个")
        
        return len(errors) == 0, errors
    
    def total_travelers(self) -> int:
        """获取总人数"""
        return (self.travelers_adults + self.travelers_children +
                self.travelers_infants + self.travelers_seniors)
    
    def calculate_children_count(self) -> int:
        """获取儿童人数（含婴幼儿）"""
        return self.travelers_children + self.travelers_infants


@dataclass
class ProfessionalItinerary:
    """专业行程数据结构"""
    itinerary_id: str
    requirements: TravelRequirements
    created_at: datetime
    status: str = "draft"  # draft/confirmed/modified/cancelled
    
    # 行程内容
    daily_plans: List[Dict[str, Any]] = field(default_factory=list)
    accommodation: Optional[Dict[str, Any]] = None
    transportation: Optional[Dict[str, Any]] = None
    budget_breakdown: Optional[Dict[str, Any]] = None
    
    # 专业信息
    planning_notes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # 元数据
    version: int = 1
    last_modified: Optional[datetime] = None


class ProfessionalPlanningStandards:
    """专业旅行规划标准"""
    
    # 时间标准（单位：小时）
    MIN_ATTRACTION_DURATION = 1.0  # 最小游览时长
    MAX_ATTRACTION_DURATION = 4.0  # 最大游览时长
    MEAL_DURATION = 1.5  # 用餐时长
    TRANSIT_TIME_BUFFER = 0.5  # 转场缓冲时间
    DAILY_START_TIME = 9.0  # 每日开始时间
    DAILY_END_TIME = 21.0  # 每日结束时间
    
    # 距离标准（单位：公里）
    MAX_DAILY_TRANSIT_DISTANCE = 50.0  # 每日最大转场距离
    OPTIMAL_ATTRACTION_DISTANCE = 5.0  # 景点间最优距离
    
    # 预算标准
    BUDGET_SAFETY_MARGIN = 0.1  # 预算安全边际10%
    CONTINGENCY_FUND_RATIO = 0.15  # 应急资金比例15%
    
    # 活动标准
    MAX_DAILY_ACTIVITIES = {
        ActivityIntensity.RELAXED: 2,
        ActivityIntensity.MODERATE: 3,
        ActivityIntensity.ACTIVE: 4,
        ActivityIntensity.INTENSE: 5
    }
    
    # 评分标准
    MIN_ATTRACTION_RATING = 4.0  # 最低评分要求
    
    @classmethod
    def get_activities_per_day(cls, intensity: ActivityIntensity) -> int:
        """根据强度获取每日建议活动数"""
        return cls.MAX_DAILY_ACTIVITIES.get(intensity, 3)
    
    @classmethod
    def calculate_daily_budget(
        cls,
        total_budget: float,
        days: int,
        budget_level: BudgetLevel
    ) -> Dict[str, float]:
        """计算每日预算分配"""
        base_daily = total_budget / days
        
        # 根据预算等级调整分配比例
        allocation_ratios = {
            BudgetLevel.BUDGET: {
                "accommodation": 0.25,
                "food": 0.30,
                "attractions": 0.25,
                "transport": 0.15,
                "other": 0.05
            },
            BudgetLevel.STANDARD: {
                "accommodation": 0.30,
                "food": 0.25,
                "attractions": 0.20,
                "transport": 0.15,
                "other": 0.10
            },
            BudgetLevel.COMFORT: {
                "accommodation": 0.35,
                "food": 0.25,
                "attractions": 0.20,
                "transport": 0.15,
                "other": 0.05
            },
            BudgetLevel.PREMIUM: {
                "accommodation": 0.40,
                "food": 0.25,
                "attractions": 0.20,
                "transport": 0.10,
                "other": 0.05
            },
            BudgetLevel.LUXURY: {
                "accommodation": 0.45,
                "food": 0.25,
                "attractions": 0.15,
                "transport": 0.10,
                "other": 0.05
            }
        }
        
        ratios = allocation_ratios.get(budget_level, allocation_ratios[BudgetLevel.STANDARD])
        
        return {
            category: round(base_daily * ratio, 2)
            for category, ratio in ratios.items()
        }
    
    @classmethod
    def validate_itinerary_time(
        cls,
        start_time: float,
        end_time: float
    ) -> tuple[bool, str]:
        """验证时间安排合理性"""
        if start_time < cls.DAILY_START_TIME:
            return False, f"开始时间不能早于 {cls.DAILY_START_TIME}:00"
        
        if end_time > cls.DAILY_END_TIME:
            return False, f"结束时间不能晚于 {cls.DAILY_END_TIME}:00"
        
        total_hours = end_time - start_time
        if total_hours > 12:
            return False, "每日活动时长不宜超过12小时"
        
        return True, ""
    
    @classmethod
    def get_meal_time_recommendations(cls) -> Dict[str, Dict[str, float]]:
        """获取用餐时间建议"""
        return {
            "breakfast": {"start": 7.0, "end": 9.0, "duration": 1.0},
            "lunch": {"start": 12.0, "end": 13.0, "duration": 1.5},
            "dinner": {"start": 18.0, "end": 20.0, "duration": 2.0}
        }


class SeasonalGuidelines:
    """季节性旅行指南"""
    
    SEASONS = {
        "spring": {"months": [3, 4, 5], "description": "春季"},
        "summer": {"months": [6, 7, 8], "description": "夏季"},
        "autumn": {"months": [9, 10, 11], "description": "秋季"},
        "winter": {"months": [12, 1, 2], "description": "冬季"}
    }
    
    DESTINATION_SEASONAL_INFO = {
        "京都": {
            "best_seasons": ["spring", "autumn"],
            "spring_tips": ["樱花季3-4月，需提前预订", "气温适中，适合观光"],
            "summer_tips": ["7-8月较热，注意防暑", "夏季有祗园祭等活动"],
            "autumn_tips": ["红叶季11月中下旬最美", "秋季气候宜人"],
            "winter_tips": ["冬季人少，部分景点关闭", "可体验雪景和温泉"]
        },
        "东京": {
            "best_seasons": ["spring", "autumn"],
            "spring_tips": ["上野公园赏樱热门", "气候舒适"],
            "summer_tips": ["炎热潮湿，推荐室内活动", "夏季祭典丰富"],
            "autumn_tips": ["各地枫叶美景", "气候干燥舒适"],
            "winter_tips": ["冬季干燥，适合购物", "新年期间许多店铺休息"]
        }
    }
    
    @classmethod
    def get_season(cls, month: int) -> str:
        """获取季节"""
        for season, info in cls.SEASONS.items():
            if month in info["months"]:
                return season
        return "unknown"
    
    @classmethod
    def get_seasonal_tips(
        cls,
        destination: str,
        month: int
    ) -> List[str]:
        """获取季节性建议"""
        season = cls.get_season(month)
        
        if destination not in cls.DESTINATION_SEASONAL_INFO:
            return [f"建议关注{season}气候特点"]
        
        info = cls.DESTINATION_SEASONAL_INFO[destination]
        tips_key = f"{season}_tips"
        
        return info.get(tips_key, [])


# 专业工作流模板
class PlanningWorkflow:
    """专业规划工作流"""
    
    STEPS = [
        "需求收集与分析",
        "目的地研究",
        "行程框架设计",
        "详细行程制定",
        "预算计算",
        "住宿与交通安排",
        "风险评估",
        "行程优化",
        "客户确认",
        "最终交付"
    ]
    
    @classmethod
    def get_step_description(cls, step: str) -> str:
        """获取工作流步骤说明"""
        descriptions = {
            "需求收集与分析": "深入了解客户需求，提取关键信息",
            "目的地研究": "调研目的地信息，收集最新资讯",
            "行程框架设计": "制定行程骨架，确定主要节点",
            "详细行程制定": "安排每日活动，优化时间路线",
            "预算计算": "精确计算各项费用，优化预算分配",
            "住宿与交通安排": "选择合适的住宿和交通方式",
            "风险评估": "识别潜在风险，制定应对方案",
            "行程优化": "根据反馈调整，完善细节",
            "客户确认": "与客户确认，获取最终同意",
            "最终交付": "输出完整行程，提供服务保障"
        }
        return descriptions.get(step, "")


# 质量检查标准
class QualityChecklist:
    """质量检查清单"""
    
    CHECK_ITEMS = {
        "completeness": [
            "日期是否完整",
            "时间安排是否合理",
            "景点信息是否准确",
            "住宿信息是否详细",
            "交通信息是否清晰"
        ],
        "feasibility": [
            "每日行程是否过于紧凑",
            "转场时间是否充足",
            "体力要求是否超出客户能力",
            "预算是否在合理范围"
        ],
        "experience": [
            "是否满足客户兴趣偏好",
            "是否包含当地特色体验",
            "餐饮安排是否多样化",
            "是否有灵活调整空间"
        ],
        "safety": [
            "是否识别潜在安全风险",
            "是否有应急联系方式",
            "是否提供保险建议",
            "特殊人群需求是否考虑"
        ]
    }
    
    @classmethod
    def check_completeness(cls, itinerary: Dict[str, Any]) -> Dict[str, Any]:
        """检查完整性"""
        results = {"passed": [], "failed": [], "warnings": []}
        
        # 检查基本信息
        required_fields = ["destination", "days", "start_date", "end_date"]
        for field in required_fields:
            if field in itinerary and itinerary[field]:
                results["passed"].append(f"{field}已填写")
            else:
                results["failed"].append(f"{field}缺失")
        
        return results
    
    @classmethod
    def check_feasibility(cls, daily_plans: List[Dict]) -> Dict[str, Any]:
        """检查可行性"""
        results = {"passed": [], "failed": [], "warnings": []}
        
        for plan in daily_plans:
            timeline = plan.get("timeline", [])
            if len(timeline) > 5:
                results["warnings"].append(f"第{plan['day']}天活动较多")
        
        return results
