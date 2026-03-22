---
name: self-improvement-enforcement
description: AgentOS v2 自我提升 enforcement 层。包含提交前检查清单、任务后复盘、每周复盘、定期自我纠正机制。确保敷衍行为在系统层被主动发现和阻止，而非依赖人工自觉。
---

# Self-Improvement Enforcement Layer

> **版本**: 1.0  
> **目的**: 把"自我提升"从口号变成有硬性 enforcement 的系统机制  
> **核心原则**: 没有 enforcement 的规则等于没有规则

---

## 为什么需要这一层

### 传统模式的失败

```
规则（文档） → 依赖个人自觉 → 敷衍行为发生 → 无机制发现 → 系统退化
```

### Enforcement 模式的成功

```
规则（文档）
    ↓
Enforcement 机制（自动检查 + 硬性阻止）
    ↓
敷衍行为在发生前被拦截 / 在发生后被立即发现
    ↓
系统自动纠正 → 持续提升
```

---

## Enforcement 三大机制

### 机制 1：提交前检查清单（Pre-Commit Checklist）

**触发时机**: 任何 commit 前

**本质**: 强制填写，不能跳过

检查项：
- [ ] 本次提交包含了规划中的全部核心交付物吗？
- [ ] README 是否按 SKILL.md 规范写完整了？（不是残缺版）
- [ ] 是否有遗漏的关联文件（测试/示例/验证用例）？
- [ ] 是否经过真实测试（非仅文件存在检查）？
- [ ] 是否主动向用户确认交付物符合预期？

**通过标准**: 5/5 全部通过，否则禁止 commit

---

### 机制 2：任务后复盘（Post-Task Review）

**触发时机**: 每个任务完成后

**本质**: 强制反思，不是可选步骤

复盘问题：
1. 本次任务的真实产出与规划一致吗？
2. 是否有环节被简化/跳过/敷衍了？
3. 如果有，是哪个环节、什么形式的敷衍？
4. 下次如何提前发现和阻止同类敷衍？
5. 有哪些经验需要写入 L1 教训层？

---

### 机制 3：每周复盘（Weekly Review）

**触发时机**: 每周结束 / heartbeat 检查

**本质**: 系统性发现模式，而非个案处理

复盘维度：

**A. 交付完整性**
- 本周计划的核心交付物实际完成了多少？
- 被跳过的部分是主动决定还是系统漏洞？

**B. 敷衍模式检测**
- 本周是否有明显简化执行的迹象？
- 文档是否与实际交付一致？
- 用户是否有明确不满表示？

**C. 失败分类统计**
- 本周失败属于哪几类？（来自 failure taxonomy）
- 是否有同一类失败连续出现？

**D. Enforcement 机制有效性**
- Pre-commit 检查表是否被实际使用？
- Post-task 复盘是否有真实填写？
- 本周是否有应该被发现但实际漏掉的敷衍？

---

## 自我纠正触发条件（Auto-Correction）

当以下任一条件触发时，立即启动自我纠正：

| 触发条件 | 纠正动作 |
|---------|---------|
| 用户明确表示不满 | 停止执行，回滚未验证的变更，触发 post-task 复盘 |
| Pre-commit 5项有2项以上不通过 | 禁止 commit，强制填写敷衍检测说明 |
| 同一类失败连续出现2次 | 触发根因分析，更新 L1 教训层 |
| Weekly review 发现系统性敷衍 | 立即通知用户，人工介入审查 |
| 文档描述与实际交付明显不符 | 立即修正文档，禁止以"已上线"为由拒绝补全 |

---

## 敷衍行为快速识别清单

以下任一描述命中，即为敷衍：

- [ ] 文档写了完整规范，但实际只有骨架或残缺版
- [ ] 功能说"已实现"，但没有测试、没有示例、无法验证
- [ ] commit message 说"完整"，但实际只提交了部分文件
- [ ] 向用户展示时用"基本完成"搪塞实际缺失的部分
- [ ] 用户要求"完整"，但只补了一小部分就说"好了"
- [ ] 项目说"已开源"，但仓库里没有实质性内容
- [ ] 声称"测试通过"，但实际只做了文件存在检查

---

## Enforcement 执行流程

### 每个任务的完整流程

```
1. 任务开始
   → 明确规划：本次的真实交付物是什么？
   → 写入 Post-Task Review 模板

2. 任务执行中
   → Pre-commit 检查：每批次完成时强制自检
   → 如有敷衍迹象 → 立即纠正

3. 任务完成
   → 真实验证：交付物是否可演示/可测试/可使用？
   → Post-Task 复盘：是否有简化？是否有遗漏？

4. 提交前（强制）
   → Pre-commit Checklist 全部通过？
   → 如有 2 项以上不通过 → 停止提交，补全后重检

5. 提交后
   → 向用户展示真实交付物
   → 等待用户反馈
   → 如用户不满 → 立即触发自我纠正
```

---

## Enforcement Validator Script

The `scripts/enforcement_validator.py` provides automated validation for all skills before commit:

**Checks performed**:
- Required files exist: SKILL.md, README.md, LICENSE
- SKILL.md frontmatter has name and description fields
- SKILL.md name field matches the directory name
- README.md contains required sections: Overview, Architecture, Usage, Files, License
- SKILL.md word count >= 500 characters
- examples/ and tests/ directories exist and have content (recommended)

**Usage**:
```bash
python scripts/enforcement_validator.py <skill_directory>
```

**Exit codes**:
- 0 = all checks passed
- 1 = passed with warnings (recommend fixing before commit)
- 2 = failed (must fix before commit)

This script is the automated enforcement layer. It runs before every commit and blocks submissions that do not meet quality standards.

## 与 AgentOS v2 其他层的关系

```
L1 治理层 ← 定义规则（任务分级/执行闸门）
L2 编排层 ← 定义分工（何时 spawn/何时自做）
L3 执行层 ← 定义执行标准（角色/handoff/验证）
L4 上下文 ← 定义记忆分层（按需加载）
L5 工具层 ← 定义工具优先级

↓ 以上全部依赖 ↓

自我提升 Enforcement 层 ← 主动发现并阻止敷衍
        ↓
   L6 观测层 ← 被动记录 trace（Enforcement 是主动雷达）
```

Enforcement 是 L6（观测）的主动版：
- L6 是"事后记录"
- Enforcement 是"事中拦截 + 事前预防"

---

## 文件结构

```
self-improvement-enforcement/
├── SKILL.md                         # 本文件
├── README.md                        # 使用说明
├── LICENSE                         # MIT License
├── checks/
│   ├── pre-commit-checklist.md      # 提交前强制检查清单
│   └── post-task-review.md          # 任务后复盘模板
├── templates/
│   ├── weekly-review.md              # 每周复盘模板
│   └── self-correction.md           # 自我纠正触发模板
└── scripts/
    └── enforcement_validator.py      # 自动验证脚本（可选）
```

---

## 激活条件

**必须激活**：
- 每次 commit 前（Pre-commit Checklist）
- 每次任务完成后（Post-Task Review）
- 每周 heartbeat 时（Weekly Review）
- 用户明确表示不满时（Self-Correction）
- 发现同一类失败连续出现时（Root Cause Analysis）

**不是可选功能，是强制 enforcement 机制。**
