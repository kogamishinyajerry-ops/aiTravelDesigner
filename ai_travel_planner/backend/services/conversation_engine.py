"""
对话流程引擎 - 职业规划师式对话管理
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from loguru import logger
from datetime import datetime


class ConversationStage(str, Enum):
    """对话阶段"""
    INIT = "init"  # 初始阶段
    DESTINATION = "destination"  # 确认目的地
    TIMING = "timing"  # 确认时间
    DURATION = "duration"  # 确认时长
    BUDGET = "budget"  # 确认预算
    TRAVELERS = "travelers"  # 确认同行人员
    STYLE = "style"  # 确认旅行风格
    PREFERENCES = "preferences"  # 偏好收集
    INFO_COLLECTION = "info_collection"  # 信息收集
    PRESENTATION = "presentation"  # 方案呈现
    FEEDBACK = "feedback"  # 用户反馈
    DEEP_DIVE = "deep_dive"  # 深度挖掘
    FINAL_PLAN = "final_plan"  # 最终方案


class TravelStyle(str, Enum):
    """旅行风格"""
    CULTURAL = "cultural"  # 文化深度游
    URBAN = "urban"  # 现代都市体验
    NATURE = "nature"  # 自然风光
    MIXED = "mixed"  # 混合型
    ADVENTURE = "adventure"  # 冒险探索
    RELAXATION = "relaxation"  # 休闲度假
    FOOD = "food"  # 美食之旅
    SHOPPING = "shopping"  # 购物之旅


class ConversationEngine:
    """对话流程引擎"""

    def __init__(self):
        self.current_stage = ConversationStage.INIT
        self.collected_info: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, str]] = []
        self.user_feedback: List[Dict[str, Any]] = []
        self.created_at = datetime.now()

    async def process_user_message(self, message: str) -> Dict[str, Any]:
        """
        处理用户消息

        Args:
            message: 用户消息

        Returns:
            包含AI回复和下一阶段信息的字典
        """
        logger.info(f"[对话引擎] 处理用户消息: {message[:50]}...")

        # 记录对话历史
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })

        # 根据当前阶段处理消息
        result = await self._process_by_stage(message)

        # 记录AI回复
        if result.get("ai_response"):
            self.conversation_history.append({
                "role": "assistant",
                "content": result["ai_response"],
                "timestamp": datetime.now().isoformat()
            })

        return result

    async def _process_by_stage(self, message: str) -> Dict[str, Any]:
        """根据当前阶段处理消息"""

        if self.current_stage == ConversationStage.INIT:
            return await self._handle_init_stage(message)

        elif self.current_stage == ConversationStage.DESTINATION:
            return await self._handle_destination_stage(message)

        elif self.current_stage == ConversationStage.TIMING:
            return await self._handle_timing_stage(message)

        elif self.current_stage == ConversationStage.DURATION:
            return await self._handle_duration_stage(message)

        elif self.current_stage == ConversationStage.BUDGET:
            return await self._handle_budget_stage(message)

        elif self.current_stage == ConversationStage.TRAVELERS:
            return await self._handle_travelers_stage(message)

        elif self.current_stage == ConversationStage.STYLE:
            return await self._handle_style_stage(message)

        elif self.current_stage == ConversationStage.PREFERENCES:
            return await self._handle_preferences_stage(message)

        elif self.current_stage == ConversationStage.INFO_COLLECTION:
            return await self._handle_info_collection_stage(message)

        elif self.current_stage == ConversationStage.PRESENTATION:
            return await self._handle_presentation_stage(message)

        elif self.current_stage == ConversationStage.FEEDBACK:
            return await self._handle_feedback_stage(message)

        elif self.current_stage == ConversationStage.DEEP_DIVE:
            return await self._handle_deep_dive_stage(message)

        elif self.current_stage == ConversationStage.FINAL_PLAN:
            return await self._handle_final_plan_stage(message)

        else:
            return {
                "ai_response": "抱歉，我遇到了一些问题。让我们重新开始吧。",
                "next_stage": ConversationStage.INIT,
                "collected_info": self.collected_info
            }

    async def _handle_init_stage(self, message: str) -> Dict[str, Any]:
        """处理初始阶段"""
        # 简单的关键词匹配来识别目的地
        if self._extract_destination(message):
            self.collected_info["destination"] = self._extract_destination(message)
            self.current_stage = ConversationStage.TIMING

            return {
                "ai_response": self._generate_timing_question(),
                "next_stage": ConversationStage.TIMING,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": "你好！我是你的AI旅行规划助手 🌍\n\n"
                             "我会像职业旅行规划师一样，通过对话了解你的需求，\n"
                             "然后为你收集信息、分析整理，提供最适合的旅行方案。\n\n"
                             "请告诉我，你想去哪里旅行？",
                "next_stage": ConversationStage.DESTINATION,
                "collected_info": self.collected_info
            }

    async def _handle_destination_stage(self, message: str) -> Dict[str, Any]:
        """处理目的地确认阶段"""
        destination = self._extract_destination(message)
        if destination:
            self.collected_info["destination"] = destination
            self.current_stage = ConversationStage.TIMING

            return {
                "ai_response": f"太好了！{destination}是个绝佳的选择 ✨\n\n" + self._generate_timing_question(),
                "next_stage": ConversationStage.TIMING,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": "能再告诉我具体想去哪个城市或国家吗？\n"
                             "比如：日本、泰国、巴黎、纽约等。",
                "next_stage": ConversationStage.DESTINATION,
                "collected_info": self.collected_info
            }

    async def _handle_timing_stage(self, message: str) -> Dict[str, Any]:
        """处理时间确认阶段"""
        timing_info = self._extract_timing(message)
        if timing_info:
            self.collected_info["timing"] = timing_info
            self.current_stage = ConversationStage.DURATION

            return {
                "ai_response": "好的！那我继续了解行程时长 ⏱️\n\n" + self._generate_duration_question(),
                "next_stage": ConversationStage.DURATION,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": self._generate_timing_question(),
                "next_stage": ConversationStage.TIMING,
                "collected_info": self.collected_info
            }

    async def _handle_duration_stage(self, message: str) -> Dict[str, Any]:
        """处理时长确认阶段"""
        duration = self._extract_duration(message)
        if duration:
            self.collected_info["duration"] = duration
            self.current_stage = ConversationStage.BUDGET

            return {
                "ai_response": "明白了！接下来是预算问题 💰\n\n" + self._generate_budget_question(),
                "next_stage": ConversationStage.BUDGET,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": "能告诉我大概旅行几天吗？\n比如：3天、1周、10天等。",
                "next_stage": ConversationStage.DURATION,
                "collected_info": self.collected_info
            }

    async def _handle_budget_stage(self, message: str) -> Dict[str, Any]:
        """处理预算确认阶段"""
        budget = self._extract_budget(message)
        if budget:
            self.collected_info["budget"] = budget
            self.current_stage = ConversationStage.TRAVELERS

            return {
                "ai_response": "好的！最后确认一下同行人员 👥\n\n" + self._generate_travelers_question(),
                "next_stage": ConversationStage.TRAVELERS,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": "能告诉我大概的预算范围吗？\n"
                             "比如：1万以内、2-3万、5万以上等。\n"
                             "如果没有特别限制，也可以说'预算灵活'。",
                "next_stage": ConversationStage.BUDGET,
                "collected_info": self.collected_info
            }

    async def _handle_travelers_stage(self, message: str) -> Dict[str, Any]:
        """处理同行人员确认阶段"""
        travelers = self._extract_travelers(message)
        if travelers:
            self.collected_info["travelers"] = travelers
            self.current_stage = ConversationStage.STYLE

            return {
                "ai_response": "很好！现在我想了解你的旅行风格 🎨\n\n" + self._generate_style_question(),
                "next_stage": ConversationStage.STYLE,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": "请问是独自旅行，还是有同伴呢？\n"
                             "比如：一个人、和伴侣、和家人、和朋友等。",
                "next_stage": ConversationStage.TRAVELERS,
                "collected_info": self.collected_info
            }

    async def _handle_style_stage(self, message: str) -> Dict[str, Any]:
        """处理旅行风格确认阶段"""
        style = self._extract_style(message)
        if style:
            self.collected_info["style"] = style
            self.current_stage = ConversationStage.PREFERENCES

            return {
                "ai_response": "太好了！还有其他特别的偏好吗？🤔\n\n" + self._generate_preferences_question(),
                "next_stage": ConversationStage.PREFERENCES,
                "collected_info": self.collected_info
            }
        else:
            return {
                "ai_response": self._generate_style_question(),
                "next_stage": ConversationStage.STYLE,
                "collected_info": self.collected_info
            }

    async def _handle_preferences_stage(self, message: str) -> Dict[str, Any]:
        """处理偏好收集阶段"""
        # 这里收集额外的偏好信息
        self.collected_info["preferences"] = message
        self.current_stage = ConversationStage.INFO_COLLECTION

        return {
            "ai_response": f"完美！我已经了解了你的旅行需求 📋\n\n"
                         f"让我总结一下：\n"
                         f"📍 目的地: {self.collected_info.get('destination')}\n"
                         f"📅 时间: {self.collected_info.get('timing')}\n"
                         f"⏱️ 时长: {self.collected_info.get('duration')}\n"
                         f"💰 预算: {self.collected_info.get('budget')}\n"
                         f"👥 同行: {self.collected_info.get('travelers')}\n"
                         f"🎨 风格: {self.collected_info.get('style')}\n\n"
                         f"现在我开始收集相关信息，请稍等... 🔍",
            "next_stage": ConversationStage.INFO_COLLECTION,
            "collected_info": self.collected_info
        }

    async def _handle_info_collection_stage(self, message: str) -> Dict[str, Any]:
        """处理信息收集阶段"""
        # 这里会调用爬虫引擎收集信息
        # 暂时返回一个占位响应
        self.current_stage = ConversationStage.PRESENTATION

        destination = self.collected_info.get("destination", "")

        return {
            "ai_response": f"信息收集完成！我为你找到了一些{destination}的精彩内容 ✨\n\n"
                         f"让我为你呈现初步方案，看看你对哪些部分最感兴趣：\n\n"
                         f"【推荐景点】\n"
                         f"1. {destination}地标景点A ⭐⭐⭐⭐⭐\n"
                         f"2. {destination}特色景点B ⭐⭐⭐⭐\n"
                         f"3. {destination}秘境景点C ⭐⭐⭐⭐\n\n"
                         f"【美食推荐】\n"
                         f"1. 当地特色餐厅A\n"
                         f"2. 必尝小吃B\n"
                         f"3. 网红咖啡厅C\n\n"
                         f"你对哪些景点最感兴趣？有什么特别想调整的吗？",
            "next_stage": ConversationStage.PRESENTATION,
            "collected_info": self.collected_info
        }

    async def _handle_presentation_stage(self, message: str) -> Dict[str, Any]:
        """处理方案呈现阶段"""
        # 分析用户反馈
        interests = self._extract_interests(message)
        self.user_feedback.append({
            "stage": "presentation",
            "message": message,
            "interests": interests,
            "timestamp": datetime.now().isoformat()
        })

        self.current_stage = ConversationStage.DEEP_DIVE

        return {
            "ai_response": f"太好了！我看到你对这些地方特别感兴趣 🎯\n\n"
                         f"让我对这些地方做更深入的调研和介绍：\n\n"
                         f"【深度信息】\n"
                         f"1. 景点A的详细攻略（最佳时间、必体验项目、周边美食）\n"
                         f"2. 景点A的交通方式、门票信息、穿着建议\n"
                         f"3. 周边推荐的住宿和餐厅\n\n"
                         f"这些信息对你有帮助吗？还需要我深入了解其他方面吗？",
            "next_stage": ConversationStage.DEEP_DIVE,
            "collected_info": self.collected_info
        }

    async def _handle_feedback_stage(self, message: str) -> Dict[str, Any]:
        """处理用户反馈阶段"""
        # 记录用户反馈
        self.user_feedback.append({
            "stage": "feedback",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

        # 根据反馈决定下一步
        if "确认" in message or "可以" in message or "好的" in message:
            self.current_stage = ConversationStage.FINAL_PLAN
            return {
                "ai_response": "好的！我现在为你生成最终的详细旅行方案 📝",
                "next_stage": ConversationStage.FINAL_PLAN,
                "collected_info": self.collected_info
            }
        else:
            # 继续收集更多信息
            return {
                "ai_response": "明白了！还有什么需要我了解或调整的吗？",
                "next_stage": ConversationStage.FEEDBACK,
                "collected_info": self.collected_info
            }

    async def _handle_deep_dive_stage(self, message: str) -> Dict[str, Any]:
        """处理深度挖掘阶段"""
        self.user_feedback.append({
            "stage": "deep_dive",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

        # 判断是否可以生成最终方案
        if "可以" in message or "确认" in message or "不需要了" in message:
            self.current_stage = ConversationStage.FINAL_PLAN
            return await self._handle_final_plan_stage(message)
        else:
            # 继续深度挖掘
            return {
                "ai_response": "好的，我继续深入了解... 📊",
                "next_stage": ConversationStage.DEEP_DIVE,
                "collected_info": self.collected_info
            }

    async def _handle_final_plan_stage(self, message: str) -> Dict[str, Any]:
        """处理最终方案生成阶段"""
        # 这里会生成最终的旅行方案
        self.current_stage = ConversationStage.FINAL_PLAN

        return {
            "ai_response": "🎉 你的专属旅行方案已生成！\n\n"
                         "【完整行程】\n"
                         "Day 1: 抵达与城市探索\n"
                         "Day 2: 深度文化体验\n"
                         "Day 3: 自然风光之旅\n"
                         "...\n\n"
                         "【预算明细】\n"
                         "【装备清单】\n"
                         "【实用贴士】\n\n"
                         "方案已保存，随时可以查看和调整！",
            "next_stage": ConversationStage.FINAL_PLAN,
            "collected_info": self.collected_info,
            "is_complete": True
        }

    # 辅助方法

    def _extract_destination(self, message: str) -> Optional[str]:
        """提取目的地"""
        destinations = ["日本", "泰国", "韩国", "新加坡", "法国", "意大利", "英国",
                      "美国", "日本东京", "日本京都", "日本大阪", "巴黎", "伦敦", "纽约"]
        for dest in destinations:
            if dest in message:
                return dest
        return None

    def _extract_timing(self, message: str) -> Optional[str]:
        """提取时间信息"""
        # 简化的时间提取
        if "春天" in message or "3月" in message or "4月" in message or "5月" in message:
            return "春季（3-5月）"
        elif "夏天" in message or "6月" in message or "7月" in message or "8月" in message:
            return "夏季（6-8月）"
        elif "秋天" in message or "9月" in message or "10月" in message or "11月" in message:
            return "秋季（9-11月）"
        elif "冬天" in message or "12月" in message or "1月" in message or "2月" in message:
            return "冬季（12-2月）"
        elif "春节" in message:
            return "春节期间"
        else:
            return None

    def _extract_duration(self, message: str) -> Optional[str]:
        """提取时长信息"""
        if "3天" in message or "三天" in message:
            return "3天"
        elif "5天" in message or "五天" in message:
            return "5天"
        elif "7天" in message or "一周" in message or "七天" in message:
            return "7天"
        elif "10天" in message or "十天" in message:
            return "10天"
        elif "半月" in message or "15天" in message:
            return "15天"
        elif "20天" in message or "二十天" in message:
            return "20天"
        elif "1月" in message or "一月" in message or "一个月" in message:
            return "30天"
        return None

    def _extract_budget(self, message: str) -> Optional[str]:
        """提取预算信息"""
        if "1万" in message or "一万" in message:
            return "1万以内"
        elif "2万" in message or "两万" in message or "三万" in message:
            return "2-3万"
        elif "5万" in message or "五万" in message:
            return "5万左右"
        elif "10万" in message or "十万" in message:
            return "10万以上"
        elif "预算灵活" in message or "不限" in message or "无所谓" in message:
            return "预算灵活"
        return None

    def _extract_travelers(self, message: str) -> Optional[str]:
        """提取同行人员信息"""
        if "一个人" in message or "独自" in message or "自己" in message:
            return "独自旅行"
        elif "女朋友" in message or "男朋友" in message or "情侣" in message or "伴侣" in message:
            return "情侣"
        elif "家人" in message or "父母" in message or "孩子" in message:
            return "家庭"
        elif "朋友" in message or "同事" in message:
            return "朋友"
        return None

    def _extract_style(self, message: str) -> Optional[str]:
        """提取旅行风格"""
        if "文化" in message or "历史" in message or "传统" in message:
            return "文化深度游"
        elif "都市" in message or "现代" in message or "购物" in message or "美食" in message:
            return "现代都市体验"
        elif "自然" in message or "风景" in message or "山水" in message:
            return "自然风光"
        elif "混合" in message or "都想去" in message or "综合" in message:
            return "混合型"
        return None

    def _extract_interests(self, message: str) -> List[str]:
        """提取用户感兴趣的内容"""
        interests = []
        keywords = ["景点", "美食", "住宿", "交通", "购物", "体验"]
        for keyword in keywords:
            if keyword in message:
                interests.append(keyword)
        return interests

    def _generate_timing_question(self) -> str:
        """生成时间相关问题"""
        return "请问计划什么时候去旅行？\n" \
               "1. 季节（春天/夏天/秋天/冬天）\n" \
               "2. 具体月份\n" \
               "3. 或者大概的时间段"

    def _generate_duration_question(self) -> str:
        """生成长度相关问题"""
        return "计划旅行多长时间？\n" \
               "比如：3天、1周、10天、15天等。"

    def _generate_budget_question(self) -> str:
        """生成预算相关问题"""
        return "预算大概是多少？\n" \
               "比如：1万以内、2-3万、5万左右，或者预算灵活。"

    def _generate_travelers_question(self) -> str:
        """生成同行人员相关问题"""
        return "和谁一起旅行呢？\n" \
               "比如：独自、情侣、家庭、朋友等。"

    def _generate_style_question(self) -> str:
        """生成旅行风格相关问题"""
        return "你更偏向哪种旅行风格？\n" \
               "A. 文化深度游（寺庙、历史、传统文化）\n" \
               "B. 现代都市体验（购物、美食、夜景）\n" \
               "C. 自然风光（山水、海滩、国家公园）\n" \
               "D. 混合型（以上都想要）"

    def _generate_preferences_question(self) -> str:
        """生成偏好相关问题"""
        return "还有什么特别的偏好吗？\n" \
               "比如：\n" \
               "- 有没有特别想去的城市或景点？\n" \
               "- 对住宿有什么要求？（酒店/民宿/青旅）\n" \
               "- 对美食有什么偏好？\n" \
               "- 需要购物吗？\n\n" \
               "如果没有特别要求，可以说'都可以'或'按你的推荐来'。"

    def get_conversation_summary(self) -> Dict[str, Any]:
        """获取对话摘要"""
        return {
            "stage": self.current_stage,
            "collected_info": self.collected_info,
            "conversation_history": self.conversation_history,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at,
            "updated_at": datetime.now().isoformat()
        }

    def reset(self):
        """重置对话"""
        self.current_stage = ConversationStage.INIT
        self.collected_info = {}
        self.conversation_history = []
        self.user_feedback = []
        self.created_at = datetime.now()
