#!/bin/bash

echo "=========================================="
echo "AI旅行规划软件 - 开发环境启动"
echo "=========================================="

# 检查环境
echo "[1/5] 检查环境..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi

echo "✅ 环境检查通过"

# 配置环境变量
echo ""
echo "[2/5] 配置环境变量..."

if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入正确的配置"
    exit 1
fi

echo "✅ 环境变量已配置"

# 安装Python依赖
echo ""
echo "[3/5] 安装后端依赖..."

if [ ! -d backend/venv ]; then
    echo "创建Python虚拟环境..."
    cd backend
    python3 -m venv venv
    cd ..
fi

echo "激活虚拟环境并安装依赖..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "✅ 后端依赖安装完成"

# 安装Node依赖
echo ""
echo "[4/5] 安装前端依赖..."

cd frontend
npm install
cd ..

echo "✅ 前端依赖安装完成"

# 初始化数据库
echo ""
echo "[5/5] 初始化数据库..."

# TODO: 这里需要配置数据库后执行
# cd backend
# source venv/bin/activate
# alembic upgrade head
# cd ..

echo "⚠️  数据库初始化需要配置数据库连接后执行"
echo "    cd backend && source venv/bin/activate && alembic upgrade head"

echo ""
echo "=========================================="
echo "✅ 开发环境准备完成！"
echo "=========================================="
echo ""
echo "启动方式："
echo ""
echo "1. 启动后端（新终端）："
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. 启动前端（新终端）："
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. 访问应用："
echo "   前端: http://localhost:3000"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/api/docs"
echo ""
echo "=========================================="
