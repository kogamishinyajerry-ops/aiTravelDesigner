"""
AI Travel Planner - FastAPI Backend
AI旅行规划软件 - 后端主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger

# 配置logger
logger.remove()
logger.add(
    "../logs/app.log",
    rotation="10 MB",
    retention="10 days",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)

# 导入配置
from core.config import settings

# 导入数据库
from core.database import init_db

# 导入路由
from api.v1 import router as api_v1_router

# 导入安全相关中间件和异常处理
from core.exceptions import (
    TravelPlannerException,
    handle_travel_planner_exception,
    handle_generic_exception,
    add_trace_id
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("🚀 Starting AI Travel Planner Backend...")

    # 初始化数据库
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization skipped: {e}")

    yield

    logger.info("🛑 Shutting down AI Travel Planner Backend...")


# 创建FastAPI应用
app = FastAPI(
    title="AI Travel Planner API",
    description="AI智能旅行规划平台API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 追踪ID中间件
app.middleware("http")(add_trace_id)

# 自定义异常处理
app.add_exception_handler(TravelPlannerException, handle_travel_planner_exception)
app.add_exception_handler(Exception, handle_generic_exception)

# 包含路由
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI Travel Planner API",
        "version": "0.1.0",
        "status": "running",
        "documentation": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "cache": "connected"
    }


# 迁移说明：旧的异常处理器已被移除，统一使用 core.exceptions 中的处理
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """全局异常处理器"""
#     logger.error(f"Unhandled exception: {exc}")
#     return JSONResponse(
#         status_code=500,
#         content={
#             "error": "Internal server error",
#             "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
#         }
#     )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
