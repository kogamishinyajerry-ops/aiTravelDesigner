"""
测试深度推理整合
Test Deep Reasoning Integration
"""

import sys
import os

# 添加backend到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.deep_reasoner import DeepReasoner
from backend.reasoner_v3 import LegalReasonerV3


def test_deep_reasoner():
    """测试深度推理引擎"""
    print("=" * 60)
    print("测试深度推理引擎")
    print("=" * 60)

    # 测试案例: 小红书恶意发帖
    test_case = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    reasoner = DeepReasoner()
    result = reasoner.reason(test_case)

    print("\n【时间序列分析】")
    print(f"  时间戳数量: {result.time_analysis.get('timestamps_count', 0)}")
    print(f"  时间线: {result.time_analysis.get('timeline', {})}")
    print(f"  时间冲突: {len(result.time_analysis.get('time_conflicts', []))} 个")
    print(f"  逻辑有效性: {'✅' if result.time_analysis.get('logic_valid', False) else '❌'}")

    print("\n【因果关系分析】")
    print(f"  因果关系: {result.causal_analysis.get('relations_count', 0)} 个")
    print(f"  因果链: {result.causal_analysis.get('chains_count', 0)} 条")
    print(f"  因果缺口: {result.causal_analysis.get('gaps_count', 0)} 个")
    print(f"  根本原因: {result.causal_analysis.get('root_cause', '无')}")
    print(f"  根本原因置信度: {result.causal_analysis.get('root_cause_confidence', 0.0):.2f}")

    print("\n【矛盾检测】")
    print(f"  总矛盾数: {result.conflict_analysis.get('total_conflicts', 0)} 个")
    print(f"  事实矛盾: {len(result.conflict_analysis.get('fact_conflicts', []))} 个")
    print(f"  证据矛盾: {len(result.conflict_analysis.get('evidence_conflicts', []))} 个")

    print("\n【逻辑分析】")
    logic = result.logical_analysis
    print(f"  逻辑有效性: {'✅' if logic.get('logic_valid', False) else '❌'}")
    print(f"  逻辑一致性: {logic.get('logical_consistency', 0.0):.2f}")
    print(f"  逻辑完整性: {logic.get('logical_completeness', 0.0):.2f}")

    print("\n【预谋性分析】")
    premeditation = result.premeditation_analysis
    print(f"  是否预谋: {'✅ 是' if premeditation.get('is_premeditated', False) else '❌ 否'}")
    print(f"  预谋得分: {premeditation.get('premeditation_score', 0.0):.2f}")
    print(f"  预谋迹象: {len(premeditation.get('indicators', []))} 个")
    for indicator in premeditation.get('indicators', []):
        print(f"    • {indicator}")
    print(f"  推理: {premeditation.get('reasoning', '')}")

    print("\n【证据链分析】")
    evidence_chain = result.evidence_chain
    print(f"  完整度: {evidence_chain.get('completeness', 0.0):.2f}")
    print(f"  一致性: {evidence_chain.get('consistency', 0.0):.2f}")
    print(f"  强度: {evidence_chain.get('strength', 'weak')}")

    print("\n【建议】")
    for rec in result.recommendations:
        print(f"  {rec}")

    print(f"\n【整体置信度】: {result.confidence:.2f}")

    # 生成报告
    print("\n" + "=" * 60)
    print("深度推理报告")
    print("=" * 60)
    report = reasoner.generate_report(result)
    print(report)


def test_v3_reasoner():
    """测试V3推理器"""
    print("\n\n" + "=" * 60)
    print("测试V3推理器(网络侵权)")
    print("=" * 60)

    test_case = """
    未经本人同意,某互联网公司在2023年12月使用我的肖像照片
    用于商业广告宣传。照片是在朋友圈发布的个人照片,该公司未经我允许
    就下载并使用在他们的产品宣传中。我发现后联系该公司要求删除和道歉,
    但对方拒绝。我的肖像权受到了严重侵害。
    """

    reasoner = LegalReasonerV3()
    analysis = reasoner.analyze(test_case)

    print(f"\n【事实要素】提取到 {len(analysis.facts)} 个事实")
    for fact in analysis.facts[:5]:
        print(f"  • {fact.category}: {fact.description} (置信度: {fact.confidence:.2f})")

    print(f"\n【争议焦点】共 {len(analysis.dispute_focuses)} 个")
    for focus in analysis.dispute_focuses:
        print(f"  • {focus.main_issue}")

    print(f"\n【证据缺口】共 {len(analysis.evidence_gaps)} 个")
    for gap in analysis.evidence_gaps:
        print(f"  • {gap.missing_evidence} (重要性: {gap.importance})")

    print(f"\n【调查计划】")
    print(f"  优先任务: {len(analysis.investigation_plan.priority_tasks)} 个")
    for task in analysis.investigation_plan.priority_tasks[:3]:
        print(f"    • {task}")

    print(f"\n【诉讼策略】共 {len(analysis.litigation_strategy)} 项")
    for strategy in analysis.litigation_strategy[:3]:
        print(f"  • {strategy}")

    print(f"\n【置信度】: {analysis.confidence:.2f}")


def test_combined_analysis():
    """测试组合分析"""
    print("\n\n" + "=" * 60)
    print("测试组合分析(V3 + 深度推理)")
    print("=" * 60)

    test_case = """
    今年12月15日下午3点,一个女生来到我的店铺。
    她在店里待了大约1小时,4点支付400余元后立刻要求退款。
    双方发生争执,对方报警并拍照。
    当晚6点47分,她在小红书发布笔记诽谤店铺诈骗。
    第二天我收到行政处罚。
    """

    # V3分析
    v3_reasoner = LegalReasonerV3()
    v3_analysis = v3_reasoner.analyze(test_case)

    # 深度推理
    deep_reasoner = DeepReasoner()
    deep_analysis = deep_reasoner.reason(test_case)

    print("\n【V3分析】")
    print(f"  事实要素: {len(v3_analysis.facts)} 个")
    print(f"  争议焦点: {len(v3_analysis.dispute_focuses)} 个")
    print(f"  证据缺口: {len(v3_analysis.evidence_gaps)} 个")
    print(f"  置信度: {v3_analysis.confidence:.2f}")

    print("\n【深度推理】")
    print(f"  时间戳: {deep_analysis.time_analysis.get('timestamps_count', 0)} 个")
    print(f"  因果关系: {deep_analysis.causal_analysis.get('relations_count', 0)} 个")
    print(f"  矛盾数: {deep_analysis.conflict_analysis.get('total_conflicts', 0)} 个")
    print(f"  预谋得分: {deep_analysis.premeditation_analysis.get('premeditation_score', 0.0):.2f}")
    print(f"  置信度: {deep_analysis.confidence:.2f}")

    print("\n【综合分析】")
    combined_confidence = (v3_analysis.confidence + deep_analysis.confidence) / 2
    print(f"  综合置信度: {combined_confidence:.2f}")

    # 关键发现
    print("\n【关键发现】")
    if deep_analysis.premeditation_analysis.get('is_premeditated'):
        print("  ⚠️ 检测到预谋性特征")
    if deep_analysis.conflict_analysis.get('total_conflicts', 0) > 0:
        print(f"  ⚠️ 发现 {deep_analysis.conflict_analysis['total_conflicts']} 个矛盾")
    if deep_analysis.causal_analysis.get('gaps_count', 0) > 0:
        print(f"  ⚠️ 存在 {deep_analysis.causal_analysis['gaps_count']} 个因果链缺口")


if __name__ == "__main__":
    test_deep_reasoner()
    test_v3_reasoner()
    test_combined_analysis()

    print("\n" + "=" * 60)
    print("✅ 所有测试完成!")
    print("=" * 60)
