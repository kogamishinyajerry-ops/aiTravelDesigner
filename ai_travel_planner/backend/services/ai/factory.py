"""
LLM服务工厂 - 支持多种LLM提供商
"""
import os
from typing import Optional
from core.config import settings
from .llm_service import LLMService
from .mock_llm_service import MockLLMService


def get_llm_service(use_mock: bool = False) -> Optional[LLMService]:
    """
    获取LLM服务
    
    Args:
        use_mock: 是否使用Mock服务（用于测试）
    
    Returns:
        LLM服务实例或None
    """
    # 如果明确要求使用Mock
    if use_mock:
        return get_mock_llm_service()
    
    # 如果没有配置API Key，使用Mock
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        return get_mock_llm_service()
    
    # 否则使用真实的LLM服务
    try:
        return LLMService()
    except Exception as e:
        print(f"Warning: Failed to initialize LLM service: {e}")
        print("Falling back to Mock LLM service...")
        return get_mock_llm_service()


def get_mock_llm_service() -> MockLLMService:
    """获取Mock LLM服务"""
    from .mock_llm_service import get_mock_llm_service as _get_mock
    return _get_mock()


__all__ = [
    "get_llm_service",
    "get_mock_llm_service",
    "LLMService",
    "MockLLMService"
]
