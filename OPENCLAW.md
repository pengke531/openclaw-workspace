# OpenViking Context Manager Skill

本 Skill 实现 OpenViking 的核心上下文管理理念，为 OpenClaw Agent 提供长期记忆和上下文管理能力。

## 功能

1. **文件系统范式管理** - 将上下文组织为虚拟文件系统
2. **三层上下文加载** - L0(摘要) / L1(概要) / L2(详情)
3. **语义检索** - 基于嵌入向量的语义搜索
4. **会话管理** - 自动提取和更新长期记忆

## 核心概念

### URI 协议
- `memory://` - 用户记忆存储
- `agent://` - Agent 技能和指令存储
- `resource://` - 外部资源存储

### 上下文层级
- **L0 (Abstract)** - 一句话摘要，快速检索
- **L1 (Overview)** - 核心信息和使用场景
- **L2 (Details)** - 完整原始数据，按需加载

## 使用方式

当需要管理长期记忆或上下文检索时使用此 Skill：

```
用户要求：
- 记住某个偏好或事实
- 查找之前的上下文
- 管理 Agent 技能
- 检索相关资源
```

## 配置

可选配置外部 OpenViking 服务器：
```json
{
  "openviking_url": "http://localhost:1933",
  "openviking_api_key": ""
}
```

如未配置外部服务器，将使用内置的简化实现。
