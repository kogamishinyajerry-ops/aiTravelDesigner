"""
Chat Endpoint
AI对话端点 - 集成LLM服务
"""
from fastapi import APIRouter, HTTPException, status
from loguru import logger
from typing import Optional
import uuid
from datetime import datetime

from schemas.chat import (
    ChatRequest, ChatResponse, ConversationRequest, ConversationResponse
)
from services.ai.factory import get_llm_service

router = APIRouter()

# 简单的会话存储（生产环境应使用Redis或数据库）
_conversations = {}


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    AI对话接口 - 理解旅行需求，生成回复

    Args:
        request: 对话请求

    Returns:
        AI响应消息，包含提取的信息和澄清问题
    """
    try:
        logger.info(f"Chat request: {request.message[:100]}...")
        
        # 获取或创建对话ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # 获取对话历史
        conversation_history = _conversations.get(conversation_id, {}).get("history", [])
        
        # 调用LLM服务
        llm_service = get_llm_service()
        
        # 1. 理解用户需求
        llm_result = await llm_service.understand_travel_need(
            user_message=request.message,
            conversation_history=[{"role": msg["role"], "content": msg["content"]} 
                                  for msg in conversation_history[-6:]]
        )
        
        if "error" in llm_result:
            logger.error(f"LLM error: {llm_result['error']}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI服务暂时不可用"
            )
        
        extracted_info = llm_result.get("extracted_info", {})
        missing_info = llm_result.get("missing_info", [])
        is_complete = llm_result.get("is_complete", False)
        confidence = llm_result.get("confidence", 0.0)
        
        # 2. 判断是否需要澄清问题
        clarification_questions = []
        response_message = ""
        needs_planning = False
        
        if is_complete:
            # 信息完整，可以开始规划
            summary = llm_result.get("summary", "")
            response_message = f"太好了！我已经了解了您的需求：\n\n{summary}\n\n是否需要我为您生成详细的行程方案？"
            needs_planning = True
        elif missing_info and not request.skip_clarification:
            # 信息不完整，生成澄清问题
            questions_result = await llm_service.generate_clarification_questions(
                extracted_info=extracted_info,
                missing_info=missing_info
            )
            
            if "error" not in questions_result:
                clarification_questions = questions_result.get("questions", [])
                
                # 生成友好的回复
                context = {
                    "extracted_info": extracted_info,
                    "missing_info": missing_info,
                    "questions": clarification_questions
                }
                response_message = await llm_service.generate_response(
                    user_message=request.message,
                    context=context,
                    response_type="clarification"
                )
            else:
                response_message = "我正在了解您的需求..."
        else:
            # 确认已提取的信息
            context = {
                "extracted_info": extracted_info,
                "is_complete": is_complete
            }
            response_message = await llm_service.generate_response(
                user_message=request.message,
                context=context,
                response_type="confirmation"
            )
        
        # 更新对话历史
        if conversation_id not in _conversations:
            _conversations[conversation_id] = {
                "history": [],
                "extracted_info": {},
                "created_at": datetime.now()
            }
        
        _conversations[conversation_id]["history"].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        _conversations[conversation_id]["history"].append({
            "role": "assistant",
            "content": response_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新提取的信息
        _conversations[conversation_id]["extracted_info"] = extracted_info
        
        logger.info(f"Chat response: complete={is_complete}, confidence={confidence}")
        
        # 构造响应
        return ChatResponse(
            success=True,
            message=response_message,
            extracted_info=extracted_info,
            missing_info=missing_info,
            clarification_questions=clarification_questions,
            is_complete=is_complete,
            confidence=confidence,
            conversation_id=conversation_id,
            needs_planning=needs_planning
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    """
    创建新的对话会话

    Args:
        request: 对话请求

    Returns:
        对话ID
    """
    try:
        conversation_id = str(uuid.uuid4())
        
        _conversations[conversation_id] = {
            "history": [],
            "extracted_info": {},
            "user_id": request.user_id,
            "created_at": datetime.now()
        }
        
        logger.info(f"Created conversation {conversation_id} for user {request.user_id}")
        
        return ConversationResponse(
            success=True,
            conversation_id=conversation_id,
            message="对话已创建，请告诉我你想去哪里旅行？"
        )
        
    except Exception as e:
        logger.error(f"Create conversation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create conversation: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    获取对话详情

    Args:
        conversation_id: 对话ID

    Returns:
        对话详情
    """
    try:
        if conversation_id not in _conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        conversation = _conversations[conversation_id]
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "history": conversation["history"],
            "extracted_info": conversation["extracted_info"],
            "created_at": conversation["created_at"].isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get conversation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    删除对话

    Args:
        conversation_id: 对话ID

    Returns:
        删除结果
    """
    try:
        if conversation_id not in _conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        del _conversations[conversation_id]
        
        logger.info(f"Deleted conversation {conversation_id}")
        
        return {"success": True, "message": "对话已删除"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete conversation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )
