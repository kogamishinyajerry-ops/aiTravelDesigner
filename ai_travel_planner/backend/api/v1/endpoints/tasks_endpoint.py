"""
任务管理API
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from services.tasks.celery_tasks import TaskManager
from core.security import get_current_user, require_permission, Permission

router = APIRouter()


@router.post("/itinerary/generate")
@require_permission(Permission.CREATE_ITINERARY)
async def generate_itinerary_async(
    user_id: str,
    destination: str,
    days: int,
    current_user: dict = Depends(get_current_user)
):
    """异步生成行程"""
    task_id = TaskManager.submit_itinerary_generation(
        user_id=user_id,
        request_data={
            "destination": destination,
            "days": days
        }
    )
    
    return {
        "task_id": task_id,
        "status": "submitted",
        "message": "行程生成任务已提交"
    }


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """获取任务状态"""
    status = TaskManager.get_task_status(task_id)
    return status


@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    """取消任务"""
    success = TaskManager.cancel_task(task_id)
    if success:
        return {"success": True, "message": "任务已取消"}
    else:
        raise HTTPException(status_code=400, detail="取消任务失败")
