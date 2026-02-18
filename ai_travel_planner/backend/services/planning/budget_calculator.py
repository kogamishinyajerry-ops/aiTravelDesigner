"""
预算计算器 - 精确估算旅行费用
支持多维度预算分析和优化建议
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
from loguru import logger


@dataclass
class CostItem:
    """费用项"""
    category: str
    name: str
    unit_cost: float
    quantity: int
    total_cost: float
    currency: str = "CNY"


class BudgetCalculator:
    """预算计算器"""
    
    def __init__(self):
        # 目的地基础数据（生产环境应从数据库读取）
        self.destination_costs = {
            "京都": {
                "avg_hotel_price": 500,  # 每晚
                "avg_meal_price": {"breakfast": 30, "lunch": 50, "dinner": 80},
                "avg_attraction_price": 35,
                "avg_transport_daily": 50,
            },
            "东京": {
                "avg_hotel_price": 700,
                "avg_meal_price": {"breakfast": 35, "lunch": 60, "dinner": 100},
                "avg_attraction_price": 40,
                "avg_transport_daily": 80,
            },
            "大阪": {
                "avg_hotel_price": 450,
                "avg_meal_price": {"breakfast": 25, "lunch": 45, "dinner": 70},
                "avg_attraction_price": 30,
                "avg_transport_daily": 40,
            },
            "曼谷": {
                "avg_hotel_price": 300,
                "avg_meal_price": {"breakfast": 20, "lunch": 30, "dinner": 50},
                "avg_attraction_price": 25,
                "avg_transport_daily": 20,
            },
            "巴黎": {
                "avg_hotel_price": 1200,
                "avg_meal_price": {"breakfast": 60, "lunch": 100, "dinner": 150},
                "avg_attraction_price": 80,
                "avg_transport_daily": 100,
            },
        }
        
        # 交通费用数据（人民币/人）
        self.flight_costs = {
            "北京-东京": 3500,
            "上海-东京": 3200,
            "广州-东京": 3000,
            "北京-曼谷": 2000,
            "上海-曼谷": 1800,
            "北京-巴黎": 8000,
            "上海-巴黎": 7500,
        }
        
        # 签证费用
        self.visa_costs = {
            "日本": 300,
            "泰国": 300,
            "法国": 800,
        }
        
        # 保险费用
        self.insurance_cost = 100  # 每人
    
    def calculate_flight_cost(
        self,
        departure: str,
        destination: str,
        travelers: int
    ) -> CostItem:
        """计算机票费用"""
        route = f"{departure}-{destination}"
        base_cost = self.flight_costs.get(route, 4000)  # 默认4000
        
        # 季节性调整
        # 这里简化处理，实际应该根据日期判断
        
        return CostItem(
            category="transport",
            name=f"往返机票 ({departure} → {destination})",
            unit_cost=base_cost,
            quantity=travelers,
            total_cost=base_cost * travelers
        )
    
    def calculate_accommodation_cost(
        self,
        destination: str,
        days: int,
        travelers: int,
        room_type: str = "standard"
    ) -> CostItem:
        """计算住宿费用"""
        if destination not in self.destination_costs:
            base_price = 500  # 默认价格
        else:
            base_price = self.destination_costs[destination]["avg_hotel_price"]
        
        # 根据房间类型调整价格
        room_multiplier = {
            "budget": 0.6,
            "standard": 1.0,
            "comfort": 1.5,
            "luxury": 2.5
        }.get(room_type, 1.0)
        
        # 根据人数调整房间数
        rooms = (travelers + 1) // 2  # 两人一间
        
        total_cost = base_price * room_multiplier * rooms * days
        
        return CostItem(
            category="accommodation",
            name=f"住宿 ({room_type}, {rooms}间 × {days}晚)",
            unit_cost=base_price * room_multiplier * rooms,
            quantity=days,
            total_cost=total_cost
        )
    
    def calculate_food_cost(
        self,
        destination: str,
        days: int,
        travelers: int,
        meal_level: str = "standard"
    ) -> CostItem:
        """计算餐饮费用"""
        if destination not in self.destination_costs:
            meal_prices = {"breakfast": 30, "lunch": 50, "dinner": 80}
        else:
            meal_prices = self.destination_costs[destination]["avg_meal_price"]
        
        # 根据餐饮水平调整
        meal_multiplier = {
            "budget": 0.6,
            "standard": 1.0,
            "premium": 1.5
        }.get(meal_level, 1.0)
        
        # 计算每日餐费
        daily_cost = sum(meal_prices.values()) * meal_multiplier
        
        total_cost = daily_cost * days * travelers
        
        return CostItem(
            category="food",
            name=f"餐饮 ({meal_level}, {days}天 × {travelers}人)",
            unit_cost=daily_cost * travelers,
            quantity=days,
            total_cost=total_cost
        )
    
    def calculate_attraction_cost(
        self,
        destination: str,
        days: int,
        travelers: int,
        attraction_count: int = 3
    ) -> CostItem:
        """计算景点门票费用"""
        if destination not in self.destination_costs:
            avg_price = 40
        else:
            avg_price = self.destination_costs[destination]["avg_attraction_price"]
        
        # 每天平均参观 attraction_count 个景点
        total_attractions = days * attraction_count
        total_cost = avg_price * total_attractions * travelers
        
        return CostItem(
            category="attraction",
            name=f"景点门票 (约{total_attractions}个景点 × {travelers}人)",
            unit_cost=avg_price * travelers,
            quantity=total_attractions,
            total_cost=total_cost
        )
    
    def calculate_transportation_cost(
        self,
        destination: str,
        days: int,
        travelers: int
    ) -> CostItem:
        """计算当地交通费用"""
        if destination not in self.destination_costs:
            daily_cost = 60
        else:
            daily_cost = self.destination_costs[destination]["avg_transport_daily"]
        
        total_cost = daily_cost * days * travelers
        
        return CostItem(
            category="transport_local",
            name=f"当地交通 ({days}天 × {travelers}人)",
            unit_cost=daily_cost * travelers,
            quantity=days,
            total_cost=total_cost
        )
    
    def calculate_visa_cost(
        self,
        destination: str,
        travelers: int
    ) -> Optional[CostItem]:
        """计算签证费用"""
        # 目的地到国家的映射
        destination_to_country = {
            "京都": "日本",
            "东京": "日本",
            "大阪": "日本",
            "曼谷": "泰国",
            "巴黎": "法国",
        }
        
        country = destination_to_country.get(destination)
        if not country:
            return None
        
        cost = self.visa_costs.get(country, 0)
        if cost == 0:
            return None
        
        return CostItem(
            category="visa",
            name=f"签证 ({country})",
            unit_cost=cost,
            quantity=travelers,
            total_cost=cost * travelers
        )
    
    def calculate_insurance_cost(
        self,
        travelers: int
    ) -> CostItem:
        """计算旅行保险费用"""
        return CostItem(
            category="insurance",
            name="旅行保险",
            unit_cost=self.insurance_cost,
            quantity=travelers,
            total_cost=self.insurance_cost * travelers
        )
    
    def calculate_other_cost(
        self,
        total_budget: float,
        percentage: float = 0.1
    ) -> CostItem:
        """计算其他费用（购物、应急等）"""
        cost = total_budget * percentage
        
        return CostItem(
            category="other",
            name="其他费用（购物、应急等）",
            unit_cost=cost,
            quantity=1,
            total_cost=cost
        )
    
    async def calculate_total_budget(
        self,
        departure: str,
        destination: str,
        days: int,
        travelers: int,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        计算总预算
        
        Args:
            departure: 出发地
            destination: 目的地
            days: 天数
            travelers: 人数
            preferences: 偏好设置
        
        Returns:
            预算详情
        """
        preferences = preferences or {}
        
        # 计算各项费用
        cost_items = []
        
        # 机票
        flight_cost = self.calculate_flight_cost(departure, destination, travelers)
        cost_items.append(flight_cost)
        
        # 住宿
        room_type = preferences.get("room_type", "standard")
        accommodation_cost = self.calculate_accommodation_cost(
            destination, days, travelers, room_type
        )
        cost_items.append(accommodation_cost)
        
        # 餐饮
        meal_level = preferences.get("meal_level", "standard")
        food_cost = self.calculate_food_cost(
            destination, days, travelers, meal_level
        )
        cost_items.append(food_cost)
        
        # 景点门票
        attraction_cost = self.calculate_attraction_cost(destination, days, travelers)
        cost_items.append(attraction_cost)
        
        # 当地交通
        transport_cost = self.calculate_transportation_cost(destination, days, travelers)
        cost_items.append(transport_cost)
        
        # 签证
        visa_cost = self.calculate_visa_cost(destination, travelers)
        if visa_cost:
            cost_items.append(visa_cost)
        
        # 保险
        insurance_cost = self.calculate_insurance_cost(travelers)
        cost_items.append(insurance_cost)
        
        # 计算小计
        subtotal = sum(item.total_cost for item in cost_items)
        
        # 其他费用
        other_cost = self.calculate_other_cost(subtotal)
        cost_items.append(other_cost)
        
        # 总计
        total_cost = subtotal + other_cost.total_cost
        
        # 按类别汇总
        breakdown = {}
        for item in cost_items:
            category = item.category
            if category not in breakdown:
                breakdown[category] = {
                    "items": [],
                    "total": 0
                }
            breakdown[category]["items"].append({
                "name": item.name,
                "cost": item.total_cost,
                "unit_cost": item.unit_cost,
                "quantity": item.quantity
            })
            breakdown[category]["total"] += item.total_cost
        
        return {
            "destination": destination,
            "departure": departure,
            "days": days,
            "travelers": travelers,
            "total_cost": round(total_cost, 2),
            "per_person": round(total_cost / travelers, 2),
            "per_day": round(total_cost / days, 2),
            "breakdown": {
                category: {
                    "total": round(data["total"], 2),
                    "items": data["items"]
                }
                for category, data in breakdown.items()
            },
            "cost_items": [
                {
                    "category": item.category,
                    "name": item.name,
                    "unit_cost": item.unit_cost,
                    "quantity": item.quantity,
                    "total_cost": item.total_cost
                }
                for item in cost_items
            ],
            "suggestions": self._generate_budget_suggestions(total_cost, breakdown)
        }
    
    def _generate_budget_suggestions(
        self,
        total_cost: float,
        breakdown: Dict[str, Any]
    ) -> List[str]:
        """生成预算优化建议"""
        suggestions = []
        
        # 住宿费用占比
        if "accommodation" in breakdown:
            accommodation_ratio = breakdown["accommodation"]["total"] / total_cost
            if accommodation_ratio > 0.4:
                suggestions.append(
                    "住宿费用占比较高，可考虑选择经济型酒店或民宿"
                )
        
        # 餐饮费用
        if "food" in breakdown:
            food_ratio = breakdown["food"]["total"] / total_cost
            if food_ratio > 0.25:
                suggestions.append(
                    "可以尝试当地小吃和市场，降低餐饮支出"
                )
        
        # 景点门票
        if "attraction" in breakdown:
            suggestions.append(
                "部分景点有联票或学生优惠，建议提前查询"
            )
        
        # 通用建议
        suggestions.extend([
            "提前预订机票和酒店可节省10-30%",
            "避开旅游旺季可降低成本",
            "准备现金，部分小店可能有折扣"
        ])
        
        return suggestions
    
    def check_budget_feasibility(
        self,
        user_budget: float,
        estimated_cost: float
    ) -> Dict[str, Any]:
        """
        检查预算可行性
        
        Args:
            user_budget: 用户预算
            estimated_cost: 估算费用
        
        Returns:
            可行性分析
        """
        difference = user_budget - estimated_cost
        ratio = estimated_cost / user_budget
        
        if ratio <= 0.9:
            status = "sufficient"
            message = "预算充足，可以选择更高品质的服务"
        elif ratio <= 1.0:
            status = "tight"
            message = "预算基本够用，建议选择经济型选项"
        elif ratio <= 1.2:
            status = "insufficient"
            message = f"预算略显不足，建议调整行程或增加预算{difference * -1:.0f}元"
        else:
            status = "significantly_insufficient"
            message = f"预算严重不足，建议缩短行程或增加预算{difference * -1:.0f}元"
        
        # 优化建议
        optimization_tips = []
        if status in ["insufficient", "significantly_insufficient"]:
            needed_reduction = abs(difference)
            
            # 计算各项可节省的金额
            possible_savings = [
                ("缩短行程", f"每缩短1天可节省约{estimated_cost/7:.0f}元"),
                ("选择经济型住宿", "可节省30-50%住宿费用"),
                ("尝试当地小吃", "餐饮费用可降低20-30%"),
                ("减少付费景点", "选择免费景点可降低门票支出"),
            ]
            optimization_tips = possible_savings
        
        return {
            "status": status,
            "message": message,
            "user_budget": user_budget,
            "estimated_cost": estimated_cost,
            "difference": round(difference, 2),
            "ratio": round(ratio, 2),
            "optimization_tips": optimization_tips
        }


# 单例
_budget_calculator = None

def get_budget_calculator() -> BudgetCalculator:
    """获取预算计算器单例"""
    global _budget_calculator
    if _budget_calculator is None:
        _budget_calculator = BudgetCalculator()
    return _budget_calculator
