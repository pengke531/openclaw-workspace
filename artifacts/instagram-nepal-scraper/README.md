# Instagram Nepal Scraper

## 功能
爬取尼泊尔地区粉丝超过10万的Instagram博主。

## 特性

- ✅ 基于 instagrapi（纯 API，无需浏览器）
- ✅ 严格控频：60秒/请求，120秒/tag
- ✅ 尼泊尔地区判断（bio + 用户名综合打分）
- ✅ 自动去重：基于 user_id
- ✅ 追加写入：不覆盖历史数据
- ✅ 通用可迁移

## 前置准备

### 1. 安装依赖
```bash
pip install instagrapi
```

### 2. 配置 sessionid（二选一）

**方式A：环境变量（推荐）**
```bash
# Windows
set INSTAGRAM_SESSIONID=你的sessionid字符串

# Mac/Linux
export INSTAGRAM_SESSIONID=你的sessionid字符串
```

**方式B：创建 session.json**
在同目录下创建 `session.json`，填入 session 字符串。

### 3. 获取 sessionid
1. 用 Chrome 打开 [instagram.com](https://instagram.com) 并登录
2. 按 **F12** → **Application** → **Cookies** → 找 `sessionid`
3. 复制值并配置

### 4. 运行
```bash
python scraper.py
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FOLLOWER_THRESHOLD` | 100,000 | 粉丝数阈值 |
| `DELAY_BETWEEN_REQUESTS` | 60 | 每次请求后延迟（秒）|
| `DELAY_BETWEEN_TAGS` | 120 | 每个 tag 之间延迟（秒）|

## 尼泊尔判断逻辑

综合打分制（score >= 3 认定尼泊尔）：

| 命中项 | 加分 |
|--------|------|
| 用户名含尼泊尔关键词 | +2 |
| Bio/全名含尼泊尔关键词 | +3 |

## 输出

- 文件：`results.jsonl`（JSON Lines，追加写入）
- 字段说明：
  ```
  username        - Instagram 用户名
  user_id        - 用户唯一ID
  follower_count - 粉丝数
  following_count - 关注数
  media_count    - 发帖数
  is_verified    - 是否认证
  profile_url    - 主页链接
  nepal_score    - 尼泊尔打分
  nepal_reasons  - 命中原因
  discovered_via  - 从哪个 hashtag 发现
  scraped_at     - 爬取时间
  ```

## 迁移

```bash
# 1. 复制
cp -r instagram-nepal-scraper /目标路径/

# 2. 安装依赖
pip install instagrapi

# 3. 配置 sessionid
export INSTAGRAM_SESSIONID=你的sessionid

# 4. 运行
python /目标路径/scraper.py
```

## 注意事项

- ⚠️ 60秒/120秒延迟是保险值，可根据账号情况调整
- ⚠️ sessionid 过期后需要重新获取
- ⚠️ 账号被封需换账号
- ℹ️ 结果文件是追加写入，不会覆盖历史数据
- ℹ️ 私密账号会被跳过
