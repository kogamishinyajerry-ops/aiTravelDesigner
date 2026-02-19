# AI Detective - 深度推理功能使用指南

## 🎯 新增功能

**v2.0** 现已集成深度推理引擎,提供更深入的案件分析能力!

### 核心能力

1. **时间序列分析** - 构建时间线,检测时间冲突
2. **因果关系分析** - 识别因果链,检测因果缺口
3. **矛盾检测** - 发现事实和证据中的矛盾
4. **预谋性分析** - 判断是否为预谋犯罪
5. **证据链分析** - 评估证据完整性和一致性
6. **逻辑分析** - 检查逻辑一致性和完整性

---

## 🚀 快速开始

### 1. 启动服务器

```bash
cd /workspace/ai_detective/backend
python main.py
```

服务器将在 `http://localhost:8000` 启动

### 2. 使用深度推理API

#### 方式一: 基础分析 + 深度推理

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "12月15日下午3点,一女生到店后待1小时支付400元。支付后立刻退款要求引发争执,对方拍照取证。6点47分在小红书发帖诽谤,次日收到行政处罚。",
    "use_v3": true,
    "use_deep_reasoning": true,
    "context": {}
  }'
```

#### 方式二: 专门的深度推理端点

```bash
curl -X POST http://localhost:8000/deep-reason \
  -H "Content-Type: application/json" \
  -d '{
    "description": "今年12月15日下午3点,一个女生来到我的店铺。她在店里待了大约1小时,大概4点左右支付了400余元。支付后她立刻要求退款,双方发生争执。对方现场报警并拍照取证。晚上6点47分,她在小红书发布了一篇笔记,称店铺诈骗。第二天,我收到了行政处罚。",
    "use_v3": true,
    "context": {}
  }'
```

### 3. 运行测试

```bash
# 测试深度推理引擎
python3 /workspace/ai_detective/test_deep_reasoning_integration.py

# 测试API
python3 /workspace/ai_detective/test_api_deep_reasoning.py
```

---

## 📊 API响应说明

### 基础分析 + 深度推理 (`/analyze`)

```json
{
  "facts": [...],
  "legal_relations": [...],
  "applicable_laws": [...],
  "dispute_focuses": [...],
  "evidence_gaps": [...],
  "investigation_plan": {...},
  "litigation_strategy": [...],
  "confidence": 0.75,
  "deep_reasoning": {
    "time_analysis": {
      "timestamps_count": 5,
      "timeline": {...},
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
    "logical_analysis": {
      "logic_valid": true,
      "logical_consistency": 0.85,
      "logical_completeness": 0.70
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

### 专门的深度推理端点 (`/deep-reason`)

```json
{
  "base_analysis": {
    "facts": [...],
    "dispute_focuses": [...],
    "evidence_gaps": [...],
    "investigation_plan": {...}
  },
  "deep_reasoning": {...},
  "deep_report": "完整的深度推理报告文本...",
  "overall_confidence": {
    "base": 0.75,
    "deep": 0.65,
    "combined": 0.70
  }
}
```

---

## 🔍 深度推理结果解读

### 时间序列分析

- **timestamps_count**: 提取到的时间戳数量
- **timeline**: 时间线摘要
- **time_conflicts**: 时间冲突列表
- **logic_valid**: 时间逻辑是否有效

**解读**:
- 时间戳越多,时间线越完整
- 时间冲突需要核实
- 逻辑有效性 = True 表示时间顺序合理

### 因果关系分析

- **relations_count**: 因果关系数量
- **chains_count**: 因果链数量
- **gaps_count**: 因果缺口数量
- **root_cause**: 根本原因
- **root_cause_confidence**: 根本原因置信度

**解读**:
- 因果关系越多,因果网络越复杂
- 缺口越多,证据链越不完整
- 根本原因置信度 > 0.7 表示可靠

### 矛盾检测

- **total_conflicts**: 总矛盾数量
- **fact_conflicts**: 事实矛盾
- **evidence_conflicts**: 证据矛盾

**解读**:
- 矛盾越多,可信度越低
- 需要核实并解决矛盾

### 预谋性分析

- **is_premeditated**: 是否预谋
- **premeditation_score**: 预谋得分 (0-1)
- **indicators**: 预谋迹象
- **reasoning**: 推理说明

**解读**:
- 得分 ≥ 0.7: 高度预谋
- 得分 0.5-0.7: 可能预谋
- 得分 < 0.5: 不太像预谋

### 证据链分析

- **completeness**: 完整度 (0-1)
- **consistency**: 一致性 (0-1)
- **strength**: 强度 (weak/moderate/strong)

**解读**:
- 完整度 > 0.8: 证据类型齐全
- 一致性 > 0.8: 证据无矛盾
- strength = strong: 证据链强大

### 逻辑分析

- **logic_valid**: 逻辑有效性
- **logical_consistency**: 逻辑一致性
- **logical_completeness**: 逻辑完整性

**解读**:
- 三项指标越高,逻辑越严密

---

## 💡 使用建议

### 1. 何时使用深度推理

✅ **推荐使用**:
- 案件复杂,需要深入分析
- 时间线混乱,需要梳理
- 需要判断预谋性
- 需要评估证据链强度

❌ **不需要使用**:
- 简单明确的案件
- 只需要基础法律分析
- 快速响应场景

### 2. 如何提高分析质量

**描述要点**:
- ✅ 详细描述事件经过
- ✅ 包含准确时间信息
- ✅ 说明各方行为
- ✅ 提供完整证据

**避免**:
- ❌ 时间模糊不清
- ❌ 逻辑混乱
- ❌ 证据缺失

### 3. 理解置信度

- **0.8-1.0**: 高度可靠,可参考
- **0.6-0.8**: 基本可靠,建议补充
- **0.4-0.6**: 部分可靠,需要核实
- **< 0.4**: 可靠性低,不建议使用

---

## 📈 性能对比

| 功能 | v1.0 (基础) | v2.0 (深度推理) |
|------|-------------|-----------------|
| 事实要素提取 | ✅ | ✅ |
| 争议焦点识别 | ✅ | ✅ |
| 法律条文匹配 | ✅ | ✅ |
| 时间序列分析 | ❌ | ✅ |
| 因果关系分析 | ❌ | ✅ |
| 矛盾检测 | ❌ | ✅ |
| 预谋性分析 | ❌ | ✅ |
| 证据链分析 | ✅ | ✅ 增强 |
| 逻辑分析 | ❌ | ✅ |

---

## 🐛 常见问题

**Q: 深度推理比基础推理慢吗?**
A: 是的,深度推理需要更多计算时间,通常增加2-3秒。

**Q: 可以只使用深度推理吗?**
A: 建议结合使用。基础推理提供法律框架,深度推理提供深度分析。

**Q: 时间冲突是什么意思?**
A: 时间冲突指时间顺序不合理或时间相互矛盾。

**Q: 预谋性分析准确吗?**
A: 基于行为模式分析,有一定参考价值,但不是最终判断。

---

## 📞 获取帮助

- 查看API文档: http://localhost:8000/docs
- 查看用户指南: USER_GUIDE.md
- 查看开发计划: DEEP_ANALYSIS_AND_DEVELOPMENT_PLAN.md

---

**版本**: v2.0
**更新时间**: 2026-02-18
**状态**: ✅ 已集成
