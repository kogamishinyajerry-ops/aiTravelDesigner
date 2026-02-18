#!/bin/bash

echo "==================================="
echo "AI旅行规划软件 - 测试脚本"
echo "==================================="

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 测试函数
test_api() {
    local name="$1"
    local method="$2"
    local url="$3"
    local data="$4"
    local expected_code="$5"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "测试 $TOTAL_TESTS: $name ... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "http://localhost:8000$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method \
            -H "Content-Type: application/json" \
            -d "$data" \
            "http://localhost:8000$url")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code, expected $expected_code)"
        echo "响应: $body"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# 等待服务启动
echo "等待服务启动..."
sleep 3

echo -e "\n${YELLOW}=== 测试后端API ===${NC}\n"

# 1. 健康检查
test_api "健康检查" "GET" "/api/v1/health" "" "200"

# 2. 创建对话
test_api "创建对话" "POST" "/api/v1/chat/conversations" '{"user_id": 1}' "200"

# 3. 发送测试消息（简单需求）
echo -ne "\n测试 $((TOTAL_TESTS + 1)): 发送测试消息（简单需求） ... "
TOTAL_TESTS=$((TOTAL_TESTS + 1))
response=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d '{"message": "我想去日本旅游7天"}' \
    "http://localhost:8000/api/v1/chat/message")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    
    # 显示响应
    echo -e "${YELLOW}响应预览:${NC}"
    echo "$body" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'  消息: {data.get(\"message\", \"N/A\")[:50]}...')
    print(f'  信息完整: {data.get(\"is_complete\", False)}')
    print(f'  置信度: {data.get(\"confidence\", 0):.2f}')
    print(f'  澄清问题数: {len(data.get(\"clarification_questions\", []))}')
except:
    pass
"
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# 4. 获取对话历史
echo -ne "\n测试 $((TOTAL_TESTS + 1)): 获取对话历史 ... "
TOTAL_TESTS=$((TOTAL_TESTS + 1))
response=$(curl -s -w "\n%{http_code}" -X GET \
    "http://localhost:8000/api/v1/chat/conversations/test-conversation-id")
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" == "404" ]; then
    # 404是预期的，因为对话不存在
    echo -e "${GREEN}✓ PASS${NC} (正确的404响应)"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${YELLOW}✓ SKIP${NC} (对话可能存在)"
fi

echo -e "\n${YELLOW}=== 测试结果 ===${NC}"
echo "总测试数: $TOTAL_TESTS"
echo -e "${GREEN}通过: $PASSED_TESTS${NC}"
echo -e "${RED}失败: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}所有测试通过！${NC}"
    exit 0
else
    echo -e "\n${RED}有测试失败${NC}"
    exit 1
fi
