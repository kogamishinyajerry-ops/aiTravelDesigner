#!/bin/bash

echo "=========================================="
echo "AI旅行规划软件 - 后端服务启动"
echo "=========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 进入目录
cd "$(dirname "$0")"

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}未找到.env文件，从.env.example复制...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}已创建.env文件${NC}"
        echo ""
        echo "请编辑.env文件配置必要的参数："
        echo "  - OPENAI_API_KEY (可选，留空则使用Mock服务)"
        echo "  - DATABASE_URL"
        echo ""
        echo "编辑完成后再次运行此脚本"
    else
        echo -e "${YELLOW}未找到.env.example文件${NC}"
    fi
    exit 1
fi

# 检查依赖
echo "检查Python依赖..."
if ! python3 -c "import fastapi, uvicorn, openai" 2>/dev/null; then
    echo -e "${YELLOW}安装依赖...${NC}"
    pip install -q -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}依赖安装完成${NC}"
    else
        echo -e "${YELLOW}依赖安装失败，请手动安装：pip install -r requirements.txt${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}依赖已安装${NC}"
fi

# 创建日志目录
mkdir -p logs

# 检查是否已有服务运行
if pgrep -f "uvicorn.*main:app" > /dev/null; then
    echo ""
    echo -e "${YELLOW}检测到已有服务运行${NC}"
    read -p "是否重启服务? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "停止旧服务..."
        pkill -f "uvicorn.*main:app"
        sleep 2
    else
        echo "退出启动"
        exit 0
    fi
fi

# 检查配置的API Key
OPENAI_KEY=$(grep OPENAI_API_KEY .env | cut -d'=' -f2 | tr -d '"')
if [ -z "$OPENAI_KEY" ] || [ "$OPENAI_KEY" == "your-api-key-here" ]; then
    echo ""
    echo -e "${YELLOW}未配置OPENAI_API_KEY${NC}"
    echo "将使用Mock LLM服务（模拟AI回复）"
    echo ""
    echo "如需使用真实AI功能，请："
    echo "  1. 编辑.env文件"
    echo "  2. 设置OPENAI_API_KEY=your_key_here"
    echo "  3. 可选：设置OPENAI_BASE_URL=https://api.deepseek.com/v1"
    echo ""
    read -p "按Enter继续使用Mock服务..."
    echo ""
fi

# 启动服务
echo "启动FastAPI服务..."
echo ""

nohup python3 -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    --reload > logs/app.log 2>&1 &

BACKEND_PID=$!

# 等待服务启动
echo "等待服务启动..."
sleep 3

# 检查服务状态
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✓ 后端服务启动成功${NC}"
    echo ""
    echo "服务信息："
    echo "  PID: $BACKEND_PID"
    echo "  地址: http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
    echo "  日志: logs/app.log"
    echo ""
    echo "测试API:"
    echo "  curl http://localhost:8000/api/v1/health"
    echo ""
    
    # 快速测试
    echo -n "健康检查... "
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
    else
        echo -e "${YELLOW}服务可能还在启动中...${NC}"
        echo "请查看日志: tail -f logs/app.log"
    fi
    echo ""
    echo "停止服务: kill $BACKEND_PID"
    echo ""
else
    echo -e "${YELLOW}✓ 后端服务启动失败${NC}"
    echo ""
    echo "查看日志:"
    tail -20 logs/app.log
    exit 1
fi
