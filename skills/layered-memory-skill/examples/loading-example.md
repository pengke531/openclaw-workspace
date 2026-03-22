# Loading Examples

## Example 1: Simple Question

**Task**: "What's the user's name and timezone?"

**Loading sequence**:
1. L0: Read `MEMORY.md` → Found in "关于彭科" → Stop

**Layers loaded**: 1 (L0 only)  
**Time**: <1 min

---

## Example 2: Project Task

**Task**: Continue working on "智惠 X4 (RLG)" project

**Loading sequence**:
1. L0: Read `MEMORY.md` → Check project index
2. L1: Read `memory/项目经验.md` → Found entry for 智惠X4
3. L2: Read `memory/2026-03-22.md` → Last session details on this project
4. L3: Read `智惠X4_技术开发手册.md` → Only if deeply technical question

**Layers loaded**: L0 + L1 + L2 (L3 only if needed)  
**Time**: 2-3 min

---

## Example 3: Complex Execution Task

**Task**: Implement the AgentOS v2 memory system and ship it

**Loading sequence**:
1. L0: Read `MEMORY.md` → Check "重要变更" and "待办"
2. L1: Read `memory/当前活跃任务.md` → Active tasks
3. L1: Read `memory/技术配置.md` → Tech baseline
4. L2: Read `memory/2026-03-23.md` → Today's session progress
5. L3: Read `docs/plans/2026-03-23-agentos-v2-blueprint.md` → Full blueprint
6. L3: Read `knowledge/task-grading.md`, `knowledge/execution-gates-v2.md` → Governance files

**Layers loaded**: L0 + L1 + L2 + L3  
**Time**: 5-10 min

---

## Example 4: New Session Resume

**Task**: Resume work after 3 days

**Loading sequence**:
1. L0: Read `MEMORY.md` → Check for updates since last session
2. L1: Read relevant domain indexes → Any changes in tech config or projects?
3. L2: Read `memory/` for last 3 days → What happened in between?
4. L3: Read detailed files only if L2 reveals significant unfinished work

**Layers loaded**: L0 + L1 + L2 (L3 selective)  
**Time**: 3-5 min

---

## Example 5: Audit / Dispute Resolution

**Task**: Resolve disagreement about what was decided on 智惠X4 tech stack

**Loading sequence**:
1. L0: Read `MEMORY.md`
2. L1: Read `memory/项目经验.md` → 智惠X4 entry
3. L2: Read all `memory/YYYY-MM-DD.md` files related to 智惠X4
4. L3: Read design docs, meeting notes, technical decisions
5. L4: If still unclear → Check conversation logs or tool outputs from those dates

**Layers loaded**: All layers as needed  
**Time**: 10-15 min
