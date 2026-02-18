"""
Destination Model
目的地模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ARRAY
from sqlalchemy.sql import func
from core.database import Base


class Destination(Base):
    """目的地表"""
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, index=True)
    name_en = Column(String(100))
    province = Column(String(50), index=True)
    country = Column(String(50), default="中国")

    # 地理位置（PostGIS扩展）
    latitude = Column(Float)
    longitude = Column(Float)

    # 描述信息
    description = Column(String(1000))
    tags = Column(ARRAY(String))

    # 旅行信息
    best_season = Column(String(50))
    average_budget = Column(Float)  # 人均预算
    suggested_days = Column(Integer)  # 建议游玩天数

    # 热度和评分
    popularity_score = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # 媒体资源
    images = Column(JSON, default=[])
    videos = Column(JSON, default=[])

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Destination(id={self.id}, name={self.name}, province={self.province})>"
