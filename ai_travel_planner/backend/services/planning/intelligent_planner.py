"""
智能行程规划器 - 整合PLTR所有哲学
结合可靠性引擎、数据驱动和可观测性
提供真正智能且可靠的行程规划
"""
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from loguru import logger
import numpy as np
from collections import defaultdict

from .itinerary_generator import ItineraryGenerator, Attraction, Restaurant
from .reliability_engine import ReliabilityEngine, ReliabilityLevel
from .data_driven_engine import DataDrivenEngine
from .observability_system import ObservabilitySystem, LogLevel


@dataclass
class PlanningContext:
    """规划上下文"""
    user_id: Optional[str]
    destination: str
    days: int
    start_date: str
    travelers: int
    preferences: Dict[str, Any]
    trace_id: str


@dataclass
class PlanningResult:
    """规划结果"""
    success: bool
    itinerary: Optional[Dict[str, Any]]
    confidence: float
    warnings: List[str]
    errors: List[str]
    execution_time_ms: float
    data_sources: List[str]


class IntelligentPlanner:
    """智能行程规划器"""
    
    def __init__(self):
        self.itinerary_generator = ItineraryGenerator()
        self.reliability_engine = ReliabilityEngine()
        self.data_engine = DataDrivenEngine()
        self.observability = ObservabilitySystem()
        
        # 注册降级处理器
        self._register_fallback_handlers()
        
        logger.info("IntelligentPlanner initialized with PLTR philosophy")
    
    def _register_fallback_handlers(self):
        """注册降级处理器"""
        async def fallback_attraction_service(*args, **kwargs):
            return self.itinerary_generator.attractions_db.get(args[0] if args else "京都", [])
        
        async def fallback_restaurant_service(*args, **kwargs):
            return self.itinerary_generator.restaurants_db.get(args[0] if args else "京都", [])
        
        async def fallback_budget_calculation(*args, **kwargs):
            return {
                "total": 0,
                "per_person": 0,
                "breakdown": {
                    "attractions": 0,
                    "accommodation": 0,
                    "food": 0,
                    "transport": 0
                }
            }
        
        self.reliability_engine.fallback_manager.register_fallback(
            "attraction_service", fallback_attraction_service
        )
        self.reliability_engine.fallback_manager.register_fallback(
            "restaurant_service", fallback_restaurant_service
        )
        self.reliability_engine.fallback_manager.register_fallback(
            "budget_service", fallback_budget_calculation
        )
    
    async def plan_itinerary(
        self,
        destination: str,
        days: int,
        start_date: str,
        travelers: int,
        preferences: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> PlanningResult:
        """
        智能规划行程
        
        整合所有PLTR原则：
        1. 可靠性 - 使用熔断器和降级策略
        2. 数据驱动 - 基于真实数据推荐
        3. 可观测性 - 全链路追踪和监控
        """
        trace_id = str(int(datetime.now().timestamp() * 1000))
        start_time = datetime.now()
        
        context = PlanningContext(
            user_id=user_id,
            destination=destination,
            days=days,
            start_date=start_date,
            travelers=travelers,
            preferences=preferences,
            trace_id=trace_id
        )
        
        warnings = []
        errors = []
        data_sources = []
        confidence = 0.8  # 默认置信度
        
        try:
            # 1. 数据验证
            self.observability.log(
                LogLevel.INFO,
                f"Validating planning request for {destination}",
                tags={"destination": destination, "days": days}
            )
            
            is_valid, validation_errors = self._validate_input(context)
            if not is_valid:
                errors.extend(validation_errors)
                return PlanningResult(
                    success=False,
                    itinerary=None,
                    confidence=0.0,
                    warnings=warnings,
                    errors=errors,
                    execution_time_ms=0.0,
                    data_sources=data_sources
                )
            
            # 2. 获取数据驱动的推荐
            self.observability.log(
                LogLevel.INFO,
                "Fetching data-driven recommendations",
                tags={"destination": destination}
            )
            
            with self.observability.trace_operation(
                "get_data_recommendations",
                trace_id
            ):
                recommendations = await self._get_data_recommendations(context)
                data_sources.append("data_driven_engine")
            
            # 3. 生成基础行程
            self.observability.log(
                LogLevel.INFO,
                "Generating base itinerary",
                tags={"destination": destination, "days": days}
            )
            
            success, base_itinerary = await self.reliability_engine.execute_with_reliability(
                "itinerary_service",
                self._generate_base_itinerary,
                ReliabilityLevel.CRITICAL,
                {"destination": destination, "days": days},
                "itinerary_request",
                context
            )
            
            if not success:
                errors.append("基础行程生成失败")
                return PlanningResult(
                    success=False,
                    itinerary=None,
                    confidence=0.0,
                    warnings=warnings,
                    errors=errors,
                    execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                    data_sources=data_sources
                )
            
            # 4. 应用数据驱动优化
            self.observability.log(
                LogLevel.INFO,
                "Applying data-driven optimization",
                tags={"destination": destination}
            )
            
            with self.observability.trace_operation(
                "optimize_itinerary",
                trace_id
            ):
                optimized_itinerary = await self._optimize_with_data(
                    base_itinerary,
                    context,
                    recommendations
                )
                confidence += 0.1  # 提升置信度
            
            # 5. 计算数据驱动的预算
            self.observability.log(
                LogLevel.INFO,
                "Calculating data-driven budget",
                tags={"destination": destination, "travelers": travelers}
            )
            
            success, budget = await self.reliability_engine.execute_with_reliability(
                "budget_service",
                self._calculate_data_driven_budget,
                ReliabilityLevel.IMPORTANT,
                {"destination": destination, "days": days, "travelers": travelers},
                "budget_request",
                context
            )
            
            if success:
                optimized_itinerary["budget"] = budget
                data_sources.append("budget_predictor")
            else:
                warnings.append("使用基础预算计算")
                confidence -= 0.1
            
            # 6. 生成智能建议
            self.observability.log(
                LogLevel.INFO,
                "Generating intelligent suggestions",
                tags={"destination": destination}
            )
            
            with self.observability.trace_operation(
                "generate_suggestions",
                trace_id
            ):
                suggestions = await self._generate_intelligent_suggestions(
                    optimized_itinerary,
                    context
                )
                optimized_itinerary["suggestions"] = suggestions
            
            # 7. 用户体验预测
            self.observability.log(
                LogLevel.INFO,
                "Predicting user satisfaction",
                tags={"user_id": user_id or "anonymous"}
            )
            
            if user_id:
                with self.observability.trace_operation(
                    "predict_satisfaction",
                    trace_id
                ):
                    satisfaction = self.data_engine.recommendation_engine.predict_satisfaction(
                        user_id,
                        [a["id"] for day in optimized_itinerary["daily_plans"] for a in day["attractions"]]
                    )
                    optimized_itinerary["predicted_satisfaction"] = satisfaction
                    confidence = max(confidence, satisfaction["confidence"])
            
            # 8. 记录用户交互
            self.observability.log(
                LogLevel.INFO,
                "Recording user interaction",
                tags={"user_id": user_id or "anonymous", "action": "plan"}
            )
            
            self._record_planning_metrics(context, optimized_itinerary)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # 记录指标
            self.observability.increment_counter(
                "planning_requests_total",
                tags={"destination": destination, "success": "true"}
            )
            self.observability.set_gauge(
                "planning_confidence",
                confidence,
                tags={"destination": destination}
            )
            
            return PlanningResult(
                success=True,
                itinerary=optimized_itinerary,
                confidence=min(confidence, 1.0),
                warnings=warnings,
                errors=errors,
                execution_time_ms=execution_time,
                data_sources=data_sources
            )
        
        except Exception as e:
            logger.error(f"Planning failed: {str(e)}")
            errors.append(str(e))
            
            self.observability.log(
                LogLevel.ERROR,
                f"Planning error: {str(e)}",
                tags={"destination": destination, "trace_id": trace_id}
            )
            
            self.observability.increment_counter(
                "planning_requests_total",
                tags={"destination": destination, "success": "false"}
            )
            
            return PlanningResult(
                success=False,
                itinerary=None,
                confidence=0.0,
                warnings=warnings,
                errors=errors,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                data_sources=data_sources
            )
    
    def _validate_input(self, context: PlanningContext) -> Tuple[bool, List[str]]:
        """验证输入数据"""
        errors = []
        
        # 目的地验证
        if context.destination not in self.itinerary_generator.attractions_db:
            available = ", ".join(self.itinerary_generator.attractions_db.keys())
            errors.append(f"不支持的目的地 '{context.destination}'。目前支持：{available}")
        
        # 天数验证
        if context.days < 1:
            errors.append("天数必须大于0")
        elif context.days > 30:
            warnings.append("天数超过30天，建议分段规划")
        
        # 日期验证
        try:
            datetime.strptime(context.start_date, "%Y-%m-%d")
        except ValueError:
            errors.append("日期格式错误，应为 YYYY-MM-DD")
        
        # 人数验证
        if context.travelers < 1:
            errors.append("人数必须大于0")
        elif context.travelers > 50:
            errors.append("人数超过限制（最大50人）")
        
        return len(errors) == 0, errors
    
    async def _get_data_recommendations(
        self,
        context: PlanningContext
    ) -> Dict[str, Any]:
        """获取数据驱动的推荐"""
        recommendations = {
            "attractions": [],
            "restaurants": [],
            "satisfaction_prediction": None
        }
        
        # 获取景点推荐
        try:
            attr_recs = self.data_engine.get_recommendations(
                context.destination,
                context.user_id,
                count=10
            )
            recommendations["attractions"] = [
                {"id": attr_id, "score": score}
                for attr_id, score in attr_recs
            ]
        except Exception as e:
            logger.warning(f"Failed to get attraction recommendations: {str(e)}")
        
        # 预测满意度
        if context.user_id:
            try:
                # 这里可以根据用户历史预测
                recommendations["satisfaction_prediction"] = {
                    "estimated": 4.2,
                    "confidence": 0.7
                }
            except Exception as e:
                logger.warning(f"Failed to predict satisfaction: {str(e)}")
        
        return recommendations
    
    async def _generate_base_itinerary(
        self,
        context: PlanningContext
    ) -> Dict[str, Any]:
        """生成基础行程"""
        itinerary = await self.itinerary_generator.generate_itinerary(
            destination=context.destination,
            days=context.days,
            start_date=context.start_date,
            travelers=context.travelers,
            preferences=context.preferences
        )
        
        return itinerary
    
    async def _optimize_with_data(
        self,
        base_itinerary: Dict[str, Any],
        context: PlanningContext,
        recommendations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """使用数据优化行程"""
        # 这里可以根据数据驱动的推荐调整行程
        # 例如：根据推荐分数调整景点顺序，替换低分景点等
        
        optimized = base_itinerary.copy()
        
        # 如果有数据驱动的推荐，应用它们
        if recommendations.get("attractions"):
            rec_attractions = {r["id"]: r["score"] for r in recommendations["attractions"]}
            
            for day_plan in optimized["daily_plans"]:
                for attraction in day_plan["attractions"]:
                    attraction_id = str(attraction["id"])
                    if attraction_id in rec_attractions:
                        attraction["data_driven_score"] = rec_attractions[attraction_id]
        
        return optimized
    
    async def _calculate_data_driven_budget(
        self,
        context: PlanningContext
    ) -> Dict[str, Any]:
        """计算数据驱动的预算"""
        return self.data_engine.predict_budget(
            destination=context.destination,
            days=context.days,
            travelers=context.travelers,
            room_type=context.preferences.get("accommodation_type", "standard")
        )
    
    async def _generate_intelligent_suggestions(
        self,
        itinerary: Dict[str, Any],
        context: PlanningContext
    ) -> List[Dict[str, Any]]:
        """生成智能建议"""
        suggestions = []
        
        # 分析预算
        budget = itinerary.get("budget", {})
        if budget.get("confidence", 0.5) < 0.7:
            suggestions.append({
                "type": "budget",
                "priority": "medium",
                "message": "预算预测置信度较低，建议预留20%的额外费用",
                "action": "increase_budget_buffer"
            })
        
        # 分析行程密度
        daily_costs = [day.get("estimated_cost", 0) for day in itinerary["daily_plans"]]
        if daily_costs and max(daily_costs) > min(daily_costs) * 2:
            suggestions.append({
                "type": "balance",
                "priority": "low",
                "message": "每日费用分布不均，建议调整行程以平衡费用",
                "action": "balance_itinerary"
            })
        
        # 分析景点评分
        low_rated_count = 0
        for day in itinerary["daily_plans"]:
            for attraction in day["attractions"]:
                if attraction.get("rating", 0) < 4.0:
                    low_rated_count += 1
        
        if low_rated_count > 0:
            suggestions.append({
                "type": "quality",
                "priority": "medium",
                "message": f"行程中有{low_rated_count}个低评分景点，可以考虑替换",
                "action": "replace_attractions"
            })
        
        return suggestions
    
    def _record_planning_metrics(
        self,
        context: PlanningContext,
        itinerary: Dict[str, Any]
    ):
        """记录规划指标"""
        # 记录事件数据
        self.data_engine.record_event(
            "planning_request",
            1.0,
            tags={
                "destination": context.destination,
                "days": context.days,
                "travelers": context.travelers,
                "user_id": context.user_id or "anonymous"
            }
        )
        
        # 记录预算
        budget = itinerary.get("budget", {})
        if budget:
            self.data_engine.record_event(
                "planned_budget",
                budget.get("total", 0),
                tags={
                    "destination": context.destination,
                    "travelers": context.travelers
                }
            )
    
    def get_system_health(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        return {
            "reliability": self.reliability_engine.get_health_status(),
            "data_engine": self.data_engine.get_data_summary(),
            "observability": self.observability.get_dashboard(),
            "metrics": self.reliability_engine.get_metrics_summary()
        }


# 全局实例
_intelligent_planner = None


def get_intelligent_planner() -> IntelligentPlanner:
    """获取智能规划器单例"""
    global _intelligent_planner
    if _intelligent_planner is None:
        _intelligent_planner = IntelligentPlanner()
    return _intelligent_planner
