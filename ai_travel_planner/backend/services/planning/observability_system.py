"""
可观测性系统 - 基于PLTR哲学
提供全链路监控、日志追踪和实时告警
"""
import json
import uuid
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from contextlib import contextmanager
from enum import Enum
from loguru import logger
from functools import wraps
import asyncio


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AlertSeverity(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class TraceEvent:
    """追踪事件"""
    event_id: str
    trace_id: str
    parent_span_id: Optional[str]
    span_id: str
    timestamp: datetime
    service: str
    operation: str
    level: LogLevel
    message: str
    tags: Dict[str, Any] = field(default_factory=dict)
    duration_ms: Optional[float] = None


@dataclass
class Alert:
    """告警"""
    alert_id: str
    severity: AlertSeverity
    service: str
    metric: str
    message: str
    timestamp: datetime
    tags: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class DistributedTracer:
    """分布式追踪器"""
    
    def __init__(self):
        self.active_traces: Dict[str, List[TraceEvent]] = {}
        self.service_name = "ai_travel_planner"
    
    def start_trace(
        self,
        operation: str,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None
    ) -> str:
        """开始追踪"""
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        span_id = str(uuid.uuid4())
        
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            span_id=span_id,
            timestamp=datetime.now(),
            service=self.service_name,
            operation=operation,
            level=LogLevel.INFO,
            message=f"Starting: {operation}"
        )
        
        self._add_event(event)
        logger.debug(f"[Trace {trace_id}] {operation} started")
        
        return span_id
    
    def end_trace(
        self,
        trace_id: str,
        span_id: str,
        operation: str,
        success: bool = True,
        result: Any = None,
        error: Optional[str] = None
    ):
        """结束追踪"""
        level = LogLevel.INFO if success else LogLevel.ERROR
        message = f"Completed: {operation}" if success else f"Failed: {operation}"
        
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=None,
            span_id=span_id,
            timestamp=datetime.now(),
            service=self.service_name,
            operation=operation,
            level=level,
            message=message,
            tags={"success": success, "error": error}
        )
        
        self._add_event(event)
        
        if success:
            logger.debug(f"[Trace {trace_id}] {operation} completed")
        else:
            logger.error(f"[Trace {trace_id}] {operation} failed: {error}")
    
    def log_event(
        self,
        trace_id: str,
        operation: str,
        level: LogLevel,
        message: str,
        tags: Dict[str, Any] = None
    ):
        """记录事件"""
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=None,
            span_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            service=self.service_name,
            operation=operation,
            level=level,
            message=message,
            tags=tags or {}
        )
        
        self._add_event(event)
        
        # 同步到日志系统
        log_func = {
            LogLevel.DEBUG: logger.debug,
            LogLevel.INFO: logger.info,
            LogLevel.WARNING: logger.warning,
            LogLevel.ERROR: logger.error,
            LogLevel.CRITICAL: logger.critical
        }.get(level, logger.info)
        
        log_func(f"[Trace {trace_id}] {message}")
    
    def _add_event(self, event: TraceEvent):
        """添加事件"""
        if event.trace_id not in self.active_traces:
            self.active_traces[event.trace_id] = []
        
        self.active_traces[event.trace_id].append(event)
        
        # 只保留最近1000个事件
        if len(self.active_traces[event.trace_id]) > 1000:
            self.active_traces[event.trace_id] = self.active_traces[event.trace_id][-1000:]
    
    def get_trace(self, trace_id: str) -> List[TraceEvent]:
        """获取追踪记录"""
        return self.active_traces.get(trace_id, [])
    
    def cleanup_old_traces(self, hours: int = 24):
        """清理旧追踪记录"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for trace_id in list(self.active_traces.keys()):
            events = self.active_traces[trace_id]
            if not events or events[-1].timestamp < cutoff:
                del self.active_traces[trace_id]


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def increment(self, name: str, value: float = 1.0, tags: Dict[str, Any] = None):
        """增加计数器"""
        key = self._make_key(name, tags)
        self.counters[key] = self.counters.get(key, 0.0) + value
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, Any] = None):
        """设置仪表值"""
        key = self._make_key(name, tags)
        self.gauges[key] = value
    
    def record_histogram(self, name: str, value: float, tags: Dict[str, Any] = None):
        """记录直方图值"""
        key = self._make_key(name, tags)
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
        
        # 只保留最近1000个值
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
    
    def get_counter(self, name: str, tags: Dict[str, Any] = None) -> float:
        """获取计数器值"""
        key = self._make_key(name, tags)
        return self.counters.get(key, 0.0)
    
    def get_gauge(self, name: str, tags: Dict[str, Any] = None) -> float:
        """获取仪表值"""
        key = self._make_key(name, tags)
        return self.gauges.get(key, 0.0)
    
    def get_histogram_stats(
        self,
        name: str,
        tags: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """获取直方图统计"""
        key = self._make_key(name, tags)
        values = self.histograms.get(key, [])
        
        if not values:
            return {
                "count": 0,
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0
            }
        
        sorted_values = sorted(values)
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "p50": sorted_values[int(len(values) * 0.5)],
            "p95": sorted_values[int(len(values) * 0.95)],
            "p99": sorted_values[int(len(values) * 0.99)]
        }
    
    def _make_key(self, name: str, tags: Dict[str, Any] = None) -> str:
        """生成键"""
        if not tags:
            return name
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有指标"""
        return {
            "counters": self.counters,
            "gauges": self.gauges,
            "histograms": {
                key: self.get_histogram_stats_from_key(key)
                for key in self.histograms.keys()
            }
        }
    
    def get_histogram_stats_from_key(self, key: str) -> Dict[str, float]:
        """从键获取直方图统计"""
        values = self.histograms.get(key, [])
        if not values:
            return {}
        
        sorted_values = sorted(values)
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "p50": sorted_values[int(len(values) * 0.5)],
            "p95": sorted_values[int(len(values) * 0.95)],
            "p99": sorted_values[int(len(values) * 0.99)]
        }


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.alert_handlers: List[Callable[[Alert], None]] = []
    
    def add_alert_rule(
        self,
        name: str,
        metric: str,
        condition: str,
        threshold: float,
        severity: AlertSeverity
    ):
        """添加告警规则"""
        self.alert_rules[name] = {
            "metric": metric,
            "condition": condition,
            "threshold": threshold,
            "severity": severity
        }
    
    def add_alert_handler(self, handler: Callable[[Alert], None]):
        """添加告警处理器"""
        self.alert_handlers.append(handler)
    
    def check_alerts(self, metrics_collector: MetricsCollector):
        """检查告警条件"""
        for rule_name, rule in self.alert_rules.items():
            metric_value = metrics_collector.get_gauge(rule["metric"])
            
            triggered = False
            if rule["condition"] == "greater_than":
                triggered = metric_value > rule["threshold"]
            elif rule["condition"] == "less_than":
                triggered = metric_value < rule["threshold"]
            elif rule["condition"] == "equals":
                triggered = metric_value == rule["threshold"]
            
            if triggered:
                self._trigger_alert(
                    severity=rule["severity"],
                    service="ai_travel_planner",
                    metric=rule["metric"],
                    message=f"Alert {rule_name}: {rule['metric']} = {metric_value} {rule['condition']} {rule['threshold']}",
                    tags={"rule": rule_name, "value": metric_value}
                )
    
    def _trigger_alert(
        self,
        severity: AlertSeverity,
        service: str,
        metric: str,
        message: str,
        tags: Dict[str, Any]
    ):
        """触发告警"""
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            severity=severity,
            service=service,
            metric=metric,
            message=message,
            timestamp=datetime.now(),
            tags=tags
        )
        
        self.alerts.append(alert)
        
        # 保留最近1000个告警
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
        
        # 调用处理器
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {str(e)}")
        
        # 记录日志
        log_func = {
            AlertSeverity.INFO: logger.info,
            AlertSeverity.WARNING: logger.warning,
            AlertSeverity.ERROR: logger.error,
            AlertSeverity.CRITICAL: logger.critical
        }.get(severity, logger.info)
        
        log_func(f"[ALERT] {message}")
    
    def get_active_alerts(self, hours: int = 24) -> List[Alert]:
        """获取活跃告警"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            alert for alert in self.alerts
            if alert.timestamp >= cutoff and not alert.resolved
        ]
    
    def resolve_alert(self, alert_id: str):
        """解决告警"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                break


class ObservabilitySystem:
    """可观测性系统"""
    
    def __init__(self):
        self.tracer = DistributedTracer()
        self.metrics = MetricsCollector()
        self.alert_manager = AlertManager()
        
        # 初始化默认告警规则
        self._init_default_alert_rules()
    
    def _init_default_alert_rules(self):
        """初始化默认告警规则"""
        self.alert_manager.add_alert_rule(
            name="high_error_rate",
            metric="error_rate",
            condition="greater_than",
            threshold=0.5,
            severity=AlertSeverity.ERROR
        )
        
        self.alert_manager.add_alert_rule(
            name="slow_response_time",
            metric="avg_response_time",
            condition="greater_than",
            threshold=5000.0,
            severity=AlertSeverity.WARNING
        )
        
        self.alert_manager.add_alert_rule(
            name="low_success_rate",
            metric="success_rate",
            condition="less_than",
            threshold=0.8,
            severity=AlertSeverity.ERROR
        )
    
    @contextmanager
    def trace_operation(
        self,
        operation: str,
        trace_id: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        tags: Dict[str, Any] = None
    ):
        """追踪操作的上下文管理器"""
        span_id = self.tracer.start_trace(operation, trace_id, parent_span_id)
        start_time = time.time()
        
        try:
            yield span_id
            duration = (time.time() - start_time) * 1000
            self.tracer.end_trace(
                trace_id or span_id,
                span_id,
                operation,
                success=True
            )
            self.metrics.record_histogram(f"duration.{operation}", duration, tags)
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.tracer.end_trace(
                trace_id or span_id,
                span_id,
                operation,
                success=False,
                error=str(e)
            )
            self.metrics.record_histogram(f"duration.{operation}", duration, tags)
            self.metrics.increment(f"error.{operation}", tags=tags)
            raise
    
    def observe_async(
        self,
        operation: str,
        tags: Dict[str, Any] = None
    ):
        """异步操作观察装饰器"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                trace_id = str(uuid.uuid4())
                with self.trace_operation(operation, trace_id, tags=tags):
                    try:
                        result = await func(*args, **kwargs)
                        self.metrics.increment(f"success.{operation}", tags=tags)
                        return result
                    except Exception as e:
                        self.metrics.increment(f"error.{operation}", tags=tags)
                        raise
            return wrapper
        return decorator
    
    def observe(
        self,
        operation: str,
        tags: Dict[str, Any] = None
    ):
        """同步操作观察装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                trace_id = str(uuid.uuid4())
                with self.trace_operation(operation, trace_id, tags=tags):
                    try:
                        result = func(*args, **kwargs)
                        self.metrics.increment(f"success.{operation}", tags=tags)
                        return result
                    except Exception as e:
                        self.metrics.increment(f"error.{operation}", tags=tags)
                        raise
            return wrapper
        return decorator
    
    def log(self, level: LogLevel, message: str, tags: Dict[str, Any] = None):
        """记录日志"""
        trace_id = str(uuid.uuid4())
        self.tracer.log_event(trace_id, "log", level, message, tags)
    
    def increment_counter(self, name: str, value: float = 1.0, tags: Dict[str, Any] = None):
        """增加计数器"""
        self.metrics.increment(name, value, tags)
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, Any] = None):
        """设置仪表"""
        self.metrics.set_gauge(name, value, tags)
    
    def get_dashboard(self) -> Dict[str, Any]:
        """获取仪表板数据"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics.get_all_metrics(),
            "alerts": {
                "active": len(self.alert_manager.get_active_alerts()),
                "recent": [
                    {
                        "severity": alert.severity.value,
                        "message": alert.message,
                        "timestamp": alert.timestamp.isoformat()
                    }
                    for alert in self.alert_manager.get_active_alerts(hours=1)
                ]
            },
            "traces": {
                "total": len(self.tracer.active_traces),
                "recent_trace_ids": list(self.tracer.active_traces.keys())[-10:]
            }
        }
    
    def check_health_alerts(self):
        """检查健康相关告警"""
        self.alert_manager.check_alerts(self.metrics)


# 全局实例
_observability_system = None


def get_observability_system() -> ObservabilitySystem:
    """获取可观测性系统单例"""
    global _observability_system
    if _observability_system is None:
        _observability_system = ObservabilitySystem()
    return _observability_system
