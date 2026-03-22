# Layered Memory Skill

> 按层加载记忆，兼顾完整性与效率。

## Problem It Solves

- **Too much context**: Loading all historical memory on every task causes token waste and slower inference
- **Forgetting important facts**: Selective loading risks missing relevant context
- **No structure**: Flat memory files make targeted retrieval impossible

## Solution: Layered + Temperature Architecture

### Layers

| Layer | Name | What It Contains | When To Load |
|-------|------|-----------------|--------------|
| **L0** | 总索引 | MEMORY.md — the master index | Always (every session) |
| **L1** | 领域索引 | Domain indexes: about user, tech config, projects, lessons | On domain match |
| **L2** | 主题摘要 | Daily logs, topic summaries | On task/project match |
| **L3** | 详细事实 | Raw decisions, full design docs,方案文档 | Complex tasks, troubleshooting |
| **L4** | 原始证据 | `evidence/conversations/`, `evidence/tool-outputs/`, `evidence/external-fetches/` | Auditing, dispute resolution; see `evidence/L4-implementation.md` |

### Temperature Zones

- **Hot** (≤7 days): Active projects, current tasks → L0-L2
- **Warm** (7-30 days): Recent past, less active → L2-L3
- **Cold** (>30 days): Archival, rarely needed → L3-L4

## Core Principle

> **Index first, load on match, drill down only when needed.**

## Quick Start

1. Read `MEMORY.md` (L0) every session
2. Match domain → load `memory/技术配置.md` or `memory/项目经验.md` (L1)
3. Match task → load `memory/YYYY-MM-DD.md` (L2)
4. Complex task → continue to L3/L4 as needed

## Decision Tree

```
Is this a simple one-step task?
  YES → L0 only
  NO  → Continue

Is it a known project/domain?
  YES → L0 + L1 (relevant files)
  NO  → Continue

Does L1 provide enough context?
  YES → Stop
  NO  → Continue to L2

Is it a complex/critical task?
  YES → L0 + L1 + L2 + L3
  NO  → L0 + L1 + L2

Audit or dispute?
  YES → May access L4
```

## File Structure

```
layered-memory-skill/
├── SKILL.md                  # This skill
├── README.md                 # Full documentation
├── examples/
│   └── loading-example.md    # Sample loading sequences
└── tests/
    └── validation-cases.md   # Test cases
```

## For Agent Developers

This skill is designed for OpenClaw agents. Integrate it by:

1. Adding `layered-memory-skill` to your skills directory
2. Following the loading sequence in your session start
3. Using the decision tree to determine how deep to load
4. Updating `MEMORY.md` (L0) and domain indexes (L1) regularly

## Loading Rules

- **Never load all layers by default**
- **Never skip L0** (it's the index)
- **Stop as soon as context is sufficient**
- **Write summaries at L2** to make L1 and L2 effective
- **Don't let daily logs replace structured indexes**

## Testing

See `tests/validation-cases.md` for test scenarios and expected behaviors.

## License

MIT — Open source for the Agent community.
