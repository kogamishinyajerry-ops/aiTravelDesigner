"""
测试行为分析功能
Test Behavior Analysis
"""

import sys
import os

# 添加backend到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from premeditation_analyzer import PremeditationAnalyzer
from habitual_offender_detector import HabitualOffenderDetector
from group_analyzer import GroupAnalyzer


def test_premeditation_analysis():
    """测试预谋性分析"""
    print("=" * 60)
    print("测试预谋性分析")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    analyzer = PremeditationAnalyzer()
    result = analyzer.analyze(test_text)

    print(f"\n✅ 预谋性分析完成")
    print(f"  是否预谋: {result.is_premeditated}")
    print(f"  预谋得分: {result.premeditation_score:.2f}")
    print(f"  预谋等级: {result.premeditation_level}")
    print(f"  预谋指标数: {len(result.indicators)}")
    print(f"  行动路线: {' → '.join(result.action_route)}")
    print(f"\n推理说明:\n{result.reasoning}")

    assert result.is_premeditated == True
    assert result.premeditation_score >= 0.5
    print(f"\n✅ 预谋性分析测试通过!")


def test_habitual_offender_detection():
    """测试惯犯识别"""
    print("\n" + "=" * 60)
    print("测试惯犯识别")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    detector = HabitualOffenderDetector()
    result = detector.analyze(test_text)

    print(f"\n✅ 惯犯识别完成")
    print(f"  是否惯犯: {result.is_habitual_offender}")
    print(f"  惯犯概率: {result.offender_probability:.2f}")
    print(f"  惯犯等级: {result.offender_level}")
    print(f"  相似帖子数: {len(result.similar_posts)}")
    print(f"  作案手法数: {len(result.modus_operandi)}")
    print(f"\n推理说明:\n{result.reasoning}")

    assert len(result.similar_posts) >= 1
    assert len(result.modus_operandi) >= 1
    print(f"\n✅ 惯犯识别测试通过!")


def test_group_analysis():
    """测试团伙分析"""
    print("\n" + "=" * 60)
    print("测试团伙分析")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    analyzer = GroupAnalyzer()
    result = analyzer.analyze(test_text)

    print(f"\n✅ 团伙分析完成")
    print(f"  是否团伙作案: {result.is_group_crime}")
    print(f"  团伙概率: {result.group_probability:.2f}")
    print(f"  团伙人数: {result.group_size}")
    print(f"  关联关系数: {len(result.associations)}")
    print(f"\n推理说明:\n{result.reasoning}")

    print(f"\n✅ 团伙分析测试通过!")


def test_integrated_analysis():
    """测试集成分析"""
    print("\n" + "=" * 60)
    print("测试集成行为分析")
    print("=" * 60)

    test_text = """
    今年12月15日下午3点左右,一个女生来到我的店铺。
    她在店里待了大约1个小时,大概4点左右支付了400余元。
    支付后她立刻要求退款,双方发生争执。
    对方现场报警并拍照取证。
    晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。
    第二天,我收到了行政处罚。
    """

    # 初始化所有分析器
    premeditation_analyzer = PremeditationAnalyzer()
    habitual_offender_detector = HabitualOffenderDetector()
    group_analyzer = GroupAnalyzer()

    # 执行所有分析
    premeditation_result = premeditation_analyzer.analyze(test_text)
    habitual_result = habitual_offender_detector.analyze(test_text)
    group_result = group_analyzer.analyze(test_text)

    # 综合评估
    risk_score = 0.0
    key_findings = []

    if premeditation_result.is_premeditated:
        risk_score += 0.4
        key_findings.append("预谋性作案")
    if habitual_result.is_habitual_offender:
        risk_score += 0.4
        key_findings.append("疑似惯犯")
    if group_result.is_group_crime:
        risk_score += 0.2
        key_findings.append("团伙作案")

    # 确定风险等级
    if risk_score >= 0.8:
        risk_level = "极高"
    elif risk_score >= 0.5:
        risk_level = "高"
    elif risk_score >= 0.3:
        risk_level = "中"
    else:
        risk_level = "低"

    print(f"\n✅ 集成分析完成")
    print(f"  综合风险评分: {risk_score:.2f}")
    print(f"  风险等级: {risk_level}")
    print(f"  关键发现 ({len(key_findings)} 个):")
    for finding in key_findings:
        print(f"    • {finding}")

    print(f"\n✅ 集成分析测试通过!")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("开始测试行为分析功能")
    print("🚀" * 30)

    try:
        test_premeditation_analysis()
        test_habitual_offender_detection()
        test_group_analysis()
        test_integrated_analysis()

        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
