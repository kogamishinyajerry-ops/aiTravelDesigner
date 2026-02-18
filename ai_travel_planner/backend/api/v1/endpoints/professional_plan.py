"""
专业行程规划API
提供标准化、规范化的行程规划接口
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from loguru import logger

from services.planning import (
    TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType,
    TravelRequirements, ProfessionalItinerary,
    get_professional_planning_service
)


# 请求模型
class TravelRequirementsRequest(BaseModel):
    """旅行需求请求模型"""
    destination: str = Field(..., description="目的地")
    departure_city: str = Field(default="北京", description="出发城市")
    start_date: str = Field(..., description="出发日期 YYYY-MM-DD")
    end_date: str = Field(..., description="返回日期 YYYY-MM-DD")
    days: int = Field(..., description="旅行天数", ge=1, le=30)
    
    # 人员信息
    travelers_adults: int = Field(default=1, description="成人人数", ge=1)
    travelers_children: int = Field(default=0, description="儿童人数", ge=0)
    travelers_infants: int = Field(default=0, description="婴幼儿人数", ge=0)
    travelers_seniors: int = Field(default=0, description="老年人数", ge=0)
    
    # 旅行偏好
    travel_style: str = Field(default="leisure", description="旅行风格")
    activity_intensity: str = Field(default="moderate", description="活动强度")
    budget_level: str = Field(default="standard", description="预算等级")
    budget_limit: Optional[float] = Field(default=None, description="预算限制")
    
    # 兴趣和偏好
    interests: List[str] = Field(default_factory=list, description="兴趣主题")
    accommodation_type: str = Field(default="standard_hotel", description="住宿类型")
    accommodation_preferences: List[str] = Field(default_factory=list, description="住宿偏好")
    meal_plan: str = Field(default="breakfast_only", description="餐饮计划")
    
    # 交通
    flight_class: str = Field(default="economy", description="航班舱位")
    transport_preference: str = Field(default="convenience", description="交通偏好")
    
    # 特殊需求
    accessibility_needs: List[str] = Field(default_factory=list, description="无障碍需求")
    dietary_restrictions: List[str] = Field(default_factory=list, description="饮食限制")
    special_occasions: List[str] = Field(default_factory=list, description="特殊场合")
    
    # 其他
    language_preference: str = Field(default="chinese", description="语言偏好")
    guide_required: bool = Field(default=False, description="是否需要导游")
    notes: str = Field(default="", description="备注")
    
    def to_travel_requirements(self) -> TravelRequirements:
        """转换为TravelRequirements对象"""
        return TravelRequirements(
            destination=self.destination,
            departure_city=self.departure_city,
            start_date=self.start_date,
            end_date=self.end_date,
            days=self.days,
            travelers_adults=self.travelers_adults,
            travelers_children=self.travelers_children,
            travelers_infants=self.travelers_infants,
            travelers_seniors=self.travelers_seniors,
            travel_style=TravelStyle(self.travel_style),
            activity_intensity=ActivityIntensity(self.activity_intensity),
            budget_level=BudgetLevel(self.budget_level),
            budget_limit=self.budget_limit,
            interests=self.interests,
            accommodation_type=AccommodationType(self.accommodation_type),
            accommodation_preferences=self.accommodation_preferences,
            meal_plan=self.meal_plan,
            flight_class=self.flight_class,
            transport_preference=self.transport_preference,
            accessibility_needs=self.accessibility_needs,
            dietary_restrictions=self.dietary_restrictions,
            special_occasions=self.special_occasions,
            language_preference=self.language_preference,
            guide_required=self.guide_required,
            notes=self.notes
        )


class ItineraryModificationRequest(BaseModel):
    """行程修改请求"""
    session_id: str = Field(..., description="会话ID")
    modifications: Dict[str, Any] = Field(..., description="修改内容")


router = APIRouter(prefix="/professional", tags=["专业行程规划"])


@router.post(
    "/create-itinerary",
    response_model=Dict[str, Any],
    summary="创建专业行程",
    description="根据标准化需求创建专业旅行行程"
)
async def create_professional_itinerary(
    request: TravelRequirementsRequest,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    创建专业行程
    
    按照专业旅行规划师的标准流程生成行程：
    1. 需求收集与分析
    2. 目的地研究
    3. 行程框架设计
    4. 详细行程制定
    5. 预算计算
    6. 住宿与交通安排
    7. 风险评估
    8. 行程优化
    9. 客户确认
    10. 最终交付
    """
    try:
        # 转换需求
        requirements = request.to_travel_requirements()
        
        # 验证需求
        is_valid, errors = requirements.validate()
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": errors}
            )
        
        # 创建行程
        service = get_professional_planning_service()
        itinerary, new_session_id = await service.create_itinerary_from_requirements(
            requirements,
            session_id
        )
        
        return {
            "success": True,
            "session_id": new_session_id,
            "itinerary_id": itinerary.itinerary_id,
            "itinerary": _format_itinerary(itinerary),
            "created_at": itinerary.created_at.isoformat()
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Failed to create itinerary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建行程失败: {str(e)}"
        )


@router.put(
    "/modify-itinerary",
    response_model=Dict[str, Any],
    summary="修改行程",
    description="根据用户反馈修改现有行程"
)
async def modify_itinerary(request: ItineraryModificationRequest) -> Dict[str, Any]:
    """
    修改行程
    
    支持修改以下内容：
    - 延长/缩短天数
    - 更改预算
    - 调整活动强度
    - 更改住宿类型
    - 修改兴趣偏好
    """
    try:
        service = get_professional_planning_service()
        itinerary = await service.update_itinerary(
            request.session_id,
            request.modifications
        )
        
        if not itinerary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在或行程未找到"
            )
        
        return {
            "success": True,
            "session_id": request.session_id,
            "itinerary_id": itinerary.itinerary_id,
            "itinerary": _format_itinerary(itinerary),
            "version": itinerary.version,
            "modified_at": itinerary.last_modified.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to modify itinerary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"修改行程失败: {str(e)}"
        )


@router.get(
    "/progress/{session_id}",
    response_model=Dict[str, Any],
    summary="获取规划进度",
    description="获取工作流规划进度"
)
async def get_progress(session_id: str) -> Dict[str, Any]:
    """获取规划进度"""
    try:
        service = get_professional_planning_service()
        progress = service.get_session_progress(session_id)
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在"
            )
        
        return {
            "success": True,
            "progress": progress
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to get progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取进度失败: {str(e)}"
        )


@router.get(
    "/report/{session_id}",
    response_model=Dict[str, Any],
    summary="导出规划报告",
    description="导出完整的规划报告和工作流详情"
)
async def export_report(session_id: str) -> Dict[str, Any]:
    """导出规划报告"""
    try:
        service = get_professional_planning_service()
        report = service.export_session_report(session_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在"
            )
        
        return {
            "success": True,
            "report": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to export report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"导出报告失败: {str(e)}"
        )


@router.get(
    "/standards",
    response_model=Dict[str, Any],
    summary="获取规划标准",
    description="获取专业旅行规划标准和指南"
)
async def get_planning_standards() -> Dict[str, Any]:
    """获取规划标准"""
    try:
        from services.planning import (
            ProfessionalPlanningStandards,
            TravelStyle, ActivityIntensity, BudgetLevel
        )
        
        return {
            "success": True,
            "standards": {
                "travel_styles": [
                    {"value": style.value, "description": style.name}
                    for style in TravelStyle
                ],
                "activity_intensities": [
                    {"value": intensity.value, "description": intensity.name}
                    for intensity in ActivityIntensity
                ],
                "budget_levels": [
                    {"value": level.value, "description": level.name}
                    for level in BudgetLevel
                ],
                "time_standards": {
                    "min_attraction_duration": ProfessionalPlanningStandards.MIN_ATTRACTION_DURATION,
                    "max_attraction_duration": ProfessionalPlanningStandards.MAX_ATTRACTION_DURATION,
                    "meal_duration": ProfessionalPlanningStandards.MEAL_DURATION,
                    "transit_time_buffer": ProfessionalPlanningStandards.TRANSIT_TIME_BUFFER,
                    "daily_start_time": ProfessionalPlanningStandards.DAILY_START_TIME,
                    "daily_end_time": ProfessionalPlanningStandards.DAILY_END_TIME
                },
                "distance_standards": {
                    "max_daily_transit_distance": ProfessionalPlanningStandards.MAX_DAILY_TRANSIT_DISTANCE,
                    "optimal_attraction_distance": ProfessionalPlanningStandards.OPTIMAL_ATTRACTION_DISTANCE
                }
            }
        }
        
    except Exception as e:
        logger.exception(f"Failed to get standards: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取标准失败: {str(e)}"
        )


@router.post(
    "/validate-requirements",
    response_model=Dict[str, Any],
    summary="验证需求完整性",
    description="验证旅行需求是否完整"
)
async def validate_requirements(request: TravelRequirementsRequest) -> Dict[str, Any]:
    """验证需求完整性"""
    try:
        requirements = request.to_travel_requirements()
        is_valid, errors = requirements.validate()
        
        return {
            "success": True,
            "is_valid": is_valid,
            "errors": errors if not is_valid else [],
            "total_travelers": requirements.total_travelers(),
            "total_children": requirements.calculate_children_count()
        }
        
    except Exception as e:
        logger.exception(f"Failed to validate requirements: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证失败: {str(e)}"
        )


def _format_itinerary(itinerary: ProfessionalItinerary) -> Dict[str, Any]:
    """格式化行程输出"""
    return {
        "itinerary_id": itinerary.itinerary_id,
        "status": itinerary.status,
        "version": itinerary.version,
        "created_at": itinerary.created_at.isoformat(),
        "last_modified": itinerary.last_modified.isoformat() if itinerary.last_modified else None,
        "destination": itinerary.requirements.destination,
        "days": itinerary.requirements.days,
        "start_date": itinerary.requirements.start_date,
        "end_date": itinerary.requirements.end_date,
        "travelers": itinerary.requirements.total_travelers(),
        "travel_style": itinerary.requirements.travel_style.value,
        "budget_level": itinerary.requirements.budget_level.value,
        "daily_plans": itinerary.daily_plans,
        "accommodation": itinerary.accommodation,
        "transportation": itinerary.transportation,
        "budget": itinerary.budget_breakdown,
        "planning_notes": itinerary.planning_notes,
        "recommendations": itinerary.recommendations,
        "warnings": itinerary.warnings
    }
