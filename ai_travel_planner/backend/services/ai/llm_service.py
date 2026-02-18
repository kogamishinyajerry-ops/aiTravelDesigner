"""
LLM服务 - AI需求理解核心模块
负责理解用户的旅行需求，提取关键信息，生成澄清问题
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from openai import AsyncOpenAI
from core.config import settings


class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        self.model = settings.OPENAI_MODEL
    
    async def understand_travel_need(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        理解用户的旅行需求，提取关键信息
        
        Args:
            user_message: 用户的输入消息
            conversation_history: 对话历史
            
        Returns:
            包含提取信息和缺失信息的字典
        """
        system_prompt = """你是一位专业的旅行规划助手，负责理解用户的旅行需求。

你的任务是：
1. 分析用户的旅行需求，提取以下关键信息：
   - destination（目的地）
   - start_date（出发日期）
   - end_date（返回日期）
   - days（天数）
   - budget（预算）
   - travelers（人数，成人/儿童）
   - travel_style（旅行风格：休闲/探险/文化/美食等）
   - interests（兴趣点：自然/历史/美食/购物等）
   - accommodation_preference（住宿偏好）
   - transportation_preference（交通偏好）
   - special_requirements（特殊要求）

2. 识别缺失的关键信息

3. 如果信息足够，生成旅行需求摘要

返回格式必须是JSON：
{
  "extracted_info": {
    "destination": "提取的目的地",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "days": 数字,
    "budget": 数字,
    "travelers": {"adults": 数字, "children": 数字},
    "travel_style": "风格",
    "interests": ["兴趣1", "兴趣2"],
    "accommodation_preference": "偏好",
    "transportation_preference": "偏好",
    "special_requirements": ["要求1", "要求2"]
  },
  "missing_info": ["缺失的信息列表"],
  "summary": "需求摘要",
  "is_complete": true/false,
  "confidence": 0.0-1.0
}
"""
        
        # 构建对话上下文
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history[-6:])  # 只保留最近6轮对话
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 添加时间戳
            result["timestamp"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "extracted_info": {},
                "missing_info": [],
                "summary": "",
                "is_complete": False,
                "confidence": 0.0
            }
    
    async def generate_clarification_questions(
        self,
        extracted_info: Dict[str, Any],
        missing_info: List[str]
    ) -> Dict[str, Any]:
        """
        根据缺失信息生成澄清问题
        
        Args:
            extracted_info: 已提取的信息
            missing_info: 缺失的信息列表
            
        Returns:
            包含澄清问题的字典
        """
        system_prompt = """你是一位专业的旅行规划助手，负责向用户询问关键信息以完善旅行计划。

你的任务是：
1. 根据已提取的信息和缺失信息，生成2-3个最关键的澄清问题
2. 问题要简洁、友好、自然
3. 一次只问最重要的问题，避免一次性问太多
4. 根据已有信息，给出一些合理的选项

返回格式必须是JSON：
{
  "questions": [
    {
      "id": "question_1",
      "question": "问题内容",
      "type": "destination/date/budget/style/travelers",
      "options": ["选项1", "选项2", "选项3"],
      "allows_multiple": false,
      "suggestions": ["建议1", "建议2"]
    }
  ],
  "current_focus": "当前重点关注的方面",
  "estimated_completeness": 0.0-1.0
}
"""
        
        user_prompt = f"""已提取的信息：
{json.dumps(extracted_info, ensure_ascii=False, indent=2)}

缺失的信息：
{json.dumps(missing_info, ensure_ascii=False, indent=2)}

请生成合适的澄清问题。"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["timestamp"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "questions": [],
                "current_focus": "",
                "estimated_completeness": 0.0
            }
    
    async def generate_response(
        self,
        user_message: str,
        context: Dict[str, Any],
        response_type: str = "clarification"
    ) -> str:
        """
        生成自然语言回复
        
        Args:
            user_message: 用户消息
            context: 上下文信息
            response_type: 回复类型（clarification/confirmation/suggestion）
            
        Returns:
            生成的回复文本
        """
        system_prompt = """你是一位友好的旅行规划助手。

你的回复风格：
- 友好、专业、简洁
- 避免过于机械的表达
- 根据回复类型调整语气：
  * clarification: 询问式，耐心引导
  * confirmation: 确认式，总结关键信息
  * suggestion: 建议式，提供有价值的信息
- 可以适当使用emoji增加亲和力
"""
        
        user_prompt = f"""用户消息：{user_message}

上下文信息：
{json.dumps(context, ensure_ascii=False, indent=2)}

回复类型：{response_type}

请生成合适的回复。"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "抱歉，我遇到了一些问题，请稍后再试。"
    
    async def summarize_itinerary(
        self,
        itinerary_data: Dict[str, Any]
    ) -> str:
        """
        生成行程摘要
        
        Args:
            itinerary_data: 行程数据
            
        Returns:
            行程摘要文本
        """
        system_prompt = """你是一位专业的旅行规划助手，负责为用户生成行程摘要。

摘要应该包括：
1. 目的地和日期
2. 核心体验和亮点
3. 预算概况
4. 贴心提示

风格：简洁、吸引人、信息丰富
"""
        
        user_prompt = f"""行程数据：
{json.dumps(itinerary_data, ensure_ascii=False, indent=2)}

请生成一个吸引人的行程摘要。"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.6,
                max_tokens=600
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "行程摘要生成失败。"
    
    async def optimize_itinerary(
        self,
        current_itinerary: Dict[str, Any],
        feedback: str
    ) -> Dict[str, Any]:
        """
        根据用户反馈优化行程
        
        Args:
            current_itinerary: 当前行程
            feedback: 用户反馈
            
        Returns:
            优化后的行程建议
        """
        system_prompt = """你是一位专业的旅行规划助手，负责根据用户反馈优化行程。

优化原则：
1. 理解用户的核心需求变化
2. 在不破坏整体平衡的前提下进行调整
3. 提供多个优化方案供选择
4. 说明调整的理由

返回格式必须是JSON：
{
  "optimized_itinerary": {...},
  "changes_made": ["修改1", "修改2"],
  "alternatives": [方案1, 方案2],
  "reasoning": "调整理由"
}
"""
        
        user_prompt = f"""当前行程：
{json.dumps(current_itinerary, ensure_ascii=False, indent=2)}

用户反馈：
{feedback}

请提供优化建议。"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["timestamp"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "optimized_itinerary": current_itinerary,
                "changes_made": [],
                "alternatives": [],
                "reasoning": "优化失败"
            }


# 单例模式
_llm_service = None

def get_llm_service() -> LLMService:
    """获取LLM服务单例"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
