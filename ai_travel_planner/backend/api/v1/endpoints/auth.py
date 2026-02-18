"""
认证授权API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta
from loguru import logger

from core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    get_current_user,
    UserRole
)
from core.config import settings

router = APIRouter()


class UserLogin(BaseModel):
    """用户登录请求"""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """用户注册请求"""
    email: EmailStr
    password: str
    username: str


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """用户信息响应"""
    id: str
    email: str
    username: str
    role: str


# 模拟用户数据库（实际应从数据库读取）
_mock_users = {
    "admin@example.com": {
        "id": "1",
        "email": "admin@example.com",
        "username": "admin",
        "password_hash": get_password_hash("admin123"),
        "role": UserRole.ADMIN
    },
    "user@example.com": {
        "id": "2",
        "email": "user@example.com",
        "username": "user",
        "password_hash": get_password_hash("user123"),
        "role": UserRole.USER
    }
}


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """
    用户注册
    
    - **email**: 邮箱地址
    - **password**: 密码
    - **username**: 用户名
    """
    # 检查邮箱是否已存在
    if user_data.email in _mock_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建用户
    user = {
        "id": str(len(_mock_users) + 1),
        "email": user_data.email,
        "username": user_data.username,
        "password_hash": get_password_hash(user_data.password),
        "role": UserRole.USER
    }
    _mock_users[user_data.email] = user
    
    logger.info(f"New user registered: {user_data.email}")
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        role=user["role"]
    )


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录
    
    - **username**: 邮箱地址
    - **password**: 密码
    """
    user = _mock_users.get(form_data.username)
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token = create_access_token(
        data={
            "sub": user["id"],
            "email": user["email"],
            "role": user["role"]
        }
    )
    
    # 创建刷新令牌
    refresh_token = create_refresh_token(
        data={
            "sub": user["id"],
            "email": user["email"]
        }
    )
    
    logger.info(f"User logged in: {user['email']}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60  # 30分钟
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    刷新访问令牌
    """
    # 创建新的访问令牌
    access_token = create_access_token(
        data={
            "sub": current_user["id"],
            "email": current_user["email"],
            "role": current_user["role"]
        }
    )
    
    # 创建新的刷新令牌
    refresh_token = create_refresh_token(
        data={
            "sub": current_user["id"],
            "email": current_user["email"]
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    # 从数据库获取完整用户信息
    user = None
    for u in _mock_users.values():
        if u["id"] == current_user["id"]:
            user = u
            break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        role=user["role"]
    )
