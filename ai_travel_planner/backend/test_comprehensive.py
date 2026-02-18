"""
全面测试框架 - 系统性测试所有模块
"""
import sys
import os
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import traceback

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loguru import logger


@dataclass
class TestResult:
    """测试结果"""
    test_name: str
    module: str
    passed: bool
    duration_ms: float
    error_message: Optional[str] = None
    details: Dict[str, Any] = None


class TestFramework:
    """测试框架"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.failed_tests: List[TestResult] = []
        self.passed_tests: List[TestResult] = []
        
    def run_test(self, test_func, test_name: str, module: str) -> TestResult:
        """运行单个测试"""
        start_time = datetime.now()
        
        try:
            # 运行测试
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # 记录结果
            if result is None or result is True:
                test_result = TestResult(
                    test_name=test_name,
                    module=module,
                    passed=True,
                    duration_ms=duration_ms
                )
                self.passed_tests.append(test_result)
                logger.success(f"✓ {test_name} - {duration_ms:.2f}ms")
            else:
                test_result = TestResult(
                    test_name=test_name,
                    module=module,
                    passed=False,
                    duration_ms=duration_ms,
                    error_message=f"测试返回了非True/None的值: {result}"
                )
                self.failed_tests.append(test_result)
                logger.error(f"✗ {test_name} - {test_result.error_message}")
            
            self.results.append(test_result)
            return test_result
            
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            
            test_result = TestResult(
                test_name=test_name,
                module=module,
                passed=False,
                duration_ms=duration_ms,
                error_message=error_msg
            )
            self.failed_tests.append(test_result)
            self.results.append(test_result)
            
            logger.error(f"✗ {test_name} - {str(e)}")
            return test_result
    
    def print_summary(self):
        """打印测试摘要"""
        total = len(self.results)
        passed = len(self.passed_tests)
        failed = len(self.failed_tests)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print("\n" + "="*80)
        print("测试摘要")
        print("="*80)
        print(f"总测试数: {total}")
        print(f"通过: {passed} ({success_rate:.1f}%)")
        print(f"失败: {failed}")
        print(f"总耗时: {sum(r.duration_ms for r in self.results):.2f}ms")
        print("="*80)
        
        if self.failed_tests:
            print("\n失败测试详情:")
            print("-"*80)
            for test in self.failed_tests:
                print(f"\n模块: {test.module}")
                print(f"测试: {test.test_name}")
                print(f"错误: {test.error_message}")
                print("-"*80)
    
    def get_report(self) -> Dict[str, Any]:
        """获取测试报告"""
        return {
            "total": len(self.results),
            "passed": len(self.passed_tests),
            "failed": len(self.failed_tests),
            "success_rate": (len(self.passed_tests) / len(self.results) * 100) if self.results else 0,
            "total_duration_ms": sum(r.duration_ms for r in self.results),
            "failed_tests": [
                {
                    "test_name": t.test_name,
                    "module": t.module,
                    "error": t.error_message
                }
                for t in self.failed_tests
            ]
        }


# 测试用例
class ModuleTests:
    """模块测试用例"""
    
    @staticmethod
    def test_professional_standards_import():
        """测试专业标准模块导入"""
        from services.planning import (
            TravelStyle, ActivityIntensity, BudgetLevel,
            TravelRequirements, ProfessionalPlanningStandards
        )
        
        # 测试枚举
        assert len(TravelStyle) == 10, "TravelStyle应该有10个选项"
        assert len(ActivityIntensity) == 4, "ActivityIntensity应该有4个等级"
        assert len(BudgetLevel) == 5, "BudgetLevel应该有5个等级"
        
        # 测试标准参数
        assert ProfessionalPlanningStandards.MIN_ATTRACTION_DURATION == 1.0
        assert ProfessionalPlanningStandards.MAX_ATTRACTION_DURATION == 4.0
        assert ProfessionalPlanningStandards.MEAL_DURATION == 1.5
        
        return True
    
    @staticmethod
    def test_travel_requirements_validation():
        """测试旅行需求验证"""
        from services.planning import TravelRequirements, TravelStyle, BudgetLevel
        
        # 有效需求
        valid_req = TravelRequirements(
            destination="京都",
            departure_city="北京",
            start_date="2024-04-01",
            end_date="2024-04-05",
            days=5,
            travelers_adults=2,
            travel_style=TravelStyle.CULTURAL,
            budget_level=BudgetLevel.COMFORT
        )
        
        is_valid, errors = valid_req.validate()
        assert is_valid, f"有效需求验证失败: {errors}"
        
        # 无效需求
        invalid_req = TravelRequirements(
            destination="",
            departure_city="北京",
            start_date="",
            end_date="",
            days=0,
            travelers_adults=0
        )
        
        is_valid, errors = invalid_req.validate()
        assert not is_valid, "无效需求应该验证失败"
        assert len(errors) > 0, "应该有错误信息"
        
        return True
    
    @staticmethod
    async def test_professional_generator_initialization():
        """测试专业行程生成器初始化"""
        from services.planning import get_professional_generator
        
        generator = get_professional_generator()
        assert generator is not None, "生成器不能为None"
        assert hasattr(generator, 'attractions_db'), "生成器应该有attractions_db属性"
        assert hasattr(generator, 'restaurants_db'), "生成器应该有restaurants_db属性"
        
        return True
    
    @staticmethod
    async def test_professional_itinerary_generation():
        """测试专业行程生成"""
        from services.planning import (
            get_professional_generator,
            TravelRequirements, TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType
        )
        
        generator = get_professional_generator()
        
        requirements = TravelRequirements(
            destination="京都",
            departure_city="北京",
            start_date="2024-04-01",
            end_date="2024-04-05",
            days=3,
            travelers_adults=2,
            travel_style=TravelStyle.CULTURAL,
            activity_intensity=ActivityIntensity.MODERATE,
            budget_level=BudgetLevel.COMFORT,
            interests=["历史", "文化"],
            accommodation_type=AccommodationType.BOUTIQUE_HOTEL
        )
        
        itinerary = await generator.generate_professional_itinerary(requirements)
        
        assert itinerary is not None, "行程不能为None"
        assert itinerary.itinerary_id is not None, "行程ID不能为None"
        assert len(itinerary.daily_plans) == requirements.days, f"应该有{requirements.days}天的行程"
        
        # 检查每日行程
        for plan in itinerary.daily_plans:
            assert 'day' in plan, "每日计划应该包含day"
            assert 'date' in plan, "每日计划应该包含date"
            assert 'timeline' in plan, "每日计划应该包含timeline"
        
        return True
    
    @staticmethod
    def test_workflow_manager_initialization():
        """测试工作流管理器初始化"""
        from services.planning import get_workflow_manager
        
        manager = get_workflow_manager()
        assert manager is not None, "管理器不能为None"
        assert hasattr(manager, 'active_sessions'), "管理器应该有active_sessions属性"
        
        return True
    
    @staticmethod
    def test_workflow_session_creation():
        """测试工作流会话创建"""
        from services.planning import get_workflow_manager
        
        manager = get_workflow_manager()
        session = manager.create_session()
        
        assert session is not None, "会话不能为None"
        assert session.session_id is not None, "会话ID不能为None"
        assert len(session.steps) == 10, "应该有10个工作流步骤"
        assert session.current_step_index == 0, "初始步骤索引应该是0"
        
        return True
    
    @staticmethod
    async def test_planning_service_initialization():
        """测试规划服务初始化"""
        from services.planning import get_professional_planning_service
        
        service = get_professional_planning_service()
        assert service is not None, "服务不能为None"
        assert hasattr(service, 'generator'), "服务应该有generator属性"
        assert hasattr(service, 'workflow_manager'), "服务应该有workflow_manager属性"
        assert hasattr(service, 'budget_calculator'), "服务应该有budget_calculator属性"
        
        return True
    
    @staticmethod
    async def test_complete_planning_workflow():
        """测试完整规划工作流"""
        from services.planning import (
            get_professional_planning_service,
            TravelRequirements, TravelStyle, ActivityIntensity, BudgetLevel, AccommodationType
        )
        
        service = get_professional_planning_service()
        
        requirements = TravelRequirements(
            destination="京都",
            departure_city="北京",
            start_date="2024-04-01",
            end_date="2024-04-03",
            days=3,
            travelers_adults=2,
            travel_style=TravelStyle.CULTURAL,
            activity_intensity=ActivityIntensity.MODERATE,
            budget_level=BudgetLevel.COMFORT,
            interests=["历史"]
        )
        
        itinerary, session_id = await service.create_itinerary_from_requirements(
            requirements
        )
        
        assert itinerary is not None, "行程不能为None"
        assert session_id is not None, "会话ID不能为None"
        assert itinerary.itinerary_id is not None, "行程ID不能为None"
        
        # 检查进度
        progress = service.get_session_progress(session_id)
        assert progress is not None, "进度不能为None"
        assert progress['progress'] == 100.0, "进度应该是100%"
        
        return True
    
    @staticmethod
    def test_budget_calculator():
        """测试预算计算器"""
        from services.planning import get_budget_calculator
        
        calculator = get_budget_calculator()
        assert calculator is not None, "计算器不能为None"
        
        # 测试单项费用计算
        flight_cost = calculator.calculate_flight_cost("北京", "东京", 2)
        assert flight_cost.total_cost > 0, "机票费用应该大于0"
        assert flight_cost.quantity == 2, "数量应该是2"
        
        accommodation_cost = calculator.calculate_accommodation_cost("东京", 5, 2, "standard")
        assert accommodation_cost.total_cost > 0, "住宿费用应该大于0"
        
        return True
    
    @staticmethod
    def test_quality_checklist():
        """测试质量检查清单"""
        from services.planning import QualityChecklist
        
        # 测试完整性检查
        test_itinerary = {
            "destination": "京都",
            "days": 5,
            "start_date": "2024-04-01",
            "end_date": "2024-04-05"
        }
        
        results = QualityChecklist.check_completeness(test_itinerary)
        assert 'passed' in results, "结果应该包含passed"
        assert 'failed' in results, "结果应该包含failed"
        assert 'warnings' in results, "结果应该包含warnings"
        
        return True
    
    @staticmethod
    def test_seasonal_guidelines():
        """测试季节性指南"""
        from services.planning import SeasonalGuidelines
        
        # 测试季节获取
        assert SeasonalGuidelines.get_season(3) == "spring"
        assert SeasonalGuidelines.get_season(7) == "summer"
        assert SeasonalGuidelines.get_season(10) == "autumn"
        assert SeasonalGuidelines.get_season(1) == "winter"
        
        # 测试季节性建议
        tips = SeasonalGuidelines.get_seasonal_tips("京都", 4)
        assert isinstance(tips, list), "建议应该是列表"
        
        return True


def run_all_tests():
    """运行所有测试"""
    framework = TestFramework()
    tests = ModuleTests()
    
    print("\n" + "="*80)
    print("开始系统性模块化测试")
    print("="*80 + "\n")
    
    # 基础模块测试
    print("【基础模块测试】")
    framework.run_test(
        tests.test_professional_standards_import,
        "专业标准模块导入",
        "professional_standards"
    )
    
    framework.run_test(
        tests.test_travel_requirements_validation,
        "旅行需求验证",
        "travel_requirements"
    )
    
    # 生成器测试
    print("\n【生成器测试】")
    framework.run_test(
        tests.test_professional_generator_initialization,
        "专业生成器初始化",
        "professional_generator"
    )
    
    framework.run_test(
        tests.test_professional_itinerary_generation,
        "专业行程生成",
        "professional_generator"
    )
    
    # 工作流测试
    print("\n【工作流测试】")
    framework.run_test(
        tests.test_workflow_manager_initialization,
        "工作流管理器初始化",
        "workflow_manager"
    )
    
    framework.run_test(
        tests.test_workflow_session_creation,
        "工作流会话创建",
        "workflow_manager"
    )
    
    # 服务测试
    print("\n【服务测试】")
    framework.run_test(
        tests.test_planning_service_initialization,
        "规划服务初始化",
        "planning_service"
    )
    
    framework.run_test(
        tests.test_complete_planning_workflow,
        "完整规划工作流",
        "planning_service"
    )
    
    # 辅助模块测试
    print("\n【辅助模块测试】")
    framework.run_test(
        tests.test_budget_calculator,
        "预算计算器",
        "budget_calculator"
    )
    
    framework.run_test(
        tests.test_quality_checklist,
        "质量检查清单",
        "quality_checklist"
    )
    
    framework.run_test(
        tests.test_seasonal_guidelines,
        "季节性指南",
        "seasonal_guidelines"
    )
    
    # 打印摘要
    framework.print_summary()
    
    return framework.get_report()


if __name__ == "__main__":
    report = run_all_tests()
    
    # 保存报告到文件
    import json
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"测试报告已保存到 test_report.json")
    
    # 退出码
    sys.exit(0 if report["failed"] == 0 else 1)
