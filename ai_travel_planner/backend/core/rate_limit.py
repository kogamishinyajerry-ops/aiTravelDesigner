"""
API限流
防止滥用，保护系统稳定性
"""
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional, Dict
from datetime import datetime, timedelta
import redis
from collections import defaultdict
from loguru import logger


class RateLimiter:
    """限流器"""
    
    def __init__(self, redis_url: str = None):
        if redis_url:
            self.redis = redis.from_url(redis_url, decode_responses=True)
            self.use_redis = True
        else:
            self.use_redis = False
            self.in_memory_store: Dict[str, list] = defaultdict(list)
    
    def _get_key(self, identifier: str, endpoint: str) -> str:
        """生成限流键"""
        return f"rate_limit:{identifier}:{endpoint}"
    
    def _get_timestamp(self) -> float:
        """获取当前时间戳"""
        return datetime.now().timestamp()
    
    async def is_allowed(
        self,
        identifier: str,
        endpoint: str,
        limit: int,
        window: int  # 秒
    ) -> tuple[bool, Dict[str, int]]:
        """检查是否允许请求"""
        key = self._get_key(identifier, endpoint)
        now = self._get_timestamp()
        window_start = now - window
        
        if self.use_redis:
            return await self._check_redis(key, now, window_start, limit)
        else:
            return self._check_in_memory(key, now, window_start, limit)
    
    async def _check_redis(
        self,
        key: str,
        now: float,
        window_start: float,
        limit: int
    ) -> tuple[bool, Dict[str, int]]:
        """使用Redis检查"""
        pipe = self.redis.pipeline()
        
        # 移除窗口外的记录
        pipe.zremrangebyscore(key, 0, window_start)
        
        # 获取当前计数
        pipe.zcard(key)
        
        # 添加当前请求
        pipe.zadd(key, {str(now): now})
        
        # 设置过期时间
        pipe.expire(key, window)
        
        results = pipe.execute()
        current_count = results[1]
        
        return current_count <= limit, {
            "limit": limit,
            "remaining": max(0, limit - current_count),
            "reset": int(now + window)
        }
    
    def _check_in_memory(
        self,
        key: str,
        now: float,
        window_start: float,
        limit: int
    ) -> tuple[bool, Dict[str, int]]:
        """使用内存检查"""
        timestamps = self.in_memory_store[key]
        
        # 移除窗口外的记录
        timestamps[:] = [t for t in timestamps if t > window_start]
        
        # 检查是否超过限制
        current_count = len(timestamps)
        
        if current_count < limit:
            timestamps.append(now)
            return True, {
                "limit": limit,
                "remaining": limit - current_count - 1,
                "reset": int(now + (window - (now - timestamps[0]) if timestamps else window))
            }
        
        return False, {
            "limit": limit,
            "remaining": 0,
            "reset": int(timestamps[0] + window)
        }


# 限流策略配置
RATE_LIMITS = {
    "default": {
        "limit": 100,
        "window": 60  # 每分钟100次
    },
    "chat": {
        "limit": 30,
        "window": 60  # 每分钟30次
    },
    "generate_itinerary": {
        "limit": 5,
        "window": 300  # 每5分钟5次
    },
    "admin": {
        "limit": 200,
        "window": 60  # 每分钟200次
    }
}


# 全局限流器
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """获取限流器"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter("redis://localhost:6379/3")
    return _rate_limiter


async def rate_limit(request: Request, endpoint_type: str = "default"):
    """限流中间件"""
    limiter = get_rate_limiter()
    
    # 获取标识符（用户ID或IP）
    auth_header = request.headers.get("Authorization")
    identifier = request.client.host  # 默认使用IP
    
    if auth_header:
        # 尝试从JWT获取用户ID
        try:
            from core.security import decode_token
            scheme, credentials = get_authorization_scheme_param(auth_header)
            if scheme.lower() == "bearer":
                payload = decode_token(credentials)
                if payload:
                    identifier = payload.get("sub", identifier)
        except:
            pass
    
    # 获取限流配置
    config = RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])
    
    # 检查是否允许
    allowed, info = await limiter.is_allowed(
        identifier=identifier,
        endpoint=endpoint_type,
        limit=config["limit"],
        window=config["window"]
    )
    
    # 添加到响应头
    request.state.rate_limit = info
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
            headers={
                "X-RateLimit-Limit": str(info["limit"]),
                "X-RateLimit-Remaining": str(info["remaining"]),
                "X-RateLimit-Reset": str(info["reset"]),
                "Retry-After": str(info["reset"] - int(datetime.now().timestamp()))
            }
        )
