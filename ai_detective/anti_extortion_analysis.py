"""
碰瓷式维权案件深度分析
Anti-Extortion Case Deep Analysis

基于AI Detective系统，针对"碰瓷式维权"案件的深度分析
"""

import sys
sys.path.insert(0, 'backend')

from outcome_predictor import OutcomePredictor
from premeditation_analyzer import PremeditationAnalyzer
from habitual_offender_detector import HabitualOffenderDetector


def analyze_extortion_case():
    """分析碰瓷式维权案件"""
    
    # 案件描述（基于用户提供的信息）
    case_description = """
    对方是一名女性游客，在12月15日下午来到我的豫园店铺。
    她在店内缠斗约60分钟，反复议价、长时间试用、阻塞门口。
    1小时后支付400余元完成交易。
    支付后立刻要求额外赠品或二次砍价（这是"爆破期"）。
    我拒绝后，对方激烈反应，我被迫退款并言语冲突。
    对方现场报警、拍照取证，表现得异常冷静。
    次日清晨6:47（社交媒体算法早高峰），在小红书发布笔记，
    使用"诈骗"、"女性权益"、"中国警察"等敏感关键词，
    精准引导舆论，导致我收到行政处罚、店铺停业。
    
    对方行为异常：
    1. 面对愤怒男性商户不躲避，反而冷静拍照报警
    2. 选取"年末、豫园、清晨6:47"三个关键节点
    3. 使用标签化、红线关键词的文案
    4. 时间线高度协同，符合预设剧本
    """

    print("=" * 70)
    print("🔍 碰瓷式维权案件 - 深度分析报告")
    print("=" * 70)

    # ========== 第一部分：预谋性分析 ==========
    print("\n" + "=" * 70)
    print("1️⃣ 预谋性分析")
    print("=" * 70)

    premeditation_analyzer = PremeditationAnalyzer()
    premeditation_result = premeditation_analyzer.analyze(
        text=case_description
    )

    print(f"\n✅ 预谋性判断: {'是' if premeditation_result.is_premeditated else '否'}")
    print(f"   预谋得分: {premeditation_result.premeditation_score:.2f} / 1.0")
    print(f"   预谋等级: {premeditation_result.premeditation_level}")

    print(f"\n   预谋性指标:")
    for indicator in premeditation_result.indicators:
        print(f"   - {indicator.indicator_type}: {indicator.description}")
        print(f"     置信度: {indicator.confidence:.2f}")
        print(f"     证据: {indicator.evidence[:50]}...")

    print(f"\n   行为模式: {premeditation_result.behavior_pattern}")
    print(f"   行动路线: {premeditation_result.action_route}")
    print(f"   推理说明: {premeditation_result.reasoning}")

    # ========== 第二部分：惯犯识别 ==========
    print("\n" + "=" * 70)
    print("2️⃣ 惯犯识别")
    print("=" * 70)

    habitual_detector = HabitualOffenderDetector()
    habitual_result = habitual_detector.analyze(
        text=case_description
    )

    print(f"\n✅ 惯犯判断: {'是' if habitual_result.is_habitual_offender else '否'}")
    print(f"   惯犯概率: {habitual_result.offender_probability:.2f} / 1.0")
    print(f"   惯犯等级: {habitual_result.offender_level}")

    print(f"\n   行为模式:")
    for pattern, value in habitual_result.behavior_patterns.items():
        print(f"   - {pattern}: {value}")

    print(f"\n   作案手法:")
    for mo in habitual_result.modus_operandi:
        print(f"   - {mo}")

    print(f"\n   历史证据:")
    for evidence in habitual_result.historical_evidence:
        print(f"   - {evidence}")

    print(f"\n   推理说明: {habitual_result.reasoning}")

    # ========== 第三部分：立案概率预测 ==========
    print("\n" + "=" * 70)
    print("3️⃣ 立案概率预测")
    print("=" * 70)

    predictor = OutcomePredictor()

    evidence_list = [
        {"type": "监控视频（冲突前1小时）", "strength": 0.95, "description": "证明对方阻塞门口、反复骚扰"},
        {"type": "证人证言（左右摊主）", "strength": 0.85, "description": "证明对方长时间滋扰"},
        {"type": "小红书发帖记录", "strength": 0.90, "description": "证明对方预谋舆论引导"},
        {"type": "退款记录", "strength": 0.95, "description": "证明没有诈骗意图"},
        {"type": "行政处罚书", "strength": 0.90, "description": "证明遭受实质损害"},
        {"type": "对方发帖时间分析", "strength": 0.85, "description": "证明6:47是精心选择的时间点"}
    ]

    filing_pred = predictor.predict_filing(
        case_description=case_description,
        case_type="民事案件",
        evidence_list=evidence_list
    )

    print(f"\n✅ 立案概率: {filing_pred.probability * 100:.1f}%")
    print(f"   风险等级: {filing_pred.risk_level.value}")
    print(f"   置信度: {filing_pred.confidence * 100:.1f}%")

    print(f"\n   关键因素（支持立案）:")
    for factor in filing_pred.key_factors:
        print(f"   ✓ {factor}")

    print(f"\n   阻碍因素（需克服）:")
    if filing_pred.blocking_factors:
        for factor in filing_pred.blocking_factors:
            print(f"   ✗ {factor}")
    else:
        print(f"   无明显阻碍因素")

    print(f"\n   建议:")
    for rec in filing_pred.recommendations:
        print(f"   - {rec}")

    # ========== 第四部分：诉讼胜算预测 ==========
    print("\n" + "=" * 70)
    print("4️⃣ 诉讼胜算预测")
    print("=" * 70)

    litigation_pred = predictor.predict_litigation(
        case_description=case_description,
        case_type="民事案件",
        evidence_list=evidence_list
    )

    print(f"\n✅ 胜诉概率: {litigation_pred.win_probability * 100:.1f}%")
    print(f"   风险等级: {litigation_pred.risk_level.value}")
    print(f"   预期结果: {litigation_pred.expected_outcome}")
    print(f"   置信度: {litigation_pred.confidence * 100:.1f}%")

    print(f"\n   成功因素:")
    for factor in litigation_pred.key_success_factors:
        print(f"   ✓ {factor}")

    print(f"\n   风险因素:")
    if litigation_pred.key_risk_factors:
        for factor in litigation_pred.key_risk_factors:
            print(f"   ⚠ {factor}")
    else:
        print(f"   无明显风险因素")

    # ========== 第五部分：补偿金额预测 ==========
    print("\n" + "=" * 70)
    print("5️⃣ 补偿金额预测")
    print("=" * 70)

    comp_pred = predictor.predict_compensation(
        case_type="名誉权",
        actual_loss=0,  # 需要用户提供具体损失数据
        impact_scope="regional",  # 豫园地区
        duration_days=1  # 持续1天
    )

    print(f"\n✅ 预估补偿范围:")
    print(f"   最低: {comp_pred.min_amount:.0f}元")
    print(f"   可能: {comp_pred.likely_amount:.0f}元")
    print(f"   最高: {comp_pred.max_amount:.0f}元")
    print(f"   置信度: {comp_pred.confidence * 100:.1f}%")

    print(f"\n   分项明细:")
    for item, amount in comp_pred.breakdown.items():
        print(f"   - {item}: {amount:.0f}元")

    print(f"\n   推理说明:")
    print(f"   {comp_pred.reasoning}")

    # ========== 第六部分：综合风险评估 ==========
    print("\n" + "=" * 70)
    print("6️⃣ 综合风险评估")
    print("=" * 70)

    risk_assess = predictor.assess_risk(
        case_description=case_description,
        filing_prediction=filing_pred,
        litigation_prediction=litigation_pred,
        compensation_prediction=comp_pred,
        evidence_list=evidence_list
    )

    print(f"\n✅ 整体风险: {risk_assess.overall_risk.value}")
    print(f"   立案风险: {risk_assess.filing_risk.value}")
    print(f"   诉讼风险: {risk_assess.litigation_risk.value}")
    print(f"   证据质量: {risk_assess.evidence_quality * 100:.1f}%")
    print(f"   案件强度: {risk_assess.strength_score * 100:.1f}%")
    print(f"   预计周期: {risk_assess.time_estimate}天")
    print(f"   整体成功概率: {risk_assess.success_probability * 100:.1f}%")

    print(f"\n   关键优势:")
    for strength in risk_assess.key_strengths:
        print(f"   ✓ {strength}")

    print(f"\n   关键劣势:")
    for weakness in risk_assess.key_weaknesses:
        print(f"   ✗ {weakness}")

    print(f"\n   建议:")
    for rec in risk_assess.recommendations:
        print(f"   - {rec}")

    # ========== 第七部分：反击策略建议 ==========
    print("\n" + "=" * 70)
    print("7️⃣ 反击策略建议")
    print("=" * 70)

    print("\n【核心策略】")
    print("""
    不要站在政府的对立面，而是要表明：
    "我坚决支持政府整治营商环境，但我也是受害者。
    对方通过'软暴力'诱发冲突，利用虚假舆论绑架行政决策。
    政府被蒙蔽了，我是来帮政府纠偏的。"
    """)

    print("\n【证据清单优先级】")
    print("""
    🔴 最高优先级（必须准备）:
    1. 监控视频 - 冲突前1小时的完整视频
       - 重点标注：对方阻塞门口的时长（具体分钟数）
       - 动作回溯：反复翻找、试用、交易后反悔的画面
       - 证明这是"非正常消费行为"

    2. 证人证言 - 左右摊主书面证言
       - 证明：对方是否长时间阻塞通道？
       - 证明：对方是否具有言语挑衅行为？
       - 证明：你的愤怒是否属于被长期骚扰后的应激反应？
       - 作用：打破"孤立无援女性"人设，证明她是"滋扰者"

    🟡 高优先级（强烈建议）:
    3. 小红书发帖记录
       - 初版和编辑版对比（6:47编辑记录）
       - 精确使用的"红线关键词"
       - 证明这是"精准舆论引导"

    4. 对方账号画像
       - 历史发帖记录
       - 如果有类似"维权成功"经历 → 惯犯证据

    5. 退款记录
       - 证明第一时间全额退款
       - 推翻"诈骗"指控

    🟢 中优先级（辅助证据）:
    6. 行政处罚书、停业通知
       - 证明遭受实质损害

    7. 过往营业额数据
       - 证明停业期间损失金额
    """)

    print("\n【法律文书策略】")
    print("""
    针对小红书内容的逐句分析（需要对方发帖的完整文本）：

    1. 诽谤指控（无中生有）
       - "诈骗" - 需要证明：已完成交易、全额退款
       - 任何虚假事实陈述

    2. 公然侮辱
       - 任何贬损人格的描述

    3. 虚假宣传
       - 歪曲事实、夸大描述

    4. 申请撤销行政处罚的突破口
       - 证明对方存在"软暴力"行为
       - 证明行政决策基于虚假信息
       - 证明自己是被误导的受害者
    """)

    print("\n【时间线对比分析】")
    print("""
    对方时间线 vs 正常消费者时间线:

    碰瓷式维权者:
    0-60min: 缠斗、骚扰（反常）
    60min: 支付（确立消费者身份）
    立刻: 要求额外赠品/砍价（制造冲突）
    冲突时: 冷静拍照报警（异常心理素质）
    次日6:47: 精准时间发帖（算法黄金点）

    正常消费者:
    5-15min: 浏览、询问、购买
    如不满意: 直接离开或温和协商
    遇到冲突: 惊慌、躲避、寻求帮助
    如发帖: 当天随机时间，无精准关键词
    """)

    print("\n【下一步行动】")
    print("""
    1. 立即行动:
       ✓ 调取监控视频（冲突前1小时）
       ✓ 联系左右摊主获取证言
       ✓ 截取对方小红书发帖内容

    2. 短期准备（1-3天）:
       ✓ 整理所有证据清单
       ✓ 撰写"行政复议申请书"
       ✓ 准备"民事起诉状"

    3. 中期准备（1周内）:
       ✓ 调查对方历史发帖
       ✓ 评估具体经济损失
       ✓ 咨询专业律师

    4. AI辅助分析:
       - 将对方小红书发帖内容发给我
       - 我将逐句分析其违法点
       - 生成专业的法律分析报告
    """)

    print("\n" + "=" * 70)
    print("📊 分析总结")
    print("=" * 70)

    summary = f"""
    案件类型: 碰瓷式维权 / 软暴力诱导冲突

    核心判断:
    • 预谋性: {'是' if premeditation_result.is_premeditated else '否'} (得分: {premeditation_result.premeditation_score:.2f})
    • 惯犯嫌疑: {'是' if habitual_result.is_habitual_offender else '否'} (概率: {habitual_result.offender_probability:.2f})
    • 立案概率: {filing_pred.probability * 100:.1f}%
    • 胜诉概率: {litigation_pred.win_probability * 100:.1f}%
    • 预估补偿: {comp_pred.likely_amount:.0f}元
    • 整体成功概率: {risk_assess.success_probability * 100:.1f}%

    关键优势:
    • 对方行为高度预谋，有明显"剧本"痕迹
    • 证据质量高 ({risk_assess.evidence_quality * 100:.1f}%)
    • 案件强度较高 ({risk_assess.strength_score * 100:.1f}%)
    • 有多个独立证据相互印证

    核心建议:
    {'积极维权，胜诉可能性很高' if risk_assess.success_probability > 0.7 else '谨慎决策，需要充分准备'}

    预计案件周期: {risk_assess.time_estimate}天
    """

    print(summary)


if __name__ == "__main__":
    analyze_extortion_case()
