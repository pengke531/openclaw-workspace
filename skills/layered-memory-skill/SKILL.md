---
name: layered-memory-skill
description: 按层加载记忆的 skill，兼顾记忆完整性与上下文精简。适用于需要高效检索、避免记忆膨胀、支持多任务并行的 Agent 系统。
---

# Layered Memory Skill

## Overview

记忆分层索引系统。通过 L0-L4 分层结构与热/温/冷分区，实现"先索引命中、再逐层下钻"的按需加载，避免每次读取过多历史上下文。

## The Core Problem This Solves

Every AI agent session starts with a context window. Loading all historical memory for every task wastes tokens and slows inference. But selective loading risks missing critical context. The solution is a structured layered system where the agent knows exactly which layer to load for which type of task.

This skill implements that system with five memory layers, temperature zones, and a decision tree that guides loading behavior automatically.

## Layer Architecture

| Layer | Name | Content | Load Trigger |
|-------|------|---------|-------------|
| L0 | 总索引层 | MEMORY.md — 长期记忆主入口与查表索引 | 每会话必读 |
| L1 | 领域索引层 | 关于用户 / 技术配置 / 项目经验 / 经验教训 | 命中领域关键词后加载 |
| L2 | 主题摘要层 | 每日日志 / 按项目的主题摘要 | 命中具体任务/项目时加载 |
| L3 | 详细事实层 | 原始决策记录 / 详细方案文档 | 复杂任务/排障/审计时加载 |
| L4 | 原始证据层 | 对话快照 / 工具完整输出 / 外部调研摘要 | 审计/争议时访问 |

## Temperature Zones

Memory has a temporal dimension. Not all memory is equally active.

- **热区 (Hot)**: 最近 7 天，频繁读写，集中在 L0-L2。包含当前项目和活跃任务。
- **温区 (Warm)**: 7-30 天，主要在 L2-L3，按需加载。包含最近完成的项目和暂时搁置的任务。
- **冷区 (Cold)**: 30 天以上，L3-L4，审计/回溯时访问。主要是归档内容。

Temperature zones are not separate directories. They are a loading strategy applied to the same layered structure.

## Core Principle

**先索引，后加载；命中后下钻；不要一次性加载全部历史。**

The agent should never load L3 or L4 by default. It should always start at L0, and only go deeper when the current layer proves insufficient.

## Activation Conditions

This skill activates when:
- Starting a new session
- Switching between projects
- Encountering a complex multi-step task
- Any task that has not been worked on in more than 7 days
- Beginning work on a project with no recent session

## Loading Sequence

### Step 1: Always Start at L0

Read MEMORY.md first. This is the master index. It tells the agent which L1 files to check and in what order.

### Step 2: Match Domain to L1

Based on L0, identify which domain indexes are relevant:
- 涉及用户/沟通/偏好 → memory/关于彭科.md
- 涉及技术/工具/环境 → memory/技术配置.md
- 涉及项目/研发/推进 → memory/项目经验.md
- 涉及教训/反思/排错 → memory/经验教训.md

### Step 3: Match Task to L2

If the task is about a specific project or topic, load the relevant daily logs and topic summaries.

### Step 4: Drill to L3 on Complex Tasks

Complex tasks, troubleshooting, architecture decisions: load L3 files (design docs, blueprints, detailed rules).

### Step 5: Access L4 Only for Audits

L4 is not a daily loading layer. It is only accessed when auditing, resolving disputes, or tracing evidence.

## Decision Rules

The decision tree determines how deep to load:

**Simple task** (one-step, <5 min): L0 only → stop

**Project task**: L0 → L1 (matched files) → L2 → stop

**Complex/execution task**: L0 → L1 → L2 → L3 (as needed)

**Audit/dispute**: May access L4 if L1-L3 insufficient

## Writing Rules

Loading only works if writing maintains the structure:

- Write daily raw logs to L2 every session
- After each session, extract key decisions to relevant L1 files
- Never leave important decisions only in daily logs with no L1 summary
- L0 always stays as an index only, never stores detailed content directly

## Anti-Patterns

This system fails when:
- L1 files are not kept current (agent cannot find recent decisions)
- Daily logs contain all details with no L1 distillation (context overflow)
- L3/L4 are loaded for simple tasks (token waste)
- L0 is skipped (index is the starting point, not optional)
- Important decisions are remembered mentally but never written to files

## Files

- `SKILL.md` — this file: core specification, layer definitions, decision rules
- `README.md` — full documentation with usage scenarios and design principles
- `examples/loading-example.md` — 5 real loading scenarios with expected layers and time
- `tests/validation-cases.md` — 8 test cases to validate the system works correctly

## Relationship with AgentOS v2

This skill is the **L4 Context System** implementation for AgentOS v2.

AgentOS v2 defines the complete six-layer architecture. This skill provides the concrete, standalone implementation of the memory layer that can be used independently or as part of the full AgentOS v2 system.

## Success Criteria

- [ ] L0 is read at the start of every session
- [ ] L1 is loaded when domain keywords are matched
- [ ] L2 is loaded for specific project/task contexts
- [ ] L3 is available for complex tasks but not loaded by default
- [ ] L4 is never loaded unless audit/dispute scenario is active
- [ ] Simple tasks never trigger unnecessary deep loading
- [ ] L1 files are kept updated with recent decisions
- [ ] Temperature zones are respected in loading priority
