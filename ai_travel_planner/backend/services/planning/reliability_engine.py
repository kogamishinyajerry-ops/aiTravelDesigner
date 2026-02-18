"""
可靠性引擎 - 基于PLTR哲学的核心组件
实现数据验证、异常处理、降级策略和系统自愈
"""
import json
import traceback
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger
import asyncio


class HealthStatus(Enum):
    """系统健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ReliabilityLevel(Enum):
    """可靠性级别"""
    CRITICAL = 1  # 关键路径，必须有结果
    IMPORTANT = 2  # 重要但可降级
    OPTIONAL = 3  # 可选功能


@dataclass
class ServiceMetrics:
    """服务指标"""
    name: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    last_error: Optional[str] = None
    last_success: Optional[datetime] = None
    error_rate: float = 0.0
    consecutive_failures: int = 0


@dataclass
class ValidationRule:
    """验证规则"""
    field: str
    required: bool = True
    type_check: Optional[type] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[Any]] = None
    custom_validator: Optional[callable] = None


class CircuitBreaker:
    """熔断器 - 防止级联故障"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def record_success(self):
        """记录成功调用"""
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logger.info("Circuit breaker transitioned to CLOSED")
    
    def record_failure(self):
        """记录失败调用"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
    
    def allow_request(self) -> bool:
        """检查是否允许请求"""
        if self.state == "CLOSED":
            return True
        
        if self.state == "OPEN":
            if (datetime.now() - self.last_failure_time).seconds >= self.timeout:
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker transitioned to HALF_OPEN")
                return True
            return False
        
        if self.state == "HALF_OPEN":
            return True
        
        return False


class DataValidator:
    """数据验证器 - 确保数据质量"""
    
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {}
    
    def add_rule(self, entity_type: str, rule: ValidationRule):
        """添加验证规则"""
        if entity_type not in self.rules:
            self.rules[entity_type] = []
        self.rules[entity_type].append(rule)
    
    def validate(
        self,
        data: Dict[str, Any],
        entity_type: str
    ) -> tuple[bool, List[str]]:
        """
        验证数据
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        if entity_type not in self.rules:
            logger.warning(f"No validation rules for entity type: {entity_type}")
            return True, []
        
        for rule in self.rules[entity_type]:
            # 检查必需字段
            if rule.required and rule.field not in data:
                errors.append(f"Missing required field: {rule.field}")
                continue
            
            if rule.field not in data:
                continue
            
            value = data[rule.field]
            
            # 类型检查
            if rule.type_check and not isinstance(value, rule.type_check):
                errors.append(f"Field {rule.field} should be {rule.type_check}")
                continue
            
            # 数值范围检查
            if rule.min_value is not None and value < rule.min_value:
                errors.append(f"Field {rule.field} below minimum: {rule.min_value}")
            
            if rule.max_value is not None and value > rule.max_value:
                errors.append(f"Field {rule.field} exceeds maximum: {rule.max_value}")
            
            # 允许值检查
            if rule.allowed_values and value not in rule.allowed_values:
                errors.append(f"Field {rule.field} not in allowed values: {rule.allowed_values}")
            
            # 自定义验证
            if rule.custom_validator:
                try:
                    is_valid, error_msg = rule.custom_validator(value)
                    if not is_valid:
                        errors.append(error_msg)
                except Exception as e:
                    errors.append(f"Custom validation failed for {rule.field}: {str(e)}")
        
        return len(errors) == 0, errors


class FallbackManager:
    """降级管理器 - 提供优雅降级"""
    
    def __init__(self):
        self.fallback_handlers: Dict[str, callable] = {}
    
    def register_fallback(self, service_name: str, handler: callable):
        """注册降级处理器"""
        self.fallback_handlers[service_name] = handler
        logger.info(f"Registered fallback handler for: {service_name}")
    
    async def execute_with_fallback(
        self,
        service_name: str,
        primary_operation: callable,
        *args,
        **kwargs
    ) -> Any:
        """
        执行操作，失败时降级
        
        Args:
            service_name: 服务名称
            primary_operation: 主要操作函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            操作结果或降级结果
        """
        try:
            result = await primary_operation(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Primary operation failed for {service_name}: {str(e)}")
            
            if service_name in self.fallback_handlers:
                logger.info(f"Executing fallback for {service_name}")
                try:
                    fallback_result = await self.fallback_handlers[service_name](*args, **kwargs)
                    logger.info(f"Fallback succeeded for {service_name}")
                    return fallback_result
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed for {service_name}: {str(fallback_error)}")
            
            # 返回安全默认值
            return self._get_safe_default(service_name)
    
    def _get_safe_default(self, service_name: str) -> Any:
        """获取安全的默认返回值"""
        defaults = {
            "attraction_service": [],
            "restaurant_service": None,
            "budget_service": {
                "total": 0,
                "breakdown": {}
            },
            "llm_service": {
                "message": "服务暂时不可用，请稍后重试"
            }
        }
        return defaults.get(service_name, None)


class ReliabilityEngine:
    """可靠性引擎 - 综合管理可靠性"""
    
    def __init__(self):
        self.validators: Dict[str, DataValidator] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fallback_manager = FallbackManager()
        self.metrics: Dict[str, ServiceMetrics] = {}
        self.health_status: HealthStatus = HealthStatus.HEALTHY
        self.check_interval = 30  # 秒
        
        # 初始化默认验证器
        self._init_default_validators()
        self._init_default_circuit_breakers()
        
        # 启动健康检查
        self._start_health_check()
    
    def _init_default_validators(self):
        """初始化默认验证规则"""
        # 行程请求验证
        itinerary_validator = DataValidator()
        itinerary_validator.add_rule("itinerary_request", ValidationRule(
            field="destination",
            required=True,
            type_check=str
        ))
        itinerary_validator.add_rule("itinerary_request", ValidationRule(
            field="days",
            required=True,
            type_check=int,
            min_value=1,
            max_value=30
        ))
        itinerary_validator.add_rule("itinerary_request", ValidationRule(
            field="start_date",
            required=True,
            type_check=str
        ))
        itinerary_validator.add_rule("itinerary_request", ValidationRule(
            field="travelers",
            required=True,
            type_check=int,
            min_value=1,
            max_value=50
        ))
        self.validators["itinerary"] = itinerary_validator
        
        # 聊天请求验证
        chat_validator = DataValidator()
        chat_validator.add_rule("chat_request", ValidationRule(
            field="message",
            required=True,
            type_check=str
        ))
        self.validators["chat"] = chat_validator
    
    def _init_default_circuit_breakers(self):
        """初始化默认熔断器"""
        self.circuit_breakers["llm_service"] = CircuitBreaker(failure_threshold=3, timeout=60)
        self.circuit_breakers["attraction_service"] = CircuitBreaker(failure_threshold=5, timeout=30)
        self.circuit_breakers["budget_service"] = CircuitBreaker(failure_threshold=5, timeout=30)
    
    def _start_health_check(self):
        """启动健康检查任务"""
        asyncio.create_task(self._health_check_loop())
    
    async def _health_check_loop(self):
        """健康检查循环"""
        while True:
            try:
                await asyncio.sleep(self.check_interval)
                await self._check_health()
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
    
    async def _check_health(self):
        """检查系统健康状态"""
        unhealthy_services = []
        degraded_services = []
        
        for service_name, metrics in self.metrics.items():
            if metrics.error_rate > 0.5:  # 错误率超过50%
                unhealthy_services.append(service_name)
            elif metrics.error_rate > 0.2:  # 错误率超过20%
                degraded_services.append(service_name)
        
        if unhealthy_services:
            self.health_status = HealthStatus.UNHEALTHY
            logger.error(f"System UNHEALTHY. Failed services: {unhealthy_services}")
        elif degraded_services:
            self.health_status = HealthStatus.DEGRADED
            logger.warning(f"System DEGRADED. Degraded services: {degraded_services}")
        else:
            self.health_status = HealthStatus.HEALTHY
    
    def record_request(
        self,
        service_name: str,
        success: bool,
        response_time: float = None,
        error: str = None
    ):
        """记录请求指标"""
        if service_name not in self.metrics:
            self.metrics[service_name] = ServiceMetrics(name=service_name)
        
        metrics = self.metrics[service_name]
        metrics.total_requests += 1
        
        if success:
            metrics.successful_requests += 1
            metrics.last_success = datetime.now()
            metrics.consecutive_failures = 0
            
            # 更新平均响应时间
            if response_time:
                metrics.avg_response_time = (
                    (metrics.avg_response_time * (metrics.successful_requests - 1) + response_time) /
                    metrics.successful_requests
                )
            
            # 记录熔断器成功
            if service_name in self.circuit_breakers:
                self.circuit_breakers[service_name].record_success()
        else:
            metrics.failed_requests += 1
            metrics.last_error = error
            metrics.consecutive_failures += 1
            
            # 记录熔断器失败
            if service_name in self.circuit_breakers:
                self.circuit_breakers[service_name].record_failure()
        
        # 更新错误率
        metrics.error_rate = metrics.failed_requests / metrics.total_requests
    
    async def execute_with_reliability(
        self,
        service_name: str,
        operation: callable,
        reliability_level: ReliabilityLevel = ReliabilityLevel.IMPORTANT,
        validation_data: Optional[Dict[str, Any]] = None,
        validation_type: Optional[str] = None,
        *args,
        **kwargs
    ) -> tuple[bool, Any]:
        """
        以可靠性模式执行操作
        
        Returns:
            (success, result)
        """
        start_time = datetime.now()
        
        # 检查熔断器
        if service_name in self.circuit_breakers:
            if not self.circuit_breakers[service_name].allow_request():
                logger.warning(f"Circuit breaker OPEN for {service_name}, using fallback")
                result = await self.fallback_manager._get_safe_default(service_name)
                return False, result
        
        # 数据验证
        if validation_data and validation_type and validation_type in self.validators:
            is_valid, errors = self.validators[validation_type].validate(
                validation_data, validation_type
            )
            if not is_valid:
                logger.error(f"Validation failed for {validation_type}: {errors}")
                self.record_request(service_name, False, error=f"Validation: {errors[0]}")
                return False, {"error": "数据验证失败", "details": errors}
        
        try:
            # 执行操作
            result = await operation(*args, **kwargs)
            
            # 记录成功
            response_time = (datetime.now() - start_time).total_seconds()
            self.record_request(service_name, True, response_time)
            
            return True, result
        
        except Exception as e:
            # 记录失败
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.record_request(service_name, False, error=error_msg)
            
            # 根据可靠性级别决定是否降级
            if reliability_level != ReliabilityLevel.CRITICAL:
                result = await self.fallback_manager.execute_with_fallback(
                    service_name, operation, *args, **kwargs
                )
                return False, result
            
            logger.error(f"Critical operation failed for {service_name}: {error_msg}")
            return False, {"error": str(e)}
    
    def get_health_status(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        return {
            "status": self.health_status.value,
            "timestamp": datetime.now().isoformat(),
            "services": {
                name: {
                    "total_requests": m.total_requests,
                    "success_rate": m.successful_requests / m.total_requests if m.total_requests > 0 else 1.0,
                    "error_rate": m.error_rate,
                    "avg_response_time": m.avg_response_time,
                    "consecutive_failures": m.consecutive_failures,
                    "circuit_breaker_state": (
                        self.circuit_breakers[name].state if name in self.circuit_breakers else "N/A"
                    )
                }
                for name, m in self.metrics.items()
            }
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        summary = {
            "total_services": len(self.metrics),
            "healthy_services": 0,
            "degraded_services": 0,
            "unhealthy_services": 0,
            "services": {}
        }
        
        for name, metrics in self.metrics.items():
            service_summary = {
                "total_requests": metrics.total_requests,
                "success_rate": (
                    metrics.successful_requests / metrics.total_requests
                    if metrics.total_requests > 0 else 1.0
                ),
                "error_rate": metrics.error_rate,
                "avg_response_time": metrics.avg_response_time
            }
            summary["services"][name] = service_summary
            
            if metrics.error_rate < 0.1:
                summary["healthy_services"] += 1
            elif metrics.error_rate < 0.5:
                summary["degraded_services"] += 1
            else:
                summary["unhealthy_services"] += 1
        
        return summary


# 全局实例
_reliability_engine = None


def get_reliability_engine() -> ReliabilityEngine:
    """获取可靠性引擎单例"""
    global _reliability_engine
    if _reliability_engine is None:
        _reliability_engine = ReliabilityEngine()
    return _reliability_engine
