"""
Scrapy中间件
用于处理请求和响应
"""
from scrapy import signals
from scrapy.exceptions import NotConfigured
import random


class RandomUserAgentMiddleware:
    """随机User-Agent中间件"""
    
    def __init__(self, user_agents):
        self.user_agents = user_agents
    
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('USER_AGENTS'):
            raise NotConfigured('USER_AGENTS setting is missing')
        return cls(crawler.settings.getlist('USER_AGENTS'))
    
    def process_request(self, request, spider):
        """为每个请求设置随机User-Agent"""
        request.headers['User-Agent'] = random.choice(self.user_agents)


class ProxyMiddleware:
    """代理中间件"""
    
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_index = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('PROXY_LIST', []))
    
    def process_request(self, request, spider):
        """为请求设置代理"""
        if self.proxy_list:
            proxy = self.proxy_list[self.current_index]
            request.meta['proxy'] = proxy
            self.current_index = (self.current_index + 1) % len(self.proxy_list)
    
    def process_exception(self, request, exception, spider):
        """处理代理异常"""
        # 可以在这里实现代理切换逻辑
        pass


class RetryMiddleware:
    """重试中间件"""
    
    def process_response(self, request, response, spider):
        """处理响应，决定是否重试"""
        # 检查HTTP状态码
        if response.status in [403, 429, 500, 502, 503, 504]:
            reason = f'HTTP {response.status}'
            return self._retry(request, reason, spider) or response
        
        return response
    
    def _retry(self, request, reason, spider):
        """重试请求"""
        retries = request.meta.get('retry_times', 0) + 1
        max_retries = request.meta.get('max_retry_times', spider.crawler.settings.get('RETRY_TIMES', 3))
        
        if retries <= max_retries:
            spider.logger.debug(f"Retrying {request.url} (failed {retries} times): {reason}")
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            return retryreq
        
        spider.logger.error(f"Gave up retrying {request.url} (failed {retries} times): {reason}")
        return None
