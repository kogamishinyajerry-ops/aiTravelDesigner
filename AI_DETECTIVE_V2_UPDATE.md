# AI Detective v2.0 - 深度推理功能更新

## 📢 重大更新

**AI Detective 现已升级到 v2.0！**

集成深度推理引擎,提供更强大的案件分析能力！

---

## 🎯 核心新增功能

### 1. 时间序列分析 ⏰
- 自动提取时间戳
- 构建完整时间线
- 检测时间冲突
- 分析时间逻辑

### 2. 因果关系分析 🔗
- 识别因果关系
- 构建因果链
- 检测因果缺口
- 分析根本原因

### 3. 矛盾检测 ⚠️
- 事实矛盾检测
- 证据矛盾检测
- 时间矛盾检测
- 陈述矛盾检测

### 4. 预谋性分析 🎯
- 行为模式识别
- 预谋迹象识别
- 预谋性评分(0-1)
- 判断是否预谋犯罪

### 5. 证据链分析 🔒
- 证据完整度计算
- 证据一致性评估
- 证据强度判断
- 证据缺口识别

### 6. 逻辑分析 🧠
- 逻辑有效性检查
- 逻辑一致性计算
- 逻辑完整性评估

---

## 🚀 快速开始

### 方式一: 使用API

```bash
# 启动服务器
cd /workspace/ai_detective/backend
python main.py

# 调用深度推理API
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "12月15日下午3点,一女生到店后待1小时支付400元。支付后立刻退款要求引发争执,对方拍照取证。6点47分在小红书发帖诽谤,次日收到行政处罚。",
    "use_v3": true,
    "use_deep_reasoning": true,
    "context": {}
  }'
```

### 方式二: 使用前端界面

1. 启动服务器: `cd /workspace/ai_detective/backend && python main.py`
2. 在浏览器打开: `file:///workspace/ai_detective/frontend/deep-reasoning.html`
3. 输入案件描述
4. 点击"开始深度分析"

### 方式三: 使用Python脚本

```python
import requests

response = requests.post(
    'http://localhost:8000/analyze',
    json={
        'description': '案件描述...',
        'use_v3': True,
        'use_deep_reasoning': True
    }
)

result = response.json()

# 查看深度推理结果
deep = result['deep_reasoning']
print(f"时间戳: {deep['time_analysis']['timestamps_count']}")
print(f"因果关系: {deep['causal_analysis']['relations_count']}")
print(f"预谋得分: {deep['premeditation_analysis']['premeditation_score']:.2f}")
```

---

## 📊 API响应示例

```json
{
  "facts": [...],
  "dispute_focuses": [...],
  "evidence_gaps": [...],
  "investigation_plan": {...},
  "confidence": 0.75,
  "deep_reasoning": {
    "time_analysis": {
      "timestamps_count": 5,
      "time_conflicts": [...],
      "logic_valid": false
    },
    "causal_analysis": {
      "relations_count": 3,
      "chains_count": 1,
      "gaps_count": 0,
      "root_cause": "...",
      "root_cause_confidence": 0.85
    },
    "conflict_analysis": {
      "total_conflicts": 2,
      "fact_conflicts": [...],
      "evidence_conflicts": [...]
    },
    "premeditation_analysis": {
      "is_premeditated": false,
      "premeditation_score": 0.40,
      "indicators": [...],
      "reasoning": "..."
    },
    "evidence_chain": {
      "completeness": 0.60,
      "consistency": 0.80,
      "strength": "moderate"
    },
    "recommendations": [...],
    "deep_confidence": 0.65
  }
}
```

---

## 🔍 新增API端点

### POST `/analyze` (增强版)

原有的分析端点,现在支持深度推理选项:

**请求参数**:
- `description` (必需): 案件描述
- `use_v3` (可选): 是否使用V3推理器,默认 `false`
- `use_deep_reasoning` (可选): 是否使用深度推理,默认 `false`
- `context` (可选): 上下文信息

### POST `/deep-reason` (新增)

专门的深度推理端点,返回完整的深度分析结果:

**请求参数**:
- `description` (必需): 案件描述
- `use_v3` (可选): 是否使用V3推理器,默认 `true`
- `context` (可选): 上下文信息

**返回内容**:
- `base_analysis`: V3基础分析结果
- `deep_reasoning`: 深度推理结果
- `deep_report`: 完整的深度推理报告文本
- `overall_confidence`: 综合置信度(基础+深度)

---

## 📈 性能提升

| 功能 | v1.0 | v2.0 |
|------|-----|------|
| 时间序列分析 | ❌ | ✅ |
| 因果关系分析 | ❌ | ✅ |
| 矛盾检测 | ❌ | ✅ |
| 预谋性分析 | ❌ | ✅ |
| 证据链分析 | ✅ 基础 | ✅ 增强 |
| 逻辑分析 | ❌ | ✅ |
| API端点 | 7个 | 8个 |

---

## 📁 新增文件

### 测试脚本
- `test_deep_reasoning_integration.py` - 深度推理单元测试
- `test_api_deep_reasoning.py` - API集成测试

### 前端界面
- `frontend/deep-reasoning.html` - 深度推理可视化界面

### 文档
- `DEEP_REASONING_GUIDE.md` - 深度推理使用指南
- `DEEP_REASONING_INTEGRATION_COMPLETE.md` - 集成完成报告

---

## 🧪 测试

### 运行单元测试

```bash
cd /workspace/ai_detective
python3 test_deep_reasoning_integration.py
```

### 运行API测试

```bash
cd /workspace/ai_detective
python3 test_api_deep_reasoning.py
```

### 查看API文档

启动服务器后访问:
```
http://localhost:8000/docs
```

---

## 💡 使用建议

### 何时使用深度推理

✅ **推荐使用**:
- 复杂案件需要深入分析
- 时间线混乱需要梳理
- 需要判断预谋性
- 需要评估证据链强度

❌ **不需要使用**:
- 简单明确的案件
- 只需要基础法律分析
- 快速响应场景

### 提高分析质量

**描述要点**:
- ✅ 详细描述事件经过
- ✅ 包含准确时间信息
- ✅ 说明各方行为
- ✅ 提供完整证据

**避免**:
- ❌ 时间模糊不清
- ❌ 逻辑混乱
- ❌ 证据缺失

---

## 📚 文档

- **使用指南**: `DEEP_REASONING_GUIDE.md`
- **完成报告**: `DEEP_REASONING_INTEGRATION_COMPLETE.md`
- **用户指南**: `USER_GUIDE.md`
- **开发计划**: `DEEP_ANALYSIS_AND_DEVELOPMENT_PLAN.md`
- **API文档**: http://localhost:8000/docs

---

## 🎉 总结

**阶段一: 核心深度推理整合 - ✅ 完成**

已完成:
- ✅ 时间序列分析引擎
- ✅ 因果推理引擎
- ✅ 矛盾检测引擎
- ✅ 预谋性分析引擎
- ✅ 证据链分析增强
- ✅ 逻辑分析引擎
- ✅ API集成完成
- ✅ 前端界面开发
- ✅ 测试覆盖完成
- ✅ 文档编写完成

**下一阶段**: 阶段二 - 预谋性/惯犯/团伙分析

---

**版本**: v2.0
**更新时间**: 2026-02-18
**状态**: ✅ 已发布
