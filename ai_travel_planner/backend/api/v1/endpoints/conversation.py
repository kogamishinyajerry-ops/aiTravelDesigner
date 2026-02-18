"""
对话API端点
"""

from fastapi import APIRouter, HTTPException, status
from loguru import logger
import time
import uuid
from typing import Optional

from services.conversation_engine import ConversationEngine, ConversationStage
from pydantic import BaseModel, Field


router = APIRouter(prefix="/conversation", tags=["对话"])


class MessageRequest(BaseModel):
    """消息请求"""
    message: str = Field(..., description="用户消息", min_length=1, max_length=1000)
    conversation_id: Optional[str] = Field(None, description="对话ID")


class MessageResponse(BaseModel):
    """消息响应"""
    success: bool = Field(..., description="是否成功")
    conversation_id: str = Field(..., description="对话ID")
    ai_response: str = Field(..., description="AI回复")
    current_stage: str = Field(..., description="当前对话阶段")
    collected_info: dict = Field(..., description="已收集的信息")
    is_complete: bool = Field(default=False, description="是否完成")


# 存储对话会话（生产环境应该使用Redis或数据库）
conversations: dict = {}


@router.post("/send", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    发送消息并获取AI回复

    这是一个职业旅行规划师式的对话系统，会通过多轮对话逐步了解用户需求，
    而不是一键生成。

    **工作流程**:
    1. 初始阶段 - 了解目的地
    2. 确认时间 - 季节、月份
    3. 确认时长 - 几天
    4. 确认预算 - 预算范围
    5. 确认同行人员 - 独自/情侣/家庭/朋友
    6. 确认旅行风格 - 文化/都市/自然/混合
    7. 收集偏好 - 特殊要求
    8. 信息收集 - 爬取实时数据
    9. 方案呈现 - 初步建议
    10. 用户反馈 - 获取兴趣点
    11. 深度挖掘 - 详细调研感兴趣的项目
    12. 最终方案 - 生成完整旅行计划
    """
    start_time = time.time()

    try:
        # 获取或创建对话会话
        conversation_id = request.conversation_id or str(uuid.uuid4())

        if conversation_id not in conversations:
            conversations[conversation_id] = ConversationEngine()
            logger.info(f"创建新对话: {conversation_id}")

        engine = conversations[conversation_id]

        # 处理用户消息
        result = await engine.process_user_message(request.message)

        generation_time = time.time() - start_time

        logger.info(f"对话 {conversation_id} | 阶段: {engine.current_stage} | 耗时: {generation_time:.2f}s")

        return MessageResponse(
            success=True,
            conversation_id=conversation_id,
            ai_response=result["ai_response"],
            current_stage=engine.current_stage.value,
            collected_info=result["collected_info"],
            is_complete=result.get("is_complete", False)
        )

    except Exception as e:
        logger.error(f"处理消息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理消息失败: {str(e)}"
        )


@router.get("/{conversation_id}/status")
async def get_conversation_status(conversation_id: str):
    """
    获取对话状态

    返回当前对话的完整状态，包括：
    - 当前阶段
    - 已收集的信息
    - 对话历史
    """
    if conversation_id not in conversations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    engine = conversations[conversation_id]
    return engine.get_conversation_summary()


@router.post("/{conversation_id}/reset")
async def reset_conversation(conversation_id: str):
    """
    重置对话

    清除当前对话的所有信息，重新开始。
    """
    if conversation_id not in conversations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )

    conversations[conversation_id].reset()

    logger.info(f"重置对话: {conversation_id}")

    return {
        "success": True,
        "message": "对话已重置",
        "conversation_id": conversation_id
    }


@router.get("/stages")
async def get_conversation_stages():
    """
    获取所有对话阶段

    返回对话流程的所有阶段，用于前端展示进度。
    """
    stages = [
        {
            "value": stage.value,
            "label": stage.value.replace("_", " ").title(),
            "description": {
                "init": "初始阶段",
                "destination": "确认目的地",
                "timing": "确认时间",
                "duration": "确认时长",
                "budget": "确认预算",
                "travelers": "确认同行人员",
                "style": "确认旅行风格",
                "preferences": "收集偏好",
                "info_collection": "信息收集中",
                "presentation": "方案呈现",
                "feedback": "用户反馈",
                "deep_dive": "深度挖掘",
                "final_plan": "最终方案"
            }.get(stage.value, stage.value)
        }
        for stage in ConversationStage
    ]

    return {"stages": stages}
