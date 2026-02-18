"""
测试所有修复
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from loguru import logger


def test_config_import():
    """测试配置导入"""
    logger.info("【测试配置模块】")
    try:
        from core.config import settings
        logger.success(f"✓ 配置导入成功")
        logger.info(f"  数据库URL: {settings.DATABASE_URL}")
        assert "+asyncpg" in settings.DATABASE_URL, "数据库应该使用asyncpg"
        logger.success("✓ 数据库使用asyncpg驱动")
        return True
    except Exception as e:
        logger.error(f"✗ 配置模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security_password():
    """测试安全模块密码处理"""
    logger.info("【测试安全模块密码处理】")
    try:
        from core.security import get_password_hash, verify_password

        # 测试正常长度密码
        normal_password = "test_password_123"
        hashed = get_password_hash(normal_password)
        verified = verify_password(normal_password, hashed)
        assert verified, "正常密码验证应该成功"
        logger.success("✓ 正常密码验证成功")

        # 测试超长密码（超过72字节）
        long_password = "a" * 100
        hashed_long = get_password_hash(long_password)
        verified_long = verify_password(long_password, hashed_long)
        assert verified_long, "截断后的超长密码验证应该成功"
        logger.success("✓ 超长密码（截断）验证成功")

        # 测试错误密码
        wrong_password = "wrong_password"
        verified_wrong = verify_password(wrong_password, hashed)
        assert not verified_wrong, "错误密码验证应该失败"
        logger.success("✓ 错误密码验证正确拒绝")

        return True
    except Exception as e:
        logger.error(f"✗ 安全模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security_tokens():
    """测试安全模块令牌生成"""
    logger.info("【测试安全模块令牌】")
    try:
        from core.security import create_access_token, decode_token, create_refresh_token

        # 测试访问令牌
        data = {"sub": "user123", "role": "user"}
        token = create_access_token(data)
        assert token, "令牌生成不应该为空"
        logger.success("✓ 访问令牌生成成功")

        # 测试令牌解码
        decoded = decode_token(token)
        assert decoded is not None, "令牌解码应该成功"
        assert decoded["sub"] == "user123", "令牌内容应该匹配"
        logger.success("✓ 令牌解码成功")

        # 测试刷新令牌
        refresh_token = create_refresh_token(data)
        assert refresh_token, "刷新令牌生成不应该为空"
        logger.success("✓ 刷新令牌生成成功")

        return True
    except Exception as e:
        logger.error(f"✗ 令牌测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_config():
    """测试数据库配置（不需要实际连接）"""
    logger.info("【测试数据库配置】")
    try:
        from core.database import engine, Base
        from core.config import settings

        # 检查数据库URL格式
        db_url = settings.DATABASE_URL
        assert "postgresql+asyncpg://" in db_url, "应该使用postgresql+asyncpg"
        logger.success("✓ 数据库URL格式正确")

        # 检查引擎配置
        assert engine is not None, "引擎不应该为None"
        logger.success("✓ 异步引擎初始化成功")

        # 检查Base
        assert Base is not None, "Base不应该为None"
        logger.success("✓ Base类初始化成功")

        return True
    except Exception as e:
        logger.error(f"✗ 数据库配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_auth_models():
    """测试认证模型"""
    logger.info("【测试认证模型】")
    try:
        from core.security import UserRole, Permission, ROLE_PERMISSIONS

        # 测试角色
        assert hasattr(UserRole, 'ADMIN'), "应该有ADMIN角色"
        assert hasattr(UserRole, 'USER'), "应该有USER角色"
        logger.success("✓ 角色定义正确")

        # 测试权限
        assert hasattr(Permission, 'CREATE_ITINERARY'), "应该有行程创建权限"
        logger.success("✓ 权限定义正确")

        # 测试角色权限映射
        admin_perms = ROLE_PERMISSIONS.get(UserRole.ADMIN, [])
        assert len(admin_perms) > 0, "管理员应该有权限"
        logger.success(f"✓ 管理员拥有{len(admin_perms)}个权限")

        return True
    except Exception as e:
        logger.error(f"✗ 认证模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints_import():
    """测试API端点导入"""
    logger.info("【测试API端点导入】")
    try:
        from api.v1.endpoints import professional_plan, intelligent_plan
        logger.success("✓ professional_plan端点导入成功")
        logger.success("✓ intelligent_plan端点导入成功")

        # 检查路由器
        assert hasattr(professional_plan, 'router'), "应该有router属性"
        assert hasattr(intelligent_plan, 'router'), "应该有router属性"
        logger.success("✓ 路由器初始化成功")

        return True
    except Exception as e:
        logger.error(f"✗ API端点导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_fix_tests():
    """运行所有修复测试"""
    print("\n" + "="*80)
    print("开始修复验证测试")
    print("="*80 + "\n")

    results = []

    # 测试配置
    results.append(test_config_import())

    # 测试安全模块
    results.append(test_security_password())
    results.append(test_security_tokens())
    results.append(test_auth_models())

    # 测试数据库配置
    results.append(test_database_config())

    # 测试API端点
    results.append(test_api_endpoints_import())

    # 打印摘要
    print("\n" + "="*80)
    print("修复验证摘要")
    print("="*80)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    print(f"总测试数: {total}")
    print(f"通过: {passed} ({passed/total*100:.1f}%)")
    print(f"失败: {failed}")
    print("="*80)

    return all(results)


if __name__ == "__main__":
    success = run_all_fix_tests()
    sys.exit(0 if success else 1)
