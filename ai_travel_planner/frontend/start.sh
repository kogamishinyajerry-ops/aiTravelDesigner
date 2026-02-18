#!/bin/bash

echo "=========================================="
echo "AI旅行规划软件 - 前端服务启动"
echo "=========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 进入目录
cd "$(dirname "$0")"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}未检测到Node.js${NC}"
    echo "请先安装Node.js: https://nodejs.org/"
    exit 1
fi

echo "Node.js版本: $(node --version)"
echo "npm版本: $(npm --version)"
echo ""

# 检查依赖
if [ ! -d node_modules ]; then
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}依赖安装完成${NC}"
    else
        echo -e "${YELLOW}依赖安装失败${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}依赖已安装${NC}"
fi

# 检查是否已有服务运行
if pgrep -f "react-scripts.*start" > /dev/null; then
    echo ""
    echo -e "${YELLOW}检测到已有服务运行${NC}"
    read -p "是否重启服务? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "停止旧服务..."
        pkill -f "react-scripts.*start"
        sleep 2
    else
        echo "退出启动"
        exit 0
    fi
fi

# 启动服务
echo "启动React开发服务器..."
echo ""

npm start

# npm start会一直运行，不会退出
