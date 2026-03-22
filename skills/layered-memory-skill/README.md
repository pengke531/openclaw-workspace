# Layered Memory Skill

## Overview

A production-grade layered memory architecture for AI agents. Implements L0-L4 layered structure with temperature zones (hot/warm/cold), enabling "index-first, then drill down on match" loading.

Core principle: Do not load all history every time. Load precisely what the task needs.

## Problem / Solution

| Problem | Solution |
|---------|----------|
| Context bloat | L0 index-first, load on demand |
| Memory gaps | L1-L3 coverage ensures match-based retrieval |
| No structure | Layered indexes + temperature zones + decision tree |

## Layer Architecture

```
Task received
  |
  v
L0 - Master Index (MEMORY.md)      <- always
  |
  v
L1 - Domain Indexes (user/tech/projects/lessons)  <- on domain match
  |
  v
L2 - Topic Summaries (daily logs)  <- on task/project match
  |
  v
L3 - Detailed Records (design docs) <- on complex/troubleshoot
  |
  v
L4 - Raw Evidence (conversations/tool-outputs/external) <- audit only
```

## Layer Definitions

| Layer | Name | Content | Load Trigger |
|-------|------|---------|-------------|
| L0 | Master Index | MEMORY.md | Every session (mandatory) |
| L1 | Domain Index | User/tech/projects/lessons | On domain keyword match |
| L2 | Topic Summary | Daily logs / topic summaries | On task/project match |
| L3 | Detailed Records | Design docs / full specs | Complex tasks / troubleshooting |
| L4 | Raw Evidence | Conversations / tool outputs / external fetches | Audit / dispute only |

## Temperature Zones

| Zone | Time Range | Typical Layers |
|------|------------|---------------|
| Hot | <= 7 days | L0-L2 (active projects) |
| Warm | 7-30 days | L2-L3 (recent past) |
| Cold | > 30 days | L3-L4 (archival) |

## Decision Tree

```
Is this a simple task (one step, <5min)?
  YES -> L0 only -> STOP

Does it involve a known domain (user/tech/project/lessons)?
  YES -> L0 + L1 (matched files) -> Is L1 sufficient? -> YES STOP / NO continue

Does it involve a specific project/task?
  YES -> L0 + L1 + L2 -> Is L2 sufficient? -> YES STOP / NO continue

Is this a complex task / troubleshooting / architecture decision?
  YES -> L0 + L1 + L2 + L3

Is this an audit / dispute?
  YES -> May access L4
```

## Usage

### 1. Copy to skills directory

```
your-openclaw-workspace/skills/layered-memory-skill/
```

### 2. On session start

Load layers per decision tree above. Do not load all layers by default.

### 3. On task end

Update relevant L1 files with key decisions. Do not leave important info only in daily log.

## Loading Scenarios

### Scenario 1: Simple Question
Task: "What is the user's name?"

Loading: L0 (MEMORY.md) -> found in user section -> STOP

Layers: 1 (L0 only)
Time: <1 min

### Scenario 2: Project Task
Task: Continue working on "智惠 X4" project

Loading: L0 -> L1 (projects.md) -> L2 (recent daily logs) -> L3 (if deeply technical)

Layers: L0 + L1 + L2 (L3 on demand)
Time: 2-3 min

### Scenario 3: Complex Execution
Task: Implement AgentOS v2 and ship it

Loading: L0 -> L1 (active tasks + tech) -> L2 (today's session) -> L3 (blueprint + governance docs)

Layers: L0 + L1 + L2 + L3
Time: 5-10 min

### Scenario 4: Audit / Dispute
Task: Verify what was decided on a past technical direction

Loading: L0 -> L1 -> L2 (all relevant daily logs) -> L3 (design docs) -> L4 (raw evidence if needed)

Layers: All layers as needed
Time: 10-15 min

## Files

```
layered-memory-skill/
├── SKILL.md                   # Core specification (activation, layers, decision tree)
├── README.md                  # This file
├── LICENSE                    # MIT License
├── examples/
│   └── loading-example.md     # 5 real loading scenarios
└── tests/
    └── validation-cases.md    # 8 validation test cases
```

## Validation Tests

See `tests/validation-cases.md` for 8 test cases:
- L0 always loads
- L1 loads on domain match
- L2 loads for active projects
- Simple tasks do not overload
- Complex tasks drill to L3
- No premature deep loading
- L4 accessible for audits
- Memory indexes stay updated

## Design Principles

1. Index first, load on match — do not blindly load history without direction
2. Stop as soon as context is sufficient — do not continue if current layer answers the question
3. Do not let history hijack judgment — context serves the task, not the other way around
4. Think about reading when writing — update L1 at task end, do not leave all in daily log
5. L4 is the last resort — not a daily loading layer, only for audits

## Relationship with AgentOS v2

Layered Memory Skill is the **L4 Context layer implementation** for AgentOS v2.

AgentOS v2 provides the complete six-layer architecture. Layered Memory Skill is the standalone reusable implementation of the context layer specifically.

## License

MIT — free to use, modify, and distribute.
