"""
实体抽取模块
Entity Extractor
从案件描述中识别和提取实体信息
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Entity:
    """实体"""
    id: str  # 实体ID
    type: str  # 实体类型: person/location/amount/organization/time/other
    text: str  # 实体文本
    start: int  # 开始位置
    end: int  # 结束位置
    confidence: float  # 置信度 (0-1)
    attributes: Dict[str, Any]  # 额外属性


@dataclass
class EntityExtractionResult:
    """实体抽取结果"""
    timestamp: datetime
    entities: List[Entity]  # 实体列表
    entity_counts: Dict[str, int]  # 各类实体计数
    key_entities: List[str]  # 关键实体


class EntityExtractor:
    """实体抽取器"""
    
    def __init__(self):
        # 人物识别模式
        self.person_patterns = [
            r"(?:女生|男子|女子|男人|女人|老板|店员|店长|经理|客服|警察|法官|律师)",
            r"(?:小明|小红|小张|小李|小王|小刘|小陈|小杨)",
            r"(?:张三|李四|王五|赵六)"
        ]
        
        # 地点识别模式
        self.location_patterns = [
            r"(?:店铺|商店|商场|超市|餐厅|酒店|银行|医院|学校)",
            r"(?:办公室|会议室|大厅|停车场|公园|街道)"
        ]
        
        # 金额识别模式
        self.amount_patterns = [
            r"(\d+(?:\.\d+)?)\s*(?:元|块|万|千|百)",
            r"人民币?\s*(\d+(?:\.\d+)?)",
            r"(\d+(?:\.\d+)?)\s*RMB"
        ]
        
        # 时间识别模式
        self.time_patterns = [
            r"(\d{4})[年/](\d{1,2})[月/](\d{1,2})[日]",
            r"(\d{1,2})[月/](\d{1,2})[日]",
            r"(?:今天|昨天|前天)",
            r"(?:上午|下午|晚上|深夜|凌晨)\s*(\d{1,2})[点:时](\d{1,2})?(?:分)?",
            r"(\d{1,2})[:：](\d{1,2})"
        ]
        
        # 机构识别模式
        self.organization_patterns = [
            r"(?:公司|企业|集团|机构|协会|委员会|派出所|法院|检察院)",
            r"(?:有限公司|股份公司|集团|组织)"
        ]
        
        # 证据相关关键词
        self.evidence_keywords = [
            "录音", "录像", "照片", "截图", "聊天记录", "合同",
            "发票", "收据", "单据", "凭证", "证明", "证人", "证词"
        ]
        
        # 行为相关关键词
        self.action_keywords = [
            "支付", "退款", "购买", "投诉", "举报", "报警",
            "取证", "协商", "谈判", "仲裁", "诉讼", "判决"
        ]
    
    def extract(self, text: str) -> EntityExtractionResult:
        """
        提取实体
        
        Args:
            text: 案件描述文本
        
        Returns:
            实体抽取结果
        """
        result = EntityExtractionResult(
            timestamp=datetime.now(),
            entities=[],
            entity_counts={},
            key_entities=[]
        )
        
        # 1. 识别人物实体
        person_entities = self._extract_persons(text)
        result.entities.extend(person_entities)
        
        # 2. 识别地点实体
        location_entities = self._extract_locations(text)
        result.entities.extend(location_entities)
        
        # 3. 识别金额实体
        amount_entities = self._extract_amounts(text)
        result.entities.extend(amount_entities)
        
        # 4. 识别时间实体
        time_entities = self._extract_times(text)
        result.entities.extend(time_entities)
        
        # 5. 识别机构实体
        org_entities = self._extract_organizations(text)
        result.entities.extend(org_entities)
        
        # 6. 识别证据实体
        evidence_entities = self._extract_evidences(text)
        result.entities.extend(evidence_entities)
        
        # 7. 识别行为实体
        action_entities = self._extract_actions(text)
        result.entities.extend(action_entities)
        
        # 8. 统计各类实体数量
        result.entity_counts = self._count_entities(result.entities)
        
        # 9. 确定关键实体
        result.key_entities = self._identify_key_entities(result.entities)
        
        return result
    
    def _extract_persons(self, text: str) -> List[Entity]:
        """提取人物实体"""
        entities = []
        entity_id = 0
        
        for pattern in self.person_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entity_id += 1
                entity = Entity(
                    id=f"person_{entity_id}",
                    type="person",
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    confidence=0.75,
                    attributes={"role": "未知"}
                )
                entities.append(entity)
        
        return entities
    
    def _extract_locations(self, text: str) -> List[Entity]:
        """提取地点实体"""
        entities = []
        entity_id = 0
        
        for pattern in self.location_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entity_id += 1
                entity = Entity(
                    id=f"location_{entity_id}",
                    type="location",
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    confidence=0.8,
                    attributes={}
                )
                entities.append(entity)
        
        return entities
    
    def _extract_amounts(self, text: str) -> List[Entity]:
        """提取金额实体"""
        entities = []
        entity_id = 0
        
        for pattern in self.amount_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entity_id += 1
                full_match = match.group()
                # 提取数字部分
                num_match = re.search(r"(\d+(?:\.\d+)?)", full_match)
                if num_match:
                    amount = float(num_match.group())
                    entity = Entity(
                        id=f"amount_{entity_id}",
                        type="amount",
                        text=full_match,
                        start=match.start(),
                        end=match.end(),
                        confidence=0.9,
                        attributes={"value": amount, "unit": "元"}
                    )
                    entities.append(entity)
        
        return entities
    
    def _extract_times(self, text: str) -> List[Entity]:
        """提取时间实体"""
        entities = []
        entity_id = 0
        
        for pattern in self.time_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entity_id += 1
                entity = Entity(
                    id=f"time_{entity_id}",
                    type="time",
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    confidence=0.85,
                    attributes={}
                )
                entities.append(entity)
        
        return entities
    
    def _extract_organizations(self, text: str) -> List[Entity]:
        """提取机构实体"""
        entities = []
        entity_id = 0
        
        for pattern in self.organization_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entity_id += 1
                entity = Entity(
                    id=f"organization_{entity_id}",
                    type="organization",
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    confidence=0.7,
                    attributes={}
                )
                entities.append(entity)
        
        return entities
    
    def _extract_evidences(self, text: str) -> List[Entity]:
        """提取证据实体"""
        entities = []
        entity_id = 0
        
        for keyword in self.evidence_keywords:
            if keyword in text:
                start = 0
                while True:
                    start = text.find(keyword, start)
                    if start == -1:
                        break
                    entity_id += 1
                    entity = Entity(
                        id=f"evidence_{entity_id}",
                        type="evidence",
                        text=keyword,
                        start=start,
                        end=start + len(keyword),
                        confidence=0.8,
                        attributes={}
                    )
                    entities.append(entity)
                    start += len(keyword)
        
        return entities
    
    def _extract_actions(self, text: str) -> List[Entity]:
        """提取行为实体"""
        entities = []
        entity_id = 0
        
        for keyword in self.action_keywords:
            if keyword in text:
                start = 0
                while True:
                    start = text.find(keyword, start)
                    if start == -1:
                        break
                    entity_id += 1
                    entity = Entity(
                        id=f"action_{entity_id}",
                        type="action",
                        text=keyword,
                        start=start,
                        end=start + len(keyword),
                        confidence=0.75,
                        attributes={}
                    )
                    entities.append(entity)
                    start += len(keyword)
        
        return entities
    
    def _count_entities(self, entities: List[Entity]) -> Dict[str, int]:
        """统计各类实体数量"""
        counts = {}
        for entity in entities:
            entity_type = entity.type
            counts[entity_type] = counts.get(entity_type, 0) + 1
        return counts
    
    def _identify_key_entities(self, entities: List[Entity]) -> List[str]:
        """识别关键实体"""
        key_entities = []
        
        # 优先级排序: person > amount > time > location > organization > evidence > action
        priority = {
            "person": 1,
            "amount": 2,
            "time": 3,
            "location": 4,
            "organization": 5,
            "evidence": 6,
            "action": 7
        }
        
        # 按优先级和置信度排序
        sorted_entities = sorted(
            entities,
            key=lambda e: (priority.get(e.type, 99), -e.confidence)
        )
        
        # 选择前10个作为关键实体
        key_entities = [e.text for e in sorted_entities[:10]]
        
        return key_entities


def extract_entities(text: str) -> Dict[str, Any]:
    """
    便捷函数: 提取实体
    
    Args:
        text: 案件描述文本
    
    Returns:
        实体抽取结果字典
    """
    extractor = EntityExtractor()
    result = extractor.extract(text)
    
    return {
        "entities": [
            {
                "id": e.id,
                "type": e.type,
                "text": e.text,
                "start": e.start,
                "end": e.end,
                "confidence": e.confidence,
                "attributes": e.attributes
            }
            for e in result.entities
        ],
        "entity_counts": result.entity_counts,
        "key_entities": result.key_entities,
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
    
    result = extract_entities(test_text)
    print("实体抽取结果:")
    print(f"  实体总数: {len(result['entities'])}")
    print(f"  实体分布: {result['entity_counts']}")
    print(f"  关键实体: {result['key_entities']}")
    
    print("\n实体列表:")
    for entity in result['entities'][:10]:
        print(f"  • [{entity['type']}] {entity['text']} (置信度: {entity['confidence']:.2f})")
