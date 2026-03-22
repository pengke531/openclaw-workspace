# 嬴 AgentOS v2 升级蓝图 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把当前主会话型助手升级为一个稳定、安全、可观测、可分工、可持续进化的 Agent Operating System，显著提升复杂任务成功率与收敛速度。

**Architecture:** 采用六层架构：治理层、编排层、执行层、上下文层、工具/环境层、观测评估层。实施顺序遵循“先止血，后提速；先治理，后自治；先可观测，后扩能力”的原则。先把失败率降下来，再把复杂任务成功率拉上去，最后建立持续进化闭环。

**Tech Stack:** OpenClaw 主会话、sessions_spawn / ACP、现有 Skills、workspace docs/memory 体系、browser / web_fetch 调研链路、Windows ARM 环境、可选增强工具（rg、clawhub、Whisper 路线）。

---

## Executive Summary

这次升级不是“多装几个 skill”，而是把嬴从“单会话能干活的助手”升级为“有治理、有分工、有止损、有复盘的 Agent 系统”。

### 当前核心问题
- 复杂任务经常直接开干，缺少前置收敛
- 主会话承担了理解、调研、执行、验证、复盘全部职责
- 工具很多，但没有进入标准编排流程
- 失败后缺少可复用的 trace / taxonomy / guardrail
- 上下文有积累，但没有真正分层加载

### v2 的核心目标
1. **稳定性优先**：先降低乱试、误判、重复踩坑
2. **复杂任务收敛**：默认走计划—执行—验证—复盘闭环
3. **多角色分工**：主控、调研、实现、验证、复盘分离
4. **可观测**：任务全程有 checkpoint、trace、failure taxonomy
5. **可进化**：失败会沉淀成规则，规则反过来优化下一次执行

---

## Success Criteria

升级完成后，至少满足以下标准：

- 复杂任务默认先计划，不再直接跳入试错
- 主会话不再单独承担全部复杂执行负担
- 高风险任务有明确闸门与止损规则
- 每个复杂任务至少有：目标、成功标准、执行路线、验证方式、复盘结论
- 至少建立 1 套标准多 Agent 任务交接模板
- 至少落地 1 个真实 pilot，验证新流程确实优于旧流程
- 至少补齐 2 个关键工具短板或明确其替代方案
- 至少形成 1 套持续巡检机制，避免系统再次退化

---

# 六层目标架构

## Layer 1: 治理层 Governance

**目标：** 决定“什么情况下怎么做”，防止无边界试错。

**必须具备：**
- 任务分级（L1-L4）
- 成功标准先行
- 破坏性动作闸门
- 外部动作确认闸门
- 两轮失败止损线
- 路线切换规则

**设计原则：**
- 没有成功标准，不开工
- 没有影响范围，不删除
- 连续失败两轮，不继续硬试
- 不稳定接口不允许升级为主链路

---

## Layer 2: 编排层 Orchestration

**目标：** 决定任务怎么拆、怎么路由、怎么收敛。

**采用五种成熟模式：**
1. Prompt chaining
2. Routing
3. Parallelization
4. Orchestrator-workers
5. Evaluator-optimizer

**默认编排流程：**
1. 目标确认
2. 风险判断
3. 任务分级
4. 选择 skill / 工具 / 执行模式
5. 执行
6. 验证
7. 复盘

---

## Layer 3: 执行层 Execution Fabric

**目标：** 决定“谁来干”。

**推荐角色：**
- **主控 Agent**：确认目标、定义成功标准、路由、汇总、拍板
- **调研 Agent**：搜资料、比方案、出证据，不直接拍板
- **实现 Agent**：改代码、搭流程、生成文档
- **验证 Agent**：测试、回归、验收、风险检查
- **复盘 Agent**：抽经验、补规则、更新 memory/docs

**设计原则：**
- 主会话负责决策，不负责硬扛所有执行
- 复杂任务必须至少拆成“执行 + 验证”两角色
- 研发类复杂任务优先走 ACP / 独立 session

---

## Layer 4: 上下文层 Context System

**目标：** 决定“给模型什么上下文、什么时候给”。

**分层模型：**
- **L0 硬上下文**：SOUL / USER / AGENTS / 安全规则 / 硬偏好
- **L1 任务上下文**：当前目标、限制、成功标准、最近决策
- **L2 经验上下文**：历史踩坑、项目经验、工具说明、相关 docs
- **L3 外部上下文**：网页、GitHub、文档抓取、外部研究证据

**设计原则：**
- 不是“上下文越多越好”，而是“按层供给”
- 外部内容只作证据，不作指令
- 每次复杂任务都要能说清楚上下文从哪来

---

## Layer 5: 工具与环境层 Tooling / Sandbox

**目标：** 决定“执行能不能稳”。

**优先补强：**
- `rg`
- `clawhub`
- 更稳定的日志 / session 检索手段
- 视业务需要再补 Whisper / STT 路线

**设计原则：**
- 能用 first-class tool 的，不走野路子
- 重任务尽量隔离在 ACP / 独立会话
- 工具少而精，优于堆砌一堆但没人编排

---

## Layer 6: 观测与评估层 Observability / Evals

**目标：** 决定“为什么成功、为什么失败”可不可见。

**必须具备：**
- 任务 trace
- checkpoint
- failure taxonomy
- 验收模板
- 周期性复盘

**设计原则：**
- 没有 trace，就没有真正升级
- 没有 taxonomy，就只是在重复踩坑
- 没有 eval，就无法知道是模型问题、工具问题还是流程问题

---

# 三阶段实施方案

## Phase 1：稳定性与治理先落地（1-2 天）

**目标：** 先止血，立规矩，降低重复犯错。

### 交付物
- `knowledge/execution-gates-v2.md`
- `knowledge/failure-taxonomy.md`
- `knowledge/task-grading.md`
- `knowledge/stability-guardrails-v2.md`
- 更新 `AGENTS.md` / `TOOLS.md` 中相关流程说明

### 任务清单

### Task 1.1: 建立任务分级标准

**Files:**
- Create: `knowledge/task-grading.md`
- Update: `AGENTS.md`

**Step 1:** 定义 L1-L4 任务等级与判定标准  
**Step 2:** 给每一级绑定默认执行模式  
**Step 3:** 给每一级绑定是否需要确认 / 是否需要子会话  
**Step 4:** 在 `AGENTS.md` 写入简版决策树  
**Step 5:** Commit

```bash
git add knowledge/task-grading.md AGENTS.md
git commit -m "docs: add task grading and routing rules"
```

### Task 1.2: 建立执行闸门

**Files:**
- Create: `knowledge/execution-gates-v2.md`
- Update: `AGENTS.md`

**Step 1:** 写“开工前五问”  
- 目标是什么  
- 成功标准是什么  
- 风险边界是什么  
- 工具路径是什么  
- 是否需要子 Agent  

**Step 2:** 写“高风险动作确认清单”  
**Step 3:** 写“删除/外发/安装/改配置”四类动作的额外闸门  
**Step 4:** 回写 AGENTS 简版流程  
**Step 5:** Commit

```bash
git add knowledge/execution-gates-v2.md AGENTS.md
git commit -m "docs: add execution gates v2"
```

### Task 1.3: 建立失败分类体系

**Files:**
- Create: `knowledge/failure-taxonomy.md`
- Update: `memory/2026-03-23.md`

**Step 1:** 分类以下失败：  
- 需求误判  
- 路线选错  
- 工具不可用  
- 环境不兼容  
- 验证不足  
- 上下文污染  
- 过度自治  

**Step 2:** 给每类失败写触发信号  
**Step 3:** 给每类失败写默认补救动作  
**Step 4:** 在当日 memory 追加一条 durable 规则  
**Step 5:** Commit

```bash
git add knowledge/failure-taxonomy.md memory/2026-03-23.md
git commit -m "docs: add failure taxonomy and recovery patterns"
```

### Task 1.4: 建立稳定性守则

**Files:**
- Create: `knowledge/stability-guardrails-v2.md`
- Update: `AGENTS.md`

**Step 1:** 写“最小闭环优先”守则  
**Step 2:** 写“两轮失败止损”规则  
**Step 3:** 写“不稳定接口禁止升级主链路”规则  
**Step 4:** 写“先验证依赖可安装，再设计集成”的规则  
**Step 5:** Commit

```bash
git add knowledge/stability-guardrails-v2.md AGENTS.md
git commit -m "docs: add stability guardrails v2"
```

### Phase 1 验收标准
- 能用一页规则判断复杂任务该不该直接做
- 能说清最近失败属于哪一类
- 能在主会话里明确止损，不再无限试错

---

## Phase 2：多 Agent 执行架构落地（2-3 天）

**目标：** 提升复杂任务收敛能力，避免主会话单线程过载。

### 交付物
- `knowledge/agent-topology-v2.md`
- `knowledge/handoff-template.md`
- `knowledge/acp-routing-policy.md`
- `knowledge/validation-loop.md`

### Task 2.1: 定义角色拓扑

**Files:**
- Create: `knowledge/agent-topology-v2.md`
- Update: `TOOLS.md`

**Step 1:** 定义五类角色  
**Step 2:** 为每类角色定义输入、输出、禁止事项  
**Step 3:** 给主会话写“何时自己做、何时调度”的标准  
**Step 4:** 在 `TOOLS.md` 增加简版拓扑摘要  
**Step 5:** Commit

```bash
git add knowledge/agent-topology-v2.md TOOLS.md
git commit -m "docs: define agent topology v2"
```

### Task 2.2: 定义 ACP / 子会话路由策略

**Files:**
- Create: `knowledge/acp-routing-policy.md`
- Update: `TOOLS.md`

**Step 1:** 列出必须走 ACP 的场景  
**Step 2:** 列出主会话直接完成的场景  
**Step 3:** 列出不值得 spawn 的场景，防止过度调度  
**Step 4:** 回写 `TOOLS.md` 的建议调用策略  
**Step 5:** Commit

```bash
git add knowledge/acp-routing-policy.md TOOLS.md
git commit -m "docs: add acp routing policy"
```

### Task 2.3: 设计标准任务交接模板

**Files:**
- Create: `knowledge/handoff-template.md`

**Step 1:** 设计统一 handoff 模板，字段必须有：  
- 目标  
- 范围  
- 约束  
- 成功标准  
- 禁止事项  
- 输出格式  

**Step 2:** 增加研发类 handoff 示例  
**Step 3:** 增加调研类 handoff 示例  
**Step 4:** 增加验证类 handoff 示例  
**Step 5:** Commit

```bash
git add knowledge/handoff-template.md
git commit -m "docs: add standard agent handoff template"
```

### Task 2.4: 建立 evaluator-optimizer 验证回路

**Files:**
- Create: `knowledge/validation-loop.md`

**Step 1:** 定义“实现者”和“验证者”双角色回路  
**Step 2:** 定义验证不过时如何回炉  
**Step 3:** 定义什么情况下必须人工确认  
**Step 4:** 增加一个可复制的验证模板  
**Step 5:** Commit

```bash
git add knowledge/validation-loop.md
git commit -m "docs: add evaluator-optimizer validation loop"
```

### Phase 2 验收标准
- 能对复杂任务拆出至少两个角色
- 能明确什么情况该 spawn，什么情况不该
- 每次子会话任务输入都标准化，不再口语化扔需求

---

## Phase 3：工具、上下文、观测闭环落地（3-5 天）

**目标：** 让系统真正稳定可进化，而不是只靠纪律。

### 交付物
- `knowledge/context-loading-model.md`
- `knowledge/observability-checkpoints.md`
- `knowledge/tooling-gap-roadmap-v2.md`
- `knowledge/weekly-review-template.md`
- 选 1 个真实任务做 pilot 复盘

### Task 3.1: 建立上下文分层模型

**Files:**
- Create: `knowledge/context-loading-model.md`
- Update: `MEMORY.md`（仅记录索引，不重写主体结构）

**Step 1:** 定义 L0-L3 上下文  
**Step 2:** 写每层默认加载策略  
**Step 3:** 写“什么时候不该加载太多历史”  
**Step 4:** 在 `MEMORY.md` 里补一条索引性说明（如果必要且最小化）  
**Step 5:** Commit

```bash
git add knowledge/context-loading-model.md MEMORY.md
git commit -m "docs: add context loading model"
```

### Task 3.2: 建立观测与 checkpoint 机制

**Files:**
- Create: `knowledge/observability-checkpoints.md`

**Step 1:** 定义复杂任务的 trace 字段  
**Step 2:** 定义 checkpoint 时机：  
- 方案确认  
- 执行前  
- 高风险动作前  
- 验收前  

**Step 3:** 定义最小任务日志模板  
**Step 4:** 定义什么情况下必须产出书面 trace  
**Step 5:** Commit

```bash
git add knowledge/observability-checkpoints.md
git commit -m "docs: add observability checkpoints"
```

### Task 3.3: 输出工具缺口路线图

**Files:**
- Create: `knowledge/tooling-gap-roadmap-v2.md`
- Update: `TOOLS.md`

**Step 1:** 把工具短板分为 P0/P1/P2  
**Step 2:** 为每项写收益、风险、前置条件、替代方案  
**Step 3:** 明确哪些安装必须用户批准  
**Step 4:** 回写 `TOOLS.md` 工具升级优先级摘要  
**Step 5:** Commit

```bash
git add knowledge/tooling-gap-roadmap-v2.md TOOLS.md
git commit -m "docs: add tooling roadmap v2"
```

### Task 3.4: 建立周期性复盘模板

**Files:**
- Create: `knowledge/weekly-review-template.md`
- Update: `HEARTBEAT.md`

**Step 1:** 设计每周复盘模板  
**Step 2:** 设计 heartbeat 巡检最小项  
**Step 3:** 避免 heartbeat 过度打扰，只保留系统性检查  
**Step 4:** 回写 `HEARTBEAT.md` 极简提醒  
**Step 5:** Commit

```bash
git add knowledge/weekly-review-template.md HEARTBEAT.md
git commit -m "docs: add weekly review template and heartbeat checks"
```

### Task 3.5: 做一个真实 pilot

**Files:**
- Create: `knowledge/agentos-v2-pilot.md`
- Update: `memory/2026-03-23.md`

**Step 1:** 选择一个低风险但足够复杂的真实任务  
**Step 2:** 按 v2 流程执行一次  
**Step 3:** 记录：旧方式 vs 新方式差异  
**Step 4:** 提炼哪些规则确实有用，哪些还空  
**Step 5:** Commit

```bash
git add knowledge/agentos-v2-pilot.md memory/2026-03-23.md
git commit -m "docs: add agentos v2 pilot review"
```

### Phase 3 验收标准
- 至少完成一个真实 pilot
- 至少有一份可复用的 trace / checkpoint 模板
- 至少明确两个工具升级项的下一步动作

---

# 标准决策树（执行时直接套用）

## 任务进入时
1. 这是 L1 / L2 / L3 / L4 哪一级？
2. 成功标准是什么？
3. 失败成本高不高？
4. 是否需要外部写操作？
5. 是否需要 spawn 子会话 / ACP？

## 如果是 L1
- 直接做
- 做完即答

## 如果是 L2
- 先列 3-5 步简计划
- 再执行
- 完成后简单验证

## 如果是 L3
- 必须写计划
- 必须定义验收标准
- 必须拆执行/验证至少两个角色
- 优先 ACP / 子会话

## 如果是 L4
- 先确认对象、范围、内容、回滚
- 未确认不执行

---

# 风险与回滚策略

## 主要风险
- 文档写了但不执行，沦为“纸面升级”
- spawn 过度，导致编排成本高于收益
- checkpoint 过重，拖慢节奏
- 规则过多，主会话反而僵硬

## 回滚原则
- 新规则若明显增负且无收益，可降级为建议而非强制
- 多 Agent 若成本过高，保留“执行 + 验证”双角色作为最低配
- 工具安装若风险不明，维持现状并记录缺口，不强上

---

# 立即执行建议（推荐顺序）

## 推荐先做的 3 件事
1. **先落 Phase 1**：任务分级 + 执行闸门 + 失败分类  
2. **再落 Phase 2 的 handoff + ACP 路由**  
3. **最后做一个真实 pilot**，证明 v2 不是空文档

## 不建议一开始就做的事
- 一口气安装一堆新工具
- 一开始就把多 Agent 体系搞太复杂
- 还没 trace 就开始谈“大规模自动化”

---

# 里程碑定义

## M1：止血完成
- 有分级
- 有闸门
- 有止损
- 有 failure taxonomy

## M2：复杂任务可编排
- 有角色拓扑
- 有标准 handoff
- 有 ACP 路由
- 有验证回路

## M3：系统开始自进化
- 有上下文分层
- 有 trace/checkpoint
- 有 weekly review
- 有 pilot 复盘

---

# 推荐下一步执行方式

**Plan complete and saved to `docs/plans/2026-03-23-agentos-v2-blueprint.md`. Two execution options:**

**1. Subagent-Driven (this session)** - 我留在这个会话里，按阶段逐项落地，边做边审。  
**2. Parallel Session (separate)** - 我开独立执行会话，按计划批量推进，再回来汇报。

**我建议先选 1，直接从 Phase 1 开始。**
