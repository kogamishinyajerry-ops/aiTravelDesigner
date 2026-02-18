# LLM集成说明文档

## 📋 概述

AI旅行规划软件支持三种LLM服务模式：

1. **Mock服务**（默认）- 无需API Key，模拟AI回复
2. **OpenAI官方** - 使用gpt-4o等模型
3. **第三方兼容服务** - DeepSeek等兼容OpenAI API的服务

---

## 🏗️ 架构设计

### 服务工厂模式

```python
# backend/services/ai/factory.py
def get_llm_service(use_mock: bool = False):
    """智能选择LLM服务"""
    
    # 1. 明确要求Mock
    if use_mock:
        return MockLLMService()
    
    # 2. 没有API Key，自动降级到Mock
    if not settings.OPENAI_API_KEY:
        return MockLLMService()
    
    # 3. 使用真实LLM
    try:
        return LLMService()
    except Exception:
        # 降级处理
        return MockLLMService()
```

### 服务类型

| 服务类 | 文件 | 说明 |
|-------|------|------|
| LLMService | `llm_service.py` | 真实OpenAI/兼容API |
| MockLLMService | `mock_llm_service.py` | 模拟AI回复（无需API） |

---

## 🔧 配置方式

### 1. 使用Mock服务（推荐用于测试）

编辑 `backend/.env`:

```env
# 不设置或留空
OPENAI_API_KEY=
```

**特点：**
- ✅ 无需API Key
- ✅ 可以完整测试功能
- ⚠️ 基于规则的回复，不够智能

**使用场景：**
- 开发测试
- 演示项目
- 没有API Key时

### 2. 使用OpenAI官方服务

编辑 `backend/.env`:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxx

# OpenAI API地址
OPENAI_BASE_URL=https://api.openai.com/v1

# 模型选择
OPENAI_MODEL=gpt-4o
# 可选: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
```

**获取API Key：**
1. 访问 https://platform.openai.com/api-keys
2. 登录或注册OpenAI账号
3. 创建新的API Key
4. 复制Key到.env文件

**费用说明：**
- gpt-4o: ~$5 / 1M tokens
- gpt-4-turbo: ~$0.01 / 1K tokens
- 新账号通常有免费额度

### 3. 使用第三方兼容服务

#### DeepSeek（推荐 - 性价比高）

编辑 `backend/.env`:

```env
# DeepSeek API Key
OPENAI_API_KEY=your-deepseek-key-here

# DeepSeek API地址
OPENAI_BASE_URL=https://api.deepseek.com/v1

# DeepSeek模型
OPENAI_MODEL=deepseek-chat
# 可选: deepseek-chat, deepseek-coder
```

**获取API Key：**
1. 访问 https://platform.deepseek.com/
2. 注册账号
3. 在API Keys页面创建Key
4. 复制到.env

**费用说明：**
- deepseek-chat: ~¥0.14 / 1M tokens
- 比OpenAI便宜很多

#### 其他兼容服务

任何兼容OpenAI API格式的服务都可以使用：

```env
# 通用配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://your-provider.com/v1
OPENAI_MODEL=your-model-name
```

常见兼容服务：
- DeepSeek: https://api.deepseek.com/v1
- 通义千问: https://dashscope.aliyuncs.com/compatible-mode/v1
- 智谱AI: https://open.bigmodel.cn/api/paas/v4/

---

## 🔄 服务切换

### 运行时切换

无需重启服务，修改`.env`后：
```bash
# 编辑.env
vim backend/.env

# 后端使用reload模式会自动重载
# 或手动重启
pkill -f "uvicorn.*main:app"
cd backend && ./start.sh
```

### 代码中强制使用Mock

```python
from services.ai.factory import get_llm_service, get_mock_llm_service

# 使用真实服务（自动选择）
llm = get_llm_service()

# 强制使用Mock
llm = get_mock_llm_service()
```

---

## 🧪 测试LLM连接

### 测试Mock服务

```bash
# 不配置API Key，直接启动
cd backend
./start.sh

# 测试对话
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "我想去日本旅游", "user_id": 1}'
```

**预期输出：**
```json
{
  "success": true,
  "message": "好的！我了解到：目的地：日本。为了给您更好的建议...",
  "extracted_info": {
    "destination": "日本",
    "days": 7
  },
  "missing_info": ["start_date", "budget"],
  "is_complete": false,
  "confidence": 0.65
}
```

### 测试真实API

```bash
# 1. 配置API Key
vim backend/.env
# 设置 OPENAI_API_KEY=sk-xxxx

# 2. 重启服务
cd backend
./start.sh

# 3. 测试对话
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "我想和爱人去京都玩5天", "user_id": 1}'
```

**预期输出：**
```json
{
  "success": true,
  "message": "太好了！京都确实是个非常适合情侣的目的地。请问...",
  "extracted_info": {
    "destination": "京都",
    "days": 5,
    "travelers": {"adults": 2, "children": 0}
  },
  "missing_info": ["start_date", "budget"],
  "is_complete": false,
  "confidence": 0.75
}
```

---

## 📊 对比表格

| 特性 | Mock服务 | OpenAI | DeepSeek |
|------|---------|---------|-----------|
| 需要API Key | ❌ | ✅ | ✅ |
| 成本 | 免费 | 付费 | 便宜 |
| 智能度 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 响应速度 | 快 | 中等 | 快 |
| 中文支持 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 推荐场景 | 测试/演示 | 正式使用 | 性价比优先 |

---

## 🐛 故障排查

### 问题1: API Key无效

**错误日志：**
```
Error: 401 Unauthorized
Invalid API key
```

**解决：**
1. 检查API Key是否正确复制（不要有空格）
2. 确认API Key是否有效（登录服务商后台检查）
3. 检查余额是否充足

### 问题2: 连接失败

**错误日志：**
```
ConnectionError: Failed to connect to API
```

**解决：**
1. 检查 `OPENAI_BASE_URL` 是否正确
2. 检查网络连接（需要能访问外网）
3. 如果使用代理，配置代理设置

### 问题3: 自动降级到Mock

**日志信息：**
```
Warning: Failed to initialize LLM service: ...
Falling back to Mock LLM service...
```

**原因：**
- 没有配置API Key
- API Key无效
- 网络连接失败

**解决：**
- 检查 `.env` 配置
- 测试网络连接
- 查看完整错误日志

---

## 💡 最佳实践

1. **开发阶段**
   - 使用Mock服务快速测试
   - 避免消耗API额度

2. **测试阶段**
   - 使用DeepSeek等便宜服务
   - 验证功能完整性

3. **生产环境**
   - 使用OpenAI或其他成熟服务
   - 实现请求缓存降低成本
   - 添加API调用监控

4. **错误处理**
   - 始终降级到Mock服务
   - 记录失败原因到日志
   - 给用户友好提示

---

## 📈 性能优化

### 1. 请求缓存

```python
# 在LLMService中添加缓存
from functools import lru_cache

@lru_cache(maxsize=100)
async def understand_travel_need(...):
    # 缓存相同请求
```

### 2. 批量请求

如果需要处理大量请求，考虑：
- 使用异步并发
- 实现请求队列
- 添加速率限制

### 3. 成本控制

```python
# 实现token计数
def estimate_tokens(text: str) -> int:
    # 简单估算：1中文字符 ≈ 1.5 tokens
    return len(text.encode('utf-8')) * 1.5

# 添加使用量监控
total_tokens_used += estimate_tokens(user_input)
```

---

## 🔗 相关资源

- OpenAI文档: https://platform.openai.com/docs
- DeepSeek文档: https://platform.deepseek.com/docs
- API兼容性: OpenAI API格式已成为事实标准
- 本项目API文档: http://localhost:8000/docs

---

## 📞 支持

如遇到问题：

1. 查看 `logs/app.log` 日志文件
2. 运行 `test-complete-workflow.sh` 测试脚本
3. 参考 `QUICK_START.md` 快速启动指南
4. 查看GitHub Issues（如果有）
