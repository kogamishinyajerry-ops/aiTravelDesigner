"""
User Model
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(255))
    phone = Column(String(20))

    # 偏好设置（JSON格式）
    preferences = Column(JSON, default={})

    # 统计信息
    total_trips = Column(Integer, default=0)
    favorite_destinations = Column(JSON, default=[])

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))

    # 账户状态
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
