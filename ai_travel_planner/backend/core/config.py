"""
配置文件
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    APP_NAME: str = "AI Travel Planner"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # 数据库配置（使用异步驱动）
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/travel_planner"

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI服务配置
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # 地图服务配置
    AMAP_API_KEY: str = ""

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENCRYPTION_KEY: str = "your-encryption-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 爬虫配置
    CRAWLER_ENABLED: bool = True
    CRAWLER_USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    ]
    CRAWLER_DELAY_MIN: int = 2
    CRAWLER_DELAY_MAX: int = 10
    CRAWLER_REQUEST_TIMEOUT: int = 30

    # 代理配置
    PROXY_ENABLED: bool = False
    PROXY_POOL_URL: str = ""

    # 监控配置
    SENTRY_DSN: str = ""
    PROMETHEUS_ENABLED: bool = False
    PROMETHEUS_PORT: int = 9090

    # 文件存储配置
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # 缓存配置
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1小时

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
