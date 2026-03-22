# Validation Cases

## Test Case 1: L0 Always Loads

**Scenario**: New session, any task  
**Expected**: `MEMORY.md` is read first  
**Verification**: Agent can correctly answer "What is the user's name?" without extra context

---

## Test Case 2: L1 Loads on Domain Match

**Scenario**: Task involves "技术配置" or "技术环境"  
**Expected**: `memory/技术配置.md` is loaded  
**Verification**: Agent correctly references ARM Windows, Python version, proxy settings

---

## Test Case 3: L2 Loads for Active Project

**Scenario**: Task is about continuing an existing project  
**Expected**: Relevant daily memory (`YYYY-MM-DD.md`) is loaded  
**Verification**: Agent knows recent project decisions without re-explaining context

---

## Test Case 4: Simple Task Stays at L0

**Scenario**: "What time is it?" or one-step factual question  
**Expected**: Only L0 loaded, no L1-L4 accessed  
**Verification**: Response is fast (<1 min), no unnecessary file reads

---

## Test Case 5: Complex Task Drills to L3

**Scenario**: Implementing a full system with multiple files  
**Expected**: L0 → L1 → L2 → L3 loaded in sequence  
**Verification**: Agent has sufficient context to make coherent architecture decisions

---

## Test Case 6: No Premature Deep Loading

**Scenario**: Simple task but agent loads L2/L3 unnecessarily  
**Expected**: Loading stops at L0 or L1  
**Verification**: Fewer than 3 memory files loaded for simple tasks

---

## Test Case 7: Audit Accesses L4

**Scenario**: Dispute about what was decided on a past date  
**Expected**: L4 (raw conversation logs, tool outputs) accessible  
**Verification**: Agent can trace back to exact decisions with evidence

---

## Test Case 8: Memory Stays Updated

**Scenario**: After significant decisions, MEMORY.md and indexes updated  
**Expected**: L1 files (项目经验, 技术配置) reflect current state  
**Verification**: New session can trust MEMORY.md as accurate index

---

## Success Criteria

- [ ] L0 is read every session
- [ ] Domain-matched tasks trigger L1 loading
- [ ] Project tasks trigger L2 loading
- [ ] Complex tasks trigger L3 loading when needed
- [ ] Simple tasks do not over-load layers
- [ ] Memory indexes are kept up to date
- [ ] Audit/dispute can access L4 when necessary
