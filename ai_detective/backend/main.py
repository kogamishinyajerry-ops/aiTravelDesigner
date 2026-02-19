"""
AI 侦探 - FastAPI 主应用
AI Detective Main Application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from conversation import ConversationManager
from reasoner import LegalReasoner
from reasoner_v3 import LegalReasonerV3
from deep_reasoner import DeepReasoner
from premeditation_analyzer import PremeditationAnalyzer
from habitual_offender_detector import HabitualOffenderDetector
from group_analyzer import GroupAnalyzer
from social_media_fetcher import SocialMediaFetcher, Platform
from legal_database_fetcher import LegalDatabaseFetcher, CaseType
from multimedia_analyzer import MultimediaAnalyzer
from outcome_predictor import OutcomePredictor
from generator import DocumentGenerator
from evidence import EvidenceAnalyzer, EvidenceType, Evidence, Validity


app = FastAPI(
    title="AI 侦探 API",
    description="基于法律推理的纠纷分析和报案材料生成系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心模块
conversation_manager = ConversationManager()
legal_reasoner = LegalReasoner()
legal_reasoner_v3 = LegalReasonerV3()  # V3版本支持网络侵权
deep_reasoner = DeepReasoner()  # 深度推理引擎
premeditation_analyzer = PremeditationAnalyzer()  # 预谋性分析
habitual_offender_detector = HabitualOffenderDetector()  # 惯犯识别
group_analyzer = GroupAnalyzer()  # 团伙分析
social_media_fetcher = SocialMediaFetcher()  # 社交媒体数据获取
legal_database_fetcher = LegalDatabaseFetcher()  # 法律数据库查询
multimedia_analyzer = MultimediaAnalyzer()  # 多媒体分析
outcome_predictor = OutcomePredictor()  # 结果预测
document_generator = DocumentGenerator()
evidence_analyzer = EvidenceAnalyzer()


# ===== 数据模型 =====

class Message(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class CreateSessionResponse(BaseModel):
    session_id: str
    created_at: str


class AnalyzeRequest(BaseModel):
    description: str
    context: Optional[Dict[str, Any]] = None
    use_deep_reasoning: bool = False  # 是否使用深度推理
    use_v3: bool = True  # 是否使用V3推理器(支持网络侵权)
    analyze_premeditation: bool = False  # 是否分析预谋性
    analyze_habitual: bool = False  # 是否识别惯犯
    analyze_group: bool = False  # 是否分析团伙


class UserInfo(BaseModel):
    name: str = ""
    phone: str = ""
    address: str = ""
    id_number: str = ""
    gender: str = ""
    ethnicity: str = ""
    birth_date: str = ""
    zip_code: str = ""


class GenerateDocumentsRequest(BaseModel):
    description: str
    user_info: UserInfo
    session_id: Optional[str] = None


class EvidenceRequest(BaseModel):
    evidences: List[Dict[str, Any]]
    case_type: str


# ===== API 端点 =====

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 侦探 API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/session/create", response_model=CreateSessionResponse)
async def create_session():
    """创建新的对话会话"""
    session_id = conversation_manager.create_session()
    return CreateSessionResponse(
        session_id=session_id,
        created_at=datetime.now().isoformat()
    )


@app.post("/session/{session_id}/message")
async def add_message(session_id: str, message: Message):
    """添加消息到会话"""
    try:
        conversation_manager.add_message(
            session_id=session_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata
        )
        return {"status": "success", "message": "消息已添加"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """获取会话信息"""
    session = conversation_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    return {
        "session_id": session.session_id,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat(),
        "message_count": len(session.messages),
        "context": session.context,
        "case_info": session.case_info
    }


@app.get("/session/{session_id}/messages")
async def get_messages(session_id: str, last_n: Optional[int] = None):
    """获取消息历史"""
    messages = conversation_manager.get_messages(session_id, last_n)
    return {
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            }
            for msg in messages
        ]
    }


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_case(request: AnalyzeRequest):
    """分析案件"""
    try:
        # 选择推理器
        reasoner = legal_reasoner_v3 if request.use_v3 else legal_reasoner
        
        # 执行法律推理
        analysis = reasoner.analyze(
            description=request.description,
            context=request.context or {}
        )

        # 基础响应
        response = {
            "facts": [
                {
                    "id": fact.id,
                    "description": fact.description,
                    "category": fact.category,
                    "confidence": fact.confidence
                }
                for fact in analysis.facts
            ],
            "legal_relations": [
                {
                    "type": relation.type,
                    "parties": relation.parties,
                    "subject": relation.subject,
                    "content": relation.content
                }
                for relation in analysis.legal_relations
            ],
            "applicable_laws": analysis.applicable_laws,
            "liability": {
                "liable_party": analysis.liability.liable_party if analysis.liability else None,
                "liability_type": analysis.liability.liability_type if analysis.liability else None,
                "basis": analysis.liability.basis if analysis.liability else None,
                "severity": analysis.liability.severity if analysis.liability else None,
                "damages": analysis.liability.damages if analysis.liability else None
            } if analysis.liability else None,
            "risk_assessment": analysis.risk_assessment,
            "suggestions": analysis.suggestions,
            "confidence": analysis.confidence,
            "created_at": analysis.created_at.isoformat()
        }

        # 如果使用V3推理器,添加V3特有字段
        if request.use_v3 and hasattr(analysis, 'dispute_focuses'):
            response["dispute_focuses"] = [
                {
                    "main_issue": df.main_issue,
                    "details": df.details,
                    "facts_support": df.facts_support,
                    "critical_evidence": df.critical_evidence
                }
                for df in analysis.dispute_focuses
            ]
            response["evidence_gaps"] = [
                {
                    "missing_evidence": eg.missing_evidence,
                    "importance": eg.importance,
                    "how_to_obtain": eg.how_to_obtain,
                    "estimated_difficulty": eg.estimated_difficulty
                }
                for eg in analysis.evidence_gaps
            ]
            response["investigation_plan"] = {
                "priority_tasks": analysis.investigation_plan.priority_tasks,
                "secondary_tasks": analysis.investigation_plan.secondary_tasks,
                "optional_tasks": analysis.investigation_plan.optional_tasks
            }
            response["litigation_strategy"] = analysis.litigation_strategy
            response["evidence_recommendations"] = analysis.evidence_recommendations

        # 如果启用深度推理,执行深度分析
        if request.use_deep_reasoning:
            from evidence import Evidence
            # 创建空证据列表(可根据需要从context中获取)
            evidences = []
            
            # 执行深度推理
            deep_result = deep_reasoner.reason(
                text=request.description,
                evidences=evidences,
                context=request.context or {}
            )

            # 添加深度推理结果
            response["deep_reasoning"] = {
                "time_analysis": deep_result.time_analysis,
                "causal_analysis": deep_result.causal_analysis,
                "conflict_analysis": deep_result.conflict_analysis,
                "logical_analysis": deep_result.logical_analysis,
                "premeditation_analysis": deep_result.premeditation_analysis,
                "evidence_chain": deep_result.evidence_chain,
                "recommendations": deep_result.recommendations,
                "deep_confidence": deep_result.confidence
            }

        # 如果启用预谋性分析
        if request.analyze_premeditation:
            premeditation_result = premeditation_analyzer.analyze(
                text=request.description,
                time_analysis=response.get("deep_reasoning", {}).get("time_analysis", {}),
                causal_analysis=response.get("deep_reasoning", {}).get("causal_analysis", {})
            )
            response["premeditation_analysis"] = {
                "is_premeditated": premeditation_result.is_premeditated,
                "premeditation_score": premeditation_result.premeditation_score,
                "premeditation_level": premeditation_result.premeditation_level,
                "indicators": [
                    {
                        "type": ind.indicator_type,
                        "description": ind.description,
                        "confidence": ind.confidence,
                        "evidence": ind.evidence
                    }
                    for ind in premeditation_result.indicators
                ],
                "behavior_pattern": premeditation_result.behavior_pattern,
                "action_route": premeditation_result.action_route,
                "reasoning": premeditation_result.reasoning,
                "confidence": premeditation_result.confidence
            }

        # 如果启用惯犯识别
        if request.analyze_habitual:
            habitual_result = habitual_offender_detector.analyze(
                text=request.description,
                social_media_data=request.context.get("social_media_data") if request.context else None
            )
            response["habitual_offender_analysis"] = {
                "is_habitual_offender": habitual_result.is_habitual_offender,
                "offender_probability": habitual_result.offender_probability,
                "offender_level": habitual_result.offender_level,
                "similar_posts": [
                    {
                        "post_id": p.post_id,
                        "platform": p.platform,
                        "content": p.content,
                        "timestamp": p.timestamp,
                        "similarity_score": p.similarity_score,
                        "matched_keywords": p.matched_keywords
                    }
                    for p in habitual_result.similar_posts
                ],
                "behavior_patterns": habitual_result.behavior_patterns,
                "modus_operandi": habitual_result.modus_operandi,
                "historical_evidence": habitual_result.historical_evidence,
                "reasoning": habitual_result.reasoning,
                "confidence": habitual_result.confidence
            }

        # 如果启用团伙分析
        if request.analyze_group:
            group_result = group_analyzer.analyze(
                text=request.description,
                time_analysis=response.get("deep_reasoning", {}).get("time_analysis", {}),
                causal_analysis=response.get("deep_reasoning", {}).get("causal_analysis", {})
            )
            response["group_analysis"] = {
                "is_group_crime": group_result.is_group_crime,
                "group_probability": group_result.group_probability,
                "group_size": group_result.group_size,
                "persons": [
                    {
                        "name": p.name,
                        "role": p.role,
                        "actions": p.actions,
                        "relationship": p.relationship,
                        "confidence": p.confidence
                    }
                    for p in group_result.persons
                ],
                "associations": [
                    {
                        "person1": a.person1,
                        "person2": a.person2,
                        "relationship_type": a.relationship_type,
                        "evidence": a.evidence,
                        "strength": a.strength
                    }
                    for a in group_result.associations
                ],
                "group_structure": group_result.group_structure,
                "coordination_evidence": group_result.coordination_evidence,
                "reasoning": group_result.reasoning,
                "confidence": group_result.confidence
            }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/generate")
async def generate_documents(request: GenerateDocumentsRequest):
    """生成报案材料"""
    try:
        # 执行分析
        analysis = legal_reasoner.analyze(
            description=request.description,
            context={}
        )

        # 生成文档
        user_info_dict = request.user_info.dict()
        documents = document_generator.generate_report(analysis, user_info_dict)

        # 转换为可序列化的格式
        return {
            "documents": [
                {
                    "title": doc.title,
                    "content": doc.content,
                    "document_type": doc.document_type,
                    "created_at": doc.created_at
                }
                for doc in documents
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/behavior-analysis")
async def analyze_behavior(request: AnalyzeRequest):
    """行为分析 - 预谋性、惯犯、团伙分析"""
    try:
        results = {}

        # 1. 预谋性分析
        premeditation_result = premeditation_analyzer.analyze(
            text=request.description
        )
        results["premeditation"] = {
            "is_premeditated": premeditation_result.is_premeditated,
            "score": premeditation_result.premeditation_score,
            "level": premeditation_result.premeditation_level,
            "indicators": [
                {
                    "type": ind.indicator_type,
                    "description": ind.description,
                    "confidence": ind.confidence,
                    "evidence": ind.evidence
                }
                for ind in premeditation_result.indicators
            ],
            "action_route": premeditation_result.action_route,
            "reasoning": premeditation_result.reasoning,
            "confidence": premeditation_result.confidence
        }

        # 2. 惯犯识别
        habitual_result = habitual_offender_detector.analyze(
            text=request.description,
            social_media_data=request.context.get("social_media_data") if request.context else None
        )
        results["habitual_offender"] = {
            "is_habitual_offender": habitual_result.is_habitual_offender,
            "probability": habitual_result.offender_probability,
            "level": habitual_result.offender_level,
            "similar_posts": [
                {
                    "platform": p.platform,
                    "content": p.content,
                    "similarity": p.similarity_score
                }
                for p in habitual_result.similar_posts
            ],
            "modus_operandi": habitual_result.modus_operandi,
            "historical_evidence": habitual_result.historical_evidence,
            "reasoning": habitual_result.reasoning,
            "confidence": habitual_result.confidence
        }

        # 3. 团伙分析
        group_result = group_analyzer.analyze(
            text=request.description
        )
        results["group_crime"] = {
            "is_group_crime": group_result.is_group_crime,
            "probability": group_result.group_probability,
            "group_size": group_result.group_size,
            "persons": [
                {
                    "name": p.name,
                    "role": p.role,
                    "relationship": p.relationship
                }
                for p in group_result.persons
            ],
            "group_structure": group_result.group_structure,
            "coordination_evidence": group_result.coordination_evidence,
            "reasoning": group_result.reasoning,
            "confidence": group_result.confidence
        }

        # 综合评估
        comprehensive_assessment = {
            "overall_risk_level": "低",
            "key_findings": []
        }

        # 评估整体风险
        risk_score = 0.0
        if premeditation_result.is_premeditated:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("预谋性作案")
        if habitual_result.is_habitual_offender:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("疑似惯犯")
        if group_result.is_group_crime:
            risk_score += 0.2
            comprehensive_assessment["key_findings"].append("团伙作案")

        # 确定风险等级
        if risk_score >= 0.8:
            comprehensive_assessment["overall_risk_level"] = "极高"
        elif risk_score >= 0.5:
            comprehensive_assessment["overall_risk_level"] = "高"
        elif risk_score >= 0.3:
            comprehensive_assessment["overall_risk_level"] = "中"

        results["comprehensive_assessment"] = comprehensive_assessment

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evidence/analyze")
async def analyze_evidence(request: EvidenceRequest):
    """分析证据"""
    try:
        # 转换证据
        evidences = []
        for i, ev_dict in enumerate(request.evidences):
            evidence_type = EvidenceType(ev_dict.get("type", "document"))
            validity = Validity(ev_dict.get("validity", "medium"))

            evidence = Evidence(
                id=f"ev_{i}",
                name=ev_dict.get("name", f"证据{i+1}"),
                evidence_type=evidence_type,
                description=ev_dict.get("description", ""),
                validity=validity,
                weight=ev_dict.get("weight", 1.0),
                source=ev_dict.get("source", ""),
                obtained_date=datetime.fromisoformat(ev_dict["obtained_date"]) if ev_dict.get("obtained_date") else None,
                metadata=ev_dict.get("metadata", {})
            )
            evidences.append(evidence)

        # 构建证据链
        evidence_chain = evidence_analyzer.build_evidence_chain(
            evidences=evidences,
            case_type=request.case_type
        )

        # 分析单个证据
        individual_analyses = [
            evidence_analyzer.analyze_evidence(ev)
            for ev in evidences
        ]

        return {
            "evidence_chain": {
                "completeness": evidence_chain.completeness,
                "consistency": evidence_chain.consistency,
                "strength": evidence_chain.strength,
                "gaps": evidence_chain.gaps,
                "suggestions": evidence_chain.suggestions
            },
            "individual_analyses": individual_analyses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/behavior-analysis")
async def analyze_behavior(request: AnalyzeRequest):
    """行为分析 - 预谋性、惯犯、团伙分析"""
    try:
        results = {}

        # 1. 预谋性分析
        premeditation_result = premeditation_analyzer.analyze(
            text=request.description
        )
        results["premeditation"] = {
            "is_premeditated": premeditation_result.is_premeditated,
            "score": premeditation_result.premeditation_score,
            "level": premeditation_result.premeditation_level,
            "indicators": [
                {
                    "type": ind.indicator_type,
                    "description": ind.description,
                    "confidence": ind.confidence,
                    "evidence": ind.evidence
                }
                for ind in premeditation_result.indicators
            ],
            "action_route": premeditation_result.action_route,
            "reasoning": premeditation_result.reasoning,
            "confidence": premeditation_result.confidence
        }

        # 2. 惯犯识别
        habitual_result = habitual_offender_detector.analyze(
            text=request.description,
            social_media_data=request.context.get("social_media_data") if request.context else None
        )
        results["habitual_offender"] = {
            "is_habitual_offender": habitual_result.is_habitual_offender,
            "probability": habitual_result.offender_probability,
            "level": habitual_result.offender_level,
            "similar_posts": [
                {
                    "platform": p.platform,
                    "content": p.content,
                    "similarity": p.similarity_score
                }
                for p in habitual_result.similar_posts
            ],
            "modus_operandi": habitual_result.modus_operandi,
            "historical_evidence": habitual_result.historical_evidence,
            "reasoning": habitual_result.reasoning,
            "confidence": habitual_result.confidence
        }

        # 3. 团伙分析
        group_result = group_analyzer.analyze(
            text=request.description
        )
        results["group_crime"] = {
            "is_group_crime": group_result.is_group_crime,
            "probability": group_result.group_probability,
            "group_size": group_result.group_size,
            "persons": [
                {
                    "name": p.name,
                    "role": p.role,
                    "relationship": p.relationship
                }
                for p in group_result.persons
            ],
            "group_structure": group_result.group_structure,
            "coordination_evidence": group_result.coordination_evidence,
            "reasoning": group_result.reasoning,
            "confidence": group_result.confidence
        }

        # 综合评估
        comprehensive_assessment = {
            "overall_risk_level": "低",
            "key_findings": []
        }

        # 评估整体风险
        risk_score = 0.0
        if premeditation_result.is_premeditated:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("预谋性作案")
        if habitual_result.is_habitual_offender:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("疑似惯犯")
        if group_result.is_group_crime:
            risk_score += 0.2
            comprehensive_assessment["key_findings"].append("团伙作案")

        # 确定风险等级
        if risk_score >= 0.8:
            comprehensive_assessment["overall_risk_level"] = "极高"
        elif risk_score >= 0.5:
            comprehensive_assessment["overall_risk_level"] = "高"
        elif risk_score >= 0.3:
            comprehensive_assessment["overall_risk_level"] = "中"

        results["comprehensive_assessment"] = comprehensive_assessment

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/evidence/suggest/{case_type}")
async def suggest_evidence(case_type: str):
    """建议证据类型"""
    suggestions = evidence_analyzer.suggest_evidence(case_type, [])
    return {
        "case_type": case_type,
        "suggested_evidences": suggestions
    }


@app.get("/intent/detect")
async def detect_intent(message: str):
    """检测用户意图"""
    intent = conversation_manager.detect_intent(message)
    return intent


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "conversation_manager": "active",
            "legal_reasoner": "active",
            "legal_reasoner_v3": "active",
            "deep_reasoner": "active",
            "premeditation_analyzer": "active",
            "habitual_offender_detector": "active",
            "group_analyzer": "active",
            "social_media_fetcher": "active",
            "legal_database_fetcher": "active",
            "multimedia_analyzer": "active",
            "outcome_predictor": "active",
            "document_generator": "active",
            "evidence_analyzer": "active"
        }
    }


# ===== 外部数据获取端点 =====

class SocialMediaRequest(BaseModel):
    """社交媒体查询请求"""
    query_type: str  # "username", "keyword", "post_id"
    query: str
    platform: str = "xiaohongshu"  # xiaohongshu, weibo, douyin
    days_back: Optional[int] = 30
    max_results: Optional[int] = 20


@app.post("/social-media/fetch")
async def fetch_social_media_data(request: SocialMediaRequest):
    """获取社交媒体数据"""
    try:
        # 转换平台枚举
        platform_map = {
            "xiaohongshu": Platform.XIAOHONGSHU,
            "weibo": Platform.WEIBO,
            "douyin": Platform.DOUYIN,
            "bilibili": Platform.BILIBILI,
            "zhihu": Platform.ZHIHU
        }
        platform = platform_map.get(request.platform, Platform.XIAOHONGSHU)
        
        # 根据查询类型调用不同方法
        if request.query_type == "username":
            result = social_media_fetcher.fetch_by_username(
                username=request.query,
                platform=platform,
                days_back=request.days_back
            )
        elif request.query_type == "keyword":
            result = social_media_fetcher.fetch_by_keyword(
                keyword=request.query,
                platform=platform,
                max_results=request.max_results
            )
        elif request.query_type == "post_id":
            result = social_media_fetcher.fetch_by_post_id(
                post_id=request.query,
                platform=platform
            )
        else:
            raise HTTPException(status_code=400, detail="无效的查询类型")
        
        # 分析用户行为
        behavior_patterns = {}
        if result.user_profile:
            behavior_patterns = social_media_fetcher.analyze_user_behavior(result)
        
        return {
            "query_type": request.query_type,
            "platform": platform.value,
            "total_results": result.total_results,
            "posts": [
                {
                    "post_id": p.post_id,
                    "content": p.content,
                    "timestamp": p.timestamp.isoformat(),
                    "likes": p.likes,
                    "comments": p.comments,
                    "shares": p.shares
                }
                for p in result.posts[:10]  # 只返回前10条
            ],
            "user_profile": {
                "username": result.user_profile.username if result.user_profile else None,
                "followers": result.user_profile.followers_count if result.user_profile else 0,
                "posts": result.user_profile.posts_count if result.user_profile else 0
            } if result.user_profile else None,
            "behavior_patterns": behavior_patterns,
            "confidence": result.confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/social-media/track")
async def track_network_traces(request: SocialMediaRequest):
    """追踪跨平台网络痕迹"""
    try:
        platform_map = {
            "xiaohongshu": Platform.XIAOHONGSHU,
            "weibo": Platform.WEIBO,
            "douyin": Platform.DOUYIN
        }
        platform = platform_map.get(request.platform, Platform.XIAOHONGSHU)
        
        traces = social_media_fetcher.track_network_traces(
            username=request.query,
            platform=platform
        )
        
        return {
            "username": request.query,
            "cross_platform_activity": traces["cross_platform_activity"],
            "accounts_found": traces["accounts_found"],
            "platforms": traces["platforms"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class LegalSearchRequest(BaseModel):
    """法律查询请求"""
    search_type: str  # "cases", "provisions", "statistics", "predict"
    query: str
    case_type: Optional[str] = None
    max_results: Optional[int] = 5


@app.post("/legal/search")
async def search_legal_data(request: LegalSearchRequest):
    """法律数据库查询"""
    try:
        # 转换案件类型
        case_type = None
        if request.case_type:
            case_type_map = {
                "civil": CaseType.CIVIL,
                "criminal": CaseType.CRIMINAL,
                "defamation": CaseType.DEFAMATION,
                "internet": CaseType.INTERNET,
                "consumer": CaseType.CONSUMER,
                "fraud": CaseType.FRAUD
            }
            case_type = case_type_map.get(request.case_type.lower())
        
        if request.search_type == "cases":
            result = legal_database_fetcher.search_similar_cases(
                description=request.query,
                case_type=case_type,
                max_results=request.max_results
            )
            
            return {
                "total_cases": result.total_cases,
                "cases": [
                    {
                        "case_id": c.case_id,
                        "case_name": c.case_name,
                        "case_type": c.case_type.value,
                        "outcome": c.case_outcome.value,
                        "facts": c.facts[:100] + "...",
                        "compensation": c.compensation,
                        "similarity": round(c.similarity_score * 100, 1)
                    }
                    for c in result.cases
                ],
                "confidence": result.confidence
            }
        
        elif request.search_type == "provisions":
            keywords = request.query.split(",")
            result = legal_database_fetcher.query_legal_provisions(
                keywords=keywords,
                max_results=request.max_results
            )
            
            return {
                "total_provisions": result.total_provisions,
                "provisions": [
                    {
                        "law_name": p.law_name,
                        "article": p.article,
                        "content": p.content,
                        "penalty": p.penalty,
                        "relevance": round(p.relevance_score * 100, 1)
                    }
                    for p in result.provisions
                ],
                "confidence": result.confidence
            }
        
        elif request.search_type == "statistics":
            result = legal_database_fetcher.get_case_statistics(case_type)
            
            if result.statistics:
                return {
                    "case_type": request.case_type or "全部",
                    "total_cases": result.statistics.total_cases,
                    "plaintiff_win_rate": round(result.statistics.plaintiff_win_rate * 100, 1),
                    "avg_compensation": round(result.statistics.avg_compensation, 0),
                    "common_outcomes": result.statistics.common_outcomes,
                    "success_factors": result.statistics.success_factors,
                    "risk_factors": result.statistics.risk_factors
                }
            else:
                return {"error": result.error_message}
        
        elif request.search_type == "predict":
            prediction = legal_database_fetcher.predict_outcome(
                description=request.query,
                case_type=case_type
            )
            
            return prediction
        
        else:
            raise HTTPException(status_code=400, detail="无效的查询类型")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/media/analyze")
async def analyze_media_file(file: UploadFile = File(...)):
    """分析上传的多媒体文件"""
    try:
        # 读取文件数据
        file_data = await file.read()
        
        # 根据文件类型进行分析
        content_type = file.content_type
        filename = file.filename
        
        if content_type and content_type.startswith("image/"):
            result = multimedia_analyzer.analyze_image(
                image_path=filename,
                enable_ocr=True
            )
            
            # 提取证据
            evidence = multimedia_analyzer.extract_evidence_from_media(result)
            
            return {
                "media_id": result.media_id,
                "media_type": "image",
                "image_type": result.image_type.value,
                "ocr_text": result.text_content,
                "objects": result.objects_detected,
                "faces": result.faces_detected,
                "evidence": evidence,
                "confidence": result.confidence
            }
        
        elif content_type and content_type.startswith("audio/"):
            result = multimedia_analyzer.analyze_audio()
            
            return {
                "media_id": result.media_id,
                "media_type": "audio",
                "duration": result.duration,
                "transcript": result.transcript,
                "speaker_count": result.speaker_count,
                "key_phrases": result.key_phrases,
                "confidence": result.confidence
            }
        
        elif content_type and content_type.startswith("video/"):
            result = multimedia_analyzer.analyze_video()
            
            return {
                "media_id": result.media_id,
                "media_type": "video",
                "duration": result.duration,
                "key_frames": result.key_frames,
                "transcript": result.transcript,
                "objects": result.objects_detected,
                "confidence": result.confidence
            }
        
        else:
            raise HTTPException(status_code=400, detail="不支持的文件类型")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/media/batch-analyze")
async def batch_analyze_media(files: List[UploadFile] = File(...)):
    """批量分析多媒体文件"""
    try:
        # 准备文件列表
        file_list = []
        for file in files:
            file_list.append({
                "path": file.filename,
                "type": "image" if file.content_type and file.content_type.startswith("image/") else "other"
            })
        
        # 批量分析
        batch_result = multimedia_analyzer.analyze_batch(file_list)
        
        return {
            "batch_id": batch_result.batch_id,
            "total_files": batch_result.total_files,
            "processed_files": batch_result.processed_files,
            "failed_files": batch_result.failed_files,
            "summary": batch_result.summary,
            "processing_time": batch_result.processing_time,
            "image_count": len(batch_result.image_results),
            "audio_count": len(batch_result.audio_results),
            "video_count": len(batch_result.video_results),
            "extracted_text": batch_result.extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 结果预测端点 =====

class PredictionRequest(BaseModel):
    """预测请求"""
    case_description: str
    case_type: str = "民事案件"
    evidence_list: List[Dict[str, Any]] = []
    context: Optional[Dict[str, Any]] = None


@app.post("/predict/all")
async def predict_all_outcomes(request: PredictionRequest):
    """综合预测 - 立案、胜算、补偿、风险评估"""
    try:
        timestamp = datetime.now()
        
        # 1. 立案概率预测
        filing_pred = outcome_predictor.predict_filing(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list,
            context=request.context
        )
        
        # 2. 诉讼胜算预测
        similar_result = legal_database_fetcher.search_similar_cases(
            description=request.case_description,
            max_results=5
        )
        similar_cases_data = [
            {
                "case_name": c.case_name,
                "outcome": c.case_outcome.value,
                "similarity": c.similarity_score
            }
            for c in similar_result.cases
        ]
        
        litigation_pred = outcome_predictor.predict_litigation(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list,
            similar_cases=similar_cases_data
        )
        
        # 3. 补偿金额预测
        actual_loss = 0
        impact_scope = "regional"
        duration_days = 30
        
        if request.context:
            actual_loss = request.context.get("actual_loss", 0)
            impact_scope = request.context.get("impact_scope", "regional")
            duration_days = request.context.get("duration_days", 30)
        
        comp_pred = outcome_predictor.predict_compensation(
            case_type="名誉权" if "名誉" in request.case_description else "民事案件",
            actual_loss=actual_loss,
            impact_scope=impact_scope,
            duration_days=duration_days
        )
        
        # 4. 综合风险评估
        risk_assess = outcome_predictor.assess_risk(
            case_description=request.case_description,
            filing_prediction=filing_pred,
            litigation_prediction=litigation_pred,
            compensation_prediction=comp_pred,
            evidence_list=request.evidence_list
        )
        
        # 5. 生成综合建议
        overall_rec = "建议积极维权" if risk_assess.success_probability > 0.7 else "建议谨慎决策"
        
        return {
            "filing_prediction": {
                "probability": filing_pred.probability,
                "risk_level": filing_pred.risk_level.value,
                "key_factors": filing_pred.key_factors,
                "blocking_factors": filing_pred.blocking_factors,
                "recommendations": filing_pred.recommendations
            },
            "litigation_prediction": {
                "win_probability": litigation_pred.win_probability,
                "risk_level": litigation_pred.risk_level.value,
                "expected_outcome": litigation_pred.expected_outcome,
                "success_factors": litigation_pred.key_success_factors,
                "risk_factors": litigation_pred.key_risk_factors
            },
            "compensation_prediction": {
                "min_amount": comp_pred.min_amount,
                "likely_amount": comp_pred.likely_amount,
                "max_amount": comp_pred.max_amount,
                "breakdown": comp_pred.breakdown,
                "reasoning": comp_pred.reasoning
            },
            "risk_assessment": {
                "overall_risk": risk_assess.overall_risk.value,
                "filing_risk": risk_assess.filing_risk.value,
                "litigation_risk": risk_assess.litigation_risk.value,
                "evidence_quality": risk_assess.evidence_quality,
                "strength_score": risk_assess.strength_score,
                "time_estimate": risk_assess.time_estimate,
                "success_probability": risk_assess.success_probability,
                "strengths": risk_assess.key_strengths,
                "weaknesses": risk_assess.key_weaknesses,
                "recommendations": risk_assess.recommendations
            },
            "overall_recommendation": overall_rec,
            "timestamp": timestamp.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/filing")
async def predict_filing_endpoint(request: PredictionRequest):
    """预测立案概率"""
    try:
        filing_pred = outcome_predictor.predict_filing(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list,
            context=request.context
        )
        
        return {
            "probability": filing_pred.probability,
            "risk_level": filing_pred.risk_level.value,
            "key_factors": filing_pred.key_factors,
            "blocking_factors": filing_pred.blocking_factors,
            "recommendations": filing_pred.recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/litigation")
async def predict_litigation_endpoint(request: PredictionRequest):
    """预测诉讼胜算"""
    try:
        litigation_pred = outcome_predictor.predict_litigation(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list
        )
        
        return {
            "win_probability": litigation_pred.win_probability,
            "risk_level": litigation_pred.risk_level.value,
            "expected_outcome": litigation_pred.expected_outcome,
            "success_factors": litigation_pred.key_success_factors,
            "risk_factors": litigation_pred.key_risk_factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/compensation")
async def predict_compensation_endpoint(request: PredictionRequest):
    """预测补偿金额"""
    try:
        actual_loss = 0
        impact_scope = "regional"
        duration_days = 30
        
        if request.context:
            actual_loss = request.context.get("actual_loss", 0)
            impact_scope = request.context.get("impact_scope", "regional")
            duration_days = request.context.get("duration_days", 30)
        
        comp_pred = outcome_predictor.predict_compensation(
            case_type="名誉权" if "名誉" in request.case_description else "民事案件",
            actual_loss=actual_loss,
            impact_scope=impact_scope,
            duration_days=duration_days
        )
        
        return {
            "min_amount": comp_pred.min_amount,
            "likely_amount": comp_pred.likely_amount,
            "max_amount": comp_pred.max_amount,
            "breakdown": comp_pred.breakdown,
            "reasoning": comp_pred.reasoning
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/risk")
async def predict_risk_endpoint(request: PredictionRequest):
    """综合风险评估"""
    try:
        filing_pred = outcome_predictor.predict_filing(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list
        )
        
        litigation_pred = outcome_predictor.predict_litigation(
            case_description=request.case_description,
            case_type=request.case_type,
            evidence_list=request.evidence_list
        )
        
        risk_assess = outcome_predictor.assess_risk(
            case_description=request.case_description,
            filing_prediction=filing_pred,
            litigation_prediction=litigation_pred,
            evidence_list=request.evidence_list
        )
        
        return {
            "overall_risk": risk_assess.overall_risk.value,
            "filing_risk": risk_assess.filing_risk.value,
            "litigation_risk": risk_assess.litigation_risk.value,
            "evidence_quality": risk_assess.evidence_quality,
            "strength_score": risk_assess.strength_score,
            "time_estimate": risk_assess.time_estimate,
            "success_probability": risk_assess.success_probability,
            "strengths": risk_assess.key_strengths,
            "weaknesses": risk_assess.key_weaknesses,
            "recommendations": risk_assess.recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/deep-reason")
async def deep_analyze_case(request: AnalyzeRequest):
    """深度推理分析 - 专门用于深度分析"""
    try:
        from .evidence import Evidence

        # 执行基础分析(V3)
        reasoner = legal_reasoner_v3
        base_analysis = reasoner.analyze(
            description=request.description,
            context=request.context or {}
        )

        # 执行深度推理
        evidences = []  # 可从context中获取证据
        deep_result = deep_reasoner.reason(
            text=request.description,
            evidences=evidences,
            context=request.context or {}
        )

        # 生成深度推理报告
        deep_report = deep_reasoner.generate_report(deep_result)

        return {
            # 基础分析结果
            "base_analysis": {
                "facts": [
                    {
                        "id": fact.id,
                        "description": fact.description,
                        "category": fact.category,
                        "confidence": fact.confidence
                    }
                    for fact in base_analysis.facts
                ],
                "dispute_focuses": [
                    {
                        "main_issue": df.main_issue,
                        "details": df.details
                    }
                    for df in base_analysis.dispute_focuses
                ],
                "evidence_gaps": [
                    {
                        "missing_evidence": eg.missing_evidence,
                        "importance": eg.importance,
                        "how_to_obtain": eg.how_to_obtain
                    }
                    for eg in base_analysis.evidence_gaps
                ],
                "investigation_plan": {
                    "priority_tasks": base_analysis.investigation_plan.priority_tasks,
                    "secondary_tasks": base_analysis.investigation_plan.secondary_tasks,
                    "optional_tasks": base_analysis.investigation_plan.optional_tasks
                }
            },
            # 深度推理结果
            "deep_reasoning": {
                "time_analysis": deep_result.time_analysis,
                "causal_analysis": deep_result.causal_analysis,
                "conflict_analysis": deep_result.conflict_analysis,
                "logical_analysis": deep_result.logical_analysis,
                "premeditation_analysis": deep_result.premeditation_analysis,
                "evidence_chain": deep_result.evidence_chain,
                "recommendations": deep_result.recommendations,
                "deep_confidence": deep_result.confidence
            },
            # 深度推理报告
            "deep_report": deep_report,
            # 综合置信度
            "overall_confidence": {
                "base": base_analysis.confidence,
                "deep": deep_result.confidence,
                "combined": (base_analysis.confidence + deep_result.confidence) / 2
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/behavior-analysis")
async def analyze_behavior(request: AnalyzeRequest):
    """行为分析 - 预谋性、惯犯、团伙分析"""
    try:
        results = {}

        # 1. 预谋性分析
        premeditation_result = premeditation_analyzer.analyze(
            text=request.description
        )
        results["premeditation"] = {
            "is_premeditated": premeditation_result.is_premeditated,
            "score": premeditation_result.premeditation_score,
            "level": premeditation_result.premeditation_level,
            "indicators": [
                {
                    "type": ind.indicator_type,
                    "description": ind.description,
                    "confidence": ind.confidence,
                    "evidence": ind.evidence
                }
                for ind in premeditation_result.indicators
            ],
            "action_route": premeditation_result.action_route,
            "reasoning": premeditation_result.reasoning,
            "confidence": premeditation_result.confidence
        }

        # 2. 惯犯识别
        habitual_result = habitual_offender_detector.analyze(
            text=request.description,
            social_media_data=request.context.get("social_media_data") if request.context else None
        )
        results["habitual_offender"] = {
            "is_habitual_offender": habitual_result.is_habitual_offender,
            "probability": habitual_result.offender_probability,
            "level": habitual_result.offender_level,
            "similar_posts": [
                {
                    "platform": p.platform,
                    "content": p.content,
                    "similarity": p.similarity_score
                }
                for p in habitual_result.similar_posts
            ],
            "modus_operandi": habitual_result.modus_operandi,
            "historical_evidence": habitual_result.historical_evidence,
            "reasoning": habitual_result.reasoning,
            "confidence": habitual_result.confidence
        }

        # 3. 团伙分析
        group_result = group_analyzer.analyze(
            text=request.description
        )
        results["group_crime"] = {
            "is_group_crime": group_result.is_group_crime,
            "probability": group_result.group_probability,
            "group_size": group_result.group_size,
            "persons": [
                {
                    "name": p.name,
                    "role": p.role,
                    "relationship": p.relationship
                }
                for p in group_result.persons
            ],
            "group_structure": group_result.group_structure,
            "coordination_evidence": group_result.coordination_evidence,
            "reasoning": group_result.reasoning,
            "confidence": group_result.confidence
        }

        # 综合评估
        comprehensive_assessment = {
            "overall_risk_level": "低",
            "key_findings": []
        }

        # 评估整体风险
        risk_score = 0.0
        if premeditation_result.is_premeditated:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("预谋性作案")
        if habitual_result.is_habitual_offender:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("疑似惯犯")
        if group_result.is_group_crime:
            risk_score += 0.2
            comprehensive_assessment["key_findings"].append("团伙作案")

        # 确定风险等级
        if risk_score >= 0.8:
            comprehensive_assessment["overall_risk_level"] = "极高"
        elif risk_score >= 0.5:
            comprehensive_assessment["overall_risk_level"] = "高"
        elif risk_score >= 0.3:
            comprehensive_assessment["overall_risk_level"] = "中"

        results["comprehensive_assessment"] = comprehensive_assessment

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/behavior-analysis")
async def analyze_behavior(request: AnalyzeRequest):
    """行为分析 - 预谋性、惯犯、团伙分析"""
    try:
        results = {}

        # 1. 预谋性分析
        premeditation_result = premeditation_analyzer.analyze(
            text=request.description
        )
        results["premeditation"] = {
            "is_premeditated": premeditation_result.is_premeditated,
            "score": premeditation_result.premeditation_score,
            "level": premeditation_result.premeditation_level,
            "indicators": [
                {
                    "type": ind.indicator_type,
                    "description": ind.description,
                    "confidence": ind.confidence,
                    "evidence": ind.evidence
                }
                for ind in premeditation_result.indicators
            ],
            "action_route": premeditation_result.action_route,
            "reasoning": premeditation_result.reasoning,
            "confidence": premeditation_result.confidence
        }

        # 2. 惯犯识别
        habitual_result = habitual_offender_detector.analyze(
            text=request.description,
            social_media_data=request.context.get("social_media_data") if request.context else None
        )
        results["habitual_offender"] = {
            "is_habitual_offender": habitual_result.is_habitual_offender,
            "probability": habitual_result.offender_probability,
            "level": habitual_result.offender_level,
            "similar_posts": [
                {
                    "platform": p.platform,
                    "content": p.content,
                    "similarity": p.similarity_score
                }
                for p in habitual_result.similar_posts
            ],
            "modus_operandi": habitual_result.modus_operandi,
            "historical_evidence": habitual_result.historical_evidence,
            "reasoning": habitual_result.reasoning,
            "confidence": habitual_result.confidence
        }

        # 3. 团伙分析
        group_result = group_analyzer.analyze(
            text=request.description
        )
        results["group_crime"] = {
            "is_group_crime": group_result.is_group_crime,
            "probability": group_result.group_probability,
            "group_size": group_result.group_size,
            "persons": [
                {
                    "name": p.name,
                    "role": p.role,
                    "relationship": p.relationship
                }
                for p in group_result.persons
            ],
            "group_structure": group_result.group_structure,
            "coordination_evidence": group_result.coordination_evidence,
            "reasoning": group_result.reasoning,
            "confidence": group_result.confidence
        }

        # 综合评估
        comprehensive_assessment = {
            "overall_risk_level": "低",
            "key_findings": []
        }

        # 评估整体风险
        risk_score = 0.0
        if premeditation_result.is_premeditated:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("预谋性作案")
        if habitual_result.is_habitual_offender:
            risk_score += 0.4
            comprehensive_assessment["key_findings"].append("疑似惯犯")
        if group_result.is_group_crime:
            risk_score += 0.2
            comprehensive_assessment["key_findings"].append("团伙作案")

        # 确定风险等级
        if risk_score >= 0.8:
            comprehensive_assessment["overall_risk_level"] = "极高"
        elif risk_score >= 0.5:
            comprehensive_assessment["overall_risk_level"] = "高"
        elif risk_score >= 0.3:
            comprehensive_assessment["overall_risk_level"] = "中"

        results["comprehensive_assessment"] = comprehensive_assessment

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
