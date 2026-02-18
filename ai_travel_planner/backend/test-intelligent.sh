#!/bin/bash

# 智能规划器测试脚本
# 基于 PLTR 哲学的智能系统测试

set -e  # 遇到错误立即退出

cd "$(dirname "$0")"
BACKEND_DIR="$(pwd)"

echo "======================================================"
echo "🚀 AI Travel Planner - 智能规划器测试"
echo "基于 PLTR 开发哲学"
echo "======================================================"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"
echo ""

# 检查依赖
echo "📦 检查依赖..."
required_packages=("fastapi" "uvicorn" "pydantic" "loguru" "numpy")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -ne 0 ]; then
    echo "❌ 缺少依赖: ${missing_packages[*]}"
    echo "正在安装依赖..."
    pip install -q "${missing_packages[@]}"
    echo "✓ 依赖安装完成"
else
    echo "✓ 所有依赖已安装"
fi
echo ""

# 运行测试
echo "======================================================"
echo "🧪 运行智能规划器测试"
echo "======================================================"
echo ""

if [ -f "test_intelligent_planner.py" ]; then
    python3 test_intelligent_planner.py
else
    echo "❌ 测试文件不存在: test_intelligent_planner.py"
    exit 1
fi

echo ""
echo "======================================================"
echo "✅ 测试完成"
echo "======================================================"
echo ""
echo "📊 后续步骤:"
echo "  1. 查看测试结果"
echo "  2. 检查日志文件: logs/app.log"
echo "  3. 启动服务: ./start.sh"
echo "  4. 访问 API 文档: http://localhost:8000/api/docs"
echo ""
