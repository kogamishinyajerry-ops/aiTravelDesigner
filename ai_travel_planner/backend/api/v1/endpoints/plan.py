"""
Plan Endpoint
行程规划端点 - 集成行程生成和预算计算
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from loguru import logger
from services.planning.itinerary_generator import get_itinerary_generator
from services.planning.budget_calculator import get_budget_calculator

router = APIRouter()


class GeneratePlanRequest(BaseModel):
    """生成行程请求"""
    destination: str = Field(..., description="目的地", min_length=1)
    days: int = Field(..., description="天数", ge=1, le=30)
    start_date: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    travelers: int = Field(1, description="人数", ge=1, le=20)
    departure: Optional[str] = Field("北京", description="出发地")
    budget: Optional[float] = Field(None, description="预算")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="偏好设置")
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "京都",
                "days": 5,
                "start_date": "2024-04-01",
                "travelers": 2,
                "departure": "北京",
                "budget": 20000,
                "preferences": {
                    "interests": ["历史", "文化"],
                    "room_type": "standard",
                    "meal_level": "standard"
                }
            }
        }


class BudgetRequest(BaseModel):
    """预算计算请求"""
    departure: str = Field(..., description="出发地")
    destination: str = Field(..., description="目的地")
    days: int = Field(..., description="天数", ge=1, le=30)
    travelers: int = Field(..., description="人数", ge=1, le=20)
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="偏好设置")


@router.post("/generate")
async def generate_itinerary(request: GeneratePlanRequest):
    """
    生成完整行程（包含每日安排 + 预算分析）
    
    Args:
        request: 行程请求
    
    Returns:
        生成的行程和预算
    """
    try:
        logger.info(f"Generating itinerary: {request.destination}, {request.days} days, {request.travelers} travelers")

        # 1. 生成行程
        generator = get_itinerary_generator()
        
        try:
            itinerary = await generator.generate_itinerary(
                destination=request.destination,
                days=request.days,
                start_date=request.start_date,
                travelers=request.travelers,
                preferences=request.preferences or {}
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        # 2. 计算预算
        calculator = get_budget_calculator()
        
        budget = await calculator.calculate_total_budget(
            departure=request.departure or "北京",
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            preferences=request.preferences or {}
        )

        # 3. 如果用户提供了预算，进行可行性分析
        feasibility = None
        if request.budget:
            feasibility = calculator.check_budget_feasibility(
                user_budget=request.budget,
                estimated_cost=budget["total_cost"]
            )

        return {
            "success": True,
            "message": "行程生成成功",
            "itinerary": itinerary,
            "budget": budget,
            "budget_feasibility": feasibility
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Itinerary generation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )


@router.post("/budget")
async def calculate_budget(request: BudgetRequest):
    """
    计算预算（独立接口）
    
    Args:
        request: 预算计算请求
    
    Returns:
        预算分解
    """
    try:
        logger.info(f"Calculating budget: {request.departure} → {request.destination}, {request.days} days")

        calculator = get_budget_calculator()
        
        budget = await calculator.calculate_total_budget(
            departure=request.departure,
            destination=request.destination,
            days=request.days,
            travelers=request.travelers,
            preferences=request.preferences or {}
        )

        return {
            "success": True,
            "message": "预算计算成功",
            "budget": budget
        }

    except Exception as e:
        logger.error(f"Budget calculation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Calculation failed: {str(e)}"
        )


@router.get("/destinations")
async def get_supported_destinations():
    """
    获取支持的目的地列表
    
    Returns:
        目的地列表和简介
    """
    try:
        destinations = [
            {
                "id": "kyoto",
                "name": "京都",
                "name_en": "Kyoto",
                "country": "日本",
                "description": "千年古都，历史文化名城",
                "recommended_days": "3-5天",
                "avg_daily_budget": 500,
                "tags": ["历史", "文化", "美食", "自然"]
            },
            {
                "id": "tokyo",
                "name": "东京",
                "name_en": "Tokyo",
                "country": "日本",
                "description": "现代都市，购物美食天堂",
                "recommended_days": "4-6天",
                "avg_daily_budget": 600,
                "tags": ["购物", "美食", "现代", "动漫"]
            },
            {
                "id": "osaka",
                "name": "大阪",
                "name_en": "Osaka",
                "country": "日本",
                "description": "美食之都，活力四射",
                "recommended_days": "2-3天",
                "avg_daily_budget": 450,
                "tags": ["美食", "购物", "主题公园"]
            },
            {
                "id": "bangkok",
                "name": "曼谷",
                "name_en": "Bangkok",
                "country": "泰国",
                "description": "热带风情，佛教文化",
                "recommended_days": "3-4天",
                "avg_daily_budget": 300,
                "tags": ["佛教", "美食", "购物", "海滩"]
            },
            {
                "id": "paris",
                "name": "巴黎",
                "name_en": "Paris",
                "country": "法国",
                "description": "浪漫之都，艺术天堂",
                "recommended_days": "4-7天",
                "avg_daily_budget": 1200,
                "tags": ["艺术", "历史", "浪漫", "美食"]
            },
        ]

        return {
            "success": True,
            "destinations": destinations
        }

    except Exception as e:
        logger.error(f"Get destinations error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/optimization")
async def optimize_plan(
    destination: str,
    days: int,
    budget: float,
    travelers: int
):
    """
    行程优化建议
    
    Args:
        destination: 目的地
        days: 天数
        budget: 预算
        travelers: 人数
    
    Returns:
        优化建议
    """
    try:
        calculator = get_budget_calculator()
        
        # 先计算标准预算
        estimated = await calculator.calculate_total_budget(
            departure="北京",
            destination=destination,
            days=days,
            travelers=travelers,
            preferences={}
        )
        
        # 分析可行性
        feasibility = calculator.check_budget_feasibility(budget, estimated["total_cost"])
        
        # 生成优化方案
        optimizations = []
        
        if feasibility["status"] in ["insufficient", "significantly_insufficient"]:
            # 缩短行程
            for reduced_days in range(days, max(1, days - 3), -1):
                reduced_budget = await calculator.calculate_total_budget(
                    departure="北京",
                    destination=destination,
                    days=reduced_days,
                    travelers=travelers,
                    preferences={}
                )
                
                if reduced_budget["total_cost"] <= budget:
                    optimizations.append({
                        "type": "reduce_days",
                        "description": f"缩短行程至{reduced_days}天",
                        "new_cost": reduced_budget["total_cost"],
                        "saving": estimated["total_cost"] - reduced_budget["total_cost"]
                    })
                    break
            
            # 调整住宿标准
            for room_type in ["budget", "standard", "comfort"]:
                adjusted_budget = await calculator.calculate_total_budget(
                    departure="北京",
                    destination=destination,
                    days=days,
                    travelers=travelers,
                    preferences={"room_type": room_type}
                )
                
                if adjusted_budget["total_cost"] <= budget and room_type != "standard":
                    optimizations.append({
                        "type": "adjust_accommodation",
                        "description": f"选择{room_type}型住宿",
                        "new_cost": adjusted_budget["total_cost"],
                        "saving": estimated["total_cost"] - adjusted_budget["total_cost"]
                    })
                    break

        return {
            "success": True,
            "feasibility": feasibility,
            "optimizations": optimizations,
            "recommendation": (
                f"建议{optimizations[0]['description']}" 
                if optimizations else feasibility["message"]
            )
        }

    except Exception as e:
        logger.error(f"Optimization error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
