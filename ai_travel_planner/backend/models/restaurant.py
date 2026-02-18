"""
Restaurant Model
餐厅模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ARRAY, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Restaurant(Base):
    """餐厅表"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # 基本信息
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200))
    cuisine = Column(String(100))  # 菜系
    description = Column(String(1000))

    # 位置信息
    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

    # 价格和评分
    average_price = Column(Float, default=0.0)  # 人均消费
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # 分类和标签
    tags = Column(ARRAY(String))
    meal_types = Column(ARRAY(String))  # 早餐、午餐、晚餐

    # 营业信息
    opening_hours = Column(JSON)
    phone = Column(String(20))

    # 媒体资源
    images = Column(JSON, default=[])

    # 特色
    features = Column(JSON, default=[])  # 停车位、包间、户外等
    is_halal = Column(Integer, default=0)  # 是否清真
    is_vegetarian_friendly = Column(Integer, default=0)

    # 数据来源
    source = Column(String(50))
    source_id = Column(String(100))

    # 热度
    popularity_score = Column(Integer, default=0)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    crawl_time = Column(DateTime(timezone=True))

    # 关系
    destination = relationship("Destination", backref="restaurants")

    def __repr__(self):
        return f"<Restaurant(id={self.id}, name={self.name}, cuisine={self.cuisine})>"
