# AI旅行规划软件 - 快速启动指南

## 🚀 快速开始（5分钟）

### 方法1: 使用启动脚本（推荐）

```bash
# 1. 启动后端
cd /workspace/ai_travel_planner/backend
./start.sh

# 2. 新开终端，启动前端
cd /workspace/ai_travel_planner/frontend
./start.sh

# 3. 访问应用
# 浏览器打开: http://localhost:3000
```

### 方法2: 手动启动

```bash
# 后端
cd /workspace/ai_travel_planner/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 前端（新终端）
cd /workspace/ai_travel_planner/frontend
npm start
```

---

## 📝 配置说明

### 后端配置（.env）

创建并编辑 `backend/.env` 文件：

```env
# 基础配置
DEBUG=True

# AI服务配置（选填）
# 留空则使用Mock服务（模拟AI，不需要API Key）
OPENAI_API_KEY=
# 可选：使用DeepSeek等兼容OpenAI的服务
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# 数据库配置
DATABASE_URL=sqlite:///./ai_travel_planner.db

# CORS配置
# 允许的前端地址
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# 安全配置
SECRET_KEY=your-secret-key-change-in-production
ENCRYPTION_KEY=your-encryption-key-change-in-production
```

### AI服务模式说明

#### 模式1: Mock服务（默认，无需API Key）

```env
OPENAI_API_KEY=
```

**特点：**
- ✅ 无需任何API Key
- ✅ 可以测试完整流程
- ✅ 基于规则模拟AI回复
- ⚠️ 不使用真实AI，回复较简单

**适用：**
- 开发测试
- 演示项目
- 没有API Key的场景

#### 模式2: 真实OpenAI服务

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

**特点：**
- ✅ 使用真实AI
- ✅ 智能理解用户需求
- ✅ 灵活的对话交互
- ⚠️ 需要OpenAI API Key（有费用）

**适用：**
- 正式使用
- 需要高质量AI回复

#### 模式3: 第三方兼容服务（DeepSeek等）

```env
OPENAI_API_KEY=your-deepseek-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

**特点：**
- ✅ 使用第三方AI服务
- ✅ 通常比OpenAI便宜
- ✅ 兼容OpenAI API格式
- ⚠️ 需要对应服务的API Key

**适用：**
- 预算有限
- 需要性价比高的方案

---

## 🧪 测试完整流程

### 自动化测试

```bash
cd /workspace/ai_travel_planner
./test-complete-workflow.sh
```

### 手动测试

#### 1. 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

预期输出：
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "..."
}
```

#### 2. AI对话

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想去日本旅游7天",
    "user_id": 1
  }'
```

#### 3. 生成行程

```bash
curl -X POST http://localhost:8000/api/v1/plan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "京都",
    "days": 3,
    "start_date": "2024-04-01",
    "travelers": 2,
    "departure": "北京",
    "budget": 15000
  }'
```

#### 4. 计算预算

```bash
curl -X POST http://localhost:8000/api/v1/plan/budget \
  -H "Content-Type: application/json" \
  -d '{
    "departure": "上海",
    "destination": "东京",
    "days": 5,
    "travelers": 2
  }'
```

---

## 🎯 支持的目的地

目前支持的目的地（行程生成）：

| 城市 | 国家 | 推荐天数 | 日均预算 | 标签 |
|------|------|----------|----------|------|
| 京都 | 日本 | 3-5天 | ¥500 | 历史、文化、美食、自然 |
| 东京 | 日本 | 4-6天 | ¥600 | 购物、美食、现代、动漫 |
| 大阪 | 日本 | 2-3天 | ¥450 | 美食、购物、主题公园 |
| 曼谷 | 泰国 | 3-4天 | ¥300 | 佛教、美食、购物、海滩 |
| 巴黎 | 法国 | 4-7天 | ¥1200 | 艺术、历史、浪漫、美食 |

---

## 📊 功能测试清单

- [ ] 后端服务启动成功（访问 http://localhost:8000/docs）
- [ ] 前端服务启动成功（访问 http://localhost:3000）
- [ ] AI对话功能正常（可以理解用户需求）
- [ ] 行程生成功能正常（可以生成每日行程）
- [ ] 预算计算功能正常（可以计算总预算）
- [ ] 前后端通信正常（可以发送和接收数据）

---

## 🔧 故障排查

### 问题1: 后端启动失败

**症状：** 运行 `./start.sh` 后服务未启动

**解决：**
```bash
# 查看日志
tail -50 logs/app.log

# 常见问题：
# 1. 端口被占用 - lsof -i:8000
# 2. 依赖缺失 - pip install -r requirements.txt
# 3. Python版本不对 - 需要 Python 3.8+
```

### 问题2: 前端启动失败

**症状：** 运行 `npm start` 后报错

**解决：**
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install

# 检查Node.js版本（需要 14+）
node --version

# 检查端口占用（默认3000）
# 可通过修改 package.json 的 scripts 使用其他端口
```

### 问题3: API请求失败

**症状：** 前端显示网络错误

**解决：**
1. 检查后端是否运行：`curl http://localhost:8000/api/v1/health`
2. 检查CORS配置：`backend/.env` 中的 `CORS_ORIGINS`
3. 查看浏览器控制台的错误信息

### 问题4: AI回复异常

**症状：** AI回复不正确或报错

**解决：**
```bash
# 1. 检查是否使用Mock服务
# 查看 .env 文件的 OPENAI_API_KEY 是否为空

# 2. 如果使用真实API，检查Key是否正确
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. 查看后端日志
tail -f logs/app.log | grep -i error
```

---

## 📖 更多文档

- [开发总结 - Phase 1 & 2](./DEVELOPMENT_SESSION_SUMMARY.md)
- [开发总结 - Phase 3 & 4](./DEVELOPMENT_SUMMARY_PHASE3_4.md)
- [TODO List](./TODO.md)
- [API文档](http://localhost:8000/docs) - 启动后访问

---

## 🎉 开始使用

一切配置好后：

1. 打开浏览器访问 http://localhost:3000
2. 在对话界面输入你的旅行需求
3. AI会引导你完成信息收集
4. 信息完整后可以生成行程方案
5. 查看详细的每日安排和预算分析

**祝旅途愉快！** ✈️
