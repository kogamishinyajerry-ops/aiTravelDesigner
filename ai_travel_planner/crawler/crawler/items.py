"""
爬虫数据项定义
"""
import scrapy


class AttractionItem(scrapy.Item):
    """景点数据项"""
    name = scrapy.Field()
    destination = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    address = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    ticket_price = scrapy.Field()
    opening_hours = scrapy.Field()
    recommended_duration = scrapy.Field()
    best_time_to_visit = scrapy.Field()
    image_urls = scrapy.Field()
    tags = scrapy.Field()
    source_url = scrapy.Field()
    source = scrapy.Field()  # 数据来源：ctrip, qunar, dianping等


class RestaurantItem(scrapy.Item):
    """餐厅数据项"""
    name = scrapy.Field()
    destination = scrapy.Field()
    cuisine_type = scrapy.Field()
    price_level = scrapy.Field()
    avg_price_per_person = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    opening_hours = scrapy.Field()
    specialties = scrapy.Field()
    image_urls = scrapy.Field()
    tags = scrapy.Field()
    source_url = scrapy.Field()
    source = scrapy.Field()


class DestinationItem(scrapy.Item):
    """目的地数据项"""
    name = scrapy.Field()
    name_en = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    best_season = scrapy.Field()
    suggested_days = scrapy.Field()
    avg_budget = scrapy.Field()
    rating = scrapy.Field()
    popularity_score = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()


class PriceItem(scrapy.Item):
    """价格数据项"""
    category = scrapy.Field()  # flight, hotel, attraction, restaurant
    origin = scrapy.Field()  # 出发地（用于机票）
    destination = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    provider = scrapy.Field()
    source_url = scrapy.Field()
    updated_at = scrapy.Field()
