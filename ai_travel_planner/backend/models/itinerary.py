"""
Itinerary Model
行程模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class Itinerary(Base):
    """行程表"""
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # 基本信息
    name = Column(String(200), nullable=False)
    description = Column(String(1000))

    # 行程时间
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False)
    days = Column(Integer, nullable=False)

    # 出行信息
    travelers = Column(Integer, default=1)
    traveler_types = Column(JSON, default=[])  # 成人、儿童

    # 预算信息
    total_budget = Column(Float)
    actual_cost = Column(Float)
    budget_breakdown = Column(JSON)  # 详细预算分解

    # 行程数据（JSON格式，存储完整行程）
    itinerary_data = Column(JSON, nullable=False)

    # 状态
    status = Column(String(20), default="planning")  # planning, booked, ongoing, completed, cancelled

    # 偏好
    preferences = Column(JSON, default={})
    tags = Column(JSON, default=[])

    # 统计
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)

    # 分享
    is_public = Column(Integer, default=0)
    share_code = Column(String(50), unique=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # 关系
    user = relationship("User", backref="itineraries")
    destination = relationship("Destination", backref="itineraries")

    def __repr__(self):
        return f"<Itinerary(id={self.id}, name={self.name}, user_id={self.user_id})>"
