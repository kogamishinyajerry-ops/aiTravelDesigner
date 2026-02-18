"""
Scrapy数据管道
用于处理和存储爬取的数据
"""
import logging
from datetime import datetime
from items import AttractionItem, RestaurantItem, DestinationItem, PriceItem

logger = logging.getLogger(__name__)


class CleanDataPipeline:
    """数据清洗管道"""
    
    def process_item(self, item, spider):
        """清洗数据"""
        # 移除空值
        for key, value in item.items():
            if value is None or value == '':
                item[key] = None
        
        # 标准化字符串（去除首尾空格）
        for key in item.fields:
            if isinstance(item.get(key), str):
                item[key] = item[key].strip()
        
        # 处理数字字段
        if 'rating' in item and isinstance(item.get('rating'), str):
            try:
                item['rating'] = float(item['rating'])
            except:
                item['rating'] = None
        
        if 'price' in item or 'ticket_price' in item or 'avg_price_per_person' in item:
            price_field = next((k for k in item.fields if 'price' in k.lower()), None)
            if price_field and isinstance(item.get(price_field), str):
                try:
                    item[price_field] = float(item[price_field].replace('¥', '').replace('￥', '').replace(',', '').strip())
                except:
                    pass
        
        # 添加爬取时间
        item['crawled_at'] = datetime.now().isoformat()
        
        return item


class DatabasePipeline:
    """数据库存储管道"""
    
    def __init__(self):
        # TODO: 初始化数据库连接
        pass
    
    def open_spider(self, spider):
        """爬虫启动时调用"""
        logger.info(f"Spider {spider.name} started, connecting to database...")
        # TODO: 连接数据库
    
    def close_spider(self, spider):
        """爬虫关闭时调用"""
        logger.info(f"Spider {spider.name} finished, closing database connection...")
        # TODO: 关闭数据库连接
    
    def process_item(self, item, spider):
        """存储数据到数据库"""
        try:
            # TODO: 根据item类型存储到不同表
            
            if isinstance(item, AttractionItem):
                # 存储景点
                pass
            elif isinstance(item, RestaurantItem):
                # 存储餐厅
                pass
            elif isinstance(item, DestinationItem):
                # 存储目的地
                pass
            elif isinstance(item, PriceItem):
                # 存储价格
                pass
            
            logger.debug(f"Saved item: {item.get('name', 'N/A')}")
            return item
            
        except Exception as e:
            logger.error(f"Error saving item: {e}")
            # 可以选择抛出异常丢弃item，或返回item继续处理
            raise


class DeduplicatePipeline:
    """去重管道"""
    
    def __init__(self):
        self.seen = set()
    
    def process_item(self, item, spider):
        """基于唯一标识去重"""
        # 生成唯一标识
        unique_key = self._get_unique_key(item)
        
        if unique_key in self.seen:
            logger.debug(f"Duplicate item skipped: {unique_key}")
            return None  # 返回None表示丢弃item
        
        self.seen.add(unique_key)
        return item
    
    def _get_unique_key(self, item):
        """生成唯一标识"""
        # 对于景点：source + name + destination
        if isinstance(item, AttractionItem):
            return f"{item.get('source')}_{item.get('name')}_{item.get('destination')}"
        
        # 对于餐厅：source + name + address
        if isinstance(item, RestaurantItem):
            return f"{item.get('source')}_{item.get('name')}_{item.get('address')}"
        
        # 对于目的地：name + city
        if isinstance(item, DestinationItem):
            return f"{item.get('name')}_{item.get('city')}"
        
        # 对于价格：category + origin + destination + date + provider
        if isinstance(item, PriceItem):
            return f"{item.get('category')}_{item.get('origin')}_{item.get('destination')}_{item.get('date')}_{item.get('provider')}"
        
        return str(hash(str(dict(item))))


class ValidatePipeline:
    """数据验证管道"""
    
    def process_item(self, item, spider):
        """验证数据完整性"""
        
        # 必填字段检查
        required_fields = {
            AttractionItem: ['name', 'destination'],
            RestaurantItem: ['name', 'destination'],
            DestinationItem: ['name', 'city'],
            PriceItem: ['category', 'destination', 'date', 'price'],
        }
        
        item_type = type(item)
        if item_type in required_fields:
            for field in required_fields[item_type]:
                if not item.get(field):
                    logger.warning(f"Missing required field '{field}' in item: {item.get('name', 'N/A')}")
                    # 可以选择返回None丢弃，或继续处理
        
        # 数据范围检查
        if 'rating' in item and item.get('rating'):
            if item['rating'] < 0 or item['rating'] > 5:
                logger.warning(f"Invalid rating {item['rating']} for {item.get('name', 'N/A')}")
        
        if 'latitude' in item and item.get('latitude'):
            if item['latitude'] < -90 or item['latitude'] > 90:
                logger.warning(f"Invalid latitude {item['latitude']} for {item.get('name', 'N/A')}")
        
        return item
