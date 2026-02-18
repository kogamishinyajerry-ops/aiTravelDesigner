"""
Pydantic模型
"""
from .chat import (
    Message,
    ChatRequest,
    ChatResponse,
    ConversationRequest,
    ConversationResponse,
    TravelPreferences,
    TravelersInfo,
    ExtractedTravelInfo,
    ClarificationQuestion,
)

__all__ = [
    "Message",
    "ChatRequest",
    "ChatResponse",
    "ConversationRequest",
    "ConversationResponse",
    "TravelPreferences",
    "TravelersInfo",
    "ExtractedTravelInfo",
    "ClarificationQuestion",
]
