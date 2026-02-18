"""
数据驱动引擎 - 基于PLTR哲学
所有决策基于真实数据和统计模型，而非规则
"""
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
from loguru import logger
import statistics


@dataclass
class DataPoint:
    """数据点"""
    timestamp: datetime
    metric: str
    value: float
    tags: Dict[str, Any] = None


@dataclass
class StatisticalInsight:
    """统计洞察"""
    metric: str
    mean: float
    median: float
    std: float
    percentile_95: float
    percentile_5: float
    trend: str  # increasing, decreasing, stable
    confidence: float


class DataCollector:
    """数据收集器 - 收集真实世界数据"""
    
    def __init__(self):
        self.data_points: List[DataPoint] = []
        self.aggregated_data: Dict[str, List[float]] = defaultdict(list)
    
    def collect(self, metric: str, value: float, tags: Dict[str, Any] = None):
        """收集数据点"""
        point = DataPoint(
            timestamp=datetime.now(),
            metric=metric,
            value=value,
            tags=tags or {}
        )
        self.data_points.append(point)
        self.aggregated_data[metric].append(value)
        
        # 保留最近10000个数据点
        if len(self.data_points) > 10000:
            self.data_points = self.data_points[-10000:]
    
    def get_recent_data(
        self,
        metric: str,
        hours: int = 24
    ) -> List[DataPoint]:
        """获取最近的数据"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            p for p in self.data_points
            if p.metric == metric and p.timestamp >= cutoff
        ]
    
    def get_values_by_tags(
        self,
        metric: str,
        tags: Dict[str, Any]
    ) -> List[float]:
        """根据标签获取值"""
        return [
            p.value
            for p in self.data_points
            if p.metric == metric and self._matches_tags(p.tags, tags)
        ]
    
    def _matches_tags(self, point_tags: Dict[str, Any], filter_tags: Dict[str, Any]) -> bool:
        """检查标签是否匹配"""
        for key, value in filter_tags.items():
            if key not in point_tags or point_tags[key] != value:
                return False
        return True


class StatisticalAnalyzer:
    """统计分析器 - 从数据中提取洞察"""
    
    def __init__(self, data_collector: DataCollector):
        self.data_collector = data_collector
    
    def analyze_metric(self, metric: str, hours: int = 24) -> StatisticalInsight:
        """分析指标"""
        values = self.data_collector.get_recent_data(metric, hours)
        
        if not values:
            return StatisticalInsight(
                metric=metric,
                mean=0.0,
                median=0.0,
                std=0.0,
                percentile_95=0.0,
                percentile_5=0.0,
                trend="stable",
                confidence=0.0
            )
        
        numeric_values = [v.value for v in values]
        
        # 计算统计量
        mean_val = statistics.mean(numeric_values)
        median_val = statistics.median(numeric_values)
        std_val = statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0.0
        
        # 百分位数
        sorted_values = sorted(numeric_values)
        p95 = sorted_values[int(len(sorted_values) * 0.95)] if sorted_values else 0.0
        p5 = sorted_values[int(len(sorted_values) * 0.05)] if sorted_values else 0.0
        
        # 趋势分析
        recent = numeric_values[-min(len(numeric_values), 10):]
        earlier = numeric_values[-min(len(numeric_values), 20):-10] if len(numeric_values) > 10 else []
        
        if earlier:
            trend = self._calculate_trend(earlier, recent)
        else:
            trend = "stable"
        
        # 置信度（基于样本量）
        confidence = min(len(numeric_values) / 100.0, 1.0)
        
        return StatisticalInsight(
            metric=metric,
            mean=mean_val,
            median=median_val,
            std=std_val,
            percentile_95=p95,
            percentile_5=p5,
            trend=trend,
            confidence=confidence
        )
    
    def _calculate_trend(self, earlier: List[float], recent: List[float]) -> str:
        """计算趋势"""
        if len(earlier) < 3 or len(recent) < 3:
            return "stable"
        
        earlier_avg = statistics.mean(earlier)
        recent_avg = statistics.mean(recent)
        
        # 使用相对变化率
        change_rate = (recent_avg - earlier_avg) / earlier_avg if earlier_avg > 0 else 0
        
        if abs(change_rate) < 0.05:  # 变化小于5%
            return "stable"
        elif change_rate > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def detect_anomalies(
        self,
        metric: str,
        threshold: float = 2.0
    ) -> List[DataPoint]:
        """检测异常值（使用Z-score）"""
        values = self.data_collector.get_recent_data(metric, 24)
        
        if len(values) < 10:
            return []
        
        numeric_values = [v.value for v in values]
        mean_val = statistics.mean(numeric_values)
        std_val = statistics.stdev(numeric_values) if len(numeric_values) > 1 else 1.0
        
        anomalies = []
        for v in values:
            z_score = (v.value - mean_val) / std_val if std_val > 0 else 0
            if abs(z_score) > threshold:
                anomalies.append(v)
        
        return anomalies


class RecommendationEngine:
    """推荐引擎 - 基于数据的推荐"""
    
    def __init__(self, data_collector: DataCollector, analyzer: StatisticalAnalyzer):
        self.data_collector = data_collector
        self.analyzer = analyzer
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        self.attraction_scores: Dict[str, Dict[str, float]] = {}
    
    def record_user_interaction(
        self,
        user_id: str,
        action: str,  # view, book, like, dislike
        attraction_id: str,
        destination: str
    ):
        """记录用户交互"""
        tags = {
            "user_id": user_id,
            "action": action,
            "attraction_id": attraction_id,
            "destination": destination
        }
        
        # 收集交互数据
        self.data_collector.collect(
            metric="user_interaction",
            value=1.0 if action in ["like", "book"] else 0.5,
            tags=tags
        )
        
        # 更新用户偏好
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = defaultdict(float)
        
        score_modifier = {
            "book": 2.0,
            "like": 1.0,
            "view": 0.3,
            "dislike": -1.0
        }
        
        self.user_preferences[user_id][attraction_id] += score_modifier.get(action, 0)
    
    def get_attraction_score(
        self,
        attraction_id: str,
        user_id: Optional[str] = None
    ) -> float:
        """
        获取景点综合评分
        
        基于多个因素：
        1. 全局评分（来自所有用户）
        2. 个人偏好（如果提供了user_id）
        3. 热门度（最近浏览量）
        4. 评分稳定性（标准差）
        """
        # 全局评分
        rating_values = self.data_collector.get_values_by_tags(
            "attraction_rating",
            {"attraction_id": attraction_id}
        )
        global_score = statistics.mean(rating_values) if rating_values else 3.0
        
        # 个人偏好分数
        personal_score = 0.0
        if user_id and user_id in self.user_preferences:
            personal_score = self.user_preferences[user_id].get(attraction_id, 0.0)
        
        # 热门度（最近7天）
        recent_views = len(self.data_collector.get_recent_data(
            "attraction_view",
            hours=24 * 7
        ))
        popularity_score = min(recent_views / 100.0, 2.0)  # 最多加2分
        
        # 评分稳定性（越稳定越可信）
        stability = 1.0
        if rating_values and len(rating_values) > 1:
            std_val = statistics.stdev(rating_values)
            stability = max(0.5, 1.0 - std_val / 2.0)  # 标准差越小，稳定性越高
        
        # 综合评分
        total_score = (
            global_score * 0.6 +  # 60% 权重
            personal_score * 0.2 +  # 20% 权重
            popularity_score * 0.1 +  # 10% 权重
            stability * 0.5  # 10% 权重
        )
        
        return min(max(total_score, 0.0), 5.0)  # 限制在0-5范围
    
    def recommend_attractions(
        self,
        destination: str,
        user_id: Optional[str] = None,
        count: int = 5
    ) -> List[Tuple[str, float]]:
        """推荐景点"""
        # 获取该目的地的所有景点
        all_attractions = set()
        for data in self.data_collector.get_recent_data("attraction_rating", hours=24 * 30):
            if data.tags and data.tags.get("destination") == destination:
                all_attractions.add(data.tags.get("attraction_id"))
        
        # 评分并排序
        scored_attractions = [
            (attr_id, self.get_attraction_score(attr_id, user_id))
            for attr_id in all_attractions
        ]
        
        # 按分数排序
        scored_attractions.sort(key=lambda x: x[1], reverse=True)
        
        return scored_attractions[:count]
    
    def predict_satisfaction(
        self,
        user_id: str,
        attractions: List[str]
    ) -> Dict[str, Any]:
        """预测用户满意度"""
        scores = [
            self.get_attraction_score(attr_id, user_id)
            for attr_id in attractions
        ]
        
        if not scores:
            return {
                "predicted_satisfaction": 3.0,
                "confidence": 0.0,
                "best_attraction": None,
                "worst_attraction": None
            }
        
        return {
            "predicted_satisfaction": statistics.mean(scores),
            "confidence": min(len(scores) / 5.0, 1.0),
            "best_attraction": max(zip(attractions, scores), key=lambda x: x[1])[0],
            "worst_attraction": min(zip(attractions, scores), key=lambda x: x[1])[0],
            "score_distribution": scores
        }


class BudgetPredictor:
    """预算预测器 - 基于历史数据预测费用"""
    
    def __init__(self, data_collector: DataCollector):
        self.data_collector = data_collector
    
    def predict_attraction_cost(
        self,
        destination: str,
        days: int,
        travelers: int
    ) -> Dict[str, Any]:
        """预测景点费用"""
        cost_values = self.data_collector.get_values_by_tags(
            "attraction_cost",
            {"destination": destination}
        )
        
        if not cost_values:
            # 使用默认值
            default_costs = {
                "京都": 50,
                "东京": 80,
                "大阪": 40
            }
            avg_cost = default_costs.get(destination, 50)
        else:
            avg_cost = statistics.mean(cost_values)
        
        # 预测总费用（基于历史平均）
        predicted_total = avg_cost * days * travelers
        
        # 计算置信区间
        if len(cost_values) > 1:
            std_val = statistics.stdev(cost_values)
            margin = 1.96 * std_val  # 95% 置信区间
        else:
            margin = avg_cost * 0.2  # 默认20%误差
        
        return {
            "predicted_total": predicted_total,
            "per_person_per_day": avg_cost,
            "confidence_interval": {
                "lower": predicted_total - margin,
                "upper": predicted_total + margin
            },
            "confidence": min(len(cost_values) / 50.0, 1.0)
        }
    
    def predict_accommodation_cost(
        self,
        destination: str,
        days: int,
        room_type: str = "standard"
    ) -> Dict[str, Any]:
        """预测住宿费用"""
        cost_values = self.data_collector.get_values_by_tags(
            "accommodation_cost",
            {"destination": destination, "room_type": room_type}
        )
        
        if not cost_values:
            # 使用默认值
            default_costs = {
                ("京都", "standard"): 500,
                ("东京", "standard"): 700,
                ("京都", "luxury"): 1500,
                ("东京", "luxury"): 2000
            }
            avg_cost = default_costs.get((destination, room_type), 600)
        else:
            avg_cost = statistics.mean(cost_values)
        
        predicted_total = avg_cost * (days - 1)  # nights
        
        return {
            "predicted_total": predicted_total,
            "per_night": avg_cost,
            "total_nights": days - 1
        }


class DataDrivenEngine:
    """数据驱动引擎 - 整合所有组件"""
    
    def __init__(self):
        self.data_collector = DataCollector()
        self.analyzer = StatisticalAnalyzer(self.data_collector)
        self.recommendation_engine = RecommendationEngine(
            self.data_collector, self.analyzer
        )
        self.budget_predictor = BudgetPredictor(self.data_collector)
    
    def record_event(
        self,
        metric: str,
        value: float,
        tags: Dict[str, Any] = None
    ):
        """记录事件数据"""
        self.data_collector.collect(metric, value, tags)
    
    def get_insights(self, metric: str, hours: int = 24) -> StatisticalInsight:
        """获取数据洞察"""
        return self.analyzer.analyze_metric(metric, hours)
    
    def detect_anomalies(self, metric: str) -> List[DataPoint]:
        """检测异常"""
        return self.analyzer.detect_anomalies(metric)
    
    def get_recommendations(
        self,
        destination: str,
        user_id: Optional[str] = None
    ) -> List[Tuple[str, float]]:
        """获取推荐"""
        return self.recommendation_engine.recommend_attractions(destination, user_id)
    
    def predict_budget(
        self,
        destination: str,
        days: int,
        travelers: int,
        room_type: str = "standard"
    ) -> Dict[str, Any]:
        """预测预算"""
        attraction_cost = self.budget_predictor.predict_attraction_cost(
            destination, days, travelers
        )
        accommodation_cost = self.budget_predictor.predict_accommodation_cost(
            destination, days, room_type
        )
        
        # 餐饮费用估算（基于历史数据）
        food_values = self.data_collector.get_values_by_tags(
            "food_cost_per_person",
            {"destination": destination}
        )
        avg_food_cost = statistics.mean(food_values) if food_values else 200
        
        food_cost = avg_food_cost * days * travelers
        
        # 交通费用估算
        transport_values = self.data_collector.get_values_by_tags(
            "transport_cost_per_day",
            {"destination": destination}
        )
        avg_transport_cost = statistics.mean(transport_values) if transport_values else 50
        
        transport_cost = avg_transport_cost * days
        
        total = (
            attraction_cost["predicted_total"] +
            accommodation_cost["predicted_total"] +
            food_cost +
            transport_cost
        )
        
        return {
            "total": total,
            "breakdown": {
                "attractions": attraction_cost,
                "accommodation": accommodation_cost,
                "food": food_cost,
                "transport": transport_cost
            },
            "per_person": total / travelers,
            "confidence": min(
                attraction_cost.get("confidence", 0.5),
                len(food_values) / 100.0,
                len(transport_values) / 100.0
            )
        }
    
    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要"""
        summary = {
            "total_data_points": len(self.data_collector.data_points),
            "metrics": list(self.data_collector.aggregated_data.keys()),
            "data_by_metric": {
                metric: len(values)
                for metric, values in self.data_collector.aggregated_data.items()
            }
        }
        return summary


# 全局实例
_data_driven_engine = None


def get_data_driven_engine() -> DataDrivenEngine:
    """获取数据驱动引擎单例"""
    global _data_driven_engine
    if _data_driven_engine is None:
        _data_driven_engine = DataDrivenEngine()
    return _data_driven_engine
