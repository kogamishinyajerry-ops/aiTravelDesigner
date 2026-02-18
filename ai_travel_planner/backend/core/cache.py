"""
智能缓存层
支持多级缓存、缓存预热、缓存失效策略
"""
from typing import Any, Optional, Callable, Dict, List
from datetime import timedelta
from enum import Enum
import hashlib
import json
import redis
import asyncio
from functools import wraps
from loguru import logger


class CacheStrategy(Enum):
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    TTL = "ttl"


class CacheConfig:
    """缓存配置"""
    def __init__(
        self,
        ttl: int = 3600,
        strategy: CacheStrategy = CacheStrategy.TTL,
        prefix: str = "app"
    ):
        self.ttl = ttl
        self.strategy = strategy
        self.prefix = prefix


class CacheBackend(ABC):
    """缓存后端抽象"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass


class RedisCache:
    """Redis缓存实现"""
    
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url, decode_responses=True)
    
    def _serialize(self, value: Any) -> str:
        """序列化"""
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> Any:
        """反序列化"""
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return self._deserialize(value)
        except Exception as e:
            logger.error(f"Cache get failed: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        try:
            serialized = self._serialize(value)
            if ttl:
                self.client.setex(key, ttl, serialized)
            else:
                self.client.set(key, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache set failed: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete failed: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists check failed: {e}")
            return False
    
    async def get_pattern(self, pattern: str) -> List[str]:
        """获取匹配的所有键"""
        try:
            return self.client.keys(pattern)
        except Exception as e:
            logger.error(f"Cache pattern search failed: {e}")
            return []
    
    async def invalidate_pattern(self, pattern: str):
        """使匹配模式的所有缓存失效"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache entries matching {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation failed: {e}")


class MultiLevelCache:
    """多级缓存（内存 + Redis）"""
    
    def __init__(
        self,
        redis_url: str,
        memory_size: int = 1000,
        memory_ttl: int = 60
    ):
        self.redis = RedisCache(redis_url)
        self.memory_cache: Dict[str, tuple[Any, float]] = {}
        self.memory_size = memory_size
        self.memory_ttl = memory_ttl
    
    def _generate_key(self, prefix: str, *args) -> str:
        """生成缓存键"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ":".join(key_parts)
    
    def _hash_key(self, key: str) -> str:
        """哈希键"""
        return hashlib.md5(key.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存（先查内存，再查Redis）"""
        # 1. 检查内存缓存
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if expiry > asyncio.get_event_loop().time():
                logger.debug(f"Memory cache hit: {key}")
                return value
            else:
                del self.memory_cache[key]
        
        # 2. 检查Redis缓存
        value = await self.redis.get(key)
        if value is not None:
            logger.debug(f"Redis cache hit: {key}")
            # 回写到内存缓存
            self._set_memory(key, value)
            return value
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存"""
        # 设置Redis缓存
        success = await self.redis.set(key, value, ttl)
        
        # 设置内存缓存
        self._set_memory(key, value)
        
        return success
    
    def _set_memory(self, key: str, value: Any):
        """设置内存缓存"""
        loop = asyncio.get_event_loop()
        expiry = loop.time() + self.memory_ttl
        
        # 如果超过大小限制，淘汰旧项
        if len(self.memory_cache) >= self.memory_size:
            oldest_key = min(
                self.memory_cache.keys(),
                key=lambda k: self.memory_cache[k][1]
            )
            del self.memory_cache[oldest_key]
        
        self.memory_cache[key] = (value, expiry)
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        self.memory_cache.pop(key, None)
        return await self.redis.delete(key)
    
    async def invalidate_pattern(self, pattern: str):
        """使匹配模式的所有缓存失效"""
        # 删除内存缓存
        keys_to_delete = [k for k in self.memory_cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self.memory_cache[key]
        
        # 删除Redis缓存
        await self.redis.invalidate_pattern(pattern)


# 全局缓存实例
_cache = None


def get_cache() -> MultiLevelCache:
    """获取缓存实例"""
    global _cache
    if _cache is None:
        _cache = MultiLevelCache("redis://localhost:6379/0")
    return _cache


def cached(
    ttl: int = 3600,
    key_prefix: str = "cache",
    vary_by: Optional[List[str]] = None
):
    """缓存装饰器"""
    cache = get_cache()
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            key_parts = [key_prefix, func.__name__]
            
            if vary_by:
                for arg_name in vary_by:
                    if arg_name in kwargs:
                        key_parts.append(str(kwargs[arg_name]))
            
            cache_key = ":".join(key_parts)
            
            # 尝试从缓存获取
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 缓存结果
            await cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator


# 使用示例
# @cached(ttl=1800, key_prefix="attractions", vary_by=["destination"])
# async def get_attractions(destination: str) -> List[Dict]:
#     """获取景点列表（带缓存）"""
#     # 实际查询逻辑
#     # return await db.query(Attraction).filter(Attraction.destination == destination).all()
#     return []
