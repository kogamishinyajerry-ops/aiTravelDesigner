"""
携程景点爬虫 - 示例实现
注意：实际使用时需要遵守网站的robots.txt和反爬策略
"""
import scrapy
from items import AttractionItem
import re
import json


class CtripAttractionSpider(scrapy.Spider):
    """携程景点爬虫"""
    
    name = 'ctrip_attraction'
    allowed_domains = ['you.ctrip.com', 'ctrip.com']
    start_urls = [
        'https://you.ctrip.com/sight/kyoto1.html',  # 京都景点
        'https://you.ctrip.com/sight/tokyo1.html',   # 东京景点
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 4,
    }
    
    def __init__(self, destination='kyoto', *args, **kwargs):
        super(CtripAttractionSpider, self).__init__(*args, **kwargs)
        self.destination = destination
        self.base_url = f'https://you.ctrip.com/sight/{destination}1.html'
    
    def start_requests(self):
        """生成初始请求"""
        yield scrapy.Request(
            url=self.base_url,
            callback=self.parse_list,
            meta={'page': 1}
        )
    
    def parse_list(self, response):
        """解析景点列表页"""
        # TODO: 根据实际网页结构调整选择器
        # 这里是示例代码，实际使用时需要分析网页结构
        
        # 提取景点链接
        # attraction_links = response.css('.list-item a::attr(href)').getall()
        attraction_links = self._extract_attraction_links(response)
        
        for link in attraction_links:
            yield response.follow(
                link,
                callback=self.parse_detail
            )
        
        # 翻页
        # next_page = response.css('.next::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse_list)
    
    def parse_detail(self, response):
        """解析景点详情页"""
        item = AttractionItem()
        
        # TODO: 根据实际网页结构调整选择器
        
        # 提取基本信息
        item['name'] = self._extract_text(response, 'h1.title')
        item['description'] = self._extract_text(response, '.description')
        
        # 提取评分和评论数
        item['rating'] = self._extract_rating(response)
        item['review_count'] = self._extract_review_count(response)
        
        # 提取价格
        item['ticket_price'] = self._extract_price(response)
        
        # 提取开放时间
        item['opening_hours'] = self._extract_opening_hours(response)
        
        # 提取建议游览时长
        item['recommended_duration'] = self._extract_duration(response)
        
        # 提取位置信息
        location = self._extract_location(response)
        item['latitude'] = location.get('latitude')
        item['longitude'] = location.get('longitude')
        item['address'] = location.get('address')
        
        # 提取图片
        item['image_urls'] = self._extract_images(response)
        
        # 提取标签
        item['tags'] = self._extract_tags(response)
        
        # 提取分类
        item['category'] = self._extract_category(response)
        
        # 设置元数据
        item['destination'] = self.destination
        item['source'] = 'ctrip'
        item['source_url'] = response.url
        
        yield item
    
    def _extract_attraction_links(self, response):
        """提取景点链接（示例）"""
        # 实际实现需要分析网页结构
        return []
    
    def _extract_text(self, response, selector):
        """提取文本"""
        element = response.css(selector).get()
        return element.strip() if element else None
    
    def _extract_rating(self, response):
        """提取评分"""
        rating_text = response.css('.rating::text').get()
        if rating_text:
            match = re.search(r'(\d+\.?\d*)', rating_text)
            if match:
                return float(match.group(1))
        return None
    
    def _extract_review_count(self, response):
        """提取评论数"""
        count_text = response.css('.review-count::text').get()
        if count_text:
            match = re.search(r'(\d+)', count_text)
            if match:
                return int(match.group(1))
        return 0
    
    def _extract_price(self, response):
        """提取门票价格"""
        price_text = response.css('.price::text').get()
        if price_text:
            match = re.search(r'(\d+)', price_text)
            if match:
                return float(match.group(1))
        return None
    
    def _extract_opening_hours(self, response):
        """提取开放时间"""
        # 示例：返回一个字典
        return {
            'mon': '09:00-17:00',
            'tue': '09:00-17:00',
            'wed': '09:00-17:00',
            'thu': '09:00-17:00',
            'fri': '09:00-17:00',
            'sat': '09:00-17:00',
            'sun': '09:00-17:00',
        }
    
    def _extract_duration(self, response):
        """提取建议游览时长"""
        duration_text = response.css('.duration::text').get()
        if duration_text:
            match = re.search(r'(\d+)\s*[小时hourh]', duration_text, re.IGNORECASE)
            if match:
                return int(match.group(1)) * 60  # 转换为分钟
        return 90  # 默认90分钟
    
    def _extract_location(self, response):
        """提取位置信息"""
        # 尝试从JavaScript数据中提取
        script_text = response.text
        lat_match = re.search(r'"lat"\s*:\s*([-\d.]+)', script_text)
        lon_match = re.search(r'"lng"\s*:\s*([-\d.]+)', script_text)
        
        location = {}
        if lat_match:
            location['latitude'] = float(lat_match.group(1))
        if lon_match:
            location['longitude'] = float(lon_match.group(1))
        
        address = response.css('.address::text').get()
        if address:
            location['address'] = address.strip()
        
        return location
    
    def _extract_images(self, response):
        """提取图片URL"""
        images = response.css('.gallery img::attr(src)').getall()
        return [img for img in images if img]
    
    def _extract_tags(self, response):
        """提取标签"""
        tags = response.css('.tags a::text').getall()
        return [tag.strip() for tag in tags if tag.strip()]
    
    def _extract_category(self, response):
        """提取分类"""
        category = response.css('.category::text').get()
        return category.strip() if category else None


# 示例：使用方式
# scrapy crawl ctrip_attraction -a destination=kyoto
