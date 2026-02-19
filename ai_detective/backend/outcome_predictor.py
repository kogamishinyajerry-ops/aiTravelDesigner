"""
结果预测模块
Outcome Predictor

功能:
- 立案概率预测
- 诉讼胜算预测
- 补偿金额预测
- 综合风险评估
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class RiskLevel(Enum):
    """风险等级"""
    VERY_LOW = "极低"
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    VERY_HIGH = "极高"


@dataclass
class FilingPrediction:
    """立案预测"""
    probability: float  # 立案概率 (0-1)
    risk_level: RiskLevel
    key_factors: List[str]  # 关键影响因素
    blocking_factors: List[str]  # 阻碍因素
    recommendations: List[str]  # 建议
    confidence: float  # 置信度


@dataclass
class LitigationPrediction:
    """诉讼胜算预测"""
    win_probability: float  # 胜诉概率 (0-1)
    risk_level: RiskLevel
    expected_outcome: str  # 预期结果
    key_success_factors: List[str]  # 成功因素
    key_risk_factors: List[str]  # 风险因素
    similar_cases: List[Dict[str, Any]]  # 相似案例
    confidence: float


@dataclass
class CompensationPrediction:
    """补偿金额预测"""
    min_amount: float  # 最低金额
    likely_amount: float  # 可能金额
    max_amount: float  # 最高金额
    breakdown: Dict[str, float]  # 分项明细
    reasoning: str  # 推理说明
    confidence: float


@dataclass
class RiskAssessment:
    """风险评估"""
    overall_risk: RiskLevel
    filing_risk: RiskLevel  # 立案风险
    litigation_risk: RiskLevel  # 诉讼风险
    evidence_quality: float  # 证据质量 (0-1)
    strength_score: float  # 案件强度 (0-1)
    time_estimate: int  # 预计周期（天）
    success_probability: float  # 整体成功概率
    key_strengths: List[str]  # 关键优势
    key_weaknesses: List[str]  # 关键劣势
    recommendations: List[str]  # 建议


class OutcomePredictor:
    """结果预测器"""
    
    def __init__(self):
        self._initialize_filing_thresholds()
        self._initialize_compensation_standards()
    
    def _initialize_filing_thresholds(self):
        """初始化立案标准"""
        self.filing_standards = {
            "required_elements": {
                "民事案件": [
                    "明确的被告",
                    "具体的诉讼请求",
                    "事实和理由",
                    "属于法院受理范围"
                ],
                "刑事案件": [
                    "有犯罪事实",
                    "需要追究刑事责任",
                    "属于管辖范围"
                ],
                "行政案件": [
                    "具体的行政行为",
                    "合法权益受损",
                    "属于受案范围"
                ]
            },
            "evidence_quality_weights": {
                "直接证据": 0.9,
                "间接证据": 0.6,
                "证人证言": 0.7,
                "书证": 0.85,
                "物证": 0.8,
                "视听资料": 0.75
            }
        }
    
    def _initialize_compensation_standards(self):
        """初始化补偿标准"""
        self.compensation_standards = {
            "名誉权": {
                "min": 1000,
                "base": 3000,
                "max": 10000,
                "factors": ["影响范围", "持续时间", "损害程度"]
            },
            "隐私权": {
                "min": 500,
                "base": 2000,
                "max": 8000,
                "factors": ["信息敏感性", "扩散范围", "损害程度"]
            },
            "违约": {
                "min": 0,
                "base": 0,
                "max": 0,
                "factors": ["违约金额", "利息", "损失"]
            },
            "网络侵权": {
                "min": 1000,
                "base": 3000,
                "max": 15000,
                "factors": ["传播范围", "持续时间", "点击量"]
            }
        }
    
    def predict_filing(
        self,
        case_description: str,
        case_type: str = "民事案件",
        evidence_list: List[Dict[str, Any]] = None,
        context: Dict[str, Any] = None
    ) -> FilingPrediction:
        """预测立案概率"""
        
        # 计算立案概率
        probability = self._calculate_filing_probability(
            case_description,
            case_type,
            evidence_list,
            context
        )
        
        # 确定风险等级
        risk_level = self._determine_risk_level(probability)
        
        # 分析关键因素
        key_factors = self._analyze_filing_factors(
            case_description,
            evidence_list,
            positive=True
        )
        
        # 分析阻碍因素
        blocking_factors = self._analyze_filing_factors(
            case_description,
            evidence_list,
            positive=False
        )
        
        # 生成建议
        recommendations = self._generate_filing_recommendations(
            probability,
            blocking_factors
        )
        
        return FilingPrediction(
            probability=round(probability, 3),
            risk_level=risk_level,
            key_factors=key_factors,
            blocking_factors=blocking_factors,
            recommendations=recommendations,
            confidence=0.80
        )
    
    def predict_litigation(
        self,
        case_description: str,
        case_type: str = "民事案件",
        evidence_list: List[Dict[str, Any]] = None,
        similar_cases: List[Dict[str, Any]] = None,
        deep_analysis: Dict[str, Any] = None
    ) -> LitigationPrediction:
        """预测诉讼胜算"""
        
        # 计算胜诉概率
        win_probability = self._calculate_win_probability(
            case_description,
            case_type,
            evidence_list,
            similar_cases,
            deep_analysis
        )
        
        # 确定风险等级
        risk_level = self._determine_risk_level(win_probability)
        
        # 确定预期结果
        expected_outcome = self._determine_expected_outcome(win_probability)
        
        # 分析成功因素
        success_factors = self._analyze_success_factors(
            case_description,
            evidence_list,
            deep_analysis
        )
        
        # 分析风险因素
        risk_factors = self._analyze_risk_factors(
            case_description,
            evidence_list,
            deep_analysis
        )
        
        return LitigationPrediction(
            win_probability=round(win_probability, 3),
            risk_level=risk_level,
            expected_outcome=expected_outcome,
            key_success_factors=success_factors,
            key_risk_factors=risk_factors,
            similar_cases=similar_cases or [],
            confidence=0.75
        )
    
    def predict_compensation(
        self,
        case_type: str,
        actual_loss: float = 0,
        impact_scope: str = "local",
        duration_days: int = 30,
        additional_factors: Dict[str, float] = None
    ) -> CompensationPrediction:
        """预测补偿金额"""
        
        # 获取基础标准
        standard = self.compensation_standards.get(case_type, {
            "min": 1000, "base": 3000, "max": 10000,
            "factors": []
        })
        
        # 计算影响系数
        impact_factor = self._calculate_impact_factor(impact_scope)
        duration_factor = self._calculate_duration_factor(duration_days)
        
        # 计算分项明细
        breakdown = {
            "直接损失": actual_loss,
            "精神损害": standard["base"] * impact_factor * duration_factor,
            "维权成本": 2000,
            "利息损失": actual_loss * 0.05 if actual_loss > 0 else 0
        }
        
        # 添加额外因素
        if additional_factors:
            for factor, value in additional_factors.items():
                breakdown[factor] = value
        
        # 计算总金额
        total_amount = sum(breakdown.values())
        
        # 确定范围
        min_amount = total_amount * 0.7
        likely_amount = total_amount
        max_amount = total_amount * 1.3
        
        # 生成推理说明
        reasoning = self._generate_compensation_reasoning(
            case_type,
            actual_loss,
            impact_scope,
            duration_days,
            breakdown
        )
        
        return CompensationPrediction(
            min_amount=round(min_amount, 0),
            likely_amount=round(likely_amount, 0),
            max_amount=round(max_amount, 0),
            breakdown=breakdown,
            reasoning=reasoning,
            confidence=0.70
        )
    
    def assess_risk(
        self,
        case_description: str,
        filing_prediction: FilingPrediction = None,
        litigation_prediction: LitigationPrediction = None,
        compensation_prediction: CompensationPrediction = None,
        evidence_list: List[Dict[str, Any]] = None,
        deep_analysis: Dict[str, Any] = None
    ) -> RiskAssessment:
        """综合风险评估"""
        
        # 评估立案风险
        filing_risk = filing_prediction.risk_level if filing_prediction else RiskLevel.MEDIUM
        
        # 评估诉讼风险
        litigation_risk = litigation_prediction.risk_level if litigation_prediction else RiskLevel.MEDIUM
        
        # 评估证据质量
        evidence_quality = self._assess_evidence_quality(evidence_list or [])
        
        # 评估案件强度
        strength_score = self._calculate_strength_score(
            evidence_quality,
            litigation_prediction.win_probability if litigation_prediction else 0.5,
            deep_analysis
        )
        
        # 计算整体成功概率
        success_probability = (
            filing_prediction.probability if filing_prediction else 0.5
        ) * 0.4 + (
            litigation_prediction.win_probability if litigation_prediction else 0.5
        ) * 0.6
        
        # 确定整体风险
        overall_risk = self._determine_risk_level(success_probability)
        
        # 预计周期
        time_estimate = self._estimate_case_duration(
            case_description,
            success_probability
        )
        
        # 分析优势
        strengths = self._analyze_strengths(
            case_description,
            evidence_list,
            deep_analysis
        )
        
        # 分析劣势
        weaknesses = self._analyze_weaknesses(
            case_description,
            evidence_list,
            deep_analysis
        )
        
        # 生成建议
        recommendations = self._generate_risk_recommendations(
            overall_risk,
            filing_risk,
            litigation_risk,
            strengths,
            weaknesses
        )
        
        return RiskAssessment(
            overall_risk=overall_risk,
            filing_risk=filing_risk,
            litigation_risk=litigation_risk,
            evidence_quality=round(evidence_quality, 3),
            strength_score=round(strength_score, 3),
            time_estimate=time_estimate,
            success_probability=round(success_probability, 3),
            key_strengths=strengths,
            key_weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    # ============ 辅助方法 ============
    
    def _calculate_filing_probability(
        self,
        description: str,
        case_type: str,
        evidence_list: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> float:
        """计算立案概率"""
        probability = 0.5  # 基础概率
        
        # 检查基本要素
        required_elements = self.filing_standards["required_elements"].get(
            case_type, self.filing_standards["required_elements"]["民事案件"]
        )
        
        has_defendant = "被告" in description or "对方" in description
        has_claim = "要求" in description or "请求" in description
        has_reason = "因为" in description or "由于" in description
        
        if has_defendant:
            probability += 0.15
        if has_claim:
            probability += 0.15
        if has_reason:
            probability += 0.10
        
        # 证据加分
        if evidence_list and len(evidence_list) > 0:
            probability += 0.15
        
        # 限制在0-1之间
        return min(probability, 0.95)
    
    def _calculate_win_probability(
        self,
        description: str,
        case_type: str,
        evidence_list: List[Dict[str, Any]],
        similar_cases: List[Dict[str, Any]],
        deep_analysis: Dict[str, Any]
    ) -> float:
        """计算胜诉概率"""
        probability = 0.5  # 基础概率
        
        # 证据质量影响
        if evidence_list:
            strong_evidence = sum(1 for e in evidence_list if e.get("strength", 0.5) > 0.7)
            probability += (strong_evidence / max(len(evidence_list), 1)) * 0.2
        
        # 相似案例影响
        if similar_cases:
            win_cases = sum(1 for c in similar_cases if c.get("outcome") == "胜诉")
            if win_cases > 0:
                probability += 0.15
        
        # 深度分析影响
        if deep_analysis:
            # 预谋性分析
            if deep_analysis.get("premeditation", {}).get("is_premeditated", False):
                probability += 0.10
            
            # 惯犯分析
            if deep_analysis.get("habitual", {}).get("is_habitual_offender", False):
                probability += 0.10
            
            # 团伙分析
            if deep_analysis.get("group", {}).get("is_group_crime", False):
                probability -= 0.05
        
        # 限制在0-1之间
        return min(max(probability, 0.1), 0.95)
    
    def _calculate_impact_factor(self, impact_scope: str) -> float:
        """计算影响系数"""
        scope_factors = {
            "local": 0.8,
            "regional": 1.0,
            "national": 1.3,
            "international": 1.5
        }
        return scope_factors.get(impact_scope.lower(), 1.0)
    
    def _calculate_duration_factor(self, duration_days: int) -> float:
        """计算持续时间系数"""
        if duration_days < 7:
            return 0.5
        elif duration_days < 30:
            return 0.8
        elif duration_days < 90:
            return 1.0
        elif duration_days < 180:
            return 1.2
        else:
            return 1.5
    
    def _determine_risk_level(self, probability: float) -> RiskLevel:
        """确定风险等级"""
        if probability >= 0.9:
            return RiskLevel.VERY_LOW
        elif probability >= 0.75:
            return RiskLevel.LOW
        elif probability >= 0.5:
            return RiskLevel.MEDIUM
        elif probability >= 0.3:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def _determine_expected_outcome(self, win_probability: float) -> str:
        """确定预期结果"""
        if win_probability >= 0.8:
            return "胜诉可能性很高"
        elif win_probability >= 0.6:
            return "胜诉可能性较高"
        elif win_probability >= 0.4:
            return "胜败参半"
        elif win_probability >= 0.2:
            return "败诉可能性较高"
        else:
            return "败诉可能性很高"
    
    def _analyze_filing_factors(
        self,
        description: str,
        evidence_list: List[Dict[str, Any]],
        positive: bool
    ) -> List[str]:
        """分析立案因素"""
        factors = []
        
        if positive:
            if "被告" in description:
                factors.append("有明确被告")
            if "证据" in description or (evidence_list and len(evidence_list) > 0):
                factors.append("有相关证据")
            if "金额" in description or "赔偿" in description:
                factors.append("诉讼请求明确")
            if "事实" in description:
                factors.append("事实清楚")
        else:
            if "证据不足" in description or (not evidence_list or len(evidence_list) == 0):
                factors.append("证据可能不足")
            if "不清楚" in description:
                factors.append("事实不够清楚")
            if "可能" in description:
                factors.append("存在不确定性")
        
        return factors
    
    def _analyze_success_factors(
        self,
        description: str,
        evidence_list: List[Dict[str, Any]],
        deep_analysis: Dict[str, Any]
    ) -> List[str]:
        """分析成功因素"""
        factors = []
        
        if evidence_list and len(evidence_list) > 2:
            factors.append("证据充分")
        
        if "合同" in description or "协议" in description:
            factors.append("有合同依据")
        
        if deep_analysis:
            if deep_analysis.get("premeditation", {}).get("is_premeditated", False):
                factors.append("对方有明显恶意")
        
        return factors
    
    def _analyze_risk_factors(
        self,
        description: str,
        evidence_list: List[Dict[str, Any]],
        deep_analysis: Dict[str, Any]
    ) -> List[str]:
        """分析风险因素"""
        factors = []
        
        if not evidence_list or len(evidence_list) < 2:
            factors.append("证据不够充分")
        
        if "可能" in description or "不确定" in description:
            factors.append("存在不确定性")
        
        if deep_analysis:
            if deep_analysis.get("group", {}).get("is_group_crime", False):
                factors.append("对方可能存在团伙作案")
        
        return factors
    
    def _assess_evidence_quality(self, evidence_list: List[Dict[str, Any]]) -> float:
        """评估证据质量"""
        if not evidence_list or len(evidence_list) == 0:
            return 0.3
        
        total_quality = 0.0
        for evidence in evidence_list:
            strength = evidence.get("strength", 0.5)
            total_quality += strength
        
        return min(total_quality / len(evidence_list), 1.0)
    
    def _calculate_strength_score(
        self,
        evidence_quality: float,
        win_probability: float,
        deep_analysis: Dict[str, Any]
    ) -> float:
        """计算案件强度"""
        score = (evidence_quality * 0.4) + (win_probability * 0.4) + 0.2
        
        # 深度分析调整
        if deep_analysis:
            if deep_analysis.get("premeditation", {}).get("is_premeditated", False):
                score += 0.05
        
        return min(score, 1.0)
    
    def _estimate_case_duration(self, description: str, success_probability: float) -> int:
        """估算案件周期"""
        base_days = 90  # 基础周期3个月
        
        # 根据成功概率调整
        if success_probability > 0.8:
            base_days -= 15  # 快速解决
        elif success_probability < 0.5:
            base_days += 30  # 可能需要更长时间
        
        # 根据复杂度调整
        if "复杂" in description or "多次" in description:
            base_days += 30
        
        return min(max(base_days, 30), 365)  # 限制在1个月到1年之间
    
    def _analyze_strengths(
        self,
        description: str,
        evidence_list: List[Dict[str, Any]],
        deep_analysis: Dict[str, Any]
    ) -> List[str]:
        """分析优势"""
        strengths = []
        
        if evidence_list and len(evidence_list) > 2:
            strengths.append("证据数量充足")
        
        if "合同" in description:
            strengths.append("有合同等书面依据")
        
        if deep_analysis:
            if deep_analysis.get("premeditation", {}).get("is_premeditated", False):
                strengths.append("对方存在恶意预谋")
            if deep_analysis.get("habitual", {}).get("is_habitual_offender", False):
                strengths.append("对方可能是惯犯")
        
        return strengths
    
    def _analyze_weaknesses(
        self,
        description: str,
        evidence_list: List[Dict[str, Any]],
        deep_analysis: Dict[str, Any]
    ) -> List[str]:
        """分析劣势"""
        weaknesses = []
        
        if not evidence_list or len(evidence_list) < 2:
            weaknesses.append("证据数量不足")
        
        if "不确定" in description:
            weaknesses.append("事实不够明确")
        
        return weaknesses
    
    def _generate_filing_recommendations(
        self,
        probability: float,
        blocking_factors: List[str]
    ) -> List[str]:
        """生成立案建议"""
        recommendations = []
        
        if probability < 0.5:
            recommendations.append("建议补充更多证据后再立案")
        if probability < 0.7:
            recommendations.append("建议咨询专业律师")
        
        if "证据可能不足" in blocking_factors:
            recommendations.append("建议收集更多直接证据")
        
        return recommendations
    
    def _generate_compensation_reasoning(
        self,
        case_type: str,
        actual_loss: float,
        impact_scope: str,
        duration_days: int,
        breakdown: Dict[str, float]
    ) -> str:
        """生成补偿推理说明"""
        reasoning = f"根据{case_type}相关法律规定，"
        
        if actual_loss > 0:
            reasoning += f"直接损失{actual_loss:.0f}元，"
        
        if impact_scope != "local":
            reasoning += f"影响范围为{impact_scope}，"
        
        if duration_days > 30:
            reasoning += f"持续时间{duration_days}天，"
        
        reasoning += f"综合考虑各项因素，预计补偿金额为{sum(breakdown.values()):.0f}元。"
        
        return reasoning
    
    def _generate_risk_recommendations(
        self,
        overall_risk: RiskLevel,
        filing_risk: RiskLevel,
        litigation_risk: RiskLevel,
        strengths: List[str],
        weaknesses: List[str]
    ) -> List[str]:
        """生成风险建议"""
        recommendations = []
        
        if overall_risk in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]:
            recommendations.append("风险较高，建议谨慎决策")
        elif overall_risk == RiskLevel.MEDIUM:
            recommendations.append("存在一定风险，建议充分准备")
        else:
            recommendations.append("风险可控，可以积极维权")
        
        if weaknesses:
            recommendations.append(f"主要劣势: {', '.join(weaknesses[:2])}")
        
        if filing_risk != RiskLevel.LOW:
            recommendations.append("建议咨询律师优化立案材料")
        
        return recommendations


# ============ 测试代码 ============

if __name__ == "__main__":
    print("=" * 60)
    print("结果预测器 - 测试")
    print("=" * 60)
    
    predictor = OutcomePredictor()
    
    # 测试1: 立案概率预测
    print("\n1️⃣ 测试: 立案概率预测")
    print("-" * 40)
    case_desc = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。我有截图证据，要求赔偿损失。"
    evidence_list = [
        {"type": "截图", "strength": 0.8},
        {"type": "聊天记录", "strength": 0.7}
    ]
    
    filing_pred = predictor.predict_filing(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list
    )
    print(f"✅ 立案概率: {filing_pred.probability * 100:.1f}%")
    print(f"   风险等级: {filing_pred.risk_level.value}")
    print(f"   关键因素: {filing_pred.key_factors}")
    print(f"   建议: {filing_pred.recommendations}")
    
    # 测试2: 诉讼胜算预测
    print("\n2️⃣ 测试: 诉讼胜算预测")
    print("-" * 40)
    similar_cases = [
        {"outcome": "胜诉", "similarity": 0.8},
        {"outcome": "胜诉", "similarity": 0.7}
    ]
    
    litigation_pred = predictor.predict_litigation(
        case_description=case_desc,
        case_type="民事案件",
        evidence_list=evidence_list,
        similar_cases=similar_cases
    )
    print(f"✅ 胜诉概率: {litigation_pred.win_probability * 100:.1f}%")
    print(f"   预期结果: {litigation_pred.expected_outcome}")
    print(f"   成功因素: {litigation_pred.key_success_factors}")
    print(f"   风险因素: {litigation_pred.key_risk_factors}")
    
    # 测试3: 补偿金额预测
    print("\n3️⃣ 测试: 补偿金额预测")
    print("-" * 40)
    comp_pred = predictor.predict_compensation(
        case_type="名誉权",
        actual_loss=0,
        impact_scope="regional",
        duration_days=15
    )
    print(f"✅ 预估补偿: {comp_pred.min_amount:.0f} - {comp_pred.max_amount:.0f}元")
    print(f"   可能金额: {comp_pred.likely_amount:.0f}元")
    print(f"   分项明细: {comp_pred.breakdown}")
    
    # 测试4: 综合风险评估
    print("\n4️⃣ 测试: 综合风险评估")
    print("-" * 40)
    risk_assess = predictor.assess_risk(
        case_description=case_desc,
        filing_prediction=filing_pred,
        litigation_prediction=litigation_pred,
        compensation_prediction=comp_pred,
        evidence_list=evidence_list
    )
    print(f"✅ 整体风险: {risk_assess.overall_risk.value}")
    print(f"   立案风险: {risk_assess.filing_risk.value}")
    print(f"   诉讼风险: {risk_assess.litigation_risk.value}")
    print(f"   证据质量: {risk_assess.evidence_quality:.2f}")
    print(f"   案件强度: {risk_assess.strength_score:.2f}")
    print(f"   预计周期: {risk_assess.time_estimate}天")
    print(f"   成功概率: {risk_assess.success_probability * 100:.1f}%")
    print(f"   建议: {risk_assess.recommendations}")
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成!")
    print("=" * 60)
