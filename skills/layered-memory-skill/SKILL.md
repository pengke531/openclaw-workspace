---
name: layered-memory-skill
description: 按层加载记忆的 skill，兼顾记忆完整性与上下文精简。适用于需要高效检索、避免记忆膨胀、支持多任务并行的 Agent 系统。
---

# Layered Memory Skill

## Overview

记忆分层索引系统。通过 L0-L4 分层结构与热/温/冷分区，实现"先索引命中、再逐层下钻"的按需加载，避免每次读取过多历史上下文。

## Layer Architecture

| Layer | Name | Content | Load Trigger |
|-------|------|---------|-------------|
| L0 | 总索引层 | MEMORY.md — 长期记忆主入口与查表索引 | 每会话必读 |
| L1 | 领域索引层 | `memory/关于彭科.md`、`memory/技术配置.md`、`memory/项目经验.md`、`memory/经验教训.md` | 命中领域关键词后加载 |
| L2 | 主题摘要层 | `memory/YYYY-MM-DD.md`（当日）、按项目/主题的摘要文件 | 命中具体任务/项目时加载 |
| L3 | 详细事实层 | 原始决策记录、详细方案文档 | 复杂任务/排障/审计时加载 |
| L4 | 原始证据层 | `evidence/conversations/`、`evidence/tool-outputs/`、`evidence/external-fetches/` | 审计/争议时访问，见 `evidence/L4-implementation.md` |

## Temperature Zones

- **热区**：最近 7 天，频繁读写，集中在 L0-L2
- **温区**：7-30 天，主要在 L2-L3，按需加载
- **冷区**：30 天以上，L3-L4，审计/回溯时访问

## Core Principle

**先索引，后加载；命中后下钻；不要一次性加载全部历史。**

## Usage

### Activation

When to activate this skill:
- Starting a new session
- Switching between projects
- Encountering a complex multi-step task
- Any task that has not been worked on in more than 7 days

### Loading Sequence

1. **L0** (always): Read `MEMORY.md`
2. **L1** (on relevant domain): Read `memory/关于彭科.md`, `memory/技术配置.md`, `memory/项目经验.md`, `memory/经验教训.md`
3. **L2** (on task/project): Read relevant `memory/YYYY-MM-DD.md` or topic summary
4. **L3** (complex tasks): Drill into detailed records, design docs
5. **L4** (auditing/verification): Access raw conversation logs, tool outputs

### When to Stop Loading

- If L1 answers the question → stop
- If L2 provides sufficient context → stop
- Only go deeper when the current layer is insufficient

## Decision Rules

**Simple task** (one-step, <5 min): L0 only  
**Project task**: L0 → L1 → L2 (if project-related)  
**Complex/execution task**: L0 → L1 → L2 → L3 (as needed)  
**Audit/dispute**: May access L4

## Files

- `SKILL.md` — this file
- `README.md` — full documentation
- `examples/loading-example.md` — sample loading sequence
- `tests/validation-cases.md` — test cases for the layered system
