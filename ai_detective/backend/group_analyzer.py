"""
团伙分析引擎
Group Analysis Engine
识别和分析团伙作案特征
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class Person:
    """人物"""
    name: str
    role: str  # 角色: 主犯/从犯/帮凶
    actions: List[str]  # 行为列表
    relationship: str  # 与其他人的关系
    confidence: float  # 置信度


@dataclass
class Association:
    """关联"""
    person1: str
    person2: str
    relationship_type: str  # 关系类型: 同伙/共犯/串通
    evidence: str  # 证据
    strength: float  # 关联强度 (0-1)


@dataclass
class GroupAnalysisResult:
    """团伙分析结果"""
    timestamp: datetime
    is_group_crime: bool  # 是否团伙作案
    group_probability: float  # 团伙作案概率 (0-1)
    group_size: int  # 团伙人数
    persons: List[Person]  # 涉及人员
    associations: List[Association]  # 关联关系
    group_structure: Dict[str, Any]  # 团伙结构
    coordination_evidence: List[str]  # 配合证据
    reasoning: str  # 推理说明
    confidence: float  # 置信度


class GroupAnalyzer:
    """团伙分析引擎"""
    
    def __init__(self):
        # 团伙作案特征关键词
        self.group_keywords = [
            "同伙", "共犯", "团伙", "勾结", "串通",
            "合谋", "配合", "协作", "分工"
        ]
        
        # 角色指示词
        self.role_indicators = {
            "主犯": ["主导", "策划", "组织", "安排", "指使"],
            "从犯": ["跟随", "协助", "配合", "执行"],
            "帮凶": ["协助", "掩护", "配合", "在场"]
        }
        
        # 配合行为
        self.coordination_patterns = [
            r"一人.*另一人",
            r"一个.*另一个",
            r"同时.*",
            r"一起.*",
            r"分工.*"
        ]
    
    def analyze(self, text: str, time_analysis: Dict[str, Any] = None,
                causal_analysis: Dict[str, Any] = None) -> GroupAnalysisResult:
        """
        分析是否为团伙作案
        
        Args:
            text: 案件描述文本
            time_analysis: 时间分析结果
            causal_analysis: 因果分析结果
        
        Returns:
            团伙分析结果
        """
        if time_analysis is None:
            time_analysis = {}
        if causal_analysis is None:
            causal_analysis = {}
        
        result = GroupAnalysisResult(
            timestamp=datetime.now(),
            is_group_crime=False,
            group_probability=0.0,
            group_size=0,
            persons=[],
            associations=[],
            group_structure={},
            coordination_evidence=[],
            reasoning="",
            confidence=0.0
        )
        
        # 1. 识别涉及人员
        result.persons = self._identify_persons(text)
        
        # 2. 识别关联关系
        result.associations = self._identify_associations(text, result.persons)
        
        # 3. 分析团伙结构
        result.group_structure = self._analyze_group_structure(
            result.persons, 
            result.associations
        )
        
        # 4. 收集配合证据
        result.coordination_evidence = self._collect_coordination_evidence(text)
        
        # 5. 计算团伙作案概率
        probability = self._calculate_group_probability(
            result.persons,
            result.associations,
            result.coordination_evidence,
            time_analysis,
            causal_analysis
        )
        result.group_probability = probability
        
        # 6. 判断团伙人数
        result.group_size = len(result.persons)
        
        # 7. 判断是否团伙作案
        result.is_group_crime = probability >= 0.5 and result.group_size >= 2
        
        # 8. 生成推理说明
        result.reasoning = self._generate_reasoning(result)
        
        # 9. 计算置信度
        result.confidence = self._calculate_confidence(result)
        
        return result
    
    def _identify_persons(self, text: str) -> List[Person]:
        """识别涉及人员"""
        persons = []
        
        # 简化版: 从文本中识别人物指示词
        # 实际应用中应该使用NER(命名实体识别)
        
        # 检查是否提到多人
        multi_person_patterns = [
            r"一人.*另一人",
            r"一个.*另一个",
            r"女生.*和她",
            r"男子.*和.*男子"
        ]
        
        found_multi = False
        for pattern in multi_person_patterns:
            matches = re.findall(pattern, text)
            if matches:
                found_multi = True
                break
        
        if found_multi:
            # 创建两个人物 (简化)
            persons.append(Person(
                name="人员A",
                role="未知",
                actions=[],
                relationship="与人员B疑似同伙",
                confidence=0.6
            ))
            persons.append(Person(
                name="人员B",
                role="未知",
                actions=[],
                relationship="与人员A疑似同伙",
                confidence=0.6
            ))
        else:
            # 如果没有明确提到多人,基于行为判断是否有隐含同伙
            if "同伙" in text or "团伙" in text:
                persons.append(Person(
                    name="主犯",
                    role="主犯",
                    actions=["策划", "执行"],
                    relationship="与同伙协同",
                    confidence=0.8
                ))
                persons.append(Person(
                    name="同伙",
                    role="从犯",
                    actions=["配合", "掩护"],
                    relationship="与主犯协同",
                    confidence=0.7
                ))
        
        return persons
    
    def _identify_associations(self, text: str, 
                               persons: List[Person]) -> List[Association]:
        """识别关联关系"""
        associations = []
        
        if len(persons) >= 2:
            # 如果有2个以上人员,检查是否有关联证据
            
            # 检查团伙关键词
            for kw in self.group_keywords:
                if kw in text:
                    associations.append(Association(
                        person1=persons[0].name,
                        person2=persons[1].name,
                        relationship_type="同伙",
                        evidence=f"文本中提到'{kw}'",
                        strength=0.7
                    ))
                    break
            
            # 如果没有找到关键词但有2个以上人员,给予低置信度关联
            if not associations and len(persons) >= 2:
                associations.append(Association(
                    person1=persons[0].name,
                    person2=persons[1].name,
                    relationship_type="疑似同伙",
                    evidence="同时出现在案件中",
                    strength=0.3
                ))
        
        return associations
    
    def _analyze_group_structure(self, persons: List[Person],
                                 associations: List[Association]) -> Dict[str, Any]:
        """分析团伙结构"""
        structure = {
            "type": "unknown",  # 结构类型: 单一/层级/网络
            "leader": None,  # 首领
            "members": [],  # 成员
            "roles": {},  # 角色分配
            "coordination_level": "unknown"  # 配合程度: 高/中/低
        }
        
        if not persons:
            return structure
        
        # 确定结构类型
        if len(persons) == 2:
            structure["type"] = "单一"
        elif len(persons) > 2:
            structure["type"] = "层级"
        
        # 识别首领
        leaders = [p for p in persons if p.role == "主犯"]
        if leaders:
            structure["leader"] = leaders[0].name
        
        # 收集成员
        structure["members"] = [p.name for p in persons if p.role != "主犯"]
        
        # 统计角色
        roles = {}
        for person in persons:
            role = person.role if person.role != "未知" else "成员"
            roles[role] = roles.get(role, 0) + 1
        structure["roles"] = roles
        
        # 评估配合程度
        if len(associations) > 0:
            avg_strength = sum(a.strength for a in associations) / len(associations)
            if avg_strength >= 0.7:
                structure["coordination_level"] = "高"
            elif avg_strength >= 0.5:
                structure["coordination_level"] = "中"
            else:
                structure["coordination_level"] = "低"
        else:
            structure["coordination_level"] = "低"
        
        return structure
    
    def _collect_coordination_evidence(self, text: str) -> List[str]:
        """收集配合证据"""
        evidence = []
        
        # 检查配合行为模式
        for pattern in self.coordination_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                evidence.append(f"发现配合行为: '{match}'")
        
        # 检查团伙关键词
        for kw in self.group_keywords:
            if kw in text:
                evidence.append(f"文本提到团伙相关词汇: '{kw}'")
        
        return evidence
    
    def _calculate_group_probability(self, persons: List[Person],
                                     associations: List[Association],
                                     coordination_evidence: List[str],
                                     time_analysis: Dict[str, Any],
                                     causal_analysis: Dict[str, Any]) -> float:
        """计算团伙作案概率"""
        probability = 0.0
        
        # 1. 基于人数 (0.3分)
        if len(persons) >= 3:
            probability += 0.3
        elif len(persons) >= 2:
            probability += 0.2
        elif len(persons) >= 1:
            probability += 0.05
        
        # 2. 基于关联关系 (0.3分)
        strong_associations = [a for a in associations if a.strength >= 0.7]
        if len(strong_associations) >= 2:
            probability += 0.3
        elif len(strong_associations) >= 1:
            probability += 0.2
        elif associations:
            probability += 0.1
        
        # 3. 基于配合证据 (0.2分)
        if len(coordination_evidence) >= 3:
            probability += 0.2
        elif len(coordination_evidence) >= 2:
            probability += 0.15
        elif len(coordination_evidence) >= 1:
            probability += 0.1
        
        # 4. 基于时间分析 (0.1分)
        # 如果有多个人员在同一时间段出现,增加概率
        if time_analysis.get("timestamps_count", 0) > 0:
            critical_ts = time_analysis.get("critical_timestamps", [])
            if len(critical_ts) > 0:
                probability += 0.1
        
        # 5. 基于因果分析 (0.1分)
        # 如果有多个因果指向同一目的,增加概率
        if causal_analysis.get("chains_count", 0) > 0:
            probability += 0.05
        
        return min(1.0, probability)
    
    def _generate_reasoning(self, result: GroupAnalysisResult) -> str:
        """生成推理说明"""
        reasoning_parts = []
        
        # 团伙判断
        if result.is_group_crime:
            reasoning_parts.append(f"✅ 团伙作案: 概率 {result.group_probability:.2f}, 涉及 {result.group_size} 人")
        else:
            reasoning_parts.append(f"❌ 非团伙作案: 概率 {result.group_probability:.2f}")
        
        # 人员信息
        if result.persons:
            reasoning_parts.append(f"\n涉及人员 ({len(result.persons)} 人):")
            for person in result.persons:
                reasoning_parts.append(
                    f"  • {person.name}: {person.role} "
                    f"(置信度: {person.confidence:.2f})"
                )
        
        # 关联关系
        if result.associations:
            reasoning_parts.append(f"\n关联关系 ({len(result.associations)} 条):")
            for assoc in result.associations:
                reasoning_parts.append(
                    f"  • {assoc.person1} ←{assoc.relationship_type}→ {assoc.person2} "
                    f"(强度: {assoc.strength:.2f})"
                )
                if assoc.evidence:
                    reasoning_parts.append(f"    证据: {assoc.evidence}")
        
        # 团伙结构
        structure = result.group_structure
        if structure:
            reasoning_parts.append(f"\n团伙结构:")
            reasoning_parts.append(f"  • 结构类型: {structure['type']}")
            if structure['leader']:
                reasoning_parts.append(f"  • 首领: {structure['leader']}")
            if structure['members']:
                reasoning_parts.append(f"  • 成员: {', '.join(structure['members'])}")
            reasoning_parts.append(f"  • 配合程度: {structure['coordination_level']}")
        
        # 配合证据
        if result.coordination_evidence:
            reasoning_parts.append(f"\n配合证据 ({len(result.coordination_evidence)} 条):")
            for evidence in result.coordination_evidence:
                reasoning_parts.append(f"  • {evidence}")
        
        return "\n".join(reasoning_parts)
    
    def _calculate_confidence(self, result: GroupAnalysisResult) -> float:
        """计算置信度"""
        if not result.persons:
            return 0.5
        
        # 基于人员数量和置信度
        person_confidences = [p.confidence for p in result.persons]
        avg_person_confidence = sum(person_confidences) / len(person_confidences)
        
        # 基于关联关系
        if result.associations:
            avg_assoc_strength = sum(a.strength for a in result.associations) / len(result.associations)
        else:
            avg_assoc_strength = 0.0
        
        # 综合计算
        confidence = avg_person_confidence * 0.5 + avg_assoc_strength * 0.5
        
        return max(0.5, confidence)


def analyze_group(text: str, time_analysis: Dict[str, Any] = None,
                 causal_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    便捷函数: 分析团伙作案
    
    Args:
        text: 案件描述文本
        time_analysis: 时间分析结果
        causal_analysis: 因果分析结果
    
    Returns:
        团伙分析结果字典
    """
    analyzer = GroupAnalyzer()
    result = analyzer.analyze(text, time_analysis, causal_analysis)
    
    return {
        "is_group_crime": result.is_group_crime,
        "group_probability": result.group_probability,
        "group_size": result.group_size,
        "persons": [
            {
                "name": p.name,
                "role": p.role,
                "actions": p.actions,
                "relationship": p.relationship,
                "confidence": p.confidence
            }
            for p in result.persons
        ],
        "associations": [
            {
                "person1": a.person1,
                "person2": a.person2,
                "relationship_type": a.relationship_type,
                "evidence": a.evidence,
                "strength": a.strength
            }
            for a in result.associations
        ],
        "group_structure": result.group_structure,
        "coordination_evidence": result.coordination_evidence,
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
    
    result = analyze_group(test_text)
    print("团伙分析结果:")
    print(f"  是否团伙作案: {result['is_group_crime']}")
    print(f"  团伙概率: {result['group_probability']:.2f}")
    print(f"  团伙人数: {result['group_size']}")
    print(f"\n推理说明:\n{result['reasoning']}")
