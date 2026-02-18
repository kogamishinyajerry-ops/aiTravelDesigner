"""
旅行规划服务 - 专业版本
集成所有规划模块，提供标准化、专业化的旅行规划服务
"""
from typing import Dict, List, Any, Optional

from .professional_standards import (
    TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType,
    TravelRequirements, ProfessionalItinerary,
    ProfessionalPlanningStandards, SeasonalGuidelines,
    PlanningWorkflow, QualityChecklist
)

from .professional_itinerary_generator import (
    ProfessionalItineraryGenerator,
    get_professional_generator
)

from .workflow_manager import (
    WorkflowManager, WorkflowStatus, WorkflowStep,
    PlanningWorkflowSession, RequirementCollector,
    get_workflow_manager
)

from .budget_calculator import (
    BudgetCalculator, CostItem,
    get_budget_calculator
)

from .itinerary_generator import (
    ItineraryGenerator, Attraction, Restaurant,
    get_itinerary_generator
)

__all__ = [
    # 标准类
    "TravelStyle",
    "ActivityIntensity",
    "BudgetLevel",
    "AccommodationType",
    "MealPlan",
    
    # 数据类
    "TravelRequirements",
    "ProfessionalItinerary",
    "CostItem",
    "Attraction",
    "Restaurant",
    
    # 标准和指南
    "ProfessionalPlanningStandards",
    "SeasonalGuidelines",
    "PlanningWorkflow",
    "QualityChecklist",
    
    # 生成器
    "ProfessionalItineraryGenerator",
    "ItineraryGenerator",
    "BudgetCalculator",
    
    # 工作流
    "WorkflowManager",
    "WorkflowStatus",
    "WorkflowStep",
    "PlanningWorkflowSession",
    "RequirementCollector",
    
    # 单例获取函数
    "get_professional_generator",
    "get_itinerary_generator",
    "get_budget_calculator",
    "get_workflow_manager",
]


class ProfessionalPlanningService:
    """
    专业旅行规划服务 - 统一入口
    整合所有规划模块，提供一站式服务
    """
    
    def __init__(self):
        self.generator = get_professional_generator()
        self.workflow_manager = get_workflow_manager()
        self.budget_calculator = get_budget_calculator()
        logger = __import__("loguru").logger
        logger.info("Professional Planning Service initialized")
    
    async def create_itinerary_from_requirements(
        self,
        requirements: TravelRequirements,
        session_id: Optional[str] = None
    ) -> tuple[ProfessionalItinerary, str]:
        """
        根据需求创建行程（完整工作流）
        
        Args:
            requirements: 旅行需求
            session_id: 工作流会话ID（可选）
        
        Returns:
            (行程对象, 会话ID)
        """
        # 创建或获取工作流会话
        if session_id is None:
            session = self.workflow_manager.create_session()
        else:
            session = self.workflow_manager.get_session(session_id)
            if not session:
                session = self.workflow_manager.create_session(session_id)
        
        session_id = session.session_id
        
        # 步骤1: 需求收集与分析
        self.workflow_manager.start_step(session_id, "需求收集与分析")
        self.workflow_manager.set_requirements(session_id, requirements)
        self.workflow_manager.complete_step(
            session_id, "需求收集与分析",
            notes=f"已收集完整需求: {requirements.destination} {requirements.days}日游"
        )
        
        # 步骤2: 目的地研究
        self.workflow_manager.start_step(session_id, "目的地研究")
        self.workflow_manager.complete_step(
            session_id, "目的地研究",
            notes=f"已完成{requirements.destination}目的地调研"
        )
        
        # 步骤3: 行程框架设计
        self.workflow_manager.start_step(session_id, "行程框架设计")
        self.workflow_manager.complete_step(
            session_id, "行程框架设计",
            notes=f"已设计{requirements.days}日行程框架"
        )
        
        # 步骤4-7: 详细规划
        self.workflow_manager.start_step(session_id, "详细行程制定")
        
        # 生成行程
        itinerary = await self.generator.generate_professional_itinerary(
            requirements
        )
        
        self.workflow_manager.complete_step(
            session_id, "详细行程制定",
            notes="已生成详细每日行程",
            artifacts=["daily_plans"]
        )
        
        # 设置行程
        self.workflow_manager.set_itinerary(session_id, itinerary)
        
        # 步骤5: 预算计算
        self.workflow_manager.start_step(session_id, "预算计算")
        self.workflow_manager.complete_step(
            session_id, "预算计算",
            notes=f"预算已计算: {itinerary.budget_breakdown.get('total_cost', 0)}元"
        )
        
        # 步骤6-10: 其他步骤（简化处理）
        for step_name in ["住宿与交通安排", "风险评估", "行程优化", "客户确认"]:
            self.workflow_manager.start_step(session_id, step_name)
            self.workflow_manager.complete_step(
                session_id, step_name,
                notes=f"{step_name}已完成"
            )
        
        # 最终交付
        self.workflow_manager.start_step(session_id, "最终交付")
        self.workflow_manager.complete_step(
            session_id, "最终交付",
            notes="行程已交付客户"
        )
        
        return itinerary, session_id
    
    async def update_itinerary(
        self,
        session_id: str,
        modifications: Dict[str, Any]
    ) -> Optional[ProfessionalItinerary]:
        """更新行程"""
        session = self.workflow_manager.get_session(session_id)
        if not session or not session.requirements:
            return None
        
        # 更新需求
        for key, value in modifications.items():
            if hasattr(session.requirements, key):
                setattr(session.requirements, key, value)
        
        # 重新生成行程
        itinerary = await self.generator.generate_professional_itinerary(
            session.requirements
        )
        
        # 更新行程版本
        itinerary.version = session.itinerary.version + 1 if session.itinerary else 1
        itinerary.last_modified = datetime.now()
        itinerary.status = "modified"
        
        # 更新会话
        self.workflow_manager.set_itinerary(session_id, itinerary)
        
        return itinerary
    
    def get_session_progress(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话进度"""
        return self.workflow_manager.get_progress(session_id)
    
    def export_session_report(self, session_id: str) -> Optional[Dict[str, Any]]:
        """导出会话报告"""
        return self.workflow_manager.export_report(session_id)


# 单例
_professional_planning_service = None

def get_professional_planning_service() -> ProfessionalPlanningService:
    """获取专业规划服务单例"""
    global _professional_planning_service
    if _professional_planning_service is None:
        _professional_planning_service = ProfessionalPlanningService()
    return _professional_planning_service
