"""
异步任务队列
使用Celery实现后台任务处理
"""
from celery import Celery
from celery.result import AsyncResult
from typing import Dict, Any, List, Optional
from loguru import logger

# Celery配置
celery_app = Celery(
    "travel_planner_tasks",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1小时超时
    task_soft_time_limit=3300,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(bind=True, name="generate_itinerary_task")
def generate_itinerary_task(
    self,
    user_id: str,
    request_data: Dict[str, Any]
) -> Dict[str, Any]:
    """异步生成行程任务"""
    try:
        logger.info(f"Starting itinerary generation for user {user_id}")
        
        # 更新进度
        self.update_state(state="PROGRESS", meta={"progress": 0, "status": "初始化"})
        
        # 执行行程生成
        # generator = get_itinerary_generator()
        # itinerary = asyncio.run(generator.generate_itinerary(...))
        
        self.update_state(state="PROGRESS", meta={"progress": 50, "status": "生成中"})
        
        # 模拟处理
        import time
        time.sleep(2)
        
        self.update_state(state="PROGRESS", meta={"progress": 100, "status": "完成"})
        
        return {
            "success": True,
            "user_id": user_id,
            "itinerary": {"id": "123", "name": "Test Itinerary"}
        }
        
    except Exception as e:
        logger.error(f"Itinerary generation failed: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise


@celery_app.task(bind=True, name="crawl_attractions_task")
def crawl_attractions_task(
    self,
    destination: str,
    max_pages: int = 10
) -> Dict[str, Any]:
    """异步爬取景点任务"""
    try:
        logger.info(f"Starting crawl for {destination}")
        
        total_pages = max_pages
        results = []
        
        for page in range(1, total_pages + 1):
            # 模拟爬取
            import time
            time.sleep(0.5)
            
            results.append({
                "page": page,
                "attractions": ["Attraction 1", "Attraction 2"]
            })
            
            progress = int((page / total_pages) * 100)
            self.update_state(
                state="PROGRESS",
                meta={
                    "progress": progress,
                    "status": f"爬取第 {page}/{total_pages} 页"
                }
            )
        
        return {
            "success": True,
            "destination": destination,
            "total_attractions": len(results) * 2,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Crawl failed: {e}")
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


class TaskManager:
    """任务管理器"""
    
    @staticmethod
    def submit_itinerary_generation(
        user_id: str,
        request_data: Dict[str, Any]
    ) -> str:
        """提交行程生成任务"""
        task = generate_itinerary_task.delay(user_id, request_data)
        return task.id
    
    @staticmethod
    def submit_crawl_task(
        destination: str,
        max_pages: int = 10
    ) -> str:
        """提交爬取任务"""
        task = crawl_attractions_task.delay(destination, max_pages)
        return task.id
    
    @staticmethod
    def get_task_status(task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        task = AsyncResult(task_id, app=celery_app)
        
        response = {
            "task_id": task_id,
            "status": task.status,
            "result": None,
            "error": None
        }
        
        if task.successful():
            response["result"] = task.result
        elif task.failed():
            response["error"] = str(task.info)
        elif task.status == "PROGRESS":
            response["progress"] = task.info
        
        return response
    
    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """取消任务"""
        task = AsyncResult(task_id, app=celery_app)
        return task.revoke(terminate=True)
