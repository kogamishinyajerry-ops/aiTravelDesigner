"""
API v1 Router
"""
from fastapi import APIRouter
from api.v1.endpoints import (
    chat,
    plan,
    health,
    intelligent_plan,
    auth,
    admin,
    tasks_endpoint as tasks,
    professional_plan
)

router = APIRouter()

# 包含端点路由
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(plan.router, prefix="/plan", tags=["Plan"])
router.include_router(intelligent_plan.router, tags=["Intelligent"])
router.include_router(professional_plan.router, tags=["Professional"])
