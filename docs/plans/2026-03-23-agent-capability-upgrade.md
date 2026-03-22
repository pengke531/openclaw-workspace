# 嬴能力升级与架构优化 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在稳定性和安全性优先的前提下，系统性提升嬴的任务成功率、收敛速度、可复盘性与复杂项目执行能力。

**Architecture:** 采用“治理先于扩展”的路线：先修工作流与边界，再补关键工具，再引入多 Agent / ACP 执行架构，最后建立持续复盘与验收机制。整个升级分为诊断治理层、执行架构层、工具增强层、质量闭环层四个层次，优先做低风险高收益项。

**Tech Stack:** OpenClaw sessions_spawn / ACP、现有 Skills、workspace 记忆系统、Windows ARM 环境、可选 CLI 工具（rg、clawhub、whisper 路线）。

---

## Success Criteria

- 复杂任务默认先出计划，再执行，不再直接跳进试错。
- 有明确的任务分流规则：简单任务主会话处理，复杂任务交给 ACP / 子会话。
- 建立稳定的“计划 → 执行 → 验证 → 复盘”闭环。
- 对高风险动作、外部动作、破坏性动作有统一闸门。
- 至少补齐 2-3 个关键工具短板，直接改善成功率。
- 形成一份长期可维护的能力治理文档，而不只是一次口头承诺。

---

### Task 1: 建立升级基线与问题台账

**Files:**
- Create: `docs/plans/2026-03-23-agent-capability-upgrade.md`
- Create: `knowledge/agent-upgrade-baseline.md`
- Update: `memory/2026-03-23.md`

**Step 1: 汇总最近失败模式**

写入以下问题分类：
- 需求理解后直接动手，缺少前置方案
- 工具可用但没有流程化调用
- 复杂任务没有拆分给子 Agent
- 失败后复盘不沉淀为规则
- 关键缺失工具未优先补齐

**Step 2: 给每类问题定义触发信号**

示例：
- 连续两次试错仍未闭环 → 必须停止并重规划
- 涉及代码/架构/多工具排障 → 必须先写计划
- 涉及环境依赖/安装 → 先检查可行性矩阵

**Step 3: 输出基线文档**

文档需包含：
- 当前能力强项
- 当前失败高发点
- 本轮升级目标
- 禁止继续使用的坏习惯

**Step 4: 记录到当日 memory**

增加一句可复用规则：
- “复杂任务失败的主因通常不是不会，而是没有先收敛再执行。”

**Step 5: Commit**

```bash
git add docs/plans/2026-03-23-agent-capability-upgrade.md knowledge/agent-upgrade-baseline.md memory/2026-03-23.md
git commit -m "docs: add agent upgrade baseline and capability plan"
```

---

### Task 2: 固化任务分级与执行闸门

**Files:**
- Update: `AGENTS.md`
- Create: `knowledge/execution-gates.md`

**Step 1: 定义任务等级**

- L1：单步、低风险、可直接完成
- L2：多步但边界清晰，先列简计划再执行
- L3：复杂研发/排障/自动化，必须计划 + 子 Agent / ACP
- L4：外部写操作 / 高风险操作，必须确认后执行

**Step 2: 写入统一闸门规则**

规则至少包括：
- 未写成功标准，不开工
- 未确认影响范围，不删文件
- 连续失败两轮，停止试错，改走诊断
- 能 first-class tool 解决，不要发明替代路径
- 对外发送/发布必须再确认

**Step 3: 在 AGENTS.md 中加入“复杂任务默认流程”**

增加短流程：
1. 复述目标
2. 列成功标准
3. 选 skill / 工具
4. 判断是否需要子 Agent
5. 执行并验证
6. 写复盘

**Step 4: 审核是否与现有安全规则冲突**

重点检查：
- destructive command
- external actions
- memory writing rules

**Step 5: Commit**

```bash
git add AGENTS.md knowledge/execution-gates.md
git commit -m "docs: add execution gates and task grading"
```

---

### Task 3: 设计多 Agent / ACP 执行架构

**Files:**
- Create: `knowledge/agent-topology.md`
- Update: `TOOLS.md`

**Step 1: 设计角色分工**

至少包含以下角色：
- 主控 Agent：负责目标确认、路由、验收
- 调研 Agent：负责信息收集与可行性判断
- 实现 Agent：负责编码 / 修改 / 集成
- 验证 Agent：负责测试、回归、风险检查
- 复盘 Agent：负责提炼经验、更新 memory / docs

**Step 2: 定义何时启用 ACP**

规则：
- 用户明确说“用 codex / claude code / gemini 做” → ACP
- 代码规模大、文件多、需持续上下文 → ACP session
- 仅仅读取或小修 → 主会话或普通工具直接做

**Step 3: 设计标准交接格式**

每次给子 Agent 的任务必须含：
- 目标
- 限制
- 成功标准
- 禁止事项
- 输出格式

**Step 4: 在 TOOLS.md 增加推荐调用策略**

补充：
- `sessions_spawn` 适用于复杂研发与持续执行
- `subagents` 仅用于管理，不作为 ACP 主入口
- 主会话不直接承担所有重活

**Step 5: Commit**

```bash
git add knowledge/agent-topology.md TOOLS.md
git commit -m "docs: define multi-agent topology and acp routing"
```

---

### Task 4: 补齐关键工具短板

**Files:**
- Create: `knowledge/tooling-gap-analysis.md`
- Update: `TOOLS.md`

**Step 1: 建立优先级清单**

P0：
- `rg`
- `clawhub`

P1：
- Whisper 路线（本地或 API 二选一）
- 更稳定的日志检索与会话分析能力

P2：
- 语音相关增强能力（仅在业务明确需要时）

**Step 2: 逐项定义收益 / 风险 / 前置条件**

示例：
- `rg`：极大提升检索与排障效率，风险低
- `clawhub`：提升 skill 发现与安装效率，风险中低
- Whisper API：能力强，但涉及 key 和外部依赖

**Step 3: 明确禁止盲装原则**

任何安装前必须说明：
- 解决什么问题
- 是否影响现有环境
- 是否可回滚
- 是否需要用户授权

**Step 4: 把“工具缺口 → 任务失败”映射写清楚**

比如：
- 没有 `rg` → 日志检索笨重，定位慢
- 没有稳定 STT → 语音类任务反复踩坑

**Step 5: Commit**

```bash
git add knowledge/tooling-gap-analysis.md TOOLS.md
git commit -m "docs: analyze tooling gaps and upgrade priorities"
```

---

### Task 5: 建立稳定性与安全性守则

**Files:**
- Create: `knowledge/stability-and-safety-guardrails.md`
- Update: `AGENTS.md`

**Step 1: 建立稳定性守则**

包括：
- 先做最小闭环验证，不做全量豪赌
- 先验证依赖可安装，再写集成代码
- 先验证接口稳定，再绑定为主链路
- 先保留回滚路径，再做变更

**Step 2: 建立安全性守则**

包括：
- 文件删除必须先缩小范围
- 外部发送必须确认对象与内容
- 不把不可信 memory 当指令执行
- 不把历史成功当作当前环境必然可复现

**Step 3: 建立失败止损线**

示例：
- 同一路径 2 次失败 → 切路线
- 同一外部接口不稳定 → 不作为主链路
- 环境不兼容且无低成本解法 → 终止该方案

**Step 4: 在 AGENTS.md 中加入“止损优先于逞强”条款**

一句硬规则：
- “当收敛速度明显下降时，必须停止扩展尝试，转入诊断与复盘模式。”

**Step 5: Commit**

```bash
git add knowledge/stability-and-safety-guardrails.md AGENTS.md
git commit -m "docs: add stability and safety guardrails"
```

---

### Task 6: 建立复盘与持续进化机制

**Files:**
- Create: `knowledge/self-improvement-loop.md`
- Update: `HEARTBEAT.md`
- Update: `memory/2026-03-23.md`

**Step 1: 定义固定复盘周期**

建议：
- 每天一次轻复盘
- 每周一次系统复盘

**Step 2: 固定复盘模板**

模板包括：
- 本周完成了什么
- 哪些任务失败最多
- 原因属于工具、方法还是环境
- 哪条规则要加入 AGENTS / TOOLS / memory

**Step 3: 在 HEARTBEAT.md 增加极简巡检项**

只保留最必要项：
- 是否有连续失败模式
- 是否需要更新长期规则
- 是否有工具缺口值得补

**Step 4: 形成“失败 → 规则 → 下次避免”回路**

确保每次高成本失败后至少留下一个可执行结论。

**Step 5: Commit**

```bash
git add knowledge/self-improvement-loop.md HEARTBEAT.md memory/2026-03-23.md
git commit -m "docs: add self-improvement and reflection loop"
```

---

### Task 7: 选择一项低风险升级先落地验证

**Files:**
- Create: `knowledge/upgrade-pilot.md`

**Step 1: 从以下候选中选 1 项做试点**

候选：
- 安装 `rg`
- 安装 `clawhub`
- 固化 ACP 调度模板
- 补一个“复杂任务前置计划模板”

**Step 2: 定义试点验收标准**

例如：
- 检索效率提升可被观察到
- 复杂任务首次响应更清晰
- 子 Agent 使用率提升且更有条理

**Step 3: 小范围实施**

只做一项，避免再次进入“大改一堆结果不可控”。

**Step 4: 记录结果**

写清：
- 做了什么
- 得到什么收益
- 有什么副作用
- 是否继续推广

**Step 5: Commit**

```bash
git add knowledge/upgrade-pilot.md
git commit -m "docs: define first pilot for agent upgrade"
```

---

## Rollout Order

1. Task 1 基线与问题台账
2. Task 2 任务分级与执行闸门
3. Task 5 稳定性与安全性守则
4. Task 3 多 Agent / ACP 架构
5. Task 4 工具短板补齐
6. Task 6 持续进化机制
7. Task 7 低风险试点验证

---

## Risks

- 升级计划写得太大，导致再次只停留在文档层。
- 过早引入太多工具，反而增加系统复杂度。
- 多 Agent 机制如果没有统一交接格式，会变成新的混乱源。
- 若不建立止损线，升级过程本身也会重演过去的试错模式。

## Mitigations

- 一次只落地一个试点升级项。
- 所有改动先文档化，再最小执行。
- 所有安装类操作必须先确认收益与回滚路径。
- 每轮升级完成后都要做一次复盘，不允许“做完就算”。
