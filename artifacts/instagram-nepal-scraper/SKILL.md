# Instagram Nepal Scraper Skill

## 用途
爬取尼泊尔地区粉丝数超过10万的Instagram博主。

## Handoff Contract

```
goal: 爬取尼泊尔地区粉丝>10万的Instagram博主
actual_problem: 批量爬取有封号风险，需要严格控频 + 地区过滤
success_criteria:
  - [x] 每次请求后 sleep 60秒（防封）
  - [x] 每个 tag 之间 sleep 120秒（防封）
  - [x] 去重机制（基于 user_id）
  - [x] 尼泊尔地区判断（bio + 用户名关键词综合打分）
  - [x] 粉丝阈值判断（>= 100,000）
  - [x] 存档字段完整
  - [x] 通用 Skill 格式（SKILL.md + scraper.py）
primary_owner: A03
evidence_path: artifacts/instagram-nepal-scraper/results.jsonl
```

## 前置要求

| 依赖 | 安装命令 |
|------|---------|
| Python | 3.9+ |
| instagrapi | `pip install instagrapi` |

**无需 Playwright，无需 Chrome**

## 地区判断逻辑

综合打分制（score >= 3 认定为尼泊尔）：

| 命中项 | 分数 |
|--------|------|
| 用户名含尼泊尔关键词 | +2 |
| Bio/全名含尼泊尔关键词 | +3 |

尼泊尔关键词库：
- 用户名：`nepal`, `kathmandu`, `nepali`, `everest`, `himalaya`, `pokhara`, `visitnepal`...
- Bio：`nepal`, `kathmandu`, `🇳🇵`, `.np`, `lukla`, `everest`, `himalaya`, `pokhara`...

## 频率控制

| 操作 | 延迟 |
|------|------|
| 每次 API 请求后 | 60 秒 |
| 每个 hashtag 之间 | 120 秒 |

## 去重机制

- 基于 `user_id`（不是 username，因为用户名可变）
- 启动时从 `results.jsonl` 加载已有用户列表
- 内存中维护 `seen_user_ids` set

## 输出字段

```
username, user_id, follower_count, following_count, media_count,
is_verified, profile_url, nepal_score, nepal_reasons,
discovered_via, scraped_at
```

## 迁移到其他 OpenClaw 实例

1. 复制整个目录到目标机器的 `workspace/artifacts/instagram-nepal-scraper/`
2. 安装依赖：`pip install instagrapi`
3. 配置 sessionid（环境变量或 session.json）
4. 运行：`python scraper.py`

## 环境变量

| 变量 | 说明 |
|------|------|
| `INSTAGRAM_SESSIONID` | Instagram sessionid（优先使用）|
| `SESSION_FILE` | session.json 路径（默认同目录）|
| `RESULTS_PATH` | 结果文件路径（默认同目录 results.jsonl）|
