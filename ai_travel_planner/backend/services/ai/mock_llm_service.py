"""
Mock LLM Service - 用于测试和演示
当没有真实的API Key时使用，返回模拟的智能回复
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import random


class MockLLMService:
    """模拟LLM服务"""
    
    def __init__(self):
        self.model = "mock-gpt-4o"
        self.supported_destinations = [
            "日本", "东京", "京都", "大阪", "泰国", "曼谷", 
            "法国", "巴黎", "意大利", "意大利", "英国", "伦敦"
        ]
        
        self.conversation_states = {}  # 存储对话状态
    
    async def understand_travel_need(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """理解用户旅行需求（模拟）"""
        
        # 解析用户输入
        extracted_info = self._parse_user_input(user_message)
        
        # 检查缺失信息
        missing_info = self._check_missing_info(extracted_info)
        
        # 判断完整度
        is_complete = len(missing_info) == 0
        confidence = min(0.9, 0.5 + (8 - len(missing_info)) * 0.05)
        
        # 生成摘要
        summary = self._generate_summary(extracted_info)
        
        return {
            "extracted_info": extracted_info,
            "missing_info": missing_info,
            "summary": summary,
            "is_complete": is_complete,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
    
    async def generate_clarification_questions(
        self,
        extracted_info: Dict[str, Any],
        missing_info: List[str]
    ) -> Dict[str, Any]:
        """生成澄清问题（模拟）"""
        
        questions = []
        
        # 根据缺失信息生成问题
        if "start_date" in missing_info:
            questions.append({
                "id": "q_start_date",
                "question": "请问您计划什么时候出发呢？",
                "type": "date",
                "options": ["下个月", "今年夏天", "今年秋天", "今年冬天", "还没确定"],
                "allows_multiple": False,
                "suggestions": ["避开节假日可以节省费用"]
            })
        
        if "days" in missing_info:
            questions.append({
                "id": "q_days",
                "question": "您计划玩几天呢？",
                "type": "number",
                "options": ["3-5天", "一周左右", "两周左右", "一个月"],
                "allows_multiple": False,
                "suggestions": []
            })
        
        if "travelers" in missing_info:
            questions.append({
                "id": "q_travelers",
                "question": "这次有几个人一起旅行？",
                "type": "number",
                "options": ["1人（独自旅行）", "2人（情侣/朋友）", "3-4人（小团队）", "5人以上（团体）"],
                "allows_multiple": False,
                "suggestions": []
            })
        
        if "budget" in missing_info:
            questions.append({
                "id": "q_budget",
                "question": "您的预算大概是多少？",
                "type": "budget",
                "options": ["5000元以内", "5000-10000元", "10000-20000元", "20000元以上"],
                "allows_multiple": False,
                "suggestions": ["预算包含机票、住宿、餐饮、门票等"]
            })
        
        if "travel_style" in missing_info:
            questions.append({
                "id": "q_style",
                "question": "您更喜欢什么样的旅行体验？",
                "type": "style",
                "options": ["休闲度假", "文化探索", "美食之旅", "自然风光", "购物血拼"],
                "allows_multiple": True,
                "suggestions": []
            })
        
        # 限制问题数量，一次最多2个
        questions = questions[:2]
        
        return {
            "questions": questions,
            "current_focus": "了解旅行时间安排" if "start_date" in missing_info else "了解其他需求",
            "estimated_completeness": min(1.0, 1.0 - len(missing_info) * 0.15),
            "timestamp": datetime.now().isoformat()
        }
    
    async def generate_response(
        self,
        user_message: str,
        context: Dict[str, Any],
        response_type: str = "clarification"
    ) -> str:
        """生成自然语言回复（模拟）"""
        
        extracted_info = context.get("extracted_info", {})
        missing_info = context.get("missing_info", [])
        questions = context.get("questions", [])
        
        if response_type == "confirmation":
            return self._generate_confirmation_response(extracted_info)
        elif response_type == "suggestion":
            return self._generate_suggestion_response(extracted_info)
        else:  # clarification
            return self._generate_clarification_response(user_message, questions, extracted_info)
    
    def _parse_user_input(self, message: str) -> Dict[str, Any]:
        """解析用户输入（简单的关键词匹配）"""
        result = {
            "destination": None,
            "start_date": None,
            "end_date": None,
            "days": None,
            "budget": None,
            "travelers": {"adults": 1, "children": 0},
            "travel_style": None,
            "interests": [],
            "accommodation_preference": None,
            "transportation_preference": None,
            "special_requirements": []
        }
        
        message_lower = message.lower()
        
        # 解析目的地
        for dest in self.supported_destinations:
            if dest in message:
                result["destination"] = dest
                if dest in ["日本", "东京", "京都", "大阪"]:
                    result["destination"] = "日本"
                elif dest in ["泰国", "曼谷"]:
                    result["destination"] = "泰国"
                elif dest in ["法国", "巴黎"]:
                    result["destination"] = "法国"
                break
        
        # 解析天数
        day_patterns = [
            r'(\d+)\s*天',
            r'(\d+)\s*日',
            r'(\d+)\s*days'
        ]
        import re
        for pattern in day_patterns:
            match = re.search(pattern, message)
            if match:
                result["days"] = int(match.group(1))
                break
        
        # 解析预算
        budget_patterns = [
            r'(\d+)\s*元',
            r'(\d+)\s*万',
            r'预算.*?(\d+)'
        ]
        for pattern in budget_patterns:
            match = re.search(pattern, message)
            if match:
                amount = int(match.group(1))
                if "万" in message:
                    amount *= 10000
                result["budget"] = amount
                break
        
        # 解析人数
        people_patterns = [
            r'(\d+)\s*人',
            r'(\d+)\s*个人',
            r'情侣|夫妻'  # 2人
        ]
        for pattern in people_patterns:
            match = re.search(pattern, message)
            if match:
                if "情侣" in message or "夫妻" in message:
                    result["travelers"] = {"adults": 2, "children": 0}
                else:
                    result["travelers"] = {"adults": int(match.group(1)), "children": 0}
                break
        
        # 解析旅行风格
        style_keywords = {
            "休闲度假": "休闲",
            "文化探索": ["历史", "文化", "博物馆", "古迹"],
            "美食之旅": ["美食", "吃", "品尝"],
            "自然风光": ["自然", "风景", "山水", "海滩"],
            "购物": ["购物", "买", "逛"]
        }
        
        for style, keywords in style_keywords.items():
            if isinstance(keywords, list):
                if any(kw in message for kw in keywords):
                    result["travel_style"] = style
                    result["interests"].append(keywords[0])
            else:
                if keywords in message:
                    result["travel_style"] = style
        
        return result
    
    def _check_missing_info(self, info: Dict[str, Any]) -> List[str]:
        """检查缺失信息"""
        missing = []
        
        if not info.get("destination"):
            missing.append("destination")
        if not info.get("start_date") and not info.get("days"):
            missing.append("time_info")
        if not info.get("travelers"):
            missing.append("travelers")
        if not info.get("budget"):
            missing.append("budget")
        if not info.get("travel_style"):
            missing.append("travel_style")
        
        return missing
    
    def _generate_summary(self, info: Dict[str, Any]) -> str:
        """生成需求摘要"""
        parts = []
        
        if info.get("destination"):
            parts.append(f"目的地：{info['destination']}")
        
        if info.get("days"):
            parts.append(f"天数：{info['days']}天")
        
        if info.get("budget"):
            budget = info['budget']
            if budget >= 10000:
                parts.append(f"预算：{budget/10000:.1f}万")
            else:
                parts.append(f"预算：{budget}元")
        
        if info.get("travelers"):
            travelers = info['travelers']
            total = travelers.get("adults", 0) + travelers.get("children", 0)
            parts.append(f"人数：{total}人")
        
        if info.get("travel_style"):
            parts.append(f"风格：{info['travel_style']}")
        
        if parts:
            return "、".join(parts)
        return ""
    
    def _generate_confirmation_response(self, info: Dict[str, Any]) -> str:
        """生成确认回复"""
        summary = self._generate_summary(info)
        
        if summary:
            response = f"好的，我已经记录了您的需求：\n\n{summary}\n\n"
            
            missing = self._check_missing_info(info)
            if missing:
                response += "还需要了解一些其他信息。"
            else:
                response += "信息已经很完整了！需要我为您生成详细的行程方案吗？"
            
            return response
        
        return "请告诉我您想去哪里旅行呢？"
    
    def _generate_clarification_response(
        self,
        user_message: str,
        questions: List[Dict],
        info: Dict[str, Any]
    ) -> str:
        """生成澄清回复"""
        
        # 友好的开场
        greetings = [
            "好的！",
            "收到！",
            "明白了！",
            "了解了！"
        ]
        greeting = random.choice(greetings)
        
        # 确认已获取的信息
        summary = self._generate_summary(info)
        response = greeting
        
        if summary:
            response += f" 我了解到：{summary}\n\n"
        
        # 提出问题
        if questions:
            response += "为了给您更好的建议，我想了解一下："
            for i, q in enumerate(questions, 1):
                response += f"\n{i}. {q['question']}"
        
        return response
    
    def _generate_suggestion_response(self, info: Dict[str, Any]) -> str:
        """生成建议回复"""
        destination = info.get("destination", "目的地")
        
        suggestions = {
            "日本": "日本四季分明，春季赏樱、秋季赏枫都很美！建议准备一张西瓜卡方便出行。",
            "泰国": "泰国热带气候，全年都可以去！记得带防晒霜和轻便的夏装。",
            "法国": "法国浪漫之都，建议提前预订热门景点门票，可以节省排队时间！"
        }
        
        return suggestions.get(destination, f"{destination}是个不错的选择！")
    
    async def summarize_itinerary(self, itinerary_data: Dict[str, Any]) -> str:
        """生成行程摘要（模拟）"""
        destination = itinerary_data.get("destination", "")
        days = itinerary_data.get("days", 0)
        
        return f"""🌟 {destination}{days}日深度游 🌟

这是一次精彩的{destination}之旅！

✨ 行程亮点：
- 深度体验当地文化
- 精选热门景点
- 品尝地道美食
- 舒适住宿安排

💰 人均预算：{itinerary_data.get('budget', {}).get('per_person', '待定')}元
📅 出发日期：{itinerary_data.get('start_date', '待定')}
👥 出行人数：{itinerary_data.get('travelers', 1)}人

祝您旅途愉快！✈️
"""
    
    async def optimize_itinerary(
        self,
        current_itinerary: Dict[str, Any],
        feedback: str
    ) -> Dict[str, Any]:
        """优化行程（模拟）"""
        return {
            "optimized_itinerary": current_itinerary,
            "changes_made": ["优化了路线安排", "调整了游览顺序"],
            "alternatives": [],
            "reasoning": "根据您的反馈进行了调整",
            "timestamp": datetime.now().isoformat()
        }


# 单例
_mock_llm_service = None

def get_mock_llm_service() -> MockLLMService:
    """获取Mock LLM服务单例"""
    global _mock_llm_service
    if _mock_llm_service is None:
        _mock_llm_service = MockLLMService()
    return _mock_llm_service
