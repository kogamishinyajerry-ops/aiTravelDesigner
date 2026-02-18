#!/bin/bash

echo "========================================="
echo "AI旅行规划软件 - 完整流程测试"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8000/api/v1"

# 检查服务是否运行
check_service() {
    echo -ne "${BLUE}检查服务状态...${NC} "
    if curl -s "$API_BASE/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 运行中${NC}"
        return 0
    else
        echo -e "${RED}✗ 未运行${NC}"
        echo ""
        echo "请先启动后端服务："
        echo "  cd /workspace/ai_travel_planner/backend"
        echo "  python3 -m uvicorn main:app --host 0.0.0.0 --port 8000"
        return 1
    fi
}

# 测试1: 健康检查
test_health() {
    echo -e "\n${YELLOW}测试 1: 健康检查${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s "$API_BASE/health")
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "响应: $response"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

# 测试2: AI对话 - 简单需求
test_chat_simple() {
    echo -e "\n${YELLOW}测试 2: AI对话 - 简单需求${NC}"
    echo "----------------------------------------"
    
    echo "用户输入: 我想去日本旅游7天"
    
    response=$(curl -s -X POST "$API_BASE/chat/message" \
        -H "Content-Type: application/json" \
        -d '{
            "message": "我想去日本旅游7天",
            "user_id": 1
        }')
    
    # 解析响应
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    message=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', ''))" 2>/dev/null)
    is_complete=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('is_complete', False))" 2>/dev/null)
    confidence=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('confidence', 0))" 2>/dev/null)
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "AI回复: $message"
        echo "信息完整: $is_complete"
        echo "置信度: $confidence"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "响应: $response"
        return 1
    fi
}

# 测试3: AI对话 - 详细需求
test_chat_detailed() {
    echo -e "\n${YELLOW}测试 3: AI对话 - 详细需求${NC}"
    echo "----------------------------------------"
    
    echo "用户输入: 我想和爱人一起去京都玩5天，预算2万"
    
    # 先创建对话
    conv_response=$(curl -s -X POST "$API_BASE/chat/conversations" -H "Content-Type: application/json" -d '{"user_id": 2}')
    conv_id=$(echo "$conv_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('conversation_id', ''))")
    
    if [ -z "$conv_id" ]; then
        echo -e "${RED}✗ FAIL - 创建对话失败${NC}"
        return 1
    fi
    
    echo "对话ID: $conv_id"
    
    # 发送消息
    response=$(curl -s -X POST "$API_BASE/chat/message" \
        -H "Content-Type: application/json" \
        -d "{
            \"message\": \"我想和爱人一起去京都玩5天，预算2万\",
            \"conversation_id\": \"$conv_id\"
        }")
    
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    message=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', ''))" 2>/dev/null)
    missing_count=$(echo "$response" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('missing_info', [])))" 2>/dev/null)
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "AI回复: $message"
        echo "缺失信息数: $missing_count"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "响应: $response"
        return 1
    fi
}

# 测试4: 行程生成
test_plan_generation() {
    echo -e "\n${YELLOW}测试 4: 行程生成${NC}"
    echo "----------------------------------------"
    
    echo "请求: 京都3日游，2人，预算15000"
    
    response=$(curl -s -X POST "$API_BASE/plan/generate" \
        -H "Content-Type: application/json" \
        -d '{
            "destination": "京都",
            "days": 3,
            "start_date": "2024-04-01",
            "travelers": 2,
            "departure": "北京",
            "budget": 15000
        }')
    
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        
        # 提取关键信息
        days=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('itinerary', {}).get('days', 0))")
        total_budget=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('budget', {}).get('total_cost', 0))")
        per_person=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('budget', {}).get('per_person', 0))")
        
        echo "行程天数: $days"
        echo "总预算: ¥$total_budget"
        echo "人均: ¥$per_person"
        
        # 显示第一天的行程
        day1=$(echo "$response" | python3 -c "
import sys, json
itinerary = json.load(sys.stdin).get('itinerary', {})
daily_plans = itinerary.get('daily_plans', [])
if daily_plans:
    day = daily_plans[0]
    print(f'第一天 ({day.get(\"date\")})')
    print(f'景点: {len(day.get(\"attractions\", []))}个')
    timeline = day.get('timeline', [])
    if timeline:
        for item in timeline[:2]:
            print(f'  - {item.get(\"time\")}: {item.get(\"activity\")} - {item.get(\"location\")}')
" 2>/dev/null)
        echo "$day1"
        
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "响应: $response"
        return 1
    fi
}

# 测试5: 预算计算
test_budget() {
    echo -e "\n${YELLOW}测试 5: 预算计算${NC}"
    echo "----------------------------------------"
    
    echo "请求: 东京5日游，2人"
    
    response=$(curl -s -X POST "$API_BASE/plan/budget" \
        -H "Content-Type: application/json" \
        -d '{
            "departure": "上海",
            "destination": "东京",
            "days": 5,
            "travelers": 2
        }')
    
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        
        total=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('budget', {}).get('total_cost', 0))")
        per_person=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('budget', {}).get('per_person', 0))")
        
        echo "总预算: ¥$total"
        echo "人均: ¥$per_person"
        
        # 显示费用分解
        breakdown=$(echo "$response" | python3 -c "
import sys, json
budget = json.load(sys.stdin).get('budget', {})
breakdown = budget.get('breakdown', {})
print('费用分解:')
for category, data in breakdown.items():
    print(f'  {category}: ¥{data.get(\"total\", 0)}')
" 2>/dev/null)
        echo "$breakdown"
        
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "响应: $response"
        return 1
    fi
}

# 测试6: 获取目的地列表
test_destinations() {
    echo -e "\n${YELLOW}测试 6: 获取目的地列表${NC}"
    echo "----------------------------------------"
    
    response=$(curl -s "$API_BASE/plan/destinations")
    
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        
        count=$(echo "$response" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('destinations', [])))")
        echo "支持的目的地数: $count"
        
        echo "目的地列表:"
        echo "$response" | python3 -c "
import sys, json
destinations = json.load(sys.stdin).get('destinations', [])
for dest in destinations:
    print(f'  - {dest.get(\"name\")} ({dest.get(\"country\")}): {dest.get(\"description\")}')
" 2>/dev/null
        
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

# 测试7: 预算优化
test_optimization() {
    echo -e "\n${YELLOW}测试 7: 预算优化建议${NC}"
    echo "----------------------------------------"
    
    echo "请求: 京都5天，预算8000，2人"
    
    response=$(curl -s "$API_BASE/plan/optimization?destination=京都&days=5&budget=8000&travelers=2")
    
    success=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
    
    if [ "$success" = "True" ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        
        status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('feasibility', {}).get('status', ''))" 2>/dev/null)
        recommendation=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('recommendation', ''))" 2>/dev/null)
        
        echo "预算状态: $status"
        echo "建议: $recommendation"
        
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

# 主测试流程
main() {
    echo ""
    echo "开始完整流程测试..."
    echo ""
    
    # 检查服务
    if ! check_service; then
        exit 1
    fi
    
    # 运行测试
    tests=(
        "test_health"
        "test_chat_simple"
        "test_chat_detailed"
        "test_plan_generation"
        "test_budget"
        "test_destinations"
        "test_optimization"
    )
    
    passed=0
    failed=0
    
    for test in "${tests[@]}"; do
        if $test; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
        fi
    done
    
    # 总结
    echo ""
    echo "========================================="
    echo "测试结果"
    echo "========================================="
    echo "总测试数: $((passed + failed))"
    echo -e "${GREEN}通过: $passed${NC}"
    echo -e "${RED}失败: $failed${NC}"
    
    if [ $failed -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 所有测试通过！${NC}"
        echo ""
        echo "现在可以："
        echo "  1. 启动前端: cd frontend && npm start"
        echo "  2. 访问应用: http://localhost:3000"
        echo "  3. 开始使用AI旅行规划功能！"
        exit 0
    else
        echo ""
        echo -e "${YELLOW}部分测试失败，请检查服务配置${NC}"
        exit 1
    fi
}

# 运行主函数
main
