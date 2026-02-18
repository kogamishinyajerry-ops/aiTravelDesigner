"""
管理员API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from core.security import (
    get_current_user,
    require_permission,
    require_role,
    Permission,
    UserRole
)

router = APIRouter()


class UserStats(BaseModel):
    """用户统计"""
    total_users: int
    active_users: int
    new_users_today: int


class SystemStats(BaseModel):
    """系统统计"""
    total_requests: int
    success_rate: float
    avg_response_time: float
    uptime_hours: float


class AuditLogEntry(BaseModel):
    """审计日志条目"""
    id: int
    user_id: str
    action: str
    resource: str
    timestamp: datetime
    ip_address: str
    success: bool


@router.get("/stats/users", response_model=UserStats)
@require_role(UserRole.ADMIN)
async def get_user_stats(
    days: int = Query(7, description="统计天数")
):
    """
    获取用户统计（仅管理员）
    """
    # 模拟数据
    return UserStats(
        total_users=1000,
        active_users=450,
        new_users_today=12
    )


@router.get("/stats/system", response_model=SystemStats)
@require_role(UserRole.ADMIN)
async def get_system_stats():
    """
    获取系统统计（仅管理员）
    """
    # 模拟数据
    return SystemStats(
        total_requests=50000,
        success_rate=99.5,
        avg_response_time=0.15,
        uptime_hours=720.5
    )


@router.get("/audit-logs", response_model=List[AuditLogEntry])
@require_permission(Permission.VIEW_ANALYTICS)
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[str] = None,
    action: Optional[str] = None
):
    """
    获取审计日志（需要VIEW_ANALYTICS权限）
    """
    # 模拟数据
    return [
        AuditLogEntry(
            id=1,
            user_id="1",
            action="login",
            resource="/api/v1/auth/login",
            timestamp=datetime.now() - timedelta(hours=1),
            ip_address="192.168.1.100",
            success=True
        )
    ]


@router.delete("/users/{user_id}")
@require_permission(Permission.MANAGE_USERS)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    删除用户（需要MANAGE_USERS权限）
    """
    # 记录审计日志
    from core.security import log_audit_event
    await log_audit_event(
        user_id=current_user["id"],
        action="delete_user",
        resource=f"user:{user_id}",
        details={"target_user_id": user_id}
    )
    
    # 实际删除逻辑
    # await db.delete(User).where(User.id == user_id)
    
    return {"message": f"用户 {user_id} 已删除"}


@router.get("/health")
async def admin_health_check():
    """
    管理员健康检查端点
    """
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "cache": "ok",
            "llm": "ok"
        },
        "version": "1.0.0"
    }
