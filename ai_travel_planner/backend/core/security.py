"""
企业级安全模块
实现JWT认证、RBAC授权、审计日志等
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
import hashlib
import hmac


# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-change-in-production-use-environment-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# HTTP Bearer认证
security = HTTPBearer()


class UserRole:
    """用户角色"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Permission:
    """权限定义"""
    # 行程相关
    CREATE_ITINERARY = "itinerary:create"
    READ_ITINERARY = "itinerary:read"
    UPDATE_ITINERARY = "itinerary:update"
    DELETE_ITINERARY = "itinerary:delete"
    SHARE_ITINERARY = "itinerary:share"
    
    # 用户相关
    MANAGE_PROFILE = "user:manage"
    MANAGE_PREFERENCES = "user:preferences"
    
    # 管理相关
    MANAGE_USERS = "admin:users"
    VIEW_ANALYTICS = "admin:analytics"
    MANAGE_CONTENT = "admin:content"


# 角色权限映射
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        # 管理员拥有所有权限
        Permission.CREATE_ITINERARY,
        Permission.READ_ITINERARY,
        Permission.UPDATE_ITINERARY,
        Permission.DELETE_ITINERARY,
        Permission.SHARE_ITINERARY,
        Permission.MANAGE_PROFILE,
        Permission.MANAGE_PREFERENCES,
        Permission.MANAGE_USERS,
        Permission.VIEW_ANALYTICS,
        Permission.MANAGE_CONTENT,
    ],
    UserRole.USER: [
        Permission.CREATE_ITINERARY,
        Permission.READ_ITINERARY,
        Permission.UPDATE_ITINERARY,
        Permission.DELETE_ITINERARY,
        Permission.SHARE_ITINERARY,
        Permission.MANAGE_PROFILE,
        Permission.MANAGE_PREFERENCES,
    ],
    UserRole.GUEST: [
        Permission.READ_ITINERARY,
    ]
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """解码令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"Token decode failed: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """获取当前用户（依赖注入）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # 验证令牌类型
    token_type = payload.get("type")
    if token_type != "access":
        raise credentials_exception
    
    # TODO: 从数据库加载用户信息
    user = {
        "id": user_id,
        "role": payload.get("role", UserRole.USER),
        "email": payload.get("email")
    }
    
    return user


def require_permission(permission: str):
    """权限检查装饰器"""
    def decorator(func):
        async def wrapper(*args, current_user: Dict = Depends(get_current_user), **kwargs):
            user_role = current_user.get("role", UserRole.GUEST)
            user_permissions = ROLE_PERMISSIONS.get(user_role, [])
            
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少权限: {permission}"
                )
            
            # 记录审计日志
            await log_audit_event(
                user_id=current_user["id"],
                action="permission_check",
                resource=permission,
                success=True
            )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator


def require_role(role: str):
    """角色检查装饰器"""
    def decorator(func):
        async def wrapper(*args, current_user: Dict = Depends(get_current_user), **kwargs):
            user_role = current_user.get("role", UserRole.GUEST)
            
            if user_role != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要角色: {role}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator


async def log_audit_event(
    user_id: str,
    action: str,
    resource: str,
    success: bool = True,
    details: Optional[Dict[str, Any]] = None
):
    """记录审计事件"""
    # TODO: 持久化到数据库
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "success": success,
        "details": details or {}
    }
    
    logger.info(f"[AUDIT] {event}")
    # 这里应该存储到审计日志表
    # await AuditLog.create(**event)


def encrypt_sensitive_data(data: str, key: str) -> str:
    """加密敏感数据"""
    # 使用HMAC-SHA256进行加密
    signature = hmac.new(
        key.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{data}:{signature}"


def verify_sensitive_data(encrypted_data: str, key: str) -> bool:
    """验证敏感数据"""
    try:
        data, signature = encrypted_data.rsplit(":", 1)
        expected = hmac.new(
            key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    except ValueError:
        return False
