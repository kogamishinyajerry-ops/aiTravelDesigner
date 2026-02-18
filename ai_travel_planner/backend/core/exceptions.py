"""
增强的异常处理
提供更详细的错误信息和恢复建议
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger
import traceback


class ErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    BUSINESS_LOGIC_ERROR = "business_logic_error"
    EXTERNAL_SERVICE_ERROR = "external_service_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    INTERNAL_ERROR = "internal_error"


@dataclass
class ErrorDetail:
    """错误详情"""
    code: str
    type: ErrorType
    message: str
    details: Optional[Dict[str, Any]] = None
    suggestions: List[str] = None
    trace_id: Optional[str] = None


class TravelPlannerException(Exception):
    """自定义异常基类"""
    
    def __init__(
        self,
        message: str,
        error_type: ErrorType = ErrorType.INTERNAL_ERROR,
        code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
        suggestions: List[str] = None
    ):
        self.message = message
        self.error_type = error_type
        self.code = code
        self.details = details
        self.suggestions = suggestions or []
        super().__init__(message)


class ValidationError(TravelPlannerException):
    """验证错误"""
    
    def __init__(
        self,
        message: str,
        field: str,
        invalid_value: Any = None
    ):
        super().__init__(
            message=message,
            error_type=ErrorType.VALIDATION_ERROR,
            code="VALIDATION_ERROR",
            details={"field": field, "invalid_value": str(invalid_value)},
            suggestions=[
                "请检查输入参数的格式",
                "参考API文档中的参数说明"
            ]
        )


class ExternalServiceError(TravelPlannerException):
    """外部服务错误"""
    
    def __init__(
        self,
        service_name: str,
        message: str,
        retry_after: Optional[int] = None
    ):
        super().__init__(
            message=f"{service_name}服务不可用: {message}",
            error_type=ErrorType.EXTERNAL_SERVICE_ERROR,
            code="EXTERNAL_SERVICE_ERROR",
            details={
                "service": service_name,
                "retry_after": retry_after
            },
            suggestions=[
                "请稍后重试",
                "如果问题持续，请联系客服"
            ]
        )


class RateLimitError(TravelPlannerException):
    """限流错误"""
    
    def __init__(
        self,
        limit: int,
        window: int,
        reset_at: int
    ):
        super().__init__(
            message="请求过于频繁，请稍后再试",
            error_type=ErrorType.RATE_LIMIT_ERROR,
            code="RATE_LIMIT_EXCEEDED",
            details={
                "limit": limit,
                "window": window,
                "reset_at": reset_at
            },
            suggestions=[
                f"请在{reset_at}秒后重试",
                "升级套餐以提高限流上限"
            ]
        )


async def handle_travel_planner_exception(
    request: Request,
    exc: TravelPlannerException
) -> JSONResponse:
    """处理自定义异常"""
    trace_id = getattr(request.state, "trace_id", "unknown")
    
    error_detail = ErrorDetail(
        code=exc.code,
        type=exc.error_type,
        message=exc.message,
        details=exc.details,
        suggestions=exc.suggestions,
        trace_id=trace_id
    )
    
    # 根据错误类型确定HTTP状态码
    status_map = {
        ErrorType.VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
        ErrorType.BUSINESS_LOGIC_ERROR: status.HTTP_400_BAD_REQUEST,
        ErrorType.AUTHENTICATION_ERROR: status.HTTP_401_UNAUTHORIZED,
        ErrorType.AUTHORIZATION_ERROR: status.HTTP_403_FORBIDDEN,
        ErrorType.RATE_LIMIT_ERROR: status.HTTP_429_TOO_MANY_REQUESTS,
        ErrorType.EXTERNAL_SERVICE_ERROR: status.HTTP_503_SERVICE_UNAVAILABLE,
        ErrorType.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    
    http_status = status_map.get(exc.error_type, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 记录错误日志
    logger.error(
        f"Exception occurred: {exc.code} - {exc.message}",
        extra={
            "trace_id": trace_id,
            "details": exc.details,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=http_status,
        content={
            "error": {
                "code": error_detail.code,
                "type": error_detail.type.value,
                "message": error_detail.message,
                "details": error_detail.details,
                "suggestions": error_detail.suggestions
            },
            "trace_id": trace_id
        }
    )


async def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
    """处理通用异常"""
    trace_id = getattr(request.state, "trace_id", "unknown")
    
    # 记录完整错误堆栈
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "trace_id": trace_id,
            "path": request.url.path,
            "traceback": traceback.format_exc()
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "type": "internal_error",
                "message": "服务器内部错误",
                "details": None,
                "suggestions": [
                    "请稍后重试",
                    "如果问题持续，请联系技术支持"
                ]
            },
            "trace_id": trace_id
        }
    )


# 追踪中间件
async def add_trace_id(request: Request, call_next):
    """添加追踪ID"""
    import uuid
    request.state.trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Trace-ID"] = request.state.trace_id
    return response
