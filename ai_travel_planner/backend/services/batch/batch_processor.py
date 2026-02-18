"""
批量处理优化
提高大规模数据处理的效率
"""
import asyncio
from typing import List, Any, Callable, Optional
from dataclasses import dataclass
import math
from loguru import logger


@dataclass
class BatchConfig:
    """批量配置"""
    batch_size: int = 100
    max_concurrent_batches: int = 5
    delay_between_batches: float = 0.1


class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, config: BatchConfig):
        self.config = config
        self.semaphore = asyncio.Semaphore(config.max_concurrent_batches)
    
    async def process_items(
        self,
        items: List[Any],
        processor: Callable[[List[Any]], Any],
        progress_callback: Optional[Callable] = None
    ) -> List[Any]:
        """批量处理项目"""
        total_items = len(items)
        num_batches = math.ceil(total_items / self.config.batch_size)
        
        results = []
        
        for i in range(num_batches):
            batch = items[i * self.config.batch_size:(i + 1) * self.config.batch_size]
            
            async with self.semaphore:
                result = await processor(batch)
                results.extend(result)
            
            # 报告进度
            if progress_callback:
                progress = ((i + 1) / num_batches) * 100
                progress_callback(progress, i + 1, num_batches)
            
            # 批次间延迟
            if i < num_batches - 1:
                await asyncio.sleep(self.config.delay_between_batches)
        
        return results
    
    async def process_items_with_retry(
        self,
        items: List[Any],
        processor: Callable[[List[Any]], Any],
        max_retries: int = 3
    ) -> List[Any]:
        """带重试的批量处理"""
        results = []
        failed_items = items
        retry_count = 0
        
        while failed_items and retry_count < max_retries:
            new_results, failed_items = await self._process_and_filter(
                failed_items, processor
            )
            results.extend(new_results)
            retry_count += 1
        
        # 记录最终失败的项目
        if failed_items:
            logger.warning(f"Failed to process {len(failed_items)} items after {max_retries} retries")
        
        return results
    
    async def _process_and_filter(
        self,
        items: List[Any],
        processor: Callable
    ) -> tuple[List[Any], List[Any]]:
        """处理并过滤失败项"""
        success_results = []
        failed_items = []
        
        for item in items:
            try:
                result = await processor([item])
                success_results.extend(result)
            except Exception as e:
                logger.error(f"Processing failed for item {item}: {e}")
                failed_items.append(item)
        
        return success_results, failed_items
