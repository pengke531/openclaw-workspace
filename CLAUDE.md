# CLAUDE.md - Claude Code 配置

## Skills

本项目使用 **gstack** 作为主要技能集。

### 浏览器
- 使用 gstack 的 `/browse` skill 进行所有网页浏览，**不要使用** `mcp__claude-in-chrome__*` 工具

### 可用 Skills

| 命令 | 用途 |
|------|------|
| `/office-hours` | 办公时间 - 重构问题、讨论想法 |
| `/plan-ceo-review` | CEO审查 - 产品战略、方向把控 |
| `/plan-eng-review` | 工程审查 - 技术方案评估 |
| `/plan-design-review` | 设计审查 - 架构设计评审 |
| `/design-consultation` | 设计咨询 - UI/UX 问题 |
| `/review` | 代码审查 - 找bug、提高质量 |
| `/ship` | 发布工程师 - 合并PR、发布版本 |
| `/browse` | 浏览器自动化 - 浏览网页、操作UI |
| `/qa` | QA测试 - 完整测试流程 |
| `/qa-only` | 仅QA - 只测试不修bug |
| `/design-review` | 设计评审 |
| `/retro` | 回顾分析 - 复盘总结 |
| `/investigate` | 调查问题 - 调试、排错 |
| `/document-release` | 文档发布 |
| `/codex` | 多AI第二意见 |
| `/careful` | 谨慎模式 - 安全检查 |
| `/freeze` | 冻结模式 - 暂停AI自动操作 |
| `/guard` | 守护模式 - 保护关键文件 |
| `/unfreeze` | 解冻 - 恢复AI操作 |
| `/gstack-upgrade` | 升级gstack |

## 使用方式

直接输入 `/技能` 即可调用，例如：
- `/office-hours` - 讨论你想做什么
- `/review` - 审查当前代码改动
- `/qa` - 测试你的应用

## 项目背景

这是 OpenClaw 的工作空间，用于多Agent协作平台开发。
