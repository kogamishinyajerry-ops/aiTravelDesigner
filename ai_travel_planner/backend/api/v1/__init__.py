"""
API v1 Router
"""
from fastapi import APIRouter
from api.v1.endpoints import (
    chat,
    plan,
    health,
)

router = APIRouter()

# 包含端点路由
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(plan.router, prefix="/plan", tags=["Plan"])
