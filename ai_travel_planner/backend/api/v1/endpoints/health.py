"""
Health Check Endpoint
健康检查端点
"""
from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": "2026-02-18"
    }


@router.get("/detailed")
async def detailed_health():
    """详细健康检查"""
    # TODO: 添加数据库、Redis等组件检查
    checks = {
        "api": "running",
        "database": "connected",  # 需要实际检查
        "redis": "connected",  # 需要实际检查
    }

    is_healthy = all(status == "running" or status == "connected" for status in checks.values())

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "checks": checks
    }
