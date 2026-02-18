"""
所有模块测试 - 测试各个独立模块
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loguru import logger
from typing import List, Dict, Any
from datetime import datetime


class ModuleTester:
    """模块测试器"""
    
    def __init__(self):
        self.results = []
    
    def test_ai_services(self):
        """测试AI服务模块"""
        logger.info("【测试AI服务模块】")
        
        try:
            from services.ai.factory import get_llm_service
            
            service = get_llm_service()
            logger.success(f"✓ LLM服务初始化成功: {type(service).__name__}")
            self.results.append(("ai_service_init", True))
            
            return True
        except Exception as e:
            logger.error(f"✗ AI服务模块测试失败: {e}")
            self.results.append(("ai_service_init", False))
            return False
    
    def test_database_models(self):
        """测试数据库模型"""
        logger.info("【测试数据库模型】")
        
        try:
            from models.user import User
            from models.destination import Destination
            from models.attraction import Attraction
            from models.itinerary import Itinerary
            
            logger.success("✓ 数据库模型导入成功")
            self.results.append(("database_models", True))
            
            return True
        except Exception as e:
            logger.error(f"✗ 数据库模型测试失败: {e}")
            self.results.append(("database_models", False))
            return False
    
    def test_api_endpoints(self):
        """测试API端点"""
        logger.info("【测试API端点】")
        
        try:
            from api.v1.endpoints import chat, plan, professional_plan
            from api.v1.endpoints import health, intelligent_plan
            
            logger.success("✓ API端点导入成功")
            self.results.append(("api_endpoints", True))
            
            return True
        except Exception as e:
            logger.error(f"✗ API端点测试失败: {e}")
            self.results.append(("api_endpoints", False))
            return False
    
    def test_core_modules(self):
        """测试核心模块"""
        logger.info("【测试核心模块】")
        
        try:
            from core.config import settings
            from core.database import init_db
            
            logger.success(f"✓ 核心模块导入成功")
            self.results.append(("core_modules", True))
            
            return True
        except Exception as e:
            logger.error(f"✗ 核心模块测试失败: {e}")
            self.results.append(("core_modules", False))
            return False
    
    def test_planning_modules(self):
        """测试规划模块"""
        logger.info("【测试规划模块】")
        
        try:
            from services.planning import (
                get_professional_generator,
                get_budget_calculator,
                get_workflow_manager,
                get_professional_planning_service
            )
            
            # 测试生成器
            generator = get_professional_generator()
            logger.success(f"✓ 专业生成器初始化成功")
            
            # 测试预算计算器
            calculator = get_budget_calculator()
            logger.success(f"✓ 预算计算器初始化成功")
            
            # 测试工作流管理器
            manager = get_workflow_manager()
            logger.success(f"✓ 工作流管理器初始化成功")
            
            # 测试规划服务
            service = get_professional_planning_service()
            logger.success(f"✓ 规划服务初始化成功")
            
            self.results.append(("planning_modules", True))
            return True
            
        except Exception as e:
            logger.error(f"✗ 规划模块测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.results.append(("planning_modules", False))
            return False
    
    def test_conversation_engine(self):
        """测试对话引擎"""
        logger.info("【测试对话引擎】")
        
        try:
            from services.conversation_engine import ConversationEngine
            
            engine = ConversationEngine()
            logger.success(f"✓ 对话引擎初始化成功")
            self.results.append(("conversation_engine", True))
            
            return True
        except Exception as e:
            logger.error(f"✗ 对话引擎测试失败: {e}")
            self.results.append(("conversation_engine", False))
            return False
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "="*80)
        print("模块测试摘要")
        print("="*80)
        
        total = len(self.results)
        passed = sum(1 for _, p in self.results if p)
        failed = total - passed
        
        print(f"总模块数: {total}")
        print(f"通过: {passed} ({passed/total*100:.1f}%)")
        print(f"失败: {failed}")
        print("="*80)
        
        for module_name, passed in self.results:
            status = "✓" if passed else "✗"
            print(f"{status} {module_name}")
    
    def run_all(self):
        """运行所有测试"""
        print("\n" + "="*80)
        print("开始模块化测试")
        print("="*80 + "\n")
        
        # AI服务
        self.test_ai_services()
        
        # 数据库模型
        self.test_database_models()
        
        # API端点
        self.test_api_endpoints()
        
        # 核心模块
        self.test_core_modules()
        
        # 规划模块
        self.test_planning_modules()
        
        # 对话引擎
        self.test_conversation_engine()
        
        # 打印摘要
        self.print_summary()
        
        return self.results


if __name__ == "__main__":
    tester = ModuleTester()
    results = tester.run_all()
    
    passed_count = sum(1 for _, p in results if p)
    sys.exit(0 if passed_count == len(results) else 1)
