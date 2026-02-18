"""
增强的重试策略
实现指数退避、抖动、条件重试等高级特性
"""
import asyncio
import random
from typing import Callable, Optional, Type, Tuple, List
from functools import wraps
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class RetryStrategy(Enum):
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_DELAY = "fixed_delay"
    LINEAR_BACKOFF = "linear_backoff"
    FIBONACCI = "fibonacci"


@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    base_delay: float = 1.0  # 秒
    max_delay: float = 30.0  # 秒
    jitter: bool = True  # 添加随机抖动
    backoff_multiplier: float = 2.0
    retryable_exceptions: List[Type[Exception]] = None
    on_retry_callback: Optional[Callable] = None


class RetryPolicy:
    """重试策略"""
    
    def __init__(self, config: RetryConfig):
        self.config = config
        self.fib_cache = [1, 1]
    
    def get_delay(self, attempt: int) -> float:
        """获取重试延迟"""
        delay = self._calculate_delay(attempt)
        
        # 添加抖动避免惊群效应
        if self.config.jitter:
            delay = delay * (0.5 + random.random() * 0.5)
        
        return min(delay, self.config.max_delay)
    
    def _calculate_delay(self, attempt: int) -> float:
        """计算基础延迟"""
        if self.config.strategy == RetryStrategy.FIXED_DELAY:
            return self.config.base_delay
        
        elif self.config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return self.config.base_delay * (self.config.backoff_multiplier ** (attempt - 1))
        
        elif self.config.strategy == RetryStrategy.LINEAR_BACKOFF:
            return self.config.base_delay * attempt
        
        elif self.config.strategy == RetryStrategy.FIBONACCI:
            return self._get_fibonacci(attempt) * self.config.base_delay
        
        return self.config.base_delay
    
    def _get_fibonacci(self, n: int) -> int:
        """获取斐波那契数列"""
        while len(self.fib_cache) <= n:
            self.fib_cache.append(
                self.fib_cache[-1] + self.fib_cache[-2]
            )
        return self.fib_cache[n]
    
    def should_retry(self, exception: Exception) -> bool:
        """判断是否应该重试"""
        if self.config.retryable_exceptions is None:
            return True
        
        return any(
            isinstance(exception, exc_type)
            for exc_type in self.config.retryable_exceptions
        )


def retry(config: Optional[RetryConfig] = None):
    """重试装饰器"""
    if config is None:
        config = RetryConfig()
    
    policy = RetryPolicy(config)
    
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, config.max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    
                    if not policy.should_retry(e) or attempt == config.max_attempts:
                        logger.error(f"Retry failed after {attempt} attempts: {str(e)}")
                        raise
                    
                    delay = policy.get_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt} failed, retrying in {delay:.2f}s: {str(e)}"
                    )
                    
                    if config.on_retry_callback:
                        await config.on_retry_callback(attempt, e)
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, config.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    
                    if not policy.should_retry(e) or attempt == config.max_attempts:
                        logger.error(f"Retry failed after {attempt} attempts: {str(e)}")
                        raise
                    
                    delay = policy.get_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt} failed, retrying in {delay:.2f}s: {str(e)}"
                    )
                    
                    if config.on_retry_callback:
                        asyncio.run(config.on_retry_callback(attempt, e))
                    
                    asyncio.run(asyncio.sleep(delay))
            
            raise last_exception
        
        # 根据函数是否为协程返回不同的包装器
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# 使用示例
# @retry(config=RetryConfig(
#     max_attempts=5,
#     strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
#     retryable_exceptions=[
#         ConnectionError,
#         TimeoutError,
#         asyncio.TimeoutError
#     ]
# ))
# async def call_external_api(url: str):
#     """调用外部API"""
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.json()
