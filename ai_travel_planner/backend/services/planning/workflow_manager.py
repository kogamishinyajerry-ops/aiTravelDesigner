"""
工作流管理器 - 专业旅行规划工作流
管理整个行程规划流程的各个环节
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json
from loguru import logger

from .professional_standards import (
    TravelRequirements, ProfessionalItinerary,
    TravelStyle, ActivityIntensity, BudgetLevel,
    AccommodationType, PlanningWorkflow
)


class WorkflowStatus(Enum):
    """工作流状态"""
    INITIATED = "initiated"  # 已启动
    REQUIREMENTS_COLLECTED = "requirements_collected"  # 需求已收集
    DESTINATION_RESEARCHED = "destination_researched"  # 目的地已研究
    FRAMEWORK_DEIGNED = "framework_designed"  # 框架已设计
    DETAILS_PLANNED = "details_planned"  # 详情已规划
    BUDGET_CALCULATED = "budget_calculated"  # 预算已计算
    ARRANGEMENTS_MADE = "arrangements_made"  # 住宿交通已安排
    RISK_ASSESSED = "risk_assessed"  # 风险已评估
    OPTIMIZED = "optimized"  # 已优化
    CONFIRMED = "confirmed"  # 已确认
    DELIVERED = "delivered"  # 已交付


@dataclass
class WorkflowStep:
    """工作流步骤"""
    step_name: str
    description: str
    status: str = "pending"  # pending/in_progress/completed/skipped
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: str = ""
    artifacts: List[str] = field(default_factory=list)  # 产生的文件/数据
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_name": self.step_name,
            "description": self.description,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_minutes": (
                int((self.completed_at - self.started_at).total_seconds() / 60)
                if self.started_at and self.completed_at else 0
            ),
            "notes": self.notes,
            "artifacts": self.artifacts
        }


@dataclass
class PlanningWorkflowSession:
    """规划工作流会话"""
    session_id: str
    requirements: Optional[TravelRequirements] = None
    itinerary: Optional[ProfessionalItinerary] = None
    steps: List[WorkflowStep] = field(default_factory=list)
    current_step_index: int = 0
    status: WorkflowStatus = WorkflowStatus.INITIATED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "requirements": self.requirements.__dict__ if self.requirements else None,
            "itinerary_id": self.itinerary.itinerary_id if self.itinerary else None,
            "current_step": self.steps[self.current_step_index].step_name if self.steps else None,
            "status": self.status.value,
            "progress": self._calculate_progress(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "steps": [step.to_dict() for step in self.steps]
        }
    
    def _calculate_progress(self) -> float:
        """计算进度"""
        if not self.steps:
            return 0.0
        completed = sum(1 for step in self.steps if step.status == "completed")
        return round(completed / len(self.steps) * 100, 2)


class WorkflowManager:
    """工作流管理器"""
    
    def __init__(self):
        self.active_sessions: Dict[str, PlanningWorkflowSession] = {}
        logger.info("Workflow Manager initialized")
    
    def create_session(self, session_id: Optional[str] = None) -> PlanningWorkflowSession:
        """创建新工作流会话"""
        if session_id is None:
            session_id = f"WS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 初始化工作流步骤
        steps = []
        for step_name in PlanningWorkflow.STEPS:
            steps.append(WorkflowStep(
                step_name=step_name,
                description=PlanningWorkflow.get_step_description(step_name)
            ))
        
        session = PlanningWorkflowSession(
            session_id=session_id,
            steps=steps,
            current_step_index=0
        )
        
        self.active_sessions[session_id] = session
        logger.info(f"Created workflow session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[PlanningWorkflowSession]:
        """获取工作流会话"""
        return self.active_sessions.get(session_id)
    
    def start_step(self, session_id: str, step_name: str) -> bool:
        """开始工作流步骤"""
        session = self.get_session(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return False
        
        # 找到步骤
        step_index = None
        for i, step in enumerate(session.steps):
            if step.step_name == step_name:
                step_index = i
                break
        
        if step_index is None:
            logger.error(f"Step not found: {step_name}")
            return False
        
        # 更新步骤状态
        session.steps[step_index].status = "in_progress"
        session.steps[step_index].started_at = datetime.now()
        session.current_step_index = step_index
        session.updated_at = datetime.now()
        
        logger.info(f"Started step '{step_name}' for session {session_id}")
        return True
    
    def complete_step(
        self,
        session_id: str,
        step_name: str,
        notes: str = "",
        artifacts: List[str] = None
    ) -> bool:
        """完成工作流步骤"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # 找到步骤
        step = None
        for s in session.steps:
            if s.step_name == step_name:
                step = s
                break
        
        if not step:
            logger.error(f"Step not found: {step_name}")
            return False
        
        # 更新步骤状态
        step.status = "completed"
        step.completed_at = datetime.now()
        step.notes = notes
        if artifacts:
            step.artifacts.extend(artifacts)
        
        session.updated_at = datetime.now()
        
        # 更新整体状态
        self._update_session_status(session)
        
        logger.info(f"Completed step '{step_name}' for session {session_id}")
        return True
    
    def _update_session_status(self, session: PlanningWorkflowSession):
        """更新会话状态"""
        # 检查所有步骤是否都已完成
        all_completed = all(step.status == "completed" for step in session.steps)
        
        if all_completed:
            session.status = WorkflowStatus.DELIVERED
        else:
            # 根据当前步骤确定状态
            current_step_name = session.steps[session.current_step_index].step_name
            
            status_mapping = {
                "需求收集与分析": WorkflowStatus.REQUIREMENTS_COLLECTED,
                "目的地研究": WorkflowStatus.DESTINATION_RESEARCHED,
                "行程框架设计": WorkflowStatus.FRAMEWORK_DEIGNED,
                "详细行程制定": WorkflowStatus.DETAILS_PLANNED,
                "预算计算": WorkflowStatus.BUDGET_CALCULATED,
                "住宿与交通安排": WorkflowStatus.ARRANGEMENTS_MADE,
                "风险评估": WorkflowStatus.RISK_ASSESSED,
                "行程优化": WorkflowStatus.OPTIMIZED,
                "客户确认": WorkflowStatus.CONFIRMED,
            }
            
            session.status = status_mapping.get(
                current_step_name,
                WorkflowStatus.INITIATED
            )
    
    def set_requirements(
        self,
        session_id: str,
        requirements: TravelRequirements
    ) -> bool:
        """设置旅行需求"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.requirements = requirements
        logger.info(f"Set requirements for session {session_id}")
        return True
    
    def set_itinerary(
        self,
        session_id: str,
        itinerary: ProfessionalItinerary
    ) -> bool:
        """设置行程"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.itinerary = itinerary
        logger.info(f"Set itinerary for session {session_id}")
        return True
    
    def export_report(self, session_id: str) -> Optional[Dict[str, Any]]:
        """导出工作流报告"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # 计算统计信息
        completed_steps = [s for s in session.steps if s.status == "completed"]
        total_duration = sum(
            (s.completed_at - s.started_at).total_seconds()
            for s in completed_steps
            if s.started_at and s.completed_at
        )
        
        return {
            "session": session.to_dict(),
            "summary": {
                "total_steps": len(session.steps),
                "completed_steps": len(completed_steps),
                "progress_percent": session._calculate_progress(),
                "total_duration_minutes": int(total_duration / 60),
                "average_step_duration_minutes": (
                    int(total_duration / 60 / len(completed_steps))
                    if completed_steps else 0
                )
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def get_progress(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取进度"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "progress": session._calculate_progress(),
            "current_step": session.steps[session.current_step_index].to_dict() if session.steps else None,
            "status": session.status.value,
            "steps_status": [
                {
                    "step_name": step.step_name,
                    "status": step.status
                }
                for step in session.steps
            ]
        }


class RequirementCollector:
    """需求收集器 - 规范化需求收集流程"""
    
    REQUIRED_FIELDS = [
        "destination", "departure_city", "start_date", "end_date",
        "travelers_adults"
    ]
    
    OPTIONAL_FIELDS = [
        "travelers_children", "travelers_infants", "travelers_seniors",
        "travel_style", "activity_intensity", "budget_level", "budget_limit",
        "interests", "accommodation_type", "accommodation_preferences",
        "meal_plan", "flight_class", "transport_preference",
        "accessibility_needs", "dietary_restrictions", "special_occasions",
        "language_preference", "guide_required", "notes"
    ]
    
    @classmethod
    def collect_from_llm_response(
        cls,
        llm_response: Dict[str, Any]
    ) -> tuple[Optional[TravelRequirements], List[str]]:
        """
        从LLM响应中收集需求
        
        Returns:
            (TravelRequirements对象, 缺失字段列表)
        """
        extracted_info = llm_response.get("extracted_info", {})
        
        # 构建需求对象
        try:
            requirements = TravelRequirements(
                destination=extracted_info.get("destination", ""),
                departure_city=extracted_info.get("departure_city", "北京"),
                start_date=extracted_info.get("start_date", ""),
                end_date=extracted_info.get("end_date", ""),
                days=extracted_info.get("days", 0),
                travelers_adults=extracted_info.get("travelers", {}).get("adults", 1),
                travelers_children=extracted_info.get("travelers", {}).get("children", 0),
                travelers_infants=extracted_info.get("travelers", {}).get("infants", 0),
                travelers_seniors=extracted_info.get("travelers", {}).get("seniors", 0),
                interests=extracted_info.get("interests", []),
            )
            
            # 设置可选字段
            if "travel_style" in extracted_info:
                requirements.travel_style = TravelStyle(extracted_info["travel_style"])
            
            if "budget" in extracted_info:
                requirements.budget_limit = extracted_info["budget"]
            
            if "accommodation_preference" in extracted_info:
                requirements.accommodation_preferences.append(
                    extracted_info["accommodation_preference"]
                )
            
            # 验证完整性
            missing_info = []
            for field in cls.REQUIRED_FIELDS:
                value = getattr(requirements, field, None)
                if not value:
                    missing_info.append(field)
            
            if missing_info:
                return requirements, missing_info
            
            return requirements, []
            
        except Exception as e:
            logger.error(f"Failed to collect requirements: {e}")
            return None, list(cls.REQUIRED_FIELDS)
    
    @classmethod
    def generate_missing_questions(cls, missing_fields: List[str]) -> List[str]:
        """生成缺失信息的询问问题"""
        questions = []
        
        field_questions = {
            "destination": "请问您计划前往哪个目的地旅行？",
            "departure_city": "请问您从哪个城市出发？",
            "start_date": "请问您计划什么时候出发？(请提供具体日期)",
            "end_date": "请问您计划什么时候返回？(请提供具体日期)",
            "travelers_adults": "请问本次旅行有几位成人？",
            "travelers_children": "请问有几位儿童？(如无请忽略)",
            "days": "请问您计划旅行多少天？",
            "budget": "请问您的预算大概是多少？",
            "travel_style": "您偏好什么样的旅行风格？(休闲/探险/文化/美食等)",
            "interests": "您对哪些方面比较感兴趣？(自然/历史/美食/购物等)",
        }
        
        for field in missing_fields:
            if field in field_questions:
                questions.append(field_questions[field])
        
        return questions


# 单例
_workflow_manager = None

def get_workflow_manager() -> WorkflowManager:
    """获取工作流管理器单例"""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = WorkflowManager()
    return _workflow_manager
