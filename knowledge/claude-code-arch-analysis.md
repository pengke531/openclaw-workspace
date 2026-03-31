# Claude Code 架构分析报告
> 来源：泄露源码 claude-code-leaked (2026-03-31 v2.1.88)
> 分析时间：2026-04-01
> 适用：OPC 系统架构演进参考

---

## 一、核心架构概览

Claude Code 是一个 ~1,900 文件、512,000+ 行 TypeScript 的 CLI 应用，核心架构如下：

| 层次 | 技术选型 | 说明 |
|------|---------|------|
| 语言 | TypeScript (strict + ES modules) | |
| 运行时 | Bun | 支持 bun:bundle 特性标记做树摇 |
| 终端 UI | React + Ink | React 写 CLI 界面 |
| CLI 解析 | Commander.js | |
| API 客户端 | @anthropic-ai/sdk | |
| 验证 | Zod v4 | 所有边界输入验证 |
| 协议 | MCP (Model Context Protocol) | 工具/资源发现 |

---

## 二、多 Agent 协调模型（对 OPC 最关键）

### 2.1 Coordinator Pattern

Claude Code 实现了完整的多 Agent 协调架构：

```
用户 → Coordinator (主控) → Worker 1 + Worker 2 + ... (并行)
                    ↓
            聚合结果 → 返回用户
```

**核心工具：**
- `AgentTool` — 派生新 worker（`subagent_type: "worker"`）
- `SendMessageTool` — 继续已有 worker
- `TaskStopTool` — 停止 worker
- `TeamCreateTool / TeamDeleteTool` — 团队管理

**任务通知机制（XML格式）：**
```xml
<task-notification>
  <task-id>{agentId}</task-id>
  <status>completed|failed|killed</status>
  <summary>{摘要}</summary>
  <result>{worker最终文本}</result>
  <usage>
    <total_tokens>N</total_tokens>
    <tool_uses>N</tool_uses>
    <duration_ms>N</duration_ms>
  </usage>
</task-notification>
```

**关键设计原则：**
1. Coordinator 永远做聚合（Synthesis），不直接做研究
2. Worker 结果到达前，Coordinator 不能预测结果
3. 写给 Worker 的 prompt 必须自包含（Worker 看不到对话历史）
4. 必须包含具体文件路径、行号、错误信息
5. 明确区分"继续"（有上下文重叠）vs"新建"（完全独立任务）

### 2.2 Task Workflow 四阶段

| 阶段 | 执行者 | 说明 |
|------|--------|------|
| Research | Workers（并行） | 调研代码库、理解问题 |
| Synthesis | Coordinator | 阅读发现，综合成具体实施规格 |
| Implementation | Workers | 按规格做定向修改，提交 |
| Verification | Workers | 独立验证，不是自我确认 |

### 2.3 OPC 借鉴意义

**当前 OPC 架构已有类似设计**，但可以借鉴：
- **任务通知 XML 格式**：可引入 OPC 的 callback 机制
- **"合成规格"概念**：A01 向下派任务时必须包含具体规格，而不是"研究一下"
- **并行 Workers 的并发控制**：只读任务并行；写任务按文件锁序列化

---

## 三、Tool 系统设计（高度可借鉴）

### 3.1 buildTool 工厂模式

每个 Tool 是一个独立目录，结构如下：
```
src/tools/{ToolName}/
  {ToolName}.ts(x)   — 主逻辑
  UI.tsx             — 渲染
  prompt.ts          — 系统提示词注入
  constants.js       — 常量
```

**Tool 定义模板：**
```typescript
export const MyTool = buildTool({
  name: 'MyTool',
  aliases: ['my_tool'],
  description: 'What this tool does',
  inputSchema: z.object({ param: z.string() }),
  
  async call(args, context, canUseTool, parentMessage, onProgress) {
    return { data: result, newMessages?: [...] }
  },
  
  async checkPermissions(input, context) {
    return { granted: boolean, reason?, prompt? }
  },
  
  isConcurrencySafe(input) { return true },
  isReadOnly(input) { return false },
  
  prompt(options) { return '...' },
  renderToolUseMessage(input, options) { return <Box>...</Box> },
  renderToolResultMessage(content, progressMessages, options) { return <Box>...</Box> },
})
```

### 3.2 Permission System

**四种模式：**
| 模式 | 行为 |
|------|------|
| `default` | 每次操作弹窗确认 |
| `plan` | 显示计划，一次性确认 |
| `bypassPermissions` | 自动批准所有操作 |
| `auto` | ML 分类器决定 |

**规则匹配（通配符模式）：**
```
Bash(git *)           — 所有 git 命令
FileEdit(/src/*)      — 编辑 src 目录
```

### 3.3 OPC 借鉴意义

- **Tool 工厂模式**：OPC 的 tool 定义可以采用类似结构，增加 `checkPermissions`、`renderToolUseMessage`
- **Permission 规则模式**：A15 的安全门可以参考通配符规则
- **inputSchema 用 Zod**：OPC 所有工具输入应强制 Zod 验证

---

## 四、Command 系统（可借鉴）

**三种命令类型：**

| 类型 | 说明 | 使用场景 |
|------|------|---------|
| `PromptCommand` | 发送格式化 prompt + 注入工具 | 大多数命令 |
| `LocalCommand` | 进程内执行，返回文本 | 轻量查询 |
| `LocalJSXCommand` | 进程内执行，返回 React JSX | 交互式 UI |

**命令注册方式：**
```typescript
const command = {
  type: 'prompt',
  name: 'my-command',
  description: 'What this command does',
  progressMessage: 'working...',
  allowedTools: ['Bash(git *)', 'FileRead(*)'],
  source: 'builtin',
  async getPromptForCommand(args, context) {
    return [{ type: 'text', text: '...' }]
  },
} satisfies Command
```

**OPC 借鉴**：A06 的 workflow 命令化是一个方向；命令的 `allowedTools` 约束很像 OPC 的 `executor_type` 约束。

---

## 五、Memory 系统（可借鉴）

Claude Code 实现了多层持久化记忆：

```
.memdir/
  .claude.md       — 项目级记忆
  CLAUDE.md        — 用户级记忆
  session.md       — 会话级记忆
```

**关键设计：**
- 按目录层级查找（向上冒泡到用户 HOME 目录）
- 注入到系统 prompt 的 memory section
- 支持跨 Worker 共享的 scratchpad 目录

**OPC 借鉴**：`knowledge/` 目录应支持类似的层级冒泡查找机制。

---

## 六、启动初始化模式（可借鉴）

Claude Code 的并行初始化：
```
[ MDM 策略读取 ] ─┐
[ Keychain 预取 ]  ├→ 并行 → 核心初始化
[ 特性开关检查  ] ─┘
```

**OPC 借鉴**：A01/A03/A06 启动时的 bootstrap 可以参考并行初始化 + 依赖注入模式，减少冷启动时间。

---

## 七、Feature Flag 系统（可借鉴）

使用 Bun 的 `bun:bundle` 特性标记：
```typescript
import { feature } from 'bun:bundle'
if (feature('PROACTIVE')) { /* 主动 Agent 工具 */ }
```

**特性标记列表（部分）：**
- `PROACTIVE` — 主动建议
- `KAIROS` — 守护进程模式
- `BRIDGE_MODE` — IDE 桥接
- `VOICE_MODE` — 语音模式
- `COORDINATOR_MODE` — 多 Agent 协调
- `DAEMON` — 后台守护
- `WORKFLOW_SCRAPTS` — 工作流脚本

**OPC 借鉴**：OPC agent 的技能/能力开关可以用类似的 `feature` 机制，支持动态启用/禁用特定能力，而不用改代码。

---

## 八、QueryEngine 核心循环（参考）

```
用户消息
  ↓
构建 System Prompt (上下文 + 记忆 + 工具描述)
  ↓
调用 LLM API (流式)
  ↓
处理响应：
  ├─ text → 直接输出
  ├─ thinking → 显示思考过程
  └─ tool_use → 执行工具 → 把结果注入回去 → 继续调用 LLM
  ↓
直到 stop 或达到 max_tokens
```

**关键点：**
- 工具调用循环是"同步串行"（一个工具调用完再调用下一个）
- `isConcurrencySafe` 的工具可以并行
- 支持流式输出，token 计数实时更新

---

## 九、Services 层（参考）

| Service | 路径 | OPC 对应 |
|---------|------|---------|
| API | services/api/ | A03 的交付路由 |
| MCP | services/mcp/ | MCP 集成 |
| OAuth | services/oauth/ | A06 的认证工作流 |
| Analytics | services/analytics/ | 日志/事件 |
| Plugins | services/plugins/ | 技能市场 |
| Compact | services/compact/ | 上下文压缩 |
| Policy Limits | services/policyLimits/ | A15 限流 |

---

## 十、对 OPC 的具体改进建议

### 10.1 任务卡增强（立即可做）

当前 OPC 任务卡缺少：
- `resultFormat`: 任务结果格式（如 `<task-notification>` XML 结构）
- `contextTransfer`: 继续 vs 新建的判断规则
- `evidence_required` 的证据类型（test/artifact/log）

### 10.2 Tool 定义标准化（可推进）

建议所有 OPC 工具（尤其是 A03/A06 的执行工具）采用：
- Zod inputSchema
- `checkPermissions()` 实现
- `isConcurrencySafe()` 实现
- `renderToolUseMessage()` 实现

### 10.3 Memory 层级（可推进）

OPC 的 `knowledge/` 应支持：
- `knowledge/global/` — 全局知识
- `knowledge/agent/{agentId}/` — Agent 私有知识
- `knowledge/task/{taskId}/` — 任务级知识
- 查找时向上冒泡

### 10.4 Coordinator 实现（中期）

A01 目前是路由分发，可以强化 Coordinator 能力：
- 引入"Research → Synthesis → Implementation → Verification"四阶段
- A01 做 Synthesis，不直接执行
- Worker 结果用统一 XML 格式回调

### 10.5 Feature Flag 机制（可推进）

在 openclaw.json 或 agents 配置中增加 `features` 字段，动态控制各 Agent 的能力开关。

---

## 十一、风险提示

- Claude Code 源码为泄露数据，仅供架构研究使用
- 部分特性（如 `KAIROS` 守护进程、`Buddy` 电子宠物）属于未发布功能
- MCP 集成、Analytics 等模块与 Anthropic 内部服务紧耦合，不可直接复用
