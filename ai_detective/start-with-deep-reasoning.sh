#!/bin/bash

# AI Detective v2.0 - 深度推理版启动脚本

echo "=========================================="
echo "  AI Detective v2.0 - 深度推理版"
echo "=========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
cd /workspace/ai_detective

if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 未找到 requirements.txt"
    exit 1
fi

# 安装依赖(如果需要)
echo "🔧 安装依赖..."
pip3 install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "⚠️  警告: 依赖安装可能有问题"
fi

echo "✅ 依赖检查完成"
echo ""

# 启动后端服务器
echo "🚀 启动后端服务器..."
cd backend

echo "📡 API地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""

# 启动服务器
python3 main.py

# 如果服务器停止,显示信息
echo ""
echo "=========================================="
echo "  服务器已停止"
echo "=========================================="
echo ""
echo "💡 提示:"
echo "  - 查看前端: file://$PWD/../frontend/deep-reasoning.html"
echo "  - 运行测试: python3 ../test_deep_reasoning_integration.py"
echo "  - API测试: python3 ../test_api_deep_reasoning.py"
echo ""
