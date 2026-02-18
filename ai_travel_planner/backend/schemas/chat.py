"""
聊天相关的Pydantic模型
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    """消息模型"""
    role: str = Field(..., description="角色：user/assistant/system")
    content: str = Field(..., description="消息内容")
    timestamp: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TravelPreferences(BaseModel):
    """旅行偏好"""
    travel_style: Optional[str] = None
    interests: List[str] = []
    accommodation_preference: Optional[str] = None
    transportation_preference: Optional[str] = None
    special_requirements: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "travel_style": "休闲",
                "interests": ["美食", "历史", "自然"],
                "accommodation_preference": "精品酒店",
                "transportation_preference": "公共交通",
                "special_requirements": ["无障碍设施", "素食餐厅"]
            }
        }


class TravelersInfo(BaseModel):
    """旅行者信息"""
    adults: int = Field(1, ge=1, description="成人数")
    children: int = Field(0, ge=0, description="儿童数")
    children_ages: Optional[List[int]] = None
    
    @validator('children_ages')
    def validate_children_ages(cls, v, values):
        if v and len(v) != values.get('children', 0):
            raise ValueError("children_ages长度必须等于children数量")
        return v


class ExtractedTravelInfo(BaseModel):
    """提取的旅行信息"""
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    days: Optional[int] = None
    budget: Optional[float] = None
    travelers: Optional[TravelersInfo] = None
    preferences: Optional[TravelPreferences] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "京都",
                "start_date": "2024-04-01",
                "end_date": "2024-04-07",
                "days": 7,
                "budget": 15000,
                "travelers": {
                    "adults": 2,
                    "children": 0
                },
                "preferences": {
                    "travel_style": "文化",
                    "interests": ["历史", "美食", "购物"]
                }
            }
        }


class ClarificationQuestion(BaseModel):
    """澄清问题"""
    id: str
    question: str
    type: str = Field(..., description="问题类型")
    options: List[str] = []
    allows_multiple: bool = False
    suggestions: List[str] = []


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., min_length=1, max_length=1000, description="用户消息")
    conversation_id: Optional[str] = None
    user_id: Optional[int] = None
    skip_clarification: bool = False  # 跳过澄清，直接使用已有信息
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "我想去日本旅游，大概7天，预算2万以内",
                "conversation_id": "uuid",
                "user_id": 1,
                "skip_clarification": False
            }
        }


class ChatResponse(BaseModel):
    """聊天响应"""
    success: bool
    message: str = Field(..., description="回复给用户的消息")
    extracted_info: Optional[ExtractedTravelInfo] = None
    missing_info: List[str] = []
    clarification_questions: List[ClarificationQuestion] = []
    is_complete: bool = False
    confidence: float = 0.0
    conversation_id: Optional[str] = None
    needs_planning: bool = False  # 是否可以开始规划行程
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "好的！我了解了您想去日本旅游。请问您计划什么时候出发呢？",
                "extracted_info": {
                    "destination": "日本",
                    "days": 7,
                    "budget": 20000
                },
                "missing_info": ["start_date", "travel_style"],
                "clarification_questions": [
                    {
                        "id": "q1",
                        "question": "您计划什么时候出发？",
                        "type": "date",
                        "options": ["下个月", "今年夏天", "今年秋天", "还没确定"],
                        "allows_multiple": False
                    }
                ],
                "is_complete": False,
                "confidence": 0.6,
                "needs_planning": False
            }
        }


class ConversationSummary(BaseModel):
    """对话摘要"""
    conversation_id: str
    user_id: Optional[int]
    messages: List[Message]
    extracted_info: Optional[ExtractedTravelInfo]
    is_complete: bool
    created_at: datetime
    updated_at: datetime


class ConversationRequest(BaseModel):
    """创建对话请求"""
    user_id: Optional[int] = None


class ConversationResponse(BaseModel):
    """对话响应"""
    success: bool
    conversation_id: str
    message: str
