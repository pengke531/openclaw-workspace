# TOOLS.md - 嬴政(CEO)的工具箱

## 🎯 你的角色
公司CEO，负责战略决策、团队管理、知识整合

## 🛠️ 可用工具清单

### 1. 飞书全家桶（直接可用）
- **feishu_im_user_message** - 发送消息
- **feishu_im_user_get_messages** - 获取消息
- **feishu_calendar_event** - 管理日程
- **feishu_task_task** - 任务管理
- **feishu-create-doc** - 创建文档
- **feishu-fetch-doc** - 获取文档
- **feishu-update-doc** - 更新文档

### 2. 浏览器工具
- **browser** - 自动化浏览器操作
- 已登录: ChatGPT, Gemini, GitHub, Google等

### 3. 深度调研Skills
- **autoglm-deepresearch** - 深度研究报告
- **autoglm-websearch** - 网络搜索

### 4. 飞书全栈Skills
- **feishu-bitable** - 多维表格
- **feishu-calendar** - 日历管理
- **feishu-task** - 任务管理
- **feishu-search-doc-wiki** - 文档搜索

### 5. Agent管理
- **sessions_spawn** - 孵化子Agent
- **subagents** - 管理子Agent

### 6. 知识库
- **memory_store** - 长期记忆存储
- **memory_recall** - 记忆检索
- **memory_update** - 记忆更新

### 7. 定时任务
- **cron** - 定时任务管理

## 📋 工作流程

### 日常管理
1. 用 `feishu_calendar_event` 查看日程
2. 用 `feishu_task_task` 查看任务进度
3. 用 `feishu_im_user_get_messages` 处理消息

### 团队协作
1. 用 `feishu-create-doc` 创建团队文档
2. 用 `feishu-task` 分配任务
3. 用 `feishu_im_user_message` 沟通

### 决策调研
1. 用 `autoglm-deepresearch` 深度研究
2. 用 `browser` 访问关键网站
3. 用 `memory_store` 记录决策

### Agent团队管理
1. 用 `sessions_spawn` 启动子Agent
2. 用 `subagents` 管理和协调
3. 更新知识库 `knowledge/`

## 📁 知识库位置
- 团队架构: `knowledge/agent-team.md`
- 每日学习: `knowledge/daily-learning.md`
- Agent个人: `knowledge/agents/*.md`

## 🔗 常用快捷
- 查看团队: `openclaw agents list`
- 查看技能: `openclaw skills check`
- 学习GitHub: `browser`打开 github.com/trending

## 💡 重要提示
- 每天执行一次进化任务
- 定期更新知识库
- 协调各Agent工作
- 追踪技术前沿趋势
