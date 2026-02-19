"""
法律数据库查询模块
Legal Database Fetcher

功能:
- 模拟法律案例数据库查询（实际使用需要API接入）
- 相似案例检索
- 法律条文查询
- 判例分析
- 胜率预测数据
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
import json


class CaseType(Enum):
    """案件类型"""
    CIVIL = "民事案件"
    CRIMINAL = "刑事案件"
    ADMINISTRATIVE = "行政案件"
    ECONOMIC = "经济纠纷"
    CONSUMER = "消费者权益"
    INTERNET = "网络侵权"
    DEFAMATION = "诽谤造谣"
    FRAUD = "诈骗"


class CaseOutcome(Enum):
    """案件结果"""
    PLAINTIFF_WIN = "原告胜诉"
    DEFENDANT_WIN = "被告胜诉"
    SETTLEMENT = "调解"
    DISMISSED = "驳回"
    PENDING = "审理中"


@dataclass
class LegalCase:
    """法律案例"""
    case_id: str
    case_name: str
    case_type: CaseType
    case_outcome: CaseOutcome
    plaintiff: str
    defendant: str
    filing_date: datetime
    judgment_date: datetime
    court: str
    judge: str
    facts: str
    legal_issues: List[str]
    legal_basis: List[str]
    judgment: str
    compensation: float
    similarity_score: float = 0.0
    relevance_tags: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LegalProvision:
    """法律条文"""
    provision_id: str
    law_name: str
    article: str
    content: str
    applicable_scenarios: List[str]
    penalty: str = ""
    compensation_standard: str = ""
    relevance_score: float = 0.0


@dataclass
class CaseStatistics:
    """案件统计数据"""
    total_cases: int
    plaintiff_win_rate: float
    avg_compensation: float
    avg_case_duration_days: float
    common_outcomes: List[tuple]
    success_factors: List[str]
    risk_factors: List[str]


@dataclass
class QueryResult:
    """查询结果"""
    timestamp: datetime
    query: str
    query_type: str
    cases: List[LegalCase] = field(default_factory=list)
    provisions: List[LegalProvision] = field(default_factory=list)
    statistics: Optional[CaseStatistics] = None
    total_cases: int = 0
    total_provisions: int = 0
    confidence: float = 0.0
    error_message: str = ""


class LegalDatabaseFetcher:
    """法律数据库查询器"""
    
    def __init__(self):
        self._initialize_law_database()
        self._initialize_case_database()
        
    def _initialize_law_database(self):
        """初始化法律条文数据库"""
        self.law_database = {
            "民法典": {
                "名誉权": {
                    "article": "第1024条",
                    "content": "自然人享有名誉权。任何组织或者个人不得以侮辱、诽谤等方式侵害他人的名誉权。",
                    "penalty": "停止侵害、恢复名誉、消除影响、赔礼道歉、赔偿损失",
                    "compensation": "根据损害程度确定"
                },
                "隐私权": {
                    "article": "第1032条",
                    "content": "自然人享有隐私权。任何组织或者个人不得以刺探、侵扰、泄露、公开等方式侵害他人的隐私权。",
                    "penalty": "停止侵害、赔偿损失、赔礼道歉",
                    "compensation": "根据损害程度确定"
                },
                "违约责任": {
                    "article": "第577条",
                    "content": "当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。",
                    "penalty": "继续履行、赔偿损失、支付违约金",
                    "compensation": "实际损失+可预见的损失"
                }
            },
            "网络安全法": {
                "网络侵权": {
                    "article": "第12条",
                    "content": "任何个人和组织不得利用网络从事侵害他人名誉、隐私、知识产权等合法权益的活动。",
                    "penalty": "删除内容、道歉、赔偿损失",
                    "compensation": "根据损害程度确定"
                }
            },
            "刑法": {
                "诽谤罪": {
                    "article": "第246条",
                    "content": "以暴力或者其他方法公然侮辱他人或者捏造事实诽谤他人，情节严重的，处三年以下有期徒刑、拘役、管制或者剥夺政治权利。",
                    "penalty": "三年以下有期徒刑、拘役、管制或者剥夺政治权利",
                    "compensation": "刑事附带民事赔偿"
                },
                "诈骗罪": {
                    "article": "第266条",
                    "content": "诈骗公私财物，数额较大的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金；数额巨大或者有其他严重情节的，处三年以上十年以下有期徒刑，并处罚金。",
                    "penalty": "三年以下有期徒刑，并处罚金",
                    "compensation": "退赔赃款赃物"
                }
            }
        }
    
    def _initialize_case_database(self):
        """初始化案例数据库"""
        self.case_database = []
        self._generate_mock_cases()
    
    def _generate_mock_cases(self):
        """生成模拟案例"""
        mock_cases = [
            {
                "case_name": "张三诉李四名誉权纠纷案",
                "case_type": CaseType.DEFAMATION,
                "case_outcome": CaseOutcome.PLAINTIFF_WIN,
                "facts": "被告在社交媒体发布虚假信息，称原告存在欺诈行为，严重损害原告名誉。",
                "legal_issues": ["名誉权侵害", "虚假信息发布"],
                "legal_basis": ["民法典第1024条"],
                "judgment": "被告立即删除侵权内容，发布赔礼道歉声明，赔偿原告精神损失费2000元。",
                "compensation": 2000
            },
            {
                "case_name": "王某诉某网络平台隐私权纠纷案",
                "case_type": CaseType.INTERNET,
                "case_outcome": CaseOutcome.PLAINTIFF_WIN,
                "facts": "网络平台泄露用户个人信息，导致用户频繁受到骚扰。",
                "legal_issues": ["个人信息泄露", "隐私权侵害"],
                "legal_basis": ["民法典第1032条", "网络安全法第12条"],
                "judgment": "平台立即修复漏洞，删除泄露信息，赔偿原告5000元。",
                "compensation": 5000
            },
            {
                "case_name": "某消费者诉商家服务质量纠纷案",
                "case_type": CaseType.CONSUMER,
                "case_outcome": CaseOutcome.SETTLEMENT,
                "facts": "消费者购买服务后认为质量不符合约定，要求退款。",
                "legal_issues": ["服务质量", "合同履行"],
                "legal_basis": ["民法典第577条", "消费者权益保护法"],
                "judgment": "双方达成调解，商家退还部分款项。",
                "compensation": 800
            },
            {
                "case_name": "某公司诉员工名誉权纠纷案",
                "case_type": CaseType.DEFAMATION,
                "case_outcome": CaseOutcome.PLAINTIFF_WIN,
                "facts": "员工离职后在网络上散布公司虚假负面信息。",
                "legal_issues": ["商业诋毁", "名誉权侵害"],
                "legal_basis": ["民法典第1024条", "反不正当竞争法"],
                "judgment": "员工删除侵权内容，赔偿公司损失5000元。",
                "compensation": 5000
            },
            {
                "case_name": "张某诉购物平台消费纠纷案",
                "case_type": CaseType.CONSUMER,
                "case_outcome": CaseOutcome.DEFENDANT_WIN,
                "facts": "消费者指控平台存在欺诈行为，但证据不足。",
                "legal_issues": ["消费者权益", "欺诈认定"],
                "legal_basis": ["消费者权益保护法"],
                "judgment": "驳回原告全部诉讼请求。",
                "compensation": 0
            }
        ]
        
        for i, mock in enumerate(mock_cases):
            case = LegalCase(
                case_id=f"C{20240000 + i}",
                case_name=mock["case_name"],
                case_type=mock["case_type"],
                case_outcome=mock["case_outcome"],
                plaintiff="某原告",
                defendant="某被告",
                filing_date=datetime(2024, 1, i * 2 + 1),
                judgment_date=datetime(2024, 3, i * 2 + 1),
                court="某基层人民法院",
                judge="某法官",
                facts=mock["facts"],
                legal_issues=mock["legal_issues"],
                legal_basis=mock["legal_basis"],
                judgment=mock["judgment"],
                compensation=mock["compensation"]
            )
            self.case_database.append(case)
    
    def search_similar_cases(
        self,
        description: str,
        case_type: Optional[CaseType] = None,
        max_results: int = 5
    ) -> QueryResult:
        """搜索相似案例"""
        timestamp = datetime.now()
        
        # 计算相似度
        scored_cases = []
        for case in self.case_database:
            similarity = self._calculate_case_similarity(description, case)
            
            # 如果指定了案件类型，过滤
            if case_type and case.case_type != case_type:
                continue
                
            scored_cases.append((case, similarity))
        
        # 按相似度排序
        scored_cases.sort(key=lambda x: x[1], reverse=True)
        
        # 取前N个结果
        top_cases = scored_cases[:max_results]
        matched_cases = [case for case, score in top_cases]
        
        # 设置相似度分数
        for case, score in top_cases:
            case.similarity_score = score
        
        return QueryResult(
            timestamp=timestamp,
            query=description,
            query_type="similar_cases",
            cases=matched_cases,
            provisions=[],
            statistics=None,
            total_cases=len(matched_cases),
            confidence=0.80,
            error_message=""
        )
    
    def query_legal_provisions(
        self,
        keywords: List[str],
        max_results: int = 5
    ) -> QueryResult:
        """查询法律条文"""
        timestamp = datetime.now()
        
        provisions = []
        for law_name, law_content in self.law_database.items():
            for category, provision_data in law_content.items():
                # 检查关键词匹配
                content_lower = provision_data["content"].lower()
                category_lower = category.lower()
                
                match_score = 0.0
                matched_keywords = []
                
                for keyword in keywords:
                    if keyword.lower() in content_lower or keyword.lower() in category_lower:
                        match_score += 1.0
                        matched_keywords.append(keyword)
                
                if match_score > 0:
                    relevance_score = match_score / len(keywords)
                    
                    provision = LegalProvision(
                        provision_id=f"{law_name}_{category}",
                        law_name=law_name,
                        article=provision_data["article"],
                        content=provision_data["content"],
                        applicable_scenarios=matched_keywords,
                        penalty=provision_data.get("penalty", ""),
                        compensation_standard=provision_data.get("compensation", ""),
                        relevance_score=relevance_score
                    )
                    provisions.append(provision)
        
        # 按相关性排序
        provisions.sort(key=lambda p: p.relevance_score, reverse=True)
        top_provisions = provisions[:max_results]
        
        return QueryResult(
            timestamp=timestamp,
            query=",".join(keywords),
            query_type="legal_provisions",
            cases=[],
            provisions=top_provisions,
            statistics=None,
            total_provisions=len(top_provisions),
            confidence=0.85,
            error_message=""
        )
    
    def get_case_statistics(
        self,
        case_type: Optional[CaseType] = None
    ) -> QueryResult:
        """获取案件统计"""
        timestamp = datetime.now()
        
        # 过滤案件
        filtered_cases = self.case_database
        if case_type:
            filtered_cases = [c for c in self.case_database if c.case_type == case_type]
        
        if not filtered_cases:
            return QueryResult(
                timestamp=timestamp,
                query=case_type.value if case_type else "all",
                query_type="statistics",
                confidence=0.0,
                error_message="没有找到符合条件的案件"
            )
        
        # 计算统计数据
        total_cases = len(filtered_cases)
        plaintiff_wins = sum(1 for c in filtered_cases if c.case_outcome == CaseOutcome.PLAINTIFF_WIN)
        plaintiff_win_rate = plaintiff_wins / total_cases if total_cases > 0 else 0
        
        avg_compensation = sum(c.compensation for c in filtered_cases) / total_cases if total_cases > 0 else 0
        
        avg_duration = 60.0  # 模拟平均审理周期（天）
        
        # 常见结果
        outcome_counts = {}
        for case in filtered_cases:
            outcome = case.case_outcome
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        common_outcomes = sorted(outcome_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 成功因素
        success_factors = [
            "证据充分",
            "法律条文明确",
            "因果关系清晰",
            "损失可量化"
        ]
        
        # 风险因素
        risk_factors = [
            "证据不足",
            "因果关系模糊",
            "损害难以量化",
            "对方抗辩有力"
        ]
        
        statistics = CaseStatistics(
            total_cases=total_cases,
            plaintiff_win_rate=plaintiff_win_rate,
            avg_compensation=avg_compensation,
            avg_case_duration_days=avg_duration,
            common_outcomes=[(o.value, c) for o, c in common_outcomes],
            success_factors=success_factors,
            risk_factors=risk_factors
        )
        
        return QueryResult(
            timestamp=timestamp,
            query=case_type.value if case_type else "all",
            query_type="statistics",
            cases=[],
            provisions=[],
            statistics=statistics,
            total_cases=total_cases,
            confidence=0.75,
            error_message=""
        )
    
    def predict_outcome(
        self,
        description: str,
        case_type: Optional[CaseType] = None
    ) -> Dict[str, Any]:
        """预测案件结果"""
        prediction = {
            "win_probability": 0.0,
            "expected_outcome": "",
            "estimated_compensation": 0.0,
            "confidence": 0.0,
            "supporting_factors": [],
            "opposing_factors": [],
            "similar_cases": []
        }
        
        # 获取相似案例
        similar_result = self.search_similar_cases(description, case_type, max_results=5)
        
        if not similar_result.cases:
            return prediction
        
        # 计算胜率
        plaintiff_wins = sum(1 for c in similar_result.cases if c.case_outcome == CaseOutcome.PLAINTIFF_WIN)
        win_probability = plaintiff_wins / len(similar_result.cases)
        
        # 估算赔偿金额
        avg_compensation = sum(c.compensation for c in similar_result.cases) / len(similar_result.cases)
        
        # 确定预期结果
        if win_probability >= 0.7:
            expected_outcome = "胜诉可能性较高"
        elif win_probability >= 0.5:
            expected_outcome = "胜败参半"
        elif win_probability >= 0.3:
            expected_outcome = "败诉可能性较高"
        else:
            expected_outcome = "胜诉可能性较低"
        
        # 支持因素
        supporting_factors = []
        if win_probability > 0.5:
            supporting_factors.append("相似案例胜率较高")
            supporting_factors.append("法律条文明确")
        
        # 反对因素
        opposing_factors = []
        if win_probability < 0.5:
            opposing_factors.append("相似案例胜率较低")
            opposing_factors.append("可能存在证据不足")
        
        prediction = {
            "win_probability": round(win_probability * 100, 1),
            "expected_outcome": expected_outcome,
            "estimated_compensation": round(avg_compensation, 0),
            "confidence": round(similar_result.confidence * 100, 1),
            "supporting_factors": supporting_factors,
            "opposing_factors": opposing_factors,
            "similar_cases": [
                {
                    "case_name": c.case_name,
                    "outcome": c.case_outcome.value,
                    "compensation": c.compensation,
                    "similarity": round(c.similarity_score * 100, 1)
                }
                for c in similar_result.cases[:3]
            ]
        }
        
        return prediction
    
    def _calculate_case_similarity(self, description: str, case: LegalCase) -> float:
        """计算案例相似度"""
        score = 0.0
        desc_lower = description.lower()
        
        # 关键词匹配
        keywords = ["名誉", "侵权", "诽谤", "欺诈", "隐私", "平台", "社交媒体"]
        for keyword in keywords:
            if keyword in desc_lower and keyword in (case.facts + case.judgment).lower():
                score += 0.1
        
        # 法律问题匹配
        for issue in case.legal_issues:
            if issue.lower() in desc_lower:
                score += 0.2
        
        # 限制在0-1之间
        return min(score, 1.0)


# ============ 测试代码 ============

if __name__ == "__main__":
    print("=" * 60)
    print("法律数据库查询器 - 测试")
    print("=" * 60)
    
    fetcher = LegalDatabaseFetcher()
    
    # 测试1: 搜索相似案例
    print("\n1️⃣ 测试: 搜索相似案例")
    print("-" * 40)
    description = "对方在小红书发布虚假信息，称我店铺诈骗，损害我的名誉。"
    result1 = fetcher.search_similar_cases(description, CaseType.DEFAMATION, max_results=3)
    print(f"✅ 找到 {result1.total_cases} 个相似案例")
    for i, case in enumerate(result1.cases, 1):
        print(f"   {i}. {case.case_name} (相似度: {case.similarity_score:.2f})")
    
    # 测试2: 查询法律条文
    print("\n2️⃣ 测试: 查询法律条文")
    print("-" * 40)
    keywords = ["名誉", "侵权", "赔偿"]
    result2 = fetcher.query_legal_provisions(keywords, max_results=5)
    print(f"✅ 找到 {result2.total_provisions} 条相关法律")
    for i, provision in enumerate(result2.provisions, 1):
        print(f"   {i}. {provision.law_name} {provision.article}")
    
    # 测试3: 获取统计数据
    print("\n3️⃣ 测试: 获取案件统计")
    print("-" * 40)
    stats_result = fetcher.get_case_statistics(CaseType.DEFAMATION)
    if stats_result.statistics:
        stats = stats_result.statistics
        print(f"✅ 总案例数: {stats.total_cases}")
        print(f"   原告胜率: {stats.plaintiff_win_rate * 100:.1f}%")
        print(f"   平均赔偿: {stats.avg_compensation:.0f}元")
    
    # 测试4: 预测结果
    print("\n4️⃣ 测试: 预测案件结果")
    print("-" * 40)
    prediction = fetcher.predict_outcome(description, CaseType.DEFAMATION)
    print(f"✅ 胜诉概率: {prediction['win_probability']}%")
    print(f"   预期结果: {prediction['expected_outcome']}")
    print(f"   预估赔偿: {prediction['estimated_compensation']}元")
    print(f"   置信度: {prediction['confidence']}%")
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成!")
    print("=" * 60)
