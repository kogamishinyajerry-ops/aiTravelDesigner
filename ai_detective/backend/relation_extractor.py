"""
关系抽取模块
Relation Extractor
从案件描述中识别和提取实体间的关系
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Relation:
    """关系"""
    id: str  # 关系ID
    type: str  # 关系类型: person_person/person_location/person_amount/等
    source: str  # 源实体ID
    target: str  # 目标实体ID
    relation: str  # 关系描述
    confidence: float  # 置信度 (0-1)
    evidence: str  # 证据片段


@dataclass
class RelationExtractionResult:
    """关系抽取结果"""
    timestamp: datetime
    relations: List[Relation]  # 关系列表
    relation_counts: Dict[str, int]  # 各类关系统计
    key_relations: List[str]  # 关键关系


class RelationExtractor:
    """关系抽取器"""
    
    def __init__(self):
        # 人物关系模式
        self.person_person_patterns = [
            (r"([^，。]+)\s*(?:投诉|举报|报警|起诉)\s*([^，。]+)", "投诉"),
            (r"([^，。]+)\s*(?:支付|退款|购买)\s*([^，。]+)", "交易"),
            (r"([^，。]+)\s*(?:与|和)\s*([^，。]+)\s*(?:发生|产生)\s*(?:争执|纠纷|冲突)", "争执"),
            (r"([^，。]+)\s*(?:帮助|协助|配合)\s*([^，。]+)", "协助"),
            (r"([^，。]+)\s*(?:是|作为)\s*([^，。]+)\s*(?:的|作为|的同事|的朋友)", "关联")
        ]
        
        # 人物-地点关系模式
        self.person_location_patterns = [
            (r"([^，。]+)\s*(?:来到|到达|进入|离开)\s*([^，。]+)", "到达"),
            (r"([^，。]+)\s*(?:在)\s*([^，。]+)", "位于"),
            (r"([^，。]+)\s*(?:从)\s*([^，。]+)", "来自")
        ]
        
        # 人物-金额关系模式
        self.person_amount_patterns = [
            (r"([^，。]+)\s*(?:支付|收取|获得|损失)\s*([^，。]+)", "交易"),
            (r"([^，。]+)\s*(?:花费|花费了)\s*([^，。]+)", "花费"),
            (r"([^，。]+)\s*(?:索赔|索要)\s*([^，。]+)", "索赔")
        ]
        
        # 人物-时间关系模式
        self.person_time_patterns = [
            (r"([^，。]+)\s*(?:在|于)\s*([^，。]+)", "出现在"),
            (r"([^，。]+)\s*(?:于)\s*([^，。]+)\s*(?:发布|发表|提出)", "行动")
        ]
        
        # 事件关系模式
        self.event_relation_patterns = [
            (r"([^，。]+)\s*(?:导致|引起|造成)\s*([^，。]+)", "因果"),
            (r"([^，。]+)\s*(?:之后|随后|紧接着)\s*([^，。]+)", "顺序"),
            (r"([^，。]+)\s*(?:导致|造成)\s*([^，。]+)", "结果")
        ]
        
        # 证据-事实关系模式
        self.evidence_fact_patterns = [
            (r"([^，。]+)\s*(?:证明|证实|表明)\s*([^，。]+)", "证明"),
            (r"([^，。]+)\s*(?:作为|是)\s*([^，。]+)\s*(?:的证据|的证明)", "证据")
        ]
    
    def extract(self, text: str, entities: List[Any] = None) -> RelationExtractionResult:
        """
        提取关系
        
        Args:
            text: 案件描述文本
            entities: 实体列表（可选，如果没有则自动提取）
        
        Returns:
            关系抽取结果
        """
        if entities is None:
            # 如果没有实体列表，使用文本直接提取
            entities = []
        
        result = RelationExtractionResult(
            timestamp=datetime.now(),
            relations=[],
            relation_counts={},
            key_relations=[]
        )
        
        # 1. 提取人物关系
        person_person_relations = self._extract_person_person_relations(text, entities)
        result.relations.extend(person_person_relations)
        
        # 2. 提取人物-地点关系
        person_location_relations = self._extract_person_location_relations(text, entities)
        result.relations.extend(person_location_relations)
        
        # 3. 提取人物-金额关系
        person_amount_relations = self._extract_person_amount_relations(text, entities)
        result.relations.extend(person_amount_relations)
        
        # 4. 提取人物-时间关系
        person_time_relations = self._extract_person_time_relations(text, entities)
        result.relations.extend(person_time_relations)
        
        # 5. 提取事件关系
        event_relations = self._extract_event_relations(text)
        result.relations.extend(event_relations)
        
        # 6. 提取证据-事实关系
        evidence_fact_relations = self._extract_evidence_fact_relations(text, entities)
        result.relations.extend(evidence_fact_relations)
        
        # 7. 统计各类关系数量
        result.relation_counts = self._count_relations(result.relations)
        
        # 8. 确定关键关系
        result.key_relations = self._identify_key_relations(result.relations)
        
        return result
    
    def _extract_person_person_relations(self, text: str, 
                                        entities: List[Any]) -> List[Relation]:
        """提取人物关系"""
        relations = []
        relation_id = 0
        
        for pattern, relation_type in self.person_person_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                relation_id += 1
                relation = Relation(
                    id=f"pp_{relation_id}",
                    type="person_person",
                    source=match.group(1),
                    target=match.group(2),
                    relation=relation_type,
                    confidence=0.7,
                    evidence=match.group()
                )
                relations.append(relation)
        
        return relations
    
    def _extract_person_location_relations(self, text: str,
                                          entities: List[Any]) -> List[Relation]:
        """提取人物-地点关系"""
        relations = []
        relation_id = 0
        
        for pattern, relation_type in self.person_location_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                relation_id += 1
                relation = Relation(
                    id=f"pl_{relation_id}",
                    type="person_location",
                    source=match.group(1),
                    target=match.group(2),
                    relation=relation_type,
                    confidence=0.75,
                    evidence=match.group()
                )
                relations.append(relation)
        
        return relations
    
    def _extract_person_amount_relations(self, text: str,
                                        entities: List[Any]) -> List[Relation]:
        """提取人物-金额关系"""
        relations = []
        relation_id = 0
        
        for pattern, relation_type in self.person_amount_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                relation_id += 1
                relation = Relation(
                    id=f"pa_{relation_id}",
                    type="person_amount",
                    source=match.group(1),
                    target=match.group(2),
                    relation=relation_type,
                    confidence=0.8,
                    evidence=match.group()
                )
                relations.append(relation)
        
        return relations
    
    def _extract_person_time_relations(self, text: str,
                                      entities: List[Any]) -> List[Relation]:
        """提取人物-时间关系"""
        relations = []
        relation_id = 0
        
        for pattern, relation_type in self.person_time_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                relation_id += 1
                relation = Relation(
                    id=f"pt_{relation_id}",
                    type="person_time",
                    source=match.group(1),
                    target=match.group(2),
                    relation=relation_type,
                    confidence=0.7,
                    evidence=match.group()
                )
                relations.append(relation)
        
        return relations
    
    def _extract_event_relations(self, text: str) -> List[Relation]:
        """提取事件关系"""
        relations = []
        relation_id = 0
        
        # 分句
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        
        for i in range(len(sentences) - 1):
            sentence1 = sentences[i]
            sentence2 = sentences[i + 1]
            
            # 提取每个句子的关键事件
            events1 = self._extract_events_from_sentence(sentence1)
            events2 = self._extract_events_from_sentence(sentence2)
            
            if events1 and events2:
                relation_id += 1
                relation = Relation(
                    id=f"event_{relation_id}",
                    type="event_event",
                    source=events1[0],
                    target=events2[0],
                    relation="顺序",
                    confidence=0.6,
                    evidence=f"{sentence1} → {sentence2}"
                )
                relations.append(relation)
        
        return relations
    
    def _extract_events_from_sentence(self, sentence: str) -> List[str]:
        """从句子中提取事件"""
        events = []
        
        # 简化版: 提取动词
        action_keywords = ["支付", "退款", "购买", "投诉", "举报", "报警", "发布", "收到"]
        for keyword in action_keywords:
            if keyword in sentence:
                events.append(keyword)
        
        return events
    
    def _extract_evidence_fact_relations(self, text: str,
                                        entities: List[Any]) -> List[Relation]:
        """提取证据-事实关系"""
        relations = []
        relation_id = 0
        
        for pattern, relation_type in self.evidence_fact_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                relation_id += 1
                relation = Relation(
                    id=f"ef_{relation_id}",
                    type="evidence_fact",
                    source=match.group(1),
                    target=match.group(2),
                    relation=relation_type,
                    confidence=0.75,
                    evidence=match.group()
                )
                relations.append(relation)
        
        return relations
    
    def _count_relations(self, relations: List[Relation]) -> Dict[str, int]:
        """统计各类关系数量"""
        counts = {}
        for relation in relations:
            relation_type = relation.type
            counts[relation_type] = counts.get(relation_type, 0) + 1
        return counts
    
    def _identify_key_relations(self, relations: List[Relation]) -> List[str]:
        """识别关键关系"""
        key_relations = []
        
        # 优先级排序: person_person > person_amount > event_event > 其他
        priority = {
            "person_person": 1,
            "person_amount": 2,
            "event_event": 3,
            "person_location": 4,
            "person_time": 5,
            "evidence_fact": 6
        }
        
        # 按优先级和置信度排序
        sorted_relations = sorted(
            relations,
            key=lambda r: (priority.get(r.type, 99), -r.confidence)
        )
        
        # 选择前10个作为关键关系
        for relation in sorted_relations[:10]:
            key_relations.append(
                f"{relation.source} -[{relation.relation}]-> {relation.target}"
            )
        
        return key_relations


def extract_relations(text: str, entities: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    便捷函数: 提取关系
    
    Args:
        text: 案件描述文本
        entities: 实体列表（可选）
    
    Returns:
        关系抽取结果字典
    """
    extractor = RelationExtractor()
    result = extractor.extract(text, entities)
    
    return {
        "relations": [
            {
                "id": r.id,
                "type": r.type,
                "source": r.source,
                "target": r.target,
                "relation": r.relation,
                "confidence": r.confidence,
                "evidence": r.evidence
            }
            for r in result.relations
        ],
        "relation_counts": result.relation_counts,
        "key_relations": result.key_relations,
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
    
    result = extract_relations(test_text)
    print("关系抽取结果:")
    print(f"  关系总数: {len(result['relations'])}")
    print(f"  关系分布: {result['relation_counts']}")
    print(f"  关键关系: {result['key_relations']}")
    
    print("\n关系列表:")
    for relation in result['relations'][:10]:
        print(f"  • [{relation['type']}] {relation['source']} -[{relation['relation']}]-> {relation['target']} (置信度: {relation['confidence']:.2f})")
