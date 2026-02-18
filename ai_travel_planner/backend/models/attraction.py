"""
Attraction Model
景点模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ARRAY, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Attraction(Base):
    """景点表"""
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # 基本信息
    name = Column(String(200), nullable=False, index=True)
    name_en = Column(String(200))
    type = Column(String(50), index=True)  # 自然风光、历史文化、娱乐休闲等
    description = Column(String(2000))

    # 位置信息
    address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

    # 票务信息
    ticket_price = Column(Float, default=0.0)
    opening_hours = Column(JSON)  # {"weekdays": "09:00-17:00", "weekends": "09:00-18:00"}
    suggested_duration = Column(Integer, default=120)  # 建议游览时长（分钟）

    # 评分和评价
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # 标签和分类
    tags = Column(ARRAY(String))
    best_visit_time = Column(String(50))

    # 媒体资源
    images = Column(JSON, default=[])
    videos = Column(JSON, default=[])

    # 热度
    popularity_score = Column(Integer, default=0)
    is_recommended = Column(Integer, default=0)  # 是否推荐

    # 实用信息
    tips = Column(JSON, default=[])  # 游览提示
    facilities = Column(JSON, default=[])  # 设施

    # 数据来源
    source = Column(String(50))  # ctrip, meituan等
    source_id = Column(String(100))

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    crawl_time = Column(DateTime(timezone=True))

    # 关系
    destination = relationship("Destination", backref="attractions")

    def __repr__(self):
        return f"<Attraction(id={self.id}, name={self.name}, type={self.type})>"
