"""
测试深度推理API
Test Deep Reasoning API
"""

import requests
import json


def test_analyze_with_deep_reasoning():
    """测试基础分析+深度推理"""
    print("=" * 60)
    print("测试基础分析+深度推理API")
    print("=" * 60)

    url = "http://localhost:8000/analyze"

    test_case = """
    今年12月15日下午3点,一个女生来到我的店铺。
    她在店里待了大约1小时,4点支付400余元后立刻要求退款。
    双方发生争执,对方报警并拍照。
    当晚6点47分,她在小红书发布笔记诽谤店铺诈骗。
    第二天我收到行政处罚。
    """

    request_data = {
        "description": test_case,
        "use_v3": True,
        "use_deep_reasoning": True,
        "context": {}
    }

    print("\n请求数据:")
    print(json.dumps(request_data, ensure_ascii=False, indent=2))

    try:
        response = requests.post(url, json=request_data, timeout=30)
        print(f"\n响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            print("\n【基础分析】")
            print(f"  事实要素: {len(result.get('facts', []))} 个")
            print(f"  争议焦点: {len(result.get('dispute_focuses', []))} 个")
            print(f"  证据缺口: {len(result.get('evidence_gaps', []))} 个")
            print(f"  置信度: {result.get('confidence', 0.0):.2f}")

            if 'deep_reasoning' in result:
                print("\n【深度推理】")
                deep = result['deep_reasoning']
                print(f"  时间戳: {deep.get('time_analysis', {}).get('timestamps_count', 0)} 个")
                print(f"  因果关系: {deep.get('causal_analysis', {}).get('relations_count', 0)} 个")
                print(f"  矛盾数: {deep.get('conflict_analysis', {}).get('total_conflicts', 0)} 个")
                print(f"  预谋得分: {deep.get('premeditation_analysis', {}).get('premeditation_score', 0.0):.2f}")
                print(f"  深度置信度: {deep.get('deep_confidence', 0.0):.2f}")

                # 预谋性分析
                premeditation = deep.get('premeditation_analysis', {})
                if premeditation.get('is_premeditated'):
                    print(f"  ⚠️ 检测到预谋性特征!")

                # 建议
                print("\n【深度推理建议】")
                for rec in deep.get('recommendations', [])[:5]:
                    print(f"  {rec}")

            print("\n✅ 测试成功!")
        else:
            print(f"\n❌ 请求失败: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到API服务器")
        print("请先启动服务器: cd /workspace/ai_detective/backend && python main.py")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


def test_deep_analyze_endpoint():
    """测试专门的深度推理端点"""
    print("\n\n" + "=" * 60)
    print("测试深度推理专用端点")
    print("=" * 60)

    url = "http://localhost:8000/deep-reason"

    test_case = """
    12月15日下午3点,一女生到店后待1小时支付400元。
    支付后立刻退款要求引发争执,对方拍照取证。
    6点47分在小红书发帖诽谤,次日收到行政处罚。
    """

    request_data = {
        "description": test_case,
        "use_v3": True,
        "context": {}
    }

    try:
        response = requests.post(url, json=request_data, timeout=30)
        print(f"\n响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 基础分析
            base = result.get('base_analysis', {})
            print("\n【V3基础分析】")
            print(f"  事实要素: {len(base.get('facts', []))} 个")
            print(f"  争议焦点: {len(base.get('dispute_focuses', []))} 个")
            print(f"  证据缺口: {len(base.get('evidence_gaps', []))} 个")

            investigation = base.get('investigation_plan', {})
            print(f"  优先任务: {len(investigation.get('priority_tasks', []))} 个")

            # 深度推理
            deep = result.get('deep_reasoning', {})
            print("\n【深度推理分析】")
            time_analysis = deep.get('time_analysis', {})
            print(f"  时间戳: {time_analysis.get('timestamps_count', 0)} 个")
            print(f"  时间冲突: {len(time_analysis.get('time_conflicts', []))} 个")
            print(f"  逻辑有效性: {'✅' if time_analysis.get('logic_valid', False) else '❌'}")

            causal_analysis = deep.get('causal_analysis', {})
            print(f"  因果关系: {causal_analysis.get('relations_count', 0)} 个")
            print(f"  因果链: {causal_analysis.get('chains_count', 0)} 条")
            print(f"  因果缺口: {causal_analysis.get('gaps_count', 0)} 个")

            premeditation = deep.get('premeditation_analysis', {})
            print(f"  预谋得分: {premeditation.get('premeditation_score', 0.0):.2f}")
            print(f"  预谋迹象: {len(premeditation.get('indicators', []))} 个")

            # 综合置信度
            overall = result.get('overall_confidence', {})
            print("\n【综合置信度】")
            print(f"  基础分析: {overall.get('base', 0.0):.2f}")
            print(f"  深度推理: {overall.get('deep', 0.0):.2f}")
            print(f"  综合得分: {overall.get('combined', 0.0):.2f}")

            # 报告
            print("\n" + "=" * 60)
            print("深度推理报告")
            print("=" * 60)
            print(result.get('deep_report', '无报告'))

            print("\n✅ 测试成功!")
        else:
            print(f"\n❌ 请求失败: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到API服务器")
        print("请先启动服务器: cd /workspace/ai_detective/backend && python main.py")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


def test_health_check():
    """测试健康检查"""
    print("\n\n" + "=" * 60)
    print("测试健康检查")
    print("=" * 60)

    url = "http://localhost:8000/health"

    try:
        response = requests.get(url, timeout=10)
        print(f"\n响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n状态: {result.get('status')}")
            print(f"时间: {result.get('timestamp')}")
            print("\n模块状态:")
            for module, status in result.get('modules', {}).items():
                print(f"  • {module}: {status}")

            # 检查深度推理模块
            if 'deep_reasoner' in result.get('modules', {}):
                print("\n✅ 深度推理模块已加载!")
            else:
                print("\n⚠️ 深度推理模块未加载")

        else:
            print(f"\n❌ 请求失败: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到API服务器")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")


if __name__ == "__main__":
    print("AI Detective - 深度推理API测试")
    print("=" * 60)

    test_health_check()
    test_analyze_with_deep_reasoning()
    test_deep_analyze_endpoint()

    print("\n\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
