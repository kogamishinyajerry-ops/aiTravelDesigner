"""
惯犯识别引擎
Habitual Offender Detector
识别和分析惯犯行为特征
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class SimilarPost:
    """相似帖子"""
    post_id: str
    platform: str
    content: str
    timestamp: str
    similarity_score: float  # 相似度 (0-1)
    matched_keywords: List[str]


@dataclass
class HabitualOffenderResult:
    """惯犯分析结果"""
    timestamp: datetime
    is_habitual_offender: bool  # 是否惯犯
    offender_probability: float  # 惯犯概率 (0-1)
    offender_level: str  # 惯犯等级: 高/中/低/无
    similar_posts: List[SimilarPost]  # 相似帖子
    behavior_patterns: Dict[str, Any]  # 行为模式
    modus_operandi: List[str] = field(default_factory=list)  # 作案手法
    historical_evidence: List[str] = field(default_factory=list)  # 历史证据
    reasoning: str = ""  # 推理说明
    confidence: float = 0.0  # 置信度


class HabitualOffenderDetector:
    """惯犯识别引擎"""
    
    def __init__(self):
        # 职业碰瓷常见关键词
        self.professional_keywords = [
            "维权", "投诉", "举报", "诈骗", "虚假", "欺诈",
            "套路", "陷阱", "诱导", "设局"
        ]
        
        # 惯犯模式特征
        self.habitual_patterns = [
            r"多次.*投诉",
            r"多次.*举报",
            r"多次.*维权",
            r"经常.*",
            r"每次.*",
            r"总是.*"
        ]
        
        # 典型作案手法
        self.typical_methods = [
            "购买后立即要求退款",
            "现场报警拍照取证",
            "社交媒体发布抹黑",
            "诱导商家违规",
            "制造纠纷索要赔偿"
        ]
    
    def analyze(self, text: str, social_media_data: Dict[str, Any] = None) -> HabitualOffenderResult:
        """
        分析是否为惯犯
        
        Args:
            text: 案件描述文本
            social_media_data: 社交媒体数据 (模拟)
        
        Returns:
            惯犯分析结果
        """
        if social_media_data is None:
            social_media_data = self._mock_social_media_data(text)
        
        result = HabitualOffenderResult(
            timestamp=datetime.now(),
            is_habitual_offender=False,
            offender_probability=0.0,
            offender_level="无",
            similar_posts=[],
            behavior_patterns={},
            historical_evidence=[],
            reasoning="",
            confidence=0.0
        )
        
        # 1. 分析行为模式
        result.behavior_patterns = self._analyze_behavior_patterns(text)
        
        # 2. 识别作案手法
        result.modus_operandi = self._identify_methods(text)
        
        # 3. 查找相似帖子
        result.similar_posts = self._find_similar_posts(text, social_media_data)
        
        # 4. 收集历史证据
        result.historical_evidence = self._collect_historical_evidence(
            text, 
            result.similar_posts
        )
        
        # 5. 计算惯犯概率
        probability = self._calculate_offender_probability(
            result.behavior_patterns,
            result.modus_operandi,
            result.similar_posts,
            result.historical_evidence
        )
        result.offender_probability = probability
        
        # 6. 判断惯犯等级
        if probability >= 0.8:
            result.offender_level = "高"
        elif probability >= 0.5:
            result.offender_level = "中"
        elif probability >= 0.3:
            result.offender_level = "低"
        else:
            result.offender_level = "无"
        
        # 7. 判断是否惯犯
        result.is_habitual_offender = probability >= 0.5
        
        # 8. 生成推理说明
        result.reasoning = self._generate_reasoning(result)
        
        # 9. 计算置信度
        result.confidence = self._calculate_confidence(result)
        
        return result
    
    def _mock_social_media_data(self, text: str) -> Dict[str, Any]:
        """模拟社交媒体数据 (实际应用中应从外部API获取)"""
        # 这里模拟检测到的相似帖子
        similar_posts = []
        
        # 提取文本中的关键信息
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        
        # 模拟相似帖子
        if "小红书" in text or "发布" in text:
            similar_posts.append({
                "platform": "小红书",
                "content": "某店铺诈骗,买了东西后立即要求退款",
                "timestamp": "2024-11-10",
                "similarity": 0.75,
                "matched_keywords": ["诈骗", "退款"]
            })
            similar_posts.append({
                "platform": "小红书",
                "content": "消费陷阱,商家诱导消费后不给退款",
                "timestamp": "2024-10-05",
                "similarity": 0.65,
                "matched_keywords": ["消费", "退款"]
            })
        
        return {"similar_posts": similar_posts}
    
    def _analyze_behavior_patterns(self, text: str) -> Dict[str, Any]:
        """分析行为模式"""
        patterns = {
            "repetitive_actions": [],
            "consistent_behavior": [],
            "emotional_patterns": []
        }
        
        # 检查重复行为模式
        for pattern in self.habitual_patterns:
            matches = re.findall(pattern, text)
            if matches:
                patterns["repetitive_actions"].extend(matches)
        
        # 检查一致性行为
        if "报警" in text and "拍照" in text:
            patterns["consistent_behavior"].append("报警+取证模式")
        
        if "投诉" in text or "举报" in text:
            patterns["consistent_behavior"].append("投诉/举报行为")
        
        # 检查情绪模式
        if "冷静" in text:
            patterns["emotional_patterns"].append("情绪稳定")
        
        return patterns
    
    def _identify_methods(self, text: str) -> List[str]:
        """识别作案手法"""
        methods = []
        
        for method in self.typical_methods:
            # 简化匹配: 检查关键词
            if "购买" in method and "退款" in method:
                if "购买" in text and "退款" in text:
                    methods.append(method)
            elif "报警" in method and "拍照" in method:
                if "报警" in text or "拍照" in text:
                    methods.append(method)
            elif "社交媒体" in method or "发布" in method:
                if "发布" in text or "小红书" in text or "微博" in text:
                    methods.append(method)
        
        return methods
    
    def _find_similar_posts(self, text: str, 
                           social_media_data: Dict[str, Any]) -> List[SimilarPost]:
        """查找相似帖子"""
        similar_posts = []
        
        for i, post in enumerate(social_media_data.get("similar_posts", [])):
            similar_post = SimilarPost(
                post_id=f"post_{i}",
                platform=post.get("platform", "未知"),
                content=post.get("content", ""),
                timestamp=post.get("timestamp", ""),
                similarity_score=post.get("similarity", 0.0),
                matched_keywords=post.get("matched_keywords", [])
            )
            similar_posts.append(similar_post)
        
        # 按相似度排序
        similar_posts.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return similar_posts
    
    def _collect_historical_evidence(self, text: str,
                                    similar_posts: List[SimilarPost]) -> List[str]:
        """收集历史证据"""
        evidence = []
        
        # 基于相似帖子生成历史证据
        for post in similar_posts:
            if post.similarity_score >= 0.6:
                evidence.append(
                    f"发现相似历史帖子 ({post.platform}): "
                    f"'{post.content}' (相似度: {post.similarity_score:.2f})"
                )
        
        # 基于行为模式生成证据
        if "多次" in text or "经常" in text:
            evidence.append("文本中提到多次类似行为,显示惯犯特征")
        
        return evidence
    
    def _calculate_offender_probability(self, behavior_patterns: Dict[str, Any],
                                       methods: List[str],
                                       similar_posts: List[SimilarPost],
                                       historical_evidence: List[str]) -> float:
        """计算惯犯概率"""
        probability = 0.0
        
        # 1. 基于行为模式 (0.3分)
        if len(behavior_patterns.get("repetitive_actions", [])) > 0:
            probability += 0.15
        if len(behavior_patterns.get("consistent_behavior", [])) >= 2:
            probability += 0.15
        
        # 2. 基于作案手法 (0.3分)
        method_count = len(methods)
        if method_count >= 3:
            probability += 0.3
        elif method_count >= 2:
            probability += 0.2
        elif method_count >= 1:
            probability += 0.1
        
        # 3. 基于相似帖子 (0.3分)
        high_similarity_posts = [p for p in similar_posts if p.similarity_score >= 0.7]
        if len(high_similarity_posts) >= 3:
            probability += 0.3
        elif len(high_similarity_posts) >= 2:
            probability += 0.2
        elif len(high_similarity_posts) >= 1:
            probability += 0.1
        
        # 4. 基于历史证据 (0.1分)
        if len(historical_evidence) >= 3:
            probability += 0.1
        
        return min(1.0, probability)
    
    def _generate_reasoning(self, result: HabitualOffenderResult) -> str:
        """生成推理说明"""
        reasoning_parts = []
        
        # 惯犯等级
        level_map = {
            "高": "高度疑似惯犯",
            "中": "可能是惯犯",
            "低": "不太像惯犯",
            "无": "不太可能是惯犯"
        }
        reasoning_parts.append(f"{level_map.get(result.offender_level, '')}: 概率 {result.offender_probability:.2f}")
        
        # 相似帖子
        if result.similar_posts:
            reasoning_parts.append(f"\n发现 {len(result.similar_posts)} 个相似历史帖子:")
            for post in result.similar_posts[:3]:  # 只显示前3个
                reasoning_parts.append(
                    f"  • {post.platform}: '{post.content}' "
                    f"(相似度: {post.similarity_score:.2f})"
                )
        
        # 作案手法
        if result.modus_operandi:
            reasoning_parts.append(f"\n识别到的作案手法 ({len(result.modus_operandi)} 个):")
            for method in result.modus_operandi:
                reasoning_parts.append(f"  • {method}")
        
        # 历史证据
        if result.historical_evidence:
            reasoning_parts.append(f"\n历史证据 ({len(result.historical_evidence)} 条):")
            for evidence in result.historical_evidence[:3]:
                reasoning_parts.append(f"  • {evidence}")
        
        return "\n".join(reasoning_parts)
    
    def _calculate_confidence(self, result: HabitualOffenderResult) -> float:
        """计算置信度"""
        if not result.similar_posts and not result.modus_operandi:
            return 0.5
        
        # 基于相似帖子数量和相似度
        if result.similar_posts:
            avg_similarity = sum(p.similarity_score for p in result.similar_posts) / len(result.similar_posts)
            post_factor = avg_similarity * min(1.0, len(result.similar_posts) / 3.0)
        else:
            post_factor = 0.0
        
        # 基于作案手法数量
        method_factor = min(1.0, len(result.modus_operandi) / 3.0)
        
        # 综合计算
        confidence = post_factor * 0.7 + method_factor * 0.3
        
        return max(0.5, confidence)


def detect_habitual_offender(text: str, 
                             social_media_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    便捷函数: 检测惯犯
    
    Args:
        text: 案件描述文本
        social_media_data: 社交媒体数据
    
    Returns:
        惯犯分析结果字典
    """
    detector = HabitualOffenderDetector()
    result = detector.analyze(text, social_media_data)
    
    return {
        "is_habitual_offender": result.is_habitual_offender,
        "offender_probability": result.offender_probability,
        "offender_level": result.offender_level,
        "similar_posts": [
            {
                "post_id": p.post_id,
                "platform": p.platform,
                "content": p.content,
                "timestamp": p.timestamp,
                "similarity_score": p.similarity_score,
                "matched_keywords": p.matched_keywords
            }
            for p in result.similar_posts
        ],
        "behavior_patterns": result.behavior_patterns,
        "modus_operandi": result.modus_operandi,
        "historical_evidence": result.historical_evidence,
        "reasoning": result.reasoning,
        "confidence": result.confidence,
        "timestamp": result.timestamp.isoformat()
    }


if __name__ == "__main__":
    # 测试
    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """
    
    result = detect_habitual_offender(test_text)
    print("惯犯识别结果:")
    print(f"  是否惯犯: {result['is_habitual_offender']}")
    print(f"  惯犯概率: {result['offender_probability']:.2f}")
    print(f"  惯犯等级: {result['offender_level']}")
    print(f"  相似帖子数: {len(result['similar_posts'])}")
    print(f"\n推理说明:\n{result['reasoning']}")
