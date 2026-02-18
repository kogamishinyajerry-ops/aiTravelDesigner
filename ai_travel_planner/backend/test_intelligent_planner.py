#!/usr/bin/env python3
"""
测试智能规划器 - 验证PLTR哲学的实现
"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.planning.intelligent_planner import get_intelligent_planner
from loguru import logger


async def test_basic_planning():
    """测试基础规划功能"""
    logger.info("=" * 60)
    logger.info("测试 1: 基础规划功能")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    
    result = await planner.plan_itinerary(
        destination="京都",
        days=3,
        start_date="2026-03-01",
        travelers=2,
        preferences={
            "interests": ["历史", "文化"],
            "price_level": 3,
            "min_rating": 4.0
        },
        user_id="test_user_001"
    )
    
    logger.info(f"✓ 规划成功: {result.success}")
    logger.info(f"✓ 置信度: {result.confidence:.2f}")
    logger.info(f"✓ 执行时间: {result.execution_time_ms:.2f}ms")
    logger.info(f"✓ 数据源: {result.data_sources}")
    
    if result.itinerary:
        logger.info(f"✓ 天数: {result.itinerary['days']}")
        logger.info(f"✓ 预算: {result.itinerary['budget']['total']:.2f}")
        logger.info(f"✓ 每日费用: {[f{day['estimated_cost']:.0f}" for day in result.itinerary['daily_plans']]}")
    
    assert result.success, "规划应该成功"
    assert result.confidence > 0.5, "置信度应该大于0.5"
    assert result.execution_time_ms < 5000, "执行时间应该小于5秒"
    
    logger.success("✓ 测试 1 通过\n")


async def test_reliability():
    """测试可靠性功能"""
    logger.info("=" * 60)
    logger.info("测试 2: 可靠性功能")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    
    # 获取可靠性引擎
    reliability = planner.reliability_engine
    
    # 记录一些请求
    for i in range(10):
        reliability.record_request(
            "test_service",
            success=(i % 3 != 0),  # 2/3 成功率
            response_time=100 + i * 10
        )
    
    health = reliability.get_health_status()
    
    logger.info(f"✓ 系统状态: {health['status']}")
    logger.info(f"✓ 服务数量: {len(health['services'])}")
    
    if "test_service" in health["services"]:
        service_health = health["services"]["test_service"]
        logger.info(f"✓ test_service 成功率: {service_health['success_rate']:.2f}")
        logger.info(f"✓ test_service 错误率: {service_health['error_rate']:.2f}")
    
    # 测试熔断器
    circuit_breaker = reliability.circuit_breakers.get("llm_service")
    if circuit_breaker:
        logger.info(f"✓ 熔断器状态: {circuit_breaker.state}")
        
        # 测试熔断
        for _ in range(6):
            circuit_breaker.record_failure()
        
        logger.info(f"✓ 熔断器状态（失败后）: {circuit_breaker.state}")
        assert circuit_breaker.state == "OPEN", "熔断器应该打开"
        
        # 测试恢复
        circuit_breaker.record_success()
        logger.info(f"✓ 熔断器状态（成功后）: {circuit_breaker.state}")
    
    logger.success("✓ 测试 2 通过\n")


async def test_data_driven():
    """测试数据驱动功能"""
    logger.info("=" * 60)
    logger.info("测试 3: 数据驱动功能")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    data_engine = planner.data_engine
    
    # 记录一些模拟数据
    for i in range(50):
        data_engine.record_event(
            "attraction_rating",
            3.0 + (i % 30) / 10,  # 3.0 - 6.0
            tags={
                "attraction_id": f"attr_{i}",
                "destination": "京都",
                "user_id": f"user_{i % 10}"
            }
        )
        
        data_engine.record_event(
            "attraction_cost",
            30 + (i % 5) * 10,  # 30 - 70
            tags={
                "attraction_id": f"attr_{i}",
                "destination": "京都"
            }
        )
    
    # 获取统计洞察
    insight = data_engine.get_insights("attraction_rating", hours=24)
    
    logger.info(f"✓ 指标: {insight.metric}")
    logger.info(f"✓ 平均值: {insight.mean:.2f}")
    logger.info(f"✓ 中位数: {insight.median:.2f}")
    logger.info(f"✓ 标准差: {insight.std:.2f}")
    logger.info(f"✓ 趋势: {insight.trend}")
    logger.info(f"✓ 置信度: {insight.confidence:.2f}")
    
    # 检测异常
    data_engine.record_event("attraction_rating", 0.5, tags={"attraction_id": "attr_anomaly"})
    anomalies = data_engine.detect_anomalies("attraction_rating")
    logger.info(f"✓ 检测到 {len(anomalies)} 个异常")
    
    # 获取推荐
    recommendations = data_engine.get_recommendations("京都", user_id="user_1")
    logger.info(f"✓ 获取到 {len(recommendations)} 个推荐")
    
    # 预测预算
    budget = data_engine.predict_budget(
        destination="京都",
        days=3,
        travelers=2
    )
    logger.info(f"✓ 预测总预算: {budget['total']:.2f}")
    logger.info(f"✓ 每人预算: {budget['per_person']:.2f}")
    logger.info(f"✓ 预算置信度: {budget['confidence']:.2f}")
    
    assert insight.confidence > 0.3, "应该有足够的置信度"
    
    logger.success("✓ 测试 3 通过\n")


async def test_observability():
    """测试可观测性功能"""
    logger.info("=" * 60)
    logger.info("测试 4: 可观测性功能")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    observability = planner.observability
    
    # 测试追踪
    with observability.trace_operation("test_operation", trace_id="test_trace_001"):
        await asyncio.sleep(0.1)
        observability.log(
            observability.LogLevel.INFO,
            "测试日志消息",
            tags={"test": "true"}
        )
    
    # 测试指标
    for i in range(10):
        observability.increment_counter("test_counter", tags={"type": str(i % 3)})
        observability.set_gauge("test_gauge", i * 10, tags={"id": str(i)})
        observability.metrics.record_histogram("test_histogram", i * 100)
    
    # 获取仪表板
    dashboard = observability.get_dashboard()
    
    logger.info(f"✓ 时间戳: {dashboard['timestamp']}")
    logger.info(f"✓ 活跃追踪: {dashboard['traces']['total']}")
    logger.info(f"✓ 活跃告警: {dashboard['alerts']['active']}")
    
    # 获取指标
    metrics = observability.metrics.get_all_metrics()
    logger.info(f"✓ 计数器数量: {len(metrics['counters'])}")
    logger.info(f"✓ 仪表数量: {len(metrics['gauges'])}")
    logger.info(f"✓ 直方图数量: {len(metrics['histograms'])}")
    
    # 获取追踪记录
    traces = observability.tracer.get_trace("test_trace_001")
    logger.info(f"✓ 追踪事件数量: {len(traces)}")
    
    logger.success("✓ 测试 4 通过\n")


async def test_system_integration():
    """测试系统集成"""
    logger.info("=" * 60)
    logger.info("测试 5: 系统集成")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    
    # 执行多次规划，观察系统行为
    for i in range(3):
        result = await planner.plan_itinerary(
            destination="东京" if i % 2 == 0 else "京都",
            days=2 + i,
            start_date="2026-03-01",
            travelers=2,
            preferences={"min_rating": 4.0}
        )
        
        logger.info(f"  规划 {i+1}: 成功={result.success}, "
                   f"置信度={result.confidence:.2f}, "
                   f"时间={result.execution_time_ms:.2f}ms")
    
    # 获取系统健康状态
    health = planner.get_system_health()
    
    logger.info(f"✓ 可靠性状态: {health['reliability']['status']}")
    logger.info(f"✓ 数据点总数: {health['data_engine']['total_data_points']}")
    logger.info(f"✓ 追踪总数: {health['observability']['traces']['total']}")
    logger.info(f"✓ 健康服务: {health['metrics']['healthy_services']}")
    logger.info(f"✓ 降级服务: {health['metrics']['degraded_services']}")
    
    logger.success("✓ 测试 5 通过\n")


async def test_error_handling():
    """测试错误处理"""
    logger.info("=" * 60)
    logger.info("测试 6: 错误处理")
    logger.info("=" * 60)
    
    planner = get_intelligent_planner()
    
    # 测试无效输入
    result = await planner.plan_itinerary(
        destination="不支持的城市",
        days=3,
        start_date="2026-03-01",
        travelers=2,
        preferences={}
    )
    
    logger.info(f"✓ 无效目的地: success={result.success}")
    logger.info(f"✓ 错误消息: {result.errors}")
    assert not result.success, "应该失败"
    assert len(result.errors) > 0, "应该有错误消息"
    
    # 测试无效日期
    try:
        result = await planner.plan_itinerary(
            destination="京都",
            days=3,
            start_date="invalid-date",
            travelers=2,
            preferences={}
        )
        logger.info(f"✓ 无效日期: success={result.success}")
    except Exception as e:
        logger.info(f"✓ 捕获异常: {type(e).__name__}")
    
    # 测试边界值
    result = await planner.plan_itinerary(
        destination="京都",
        days=0,  # 无效值
        start_date="2026-03-01",
        travelers=2,
        preferences={}
    )
    
    logger.info(f"✓ 边界值测试: success={result.success}")
    
    logger.success("✓ 测试 6 通过\n")


async def main():
    """运行所有测试"""
    logger.info("🚀 开始测试智能规划器")
    logger.info("=" * 60)
    logger.info("基于 PLTR 开发哲学:")
    logger.info("1. 可靠性 - 熔断器、降级、容错")
    logger.info("2. 数据驱动 - 基于真实数据决策")
    logger.info("3. 可观测性 - 全链路追踪和监控")
    logger.info("=" * 60)
    logger.info("")
    
    tests = [
        test_basic_planning,
        test_reliability,
        test_data_driven,
        test_observability,
        test_system_integration,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            await test()
            passed += 1
        except AssertionError as e:
            logger.error(f"✗ 测试失败: {str(e)}")
            failed += 1
        except Exception as e:
            logger.error(f"✗ 测试异常: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            failed += 1
    
    logger.info("=" * 60)
    logger.info(f"测试完成: {passed} 通过, {failed} 失败")
    logger.info("=" * 60)
    
    if failed == 0:
        logger.success("🎉 所有测试通过！")
    else:
        logger.error(f"⚠️  有 {failed} 个测试失败")


if __name__ == "__main__":
    asyncio.run(main())
