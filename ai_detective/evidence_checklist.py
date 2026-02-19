"""
证据清单生成器
Evidence Checklist Generator

帮助用户快速整理和分类证据材料
"""

from datetime import datetime
from typing import List, Dict, Any


class EvidenceItem:
    """证据项"""
    def __init__(self, name: str, category: str, priority: str, 
                 source: str, description: str, status: str = "待收集"):
        self.name = name
        self.category = category  # 核心证据/辅助证据
        self.priority = priority  # 最高/高/中/低
        self.source = source  # 监控/证言/截图/记录
        self.description = description
        self.status = status  # 待收集/已收集/已验证
        self.collected_at = None
        self.notes = ""


class EvidenceChecklist:
    """证据清单"""
    
    def __init__(self, case_title: str):
        self.case_title = case_title
        self.created_at = datetime.now()
        self.evidences: List[EvidenceItem] = []
        
    def add_evidence(self, evidence: EvidenceItem):
        """添加证据"""
        self.evidences.append(evidence)
        
    def generate_checklist(self) -> Dict[str, Any]:
        """生成证据清单"""
        return {
            "case_title": self.case_title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "total_evidences": len(self.evidences),
            "collected_count": sum(1 for e in self.evidences if e.status == "已收集"),
            "pending_count": sum(1 for e in self.evidences if e.status == "待收集"),
            "evidences_by_priority": self._group_by_priority(),
            "evidences_by_category": self._group_by_category(),
            "all_evidences": [
                {
                    "name": e.name,
                    "category": e.category,
                    "priority": e.priority,
                    "source": e.source,
                    "description": e.description,
                    "status": e.status,
                    "collected_at": e.collected_at.strftime("%Y-%m-%d %H:%M:%S") if e.collected_at else None,
                    "notes": e.notes
                }
                for e in self.evidences
            ]
        }
    
    def _group_by_priority(self) -> Dict[str, List[str]]:
        """按优先级分组"""
        groups = {"最高": [], "高": [], "中": [], "低": []}
        for e in self.evidences:
            groups[e.priority].append(e.name)
        return groups
    
    def _group_by_category(self) -> Dict[str, List[str]]:
        """按类别分组"""
        groups = {"核心证据": [], "辅助证据": []}
        for e in self.evidences:
            groups[e.category].append(e.name)
        return groups
    
    def generate_report(self) -> str:
        """生成证据清单报告"""
        checklist = self.generate_checklist()
        
        report = f"""
{'=' * 70}
证据清单报告
{'=' * 70}

案件名称: {checklist['case_title']}
创建时间: {checklist['created_at']}
证据总数: {checklist['total_evidences']}
已收集: {checklist['collected_count']}  待收集: {checklist['pending_count']}

{'=' * 70}
一、按优先级分类
{'=' * 70}
"""
        
        for priority in ["最高", "高", "中", "低"]:
            evidences = checklist['evidences_by_priority'][priority]
            if evidences:
                report += f"\n【{priority}优先级】({len(evidences)}项)\n"
                for i, ev in enumerate(evidences, 1):
                    report += f"  {i}. {ev}\n"
        
        report += f"""
{'=' * 70}
二、按类别分类
{'=' * 70}
"""
        
        for category in ["核心证据", "辅助证据"]:
            evidences = checklist['evidences_by_category'][category]
            if evidences:
                report += f"\n【{category}】({len(evidences)}项)\n"
                for i, ev in enumerate(evidences, 1):
                    report += f"  {i}. {ev}\n"
        
        report += f"""
{'=' * 70}
三、证据详细清单
{'=' * 70}
"""
        
        for i, ev in enumerate(checklist['all_evidences'], 1):
            report += f"""
{i}. {ev['name']} 【{ev['priority']}】
   类别: {ev['category']}
   来源: {ev['source']}
   状态: {ev['status']}
   描述: {ev['description']}
"""
            if ev.get('notes'):
                report += f"   备注: {ev['notes']}\n"
        
        report += f"""
{'=' * 70}
四、待办事项
{'=' * 70}

"""
        
        pending = [e for e in checklist['all_evidences'] if e['status'] == '待收集']
        if pending:
            for i, ev in enumerate(pending, 1):
                report += f"{i}. 收集【{ev['name']}】\n"
                report += f"   来源: {ev['source']}\n"
                report += f"   说明: {ev['description']}\n\n"
        else:
            report += "✅ 所有证据已收集完成！\n"
        
        report += f"{'=' * 70}\n"
        
        return report


def create_anti_extortion_checklist() -> EvidenceChecklist:
    """创建碰瓷式维权案件的证据清单"""
    
    checklist = EvidenceChecklist("碰瓷式维权案件证据清单")
    
    # 🔴 最高优先级（必须准备）
    checklist.add_evidence(EvidenceItem(
        name="监控视频（冲突前1小时完整版）",
        category="核心证据",
        priority="最高",
        source="监控录像",
        description="记录对方在店内1小时的行为，重点包括：阻塞门口时长、反复试用、达成交易后反悔等画面。证明是非正常消费行为。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="证人证言（左右摊主书面）",
        category="核心证据",
        priority="最高",
        source="证人证言",
        description="证明：1)对方是否长时间阻塞通道？2)对方是否具有言语挑衅行为？3)你的愤怒是否属于长期骚扰后的应激反应？打破'孤立无援女性'人设。"
    ))
    
    # 🟡 高优先级（强烈建议）
    checklist.add_evidence(EvidenceItem(
        name="小红书发帖完整记录",
        category="核心证据",
        priority="高",
        source="社交媒体截图",
        description="包括：初版和编辑版对比、发布时间（6:47）、编辑记录、使用的红线关键词（诈骗、女性权益、中国警察）。证明是精准舆论引导。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="对方账号历史发帖记录",
        category="核心证据",
        priority="高",
        source="社交媒体调查",
        description="调查对方历史发帖，如果发现类似'维权成功'经历，即为惯犯证据。截图保存所有相关帖子。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="退款记录",
        category="核心证据",
        priority="高",
        source="支付平台记录",
        description="第一时间全额退款的截图或凭证，证明没有诈骗意图，推翻'诈骗'指控。"
    ))
    
    # 🟢 中优先级（辅助证据）
    checklist.add_evidence(EvidenceItem(
        name="行政处罚决定书",
        category="辅助证据",
        priority="中",
        source="行政机关",
        description="证明遭受实质损害，用于后续民事索赔的依据。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="停业通知/责令整改通知",
        category="辅助证据",
        priority="中",
        source="行政机关",
        description="证明停业事实和时间。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="过往营业额数据",
        category="辅助证据",
        priority="中",
        source="财务记录",
        description="证明停业期间的具体损失金额，为民事索赔计算依据。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="双方现场冲突视频",
        category="辅助证据",
        priority="中",
        source="监控录像",
        description="冲突发生时的视频，证明对方冷静表现、拍照取证等异常行为。"
    ))
    
    # 🟢 低优先级（补充证据）
    checklist.add_evidence(EvidenceItem(
        name="现场照片（对方在门口阻塞）",
        category="辅助证据",
        priority="低",
        source="拍摄照片",
        description="补充说明对方在店门口的具体行为。"
    ))
    
    checklist.add_evidence(EvidenceItem(
        name="110/12345报警记录",
        category="辅助证据",
        priority="低",
        source="报警系统",
        description="对方报警的记录，证明其在现场主动触发行政介入。"
    ))
    
    return checklist


if __name__ == "__main__":
    # 创建证据清单
    checklist = create_anti_extortion_checklist()
    
    # 生成报告
    report = checklist.generate_report()
    
    # 打印报告
    print(report)
    
    # 保存到文件
    with open("/workspace/ai_detective/evidence_checklist_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n✅ 证据清单报告已保存到: evidence_checklist_report.txt")
