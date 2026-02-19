#!/usr/bin/env python3
"""
AI 侦探 - 后端启动脚本
AI Detective Backend Launcher
"""

import uvicorn
import sys
import os

# 添加 backend 目录到 Python 路径
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

# 启动服务器
if __name__ == "__main__":
    print("🔍 AI 侦探 v4.0 - 启动中...")
    print("")
    print("✓ 后端服务启动中...")
    print("📍 API 地址: http://localhost:8000")
    print("📚 API 文档: http://localhost:8000/docs")
    print("🌐 前端地址: http://localhost:8000 (需要配置静态文件)")
    print("")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    print("")
    
    # 启动 uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
