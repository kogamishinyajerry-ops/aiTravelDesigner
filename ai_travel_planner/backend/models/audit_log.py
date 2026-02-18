"""
审计日志模型
记录所有敏感操作
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean
from sqlalchemy.sql import func
from core.database import Base


class AuditLog(Base):
    """审计日志表"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 用户信息
    user_id = Column(String(100), index=True, nullable=True)
    username = Column(String(100))
    email = Column(String(200))
    
    # 操作信息
    action = Column(String(100), index=True)  # login, create_itinerary, delete_user等
    resource_type = Column(String(50))  # itinerary, user, attraction等
    resource_id = Column(String(100), index=True)
    
    # 请求信息
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    request_method = Column(String(10))
    request_path = Column(String(200))
    request_id = Column(String(100), unique=True)  # 追踪ID
    
    # 响应信息
    status_code = Column(Integer)
    success = Column(Boolean, default=True, index=True)
    error_message = Column(Text)
    
    # 变更信息
    changes = Column(JSON)  # 记录变更前后的数据
    sensitive_data_masked = Column(Boolean, default=True)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, user={self.username})>"
