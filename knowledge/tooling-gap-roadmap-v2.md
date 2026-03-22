# 工具缺口路线图 v2

> 识别当前工具体系中的缺口，按优先级规划补强路径。

---

## 优先级定义

| 优先级 | 含义 | 响应时间 |
|--------|------|---------|
| **P0** | 当前严重影响效率或正确性 | 立即规划，1 周内解决 |
| **P1** | 当前有一定影响 | 1 周内规划，1 个月内解决 |
| **P2** | 未来有价值，当前可暂缓 | 有空再说 |

---

## 工具现状评估

### 已有工具

| 工具 | 用途 | 状态 | 备注 |
|------|------|------|------|
| sessions_spawn | 子 Agent 调度 | ✅ 可用 | ACP/subagent 两种模式 |
| sessions_list | 查看活跃会话 | ✅ 可用 |  |
| sessions_send | 向子会话发消息 | ✅ 可用 |  |
| exec | 命令行执行 | ✅ 可用 | ARM Windows 兼容 |
| browser | 浏览器自动化 | ✅ 可用 | Chrome 已登录 |
| web_fetch | 读取网页内容 | ✅ 可用 |  |
| memory_recall | 记忆检索 | ✅ 可用 |  |
| memory_store | 记忆存储 | ✅ 可用 |  |
| feishu_* | 飞书全套 | ✅ 可用 | OAuth 已授权 |
| cron | 定时任务 | ✅ 可用 |  |

### 缺口工具

| 工具 | 优先级 | 影响 | 状态 |
|------|--------|------|------|
| 文件全文搜索（`rg`） | **P0** | 无法快速搜索文件内容 | 未安装 |
| session trace 检索 | **P0** | 无法追溯历史会话细节 | 部分可用 |
| skill 自动验证 | **P1** | Enforcement 依赖手动检查 | ✅ 已实现（enforcement_validator.py） |
| 日志归档 | **P1** | 工具输出散落 | 部分实现（evidence/） |

---

## P0 缺口详情

### P0-1: 文件全文搜索（`rg` / ripgrep）

**问题**: 当需要搜索某个关键词在哪些文件中出现时，只能逐文件读取
**影响**: 
- 大型项目中查找函数/配置项效率极低
- 无法快速确认某个改动的影响范围
- 排查问题时需要手动 grep 多个文件

**解决方案**:
1. 首选：`rg`（ripgrep）— 跨平台、高性能
2. Windows ARM 兼容版：`winget install BurntSushi.ripgrep`
3. 备选：PowerShell Select-String（性能较差）

**安装验证**:
```bash
rg --version
# 预期：输出版本号
```

**使用场景**:
```bash
# 搜索包含关键词的文件
rg "task-grading" C:\Users\itach\.openclaw\workspace\knowledge\

# 搜索并显示行号
rg -n "failure-taxonomy" --type md

# 搜索不区分大小写
rg -i "openclaw" 
```

**行动计划**:
- [ ] 安装 `rg`
- [ ] 在 AGENTS.md 中增加 rg 使用说明
- [ ] 验证 ARM Windows 兼容性
- [ ] 更新 TOOLS.md

---

### P0-2: Session Trace 检索

**问题**: 只能通过 sessions_list 看到会话列表，无法搜索历史会话内容
**影响**:
- 无法追溯过去某次任务的执行细节
- 复盘时只能靠记忆或截断的总结
- 经验无法有效复用

**解决方案**:
1. sessions_history 工具 — 获取历史会话消息
2. 定期将重要会话的 trace 归档到 evidence/
3. 使用 memory_recall 检索历史记忆

**当前可用手段**:
```python
# sessions_history 可获取历史消息
sessions_history(sessionKey="xxx", limit=50)
```

**缺口**:
- 没有自动归档机制
- 搜索能力有限（只能逐个会话查看）
- 需要更好的会话元数据管理

**行动计划**:
- [ ] 建立会话归档规范（什么会话需要归档）
- [ ] 实现定期归档 cron 任务
- [ ] 在 evidence/ 中建立会话归档目录结构

---

## P1 缺口详情

### P1-1: 日志归档系统

**当前状态**: 工具输出散落在各处，没有统一归档
**目标**: 关键工具输出自动归档到 evidence/tool-outputs/

**行动计划**:
- [ ] 定义归档触发条件（高风险操作、调研结果等）
- [ ] 建立 evidence/tool-outputs/ 目录结构
- [ ] 实现手动归档流程（复杂任务后强制归档）

---

## P2 路线

### P2-1: Whisper / STT 路线

**目标**: 实现语音输入，减少打字
**状态**: 已有 skill（openai-whisper），待验证
**优先级**: P2（等核心流程稳定后再做）

---

## 工具使用原则

1. **first-class tool 优先**: OpenClaw 自带工具优先于外部工具
2. **验证后再用**: 新工具必须验证 ARM Windows 兼容性
3. **少而精**: 不追求工具数量，追求工具编排质量
4. **可回滚**: 涉及环境修改的操作必须有回滚方案
