"""
测试结果预测模块
Test Outcome Prediction Module
"""

import sys
sys.path.insert(0, 'backend')

from outcome_predictor import OutcomePredictor, RiskLevel


def test_filing_prediction():
    """测试立案概率预测"""
    print("=" * 60)
    print("1️⃣ 立案概率预测测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    case_desc = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。我有截图证据，要求赔偿损失。"
    evidence_list = [
        {"type": "截图", "strength": 0.8},
        {"type": "聊天记录", "strength": 0.7},
        {"type": "交易记录", "strength": 0.9}
    ]
    
    result = predictor.predict_filing(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    
    print(f"\n✅ 立案概率: {result.probability * 100:.1f}%")
    print(f"   风险等级: {result.risk_level.value}")
    print(f"   关键因素: {', '.join(result.key_factors)}")
    print(f"   阻碍因素: {', '.join(result.blocking_factors) if result.blocking_factors else '无'}")
    print(f"   建议: {', '.join(result.recommendations) if result.recommendations else '无'}")
    print(f"   置信度: {result.confidence * 100:.1f}%")


def test_litigation_prediction():
    """测试诉讼胜算预测"""
    print("\n" + "=" * 60)
    print("2️⃣ 诉讼胜算预测测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    case_desc = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。"
    evidence_list = [
        {"type": "截图", "strength": 0.8},
        {"type": "聊天记录", "strength": 0.7}
    ]
    
    similar_cases = [
        {"case_name": "张三诉李四名誉权纠纷案", "outcome": "胜诉", "similarity": 0.8},
        {"case_name": "某公司诉员工名誉权纠纷案", "outcome": "胜诉", "similarity": 0.7}
    ]
    
    result = predictor.predict_litigation(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list,
        similar_cases=similar_cases
    )
    
    print(f"\n✅ 胜诉概率: {result.win_probability * 100:.1f}%")
    print(f"   风险等级: {result.risk_level.value}")
    print(f"   预期结果: {result.expected_outcome}")
    print(f"   成功因素: {', '.join(result.key_success_factors) if result.key_success_factors else '无'}")
    print(f"   风险因素: {', '.join(result.key_risk_factors) if result.key_risk_factors else '无'}")
    print(f"   置信度: {result.confidence * 100:.1f}%")


def test_compensation_prediction():
    """测试补偿金额预测"""
    print("\n" + "=" * 60)
    print("3️⃣ 补偿金额预测测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    result = predictor.predict_compensation(
        case_type="名誉权",
        actual_loss=0,
        impact_scope="regional",
        duration_days=15
    )
    
    print(f"\n✅ 预估补偿范围:")
    print(f"   最低: {result.min_amount:.0f}元")
    print(f"   可能: {result.likely_amount:.0f}元")
    print(f"   最高: {result.max_amount:.0f}元")
    print(f"\n   分项明细:")
    for item, amount in result.breakdown.items():
        print(f"   - {item}: {amount:.0f}元")
    print(f"\n   推理说明: {result.reasoning}")
    print(f"   置信度: {result.confidence * 100:.1f}%")


def test_risk_assessment():
    """测试综合风险评估"""
    print("\n" + "=" * 60)
    print("4️⃣ 综合风险评估测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    case_desc = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。我有充分证据。"
    evidence_list = [
        {"type": "截图", "strength": 0.9},
        {"type": "聊天记录", "strength": 0.8},
        {"type": "交易记录", "strength": 0.9}
    ]
    
    # 先获取各预测
    filing_pred = predictor.predict_filing(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    
    litigation_pred = predictor.predict_litigation(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    
    comp_pred = predictor.predict_compensation(
        case_type="名誉权",
        actual_loss=0,
        impact_scope="regional",
        duration_days=15
    )
    
    # 综合评估
    risk_assess = predictor.assess_risk(
        case_description=case_desc,
        filing_prediction=filing_pred,
        litigation_prediction=litigation_pred,
        compensation_prediction=comp_pred,
        evidence_list=evidence_list
    )
    
    print(f"\n✅ 综合风险评估:")
    print(f"   整体风险: {risk_assess.overall_risk.value}")
    print(f"   立案风险: {risk_assess.filing_risk.value}")
    print(f"   诉讼风险: {risk_assess.litigation_risk.value}")
    print(f"   证据质量: {risk_assess.evidence_quality * 100:.1f}%")
    print(f"   案件强度: {risk_assess.strength_score * 100:.1f}%")
    print(f"   预计周期: {risk_assess.time_estimate}天")
    print(f"   成功概率: {risk_assess.success_probability * 100:.1f}%")
    print(f"\n   关键优势:")
    for strength in risk_assess.key_strengths:
        print(f"   - {strength}")
    print(f"\n   关键劣势:")
    for weakness in risk_assess.key_weaknesses:
        print(f"   - {weakness}")
    print(f"\n   建议:")
    for rec in risk_assess.recommendations:
        print(f"   - {rec}")


def test_multiple_scenarios():
    """测试多种场景"""
    print("\n" + "=" * 60)
    print("5️⃣ 多场景测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    scenarios = [
        {
            "name": "名誉权侵权 - 证据充分",
            "desc": "对方在微博发布虚假信息损害名誉，有截图、聊天记录、证人证言等充分证据。"
        },
        {
            "name": "违约纠纷 - 证据不足",
            "desc": "对方未按合同履行义务，但缺乏书面合同，只有口头约定。"
        },
        {
            "name": "网络侵权 - 影响较大",
            "desc": "虚假信息在多个平台传播，持续时间较长，影响范围广泛。"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n【场景{i}: {scenario['name']}】")
        print("-" * 40)
        
        evidence = []
        if "充分" in scenario['name']:
            evidence = [
                {"type": "截图", "strength": 0.9},
                {"type": "聊天记录", "strength": 0.8},
                {"type": "证人证言", "strength": 0.7}
            ]
        elif "不足" in scenario['name']:
            evidence = [
                {"type": "口头约定", "strength": 0.4}
            ]
        elif "影响较大" in scenario['name']:
            evidence = [
                {"type": "截图", "strength": 0.8},
                {"type": "传播记录", "strength": 0.9}
            ]
        
        filing_pred = predictor.predict_filing(
            case_description=scenario['desc'],
            case_type="民事案件",
            evidence_list=evidence
        )
        
        litigation_pred = predictor.predict_litigation(
            case_description=scenario['desc'],
            case_type="民事案件",
            evidence_list=evidence
        )
        
        risk_assess = predictor.assess_risk(
            case_description=scenario['desc'],
            filing_prediction=filing_pred,
            litigation_prediction=litigation_pred,
            evidence_list=evidence
        )
        
        print(f"   立案概率: {filing_pred.probability * 100:.1f}% | "
              f"胜诉概率: {litigation_pred.win_probability * 100:.1f}% | "
              f"整体风险: {risk_assess.overall_risk.value}")


def test_integration():
    """集成测试"""
    print("\n" + "=" * 60)
    print("6️⃣ 集成测试 - 完整预测流程")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    case_desc = """
    对方在小红书发布虚假信息，称我店铺诈骗。
    2024年12月15日下午，对方来我店铺消费400余元，
    支付后立即要求退款，双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分，在小红书发布笔记称店铺诈骗。
    我有支付记录、现场照片、对方发布的小红书截图等证据。
    要求对方删除侵权内容、赔礼道歉、赔偿损失。
    """
    
    evidence_list = [
        {"type": "支付记录", "strength": 0.95},
        {"type": "现场照片", "strength": 0.85},
        {"type": "小红书截图", "strength": 0.90}
    ]
    
    print("\n📋 案件描述: 对方在小红书发布虚假信息称店铺诈骗...")
    
    # 1. 立案预测
    print("\n[步骤1] 立案概率预测...")
    filing_pred = predictor.predict_filing(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    print(f"✅ 立案概率: {filing_pred.probability * 100:.1f}%")
    
    # 2. 胜算预测
    print("\n[步骤2] 诉讼胜算预测...")
    litigation_pred = predictor.predict_litigation(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    print(f"✅ 胜诉概率: {litigation_pred.win_probability * 100:.1f}%")
    
    # 3. 补偿预测
    print("\n[步骤3] 补偿金额预测...")
    comp_pred = predictor.predict_compensation(
        case_type="名誉权",
        actual_loss=0,
        impact_scope="regional",
        duration_days=1
    )
    print(f"✅ 预估补偿: {comp_pred.min_amount:.0f} - {comp_pred.max_amount:.0f}元")
    
    # 4. 风险评估
    print("\n[步骤4] 综合风险评估...")
    risk_assess = predictor.assess_risk(
        case_description=case_desc,
        filing_prediction=filing_pred,
        litigation_prediction=litigation_pred,
        compensation_prediction=comp_pred,
        evidence_list=evidence_list
    )
    print(f"✅ 整体风险: {risk_assess.overall_risk.value}")
    print(f"   成功概率: {risk_assess.success_probability * 100:.1f}%")
    print(f"   预计周期: {risk_assess.time_estimate}天")
    
    print("\n✅ 集成测试完成!")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AI Detective - 结果预测模块测试")
    print("=" * 60)
    
    try:
        test_filing_prediction()
        test_litigation_prediction()
        test_compensation_prediction()
        test_risk_assessment()
        test_multiple_scenarios()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
