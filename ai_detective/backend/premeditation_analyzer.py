"""
行为分析引擎 - 预谋性分析
Behavior Analyzer - Premeditation Analysis
识别和分析案件中的预谋性行为特征
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class PremeditationIndicator:
    """预谋性指标"""
    indicator_type: str  # 指标类型
    description: str  # 描述
    confidence: float  # 置信度 (0-1)
    evidence: str  # 证据片段


@dataclass
class PremeditationResult:
    """预谋性分析结果"""
    timestamp: datetime
    is_premeditated: bool  # 是否预谋
    premeditation_score: float  # 预谋得分 (0-1)
    premeditation_level: str  # 预谋等级: 高/中/低/无
    indicators: List[PremeditationIndicator]  # 预谋指标
    behavior_pattern: Dict[str, Any]  # 行为模式
    action_route: List[str]  # 行动路线
    reasoning: str  # 推理说明
    confidence: float  # 置信度


class PremeditationAnalyzer:
    """预谋性分析引擎"""
    
    def __init__(self):
        # 预谋性关键词
        self.planning_keywords = [
            "准备", "计划", "安排", "设计", "预谋", "策划",
            "提前", "事先", "预先", "有意", "故意"
        ]
        
        # 行为连贯性关键词
        self.coherent_keywords = [
            "随即", "立刻", "立即", "马上", "紧接着", "之后",
            "随后", "然后", "接着"
        ]
        
        # 专业行为关键词
        self.professional_keywords = [
            "拍照", "录像", "取证", "录音", "记录", "保存",
            "报警", "投诉", "举报", "维权"
        ]
        
        # 冷静行为关键词
        self.calm_keywords = [
            "冷静", "沉着", "淡定", "不慌", "从容", "镇定"
        ]
        
        # 重复行为模式
        self.repetitive_patterns = [
            r"多次.*投诉",
            r"多次.*举报",
            r"多次.*维权",
            r"经常.*",
            r"每次.*"
        ]
    
    def analyze(self, text: str, time_analysis: Dict[str, Any] = None,
                causal_analysis: Dict[str, Any] = None) -> PremeditationResult:
        """
        分析预谋性
        
        Args:
            text: 案件描述文本
            time_analysis: 时间分析结果
            causal_analysis: 因果分析结果
        
        Returns:
            预谋性分析结果
        """
        if time_analysis is None:
            time_analysis = {}
        if causal_analysis is None:
            causal_analysis = {}
        
        result = PremeditationResult(
            timestamp=datetime.now(),
            is_premeditated=False,
            premeditation_score=0.0,
            premeditation_level="无",
            indicators=[],
            behavior_pattern={},
            action_route=[],
            reasoning="",
            confidence=0.0
        )
        
        # 1. 提取预谋性指标
        indicators = self._extract_indicators(text)
        result.indicators = indicators
        
        # 2. 分析行为模式
        result.behavior_pattern = self._analyze_behavior_pattern(text)
        
        # 3. 构建行动路线
        result.action_route = self._build_action_route(text)
        
        # 4. 计算预谋得分
        score = self._calculate_premeditation_score(
            indicators, 
            result.behavior_pattern, 
            time_analysis, 
            causal_analysis
        )
        result.premeditation_score = score
        
        # 5. 判断预谋等级
        if score >= 0.8:
            result.premeditation_level = "高"
        elif score >= 0.5:
            result.premeditation_level = "中"
        elif score >= 0.3:
            result.premeditation_level = "低"
        else:
            result.premeditation_level = "无"
        
        # 6. 判断是否预谋
        result.is_premeditated = score >= 0.5
        
        # 7. 生成推理说明
        result.reasoning = self._generate_reasoning(result)
        
        # 8. 计算置信度
        result.confidence = self._calculate_confidence(result)
        
        return result
    
    def _extract_indicators(self, text: str) -> List[PremeditationIndicator]:
        """提取预谋性指标"""
        indicators = []
        
        # 1. 检查准备计划指标
        for kw in self.planning_keywords:
            if kw in text:
                # 找到关键词所在的句子
                pattern = rf'[^。]*{kw}[^。]*'
                matches = re.findall(pattern, text)
                for match in matches:
                    indicators.append(PremeditationIndicator(
                        indicator_type="准备计划",
                        description=f"发现准备计划词汇: '{kw}'",
                        confidence=0.7,
                        evidence=match.strip()
                    ))
        
        # 2. 检查行为连贯性
        coherent_count = sum(1 for kw in self.coherent_keywords if kw in text)
        if coherent_count >= 2:
            indicators.append(PremeditationIndicator(
                indicator_type="行为连贯",
                description=f"发现 {coherent_count} 个连贯性词汇,显示出计划性",
                confidence=0.6,
                evidence=", ".join([kw for kw in self.coherent_keywords if kw in text])
            ))
        
        # 3. 检查专业行为
        professional_count = sum(1 for kw in self.professional_keywords if kw in text)
        if professional_count >= 2:
            indicators.append(PremeditationIndicator(
                indicator_type="专业行为",
                description=f"发现 {professional_count} 个专业词汇,显示出专业性",
                confidence=0.8,
                evidence=", ".join([kw for kw in self.professional_keywords if kw in text])
            ))
        
        # 4. 检查冷静表现
        if any(kw in text for kw in self.calm_keywords):
            indicators.append(PremeditationIndicator(
                indicator_type="冷静表现",
                description="发现冷静表现词汇,显示出预谋性",
                confidence=0.6,
                evidence=", ".join([kw for kw in self.calm_keywords if kw in text])
            ))
        
        # 5. 检查重复行为模式
        for pattern in self.repetitive_patterns:
            matches = re.findall(pattern, text)
            if matches:
                indicators.append(PremeditationIndicator(
                    indicator_type="重复行为",
                    description=f"发现重复行为模式: '{matches[0]}'",
                    confidence=0.75,
                    evidence=matches[0]
                ))
        
        return indicators
    
    def _analyze_behavior_pattern(self, text: str) -> Dict[str, Any]:
        """分析行为模式"""
        pattern = {
            "steps": [],
            "time_gaps": [],
            "emotional_changes": [],
            "behavior_type": "unknown"
        }
        
        # 分句
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        
        # 提取行为步骤
        action_keywords = ["到店", "进入", "支付", "要求", "报警", "发布", "投诉", "举报"]
        for i, sentence in enumerate(sentences):
            if any(kw in sentence for kw in action_keywords):
                pattern["steps"].append({
                    "index": i,
                    "content": sentence[:50],
                    "actions": [kw for kw in action_keywords if kw in sentence]
                })
        
        # 判断行为类型
        if any("投诉" in s or "举报" in s or "报警" in s for s in sentences):
            if pattern["steps"]:
                # 如果行为步骤连贯,则认为是预谋性
                pattern["behavior_type"] = "premeditated_action"
            else:
                pattern["behavior_type"] = "reactionary_action"
        
        # 检查情绪变化
        negative_emotions = ["愤怒", "生气", "激动", "不满", "抗议"]
        positive_emotions = ["满意", "高兴", "开心", "认可", "赞同"]
        
        for sentence in sentences:
            if any(em in sentence for em in negative_emotions):
                pattern["emotional_changes"].append("负面情绪")
            elif any(em in sentence for em in positive_emotions):
                pattern["emotional_changes"].append("正面情绪")
        
        return pattern
    
    def _build_action_route(self, text: str) -> List[str]:
        """构建行动路线"""
        route = []
        
        # 分句
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        
        # 提取关键行动
        for sentence in sentences:
            if "到店" in sentence or "进入" in sentence:
                route.append("到达现场")
            elif "支付" in sentence:
                route.append("完成支付")
            elif "要求" in sentence:
                route.append("提出要求")
            elif "报警" in sentence:
                route.append("报警")
            elif "拍照" in sentence or "录像" in sentence or "取证" in sentence:
                route.append("收集证据")
            elif "发布" in sentence or "投诉" in sentence or "举报" in sentence:
                route.append("发布投诉/举报")
            elif "收到" in sentence:
                route.append("收到处罚/结果")
        
        return route
    
    def _calculate_premeditation_score(self, indicators: List[PremeditationIndicator],
                                        behavior_pattern: Dict[str, Any],
                                        time_analysis: Dict[str, Any],
                                        causal_analysis: Dict[str, Any]) -> float:
        """计算预谋得分"""
        score = 0.0
        
        # 1. 基于预谋性指标
        indicator_count = len(indicators)
        if indicator_count >= 5:
            score += 0.3
        elif indicator_count >= 3:
            score += 0.2
        elif indicator_count >= 1:
            score += 0.1
        
        # 2. 基于行为模式
        if behavior_pattern.get("behavior_type") == "premeditated_action":
            score += 0.2
        
        # 3. 基于行动路线
        action_steps = behavior_pattern.get("steps", [])
        if len(action_steps) >= 4:
            score += 0.2
        elif len(action_steps) >= 2:
            score += 0.1
        
        # 4. 基于时间分析
        time_conflicts = time_analysis.get("time_conflicts", [])
        if not time_conflicts:  # 无时间冲突,说明逻辑清晰
            score += 0.1
        
        # 5. 基于因果分析
        causal_confidence = causal_analysis.get("root_cause_confidence", 0.0)
        if causal_confidence > 0.8:
            score += 0.2
        elif causal_confidence > 0.6:
            score += 0.1
        
        return min(1.0, score)
    
    def _generate_reasoning(self, result: PremeditationResult) -> str:
        """生成推理说明"""
        reasoning_parts = []
        
        # 预谋等级
        level_map = {
            "高": "高度预谋",
            "中": "可能预谋",
            "低": "不太像预谋",
            "无": "不太可能是预谋"
        }
        reasoning_parts.append(f"{level_map.get(result.premeditation_level, '')}: 得分 {result.premeditation_score:.2f}")
        
        # 指标数量
        if result.indicators:
            reasoning_parts.append(f"发现 {len(result.indicators)} 个预谋性指标:")
            for indicator in result.indicators:
                reasoning_parts.append(f"  • {indicator.description} (置信度: {indicator.confidence:.2f})")
        
        # 行为模式
        if result.behavior_pattern.get("steps"):
            reasoning_parts.append(f"行为模式: {len(result.behavior_pattern['steps'])} 个关键步骤")
        
        # 行动路线
        if result.action_route:
            reasoning_parts.append(f"行动路线: {' → '.join(result.action_route)}")
        
        return "\n".join(reasoning_parts)
    
    def _calculate_confidence(self, result: PremeditationResult) -> float:
        """计算置信度"""
        if not result.indicators:
            return 0.5
        
        # 基于指标数量和置信度
        indicator_confidences = [ind.confidence for ind in result.indicators]
        avg_confidence = sum(indicator_confidences) / len(indicator_confidences)
        
        # 基于指标数量
        count_factor = min(1.0, len(result.indicators) / 5.0)
        
        # 综合计算
        confidence = avg_confidence * 0.7 + count_factor * 0.3
        
        return confidence


def analyze_premeditation(text: str, time_analysis: Dict[str, Any] = None,
                          causal_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    便捷函数: 分析预谋性
    
    Args:
        text: 案件描述文本
        time_analysis: 时间分析结果
        causal_analysis: 因果分析结果
    
    Returns:
        预谋性分析结果字典
    """
    analyzer = PremeditationAnalyzer()
    result = analyzer.analyze(text, time_analysis, causal_analysis)
    
    return {
        "is_premeditated": result.is_premeditated,
        "premeditation_score": result.premeditation_score,
        "premeditation_level": result.premeditation_level,
        "indicators": [
            {
                "type": ind.indicator_type,
                "description": ind.description,
                "confidence": ind.confidence,
                "evidence": ind.evidence
            }
            for ind in result.indicators
        ],
        "behavior_pattern": result.behavior_pattern,
        "action_route": result.action_route,
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
    
    result = analyze_premeditation(test_text)
    print("预谋性分析结果:")
    print(f"  是否预谋: {result['is_premeditated']}")
    print(f"  预谋得分: {result['premeditation_score']:.2f}")
    print(f"  预谋等级: {result['premeditation_level']}")
    print(f"  预谋指标数: {len(result['indicators'])}")
    print(f"\n推理说明:\n{result['reasoning']}")
