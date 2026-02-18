"""
智能规划API - 基于PLTR哲学
提供可靠、数据驱动、可观测的行程规划API
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

from ...services.planning.intelligent_planner import (
    IntelligentPlanner,
    get_intelligent_planner
)
from loguru import logger


router = APIRouter(prefix="/intelligent", tags=["intelligent"])


class ItineraryPlanningRequest(BaseModel):
    """行程规划请求"""
    destination: str = Field(..., description="目的地", example="京都")
    days: int = Field(..., ge=1, le=30, description="行程天数", example=5)
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)", example="2026-03-01")
    travelers: int = Field(..., ge=1, le=50, description="旅行人数", example=2)
    user_id: Optional[str] = Field(None, description="用户ID（用于个性化推荐）")
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="偏好设置",
        example={
            "interests": ["历史", "文化", "美食"],
            "price_level": 3,
            "accommodation_type": "酒店",
            "min_rating": 4.0
        }
    )
    
    @validator('start_date')
    def validate_start_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError('日期格式错误，应为 YYYY-MM-DD')
        return v
    
    @validator('destination')
    def validate_destination(cls, v):
        supported = ["京都", "东京", "大阪"]
        if v not in supported:
            raise ValueError(f'不支持的目的地，支持: {", ".join(supported)}')
        return v


class PlanningResponse(BaseModel):
    """规划响应"""
    success: bool
    itinerary: Optional[Dict[str, Any]] = None
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_time_ms: float
    data_sources: List[str]
    planning_id: str


class SystemHealthResponse(BaseModel):
    """系统健康响应"""
    reliability: Dict[str, Any]
    data_engine: Dict[str, Any]
    observability: Dict[str, Any]
    metrics: Dict[str, Any]
    timestamp: str


@router.post("/plan", response_model=PlanningResponse)
async def plan_itinerary(
    request: ItineraryPlanningRequest,
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    智能规划行程
    
    这个API端点集成了PLTR的所有核心原则：
    1. **可靠性**：使用熔断器、降级策略和容错机制
    2. **数据驱动**：基于真实数据和统计模型进行推荐
    3. **可观测性**：全链路追踪、指标收集和告警
    
    返回一个优化的行程方案，包含：
    - 每日详细安排
    - 预算预测
    - 智能建议
    - 用户满意度预测
    - 执行指标
    """
    try:
        logger.info(
            f"Received planning request: {request.destination}, "
            f"{request.days} days, {request.travelers} travelers"
        )
        
        # 异步执行规划
        result = await planner.plan_itinerary(
            destination=request.destination,
            days=request.days,
            start_date=request.start_date,
            travelers=request.travelers,
            preferences=request.preferences,
            user_id=request.user_id
        )
        
        # 生成规划ID
        planning_id = f"{request.destination}_{request.days}d_{int(datetime.now().timestamp())}"
        
        response = PlanningResponse(
            success=result.success,
            itinerary=result.itinerary,
            confidence=result.confidence,
            warnings=result.warnings,
            errors=result.errors,
            execution_time_ms=result.execution_time_ms,
            data_sources=result.data_sources,
            planning_id=planning_id
        )
        
        if result.success:
            logger.info(
                f"Planning succeeded: {planning_id}, "
                f"confidence={result.confidence:.2f}, "
                f"time={result.execution_time_ms:.2f}ms"
            )
        else:
            logger.warning(
                f"Planning failed: {planning_id}, "
                f"errors={result.errors}"
            )
        
        return response
    
    except Exception as e:
        logger.error(f"Planning error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"行程规划失败: {str(e)}"
        )


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health(
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    获取系统健康状态
    
    返回：
    - 可靠性引擎状态
    - 数据引擎统计
    - 可观测性仪表板
    - 系统指标摘要
    """
    try:
        health = planner.get_system_health()
        
        return SystemHealthResponse(
            reliability=health["reliability"],
            data_engine=health["data_engine"],
            observability=health["observability"],
            metrics=health["metrics"],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"健康检查失败: {str(e)}"
        )


@router.get("/metrics")
async def get_metrics(
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    获取详细指标
    
    返回系统的所有指标数据，用于监控和分析
    """
    try:
        metrics = planner.observability.metrics.get_all_metrics()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
    
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取指标失败: {str(e)}"
        )


@router.get("/traces/{trace_id}")
async def get_trace(
    trace_id: str,
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    获取追踪记录
    
    返回指定trace_id的所有追踪事件
    """
    try:
        events = planner.observability.tracer.get_trace(trace_id)
        
        return {
            "trace_id": trace_id,
            "events": [
                {
                    "event_id": e.event_id,
                    "span_id": e.span_id,
                    "timestamp": e.timestamp.isoformat(),
                    "service": e.service,
                    "operation": e.operation,
                    "level": e.level.value,
                    "message": e.message,
                    "tags": e.tags,
                    "duration_ms": e.duration_ms
                }
                for e in events
            ]
        }
    
    except Exception as e:
        logger.error(f"Trace error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取追踪记录失败: {str(e)}"
        )


@router.post("/feedback")
async def record_feedback(
    feedback: Dict[str, Any],
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    记录用户反馈
    
    用于持续改进推荐算法和行程质量
    """
    try:
        required_fields = ["user_id", "planning_id", "rating"]
        for field in required_fields:
            if field not in feedback:
                raise HTTPException(
                    status_code=400,
                    detail=f"缺少必需字段: {field}"
                )
        
        # 记录反馈到数据引擎
        user_id = feedback["user_id"]
        planning_id = feedback["planning_id"]
        rating = feedback["rating"]
        comments = feedback.get("comments", "")
        
        # 这里可以记录到数据库
        logger.info(
            f"Received feedback from {user_id} for {planning_id}: "
            f"rating={rating}, comments={comments}"
        )
        
        # 记录交互数据
        planner.data_engine.record_event(
            "user_feedback",
            rating,
            tags={
                "user_id": user_id,
                "planning_id": planning_id,
                "comments_length": len(comments)
            }
        )
        
        return {
            "success": True,
            "message": "反馈已记录",
            "feedback_id": f"{user_id}_{planning_id}_{int(datetime.now().timestamp())}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"记录反馈失败: {str(e)}"
        )


@router.get("/recommendations")
async def get_recommendations(
    destination: str,
    user_id: Optional[str] = None,
    count: int = 5,
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    获取景点推荐
    
    基于数据驱动的推荐引擎返回最佳景点
    """
    try:
        recommendations = planner.data_engine.get_recommendations(
            destination=destination,
            user_id=user_id,
            count=count
        )
        
        return {
            "destination": destination,
            "user_id": user_id,
            "count": len(recommendations),
            "recommendations": [
                {"attraction_id": attr_id, "score": score}
                for attr_id, score in recommendations
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取推荐失败: {str(e)}"
        )


@router.post("/predict/budget")
async def predict_budget(
    prediction_request: Dict[str, Any],
    planner: IntelligentPlanner = Depends(get_intelligent_planner)
):
    """
    预测预算
    
    基于历史数据和统计模型预测旅行预算
    """
    try:
        required_fields = ["destination", "days", "travelers"]
        for field in required_fields:
            if field not in prediction_request:
                raise HTTPException(
                    status_code=400,
                    detail=f"缺少必需字段: {field}"
                )
        
        budget = planner.data_engine.predict_budget(
            destination=prediction_request["destination"],
            days=prediction_request["days"],
            travelers=prediction_request["travelers"],
            room_type=prediction_request.get("room_type", "standard")
        )
        
        return {
            **budget,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Budget prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"预算预测失败: {str(e)}"
        )
