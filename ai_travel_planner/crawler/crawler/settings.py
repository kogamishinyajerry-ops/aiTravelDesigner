"""
Scrapy爬虫配置文件
"""
BOT_NAME = 'ai_travel_planner_crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# 遵守robots.txt规则
ROBOTSTXT_OBEY = False

# 并发请求数
CONCURRENT_REQUESTS = 16

# 下载延迟
DOWNLOAD_DELAY = 2

# 禁用Cookie
COOKIES_ENABLED = False

# User-Agent设置
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# 启用Item Pipeline
ITEM_PIPELINES = {
    'crawler.pipelines.CleanDataPipeline': 300,
    'crawler.pipelines.DatabasePipeline': 400,
}

# 日志级别
LOG_LEVEL = 'INFO'

# 重试次数
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 请求超时
DOWNLOAD_TIMEOUT = 30

# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# 禁用默认的UserAgent中间件
USER_AGENT_MIDDLEWARE = None

# 数据库配置
DATABASE_URL = 'sqlite:///./ai_travel_planner.db'

# 代理配置（可选）
PROXY_LIST = []

# Redis配置（用于分布式爬虫）
REDIS_URL = 'redis://localhost:6379/1'
