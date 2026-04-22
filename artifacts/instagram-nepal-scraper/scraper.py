"""
Instagram Nepal Scraper - 基于 instagrapi
频率: 60秒/请求, 120秒/tag（严格防封）
去重: user_id
依赖: instagrapi (pip install instagrapi)
"""

import json
import os
import time
from datetime import datetime
from instagrapi import Client

# ============ 配置区（可迁移） ============
HASHTAGS = [
    'nepal', 'kathmandu', 'nepali', 'nepalese', 'nepaltravel',
    'kathmandunepal', 'nepalphotography', 'nepalfood', 'nepalfashion',
    'nepaligram', 'visitnepal', 'nepalbeauty', 'nepallife'
]
FOLLOWER_THRESHOLD = 100_000
DELAY_BETWEEN_REQUESTS = 60  # 秒（防封）
DELAY_BETWEEN_TAGS = 120     # 秒（防封）

# 尼泊尔地区判断关键词
NEPAL_KEYWORDS_IN_BIO = [
    'nepal', 'kathmandu', 'nepali', 'nepalese', 'kathmandune',
    '🇳🇵', 'np', '.np', 'lukla', 'everest', 'himalaya',
    'pokhara', 'bhaktapur', 'patan', 'bhutia', 'newar', 'maithili'
]
NEPAL_KEYWORDS_IN_USERNAME = [
    'nepal', 'kathmandu', 'nepali', 'kathmandunepal', 'nepalese',
    'everest', 'himalaya', 'pokhara', 'nepaltravel', 'visitnepal'
]

# Session 配置
SESSIONID = os.environ.get('INSTAGRAM_SESSIONID', '')
SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'session.json')
RESULTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.jsonl')
# ==========================================

os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)


def is_nepal_user(user_info):
    """
    判断用户是否为尼泊尔地区
    综合 bio + 用户名 + 发帖地点 判断
    返回: (bool, score, reasons)
    """
    username = user_info.get('username', '').lower()
    bio = user_info.get('biography', '').lower()
    full_name = user_info.get('full_name', '').lower()

    score = 0
    reasons = []

    # 用户名命中
    for kw in NEPAL_KEYWORDS_IN_USERNAME:
        if kw in username:
            score += 2
            reasons.append(f'username含"{kw}"')
            break

    # bio 命中（权重更高）
    for kw in NEPAL_KEYWORDS_IN_BIO:
        if kw in bio or kw in full_name:
            score += 3
            reasons.append(f'bio含"{kw}"')
            break

    # 综合判断：score >= 3 认为尼泊尔
    is_nepal = score >= 3
    return is_nepal, score, reasons


def load_seen_user_ids():
    """从已有结果中加载已见过的 user_id（去重）"""
    seen = set()
    if os.path.exists(RESULTS_PATH):
        with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    seen.add(json.loads(line)['user_id'])
                except:
                    pass
    print(f"[去重] 已加载 {len(seen)} 个已爬取用户")
    return seen


def save_result(result):
    """追加写入结果（去重后）"""
    with open(RESULTS_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')


def build_client():
    """构建并登录 instagrapi Client"""
    cl = Client()

    if SESSIONID:
        print(f"[登录] 使用 SESSIONID 登录...")
        cl.login_by_sessionid(SESSIONID)
        return cl

    if os.path.exists(SESSION_FILE):
        print(f"[登录] 从 session.json 加载...")
        cl.load_settings(SESSION_FILE)
        try:
            cl.login_by_sessionid(cl.sessionid)
            return cl
        except Exception as e:
            print(f"[登录] session 过期: {e}")

    print("[错误] 未配置 SESSIONID，也找不到 session.json")
    print("[解决] 设置环境变量 INSTAGRAM_SESSIONID 或创建 session.json")
    return None


def get_user_info(cl, username):
    """获取单个用户详情"""
    try:
        user = cl.user_info_by_username(username)
        return {
            'pk': user.pk,
            'username': user.username,
            'full_name': user.full_name,
            'biography': user.biography,
            'follower_count': user.follower_count,
            'following_count': user.following_count,
            'media_count': user.media_count,
            'is_verified': user.is_verified,
            'profile_url': f"https://www.instagram.com/{username}/",
            'is_private': user.is_private,
        }
    except Exception as e:
        print(f"  [!] 获取用户 {username} 失败: {e}")
        return None


def scrape_hashtag(cl, hashtag, seen_user_ids):
    """爬取单个 hashtag，返回符合条件的用户"""
    results = []
    print(f"\n[Tag] 正在爬取 #{hashtag}")

    try:
        medias = cl.hashtag_medias_top(hashtag, amount=20)
        print(f"  [*] 热门帖子: {len(medias)} 个")
    except Exception as e:
        print(f"  [!] 热门帖子获取失败: {e}")
        try:
            medias = cl.hashtag_medias_recent(hashtag, amount=20)
            print(f"  [*] 改用 recent: {len(medias)} 个")
        except Exception as e2:
            print(f"  [!] recent 也失败: {e2}")
            return results

    # 提取用户名
    usernames = []
    for media in medias:
        if hasattr(media, 'user') and media.user:
            uid = str(media.user.pk)
            if uid not in seen_user_ids:
                usernames.append(media.user.username)
                seen_user_ids.add(uid)

    print(f"  [*] 待处理 {len(usernames)} 个用户")

    for username in usernames:
        time.sleep(DELAY_BETWEEN_REQUESTS)  # 严格60秒

        user_info = get_user_info(cl, username)
        if not user_info:
            continue

        uid = str(user_info['pk'])

        # 跳过私密账号
        if user_info.get('is_private'):
            print(f"  [-] {username}: 私密账号，跳过")
            continue

        # 粉丝数判断
        follower_count = user_info.get('follower_count', 0)
        if follower_count < FOLLOWER_THRESHOLD:
            print(f"  [-] {username}: {follower_count:,} 粉丝（不足{FOLLOWER_THRESHOLD:,}）")
            continue

        # 尼泊尔地区判断
        is_nepal, score, reasons = is_nepal_user(user_info)
        if not is_nepal:
            print(f"  [-] {username}: {follower_count:,} 粉丝（非尼泊尔地区，score={score}）")
            continue

        # 符合条件，存档
        result = {
            'username': user_info['username'],
            'user_id': uid,
            'follower_count': follower_count,
            'following_count': user_info.get('following_count', 0),
            'media_count': user_info.get('media_count', 0),
            'is_verified': user_info.get('is_verified', False),
            'profile_url': user_info.get('profile_url'),
            'nepal_score': score,
            'nepal_reasons': reasons,
            'discovered_via': hashtag,
            'scraped_at': datetime.now().isoformat(),
        }
        results.append(result)
        print(f"  [+] {username}: {follower_count:,} 粉丝 ✓ 尼泊尔（{'; '.join(reasons)}）")

    print(f"  [*] #{hashtag} 完成，找到 {len(results)} 个符合条件用户")
    return results


def main():
    print("=" * 60)
    print("Instagram Nepal Scraper 开始运行")
    print(f"粉丝阈值: {FOLLOWER_THRESHOLD:,}")
    print(f"请求延迟: {DELAY_BETWEEN_REQUESTS}秒 | Tag延迟: {DELAY_BETWEEN_TAGS}秒")
    print(f"地区判断: 尼泊尔关键词综合打分（score>=3）")
    print("=" * 60)

    cl = build_client()
    if not cl:
        print("[错误] 无法登录，程序退出")
        return

    seen_user_ids = load_seen_user_ids()

    for i, hashtag in enumerate(HASHTAGS):
        print(f"\n[{i+1}/{len(HASHTAGS)}] 进度")
        users = scrape_hashtag(cl, hashtag, seen_user_ids)
        for user in users:
            save_result(user)
            print(f"  [保存] {user['username']}")

        print(f"[Tag] #{hashtag} 完成，等待 {DELAY_BETWEEN_TAGS} 秒...")
        time.sleep(DELAY_BETWEEN_TAGS)

    # 保存 session
    if SESSIONID and not os.path.exists(SESSION_FILE):
        try:
            cl.dump_settings(SESSION_FILE)
            print(f"[Session] 已保存到 session.json")
        except Exception as e:
            print(f"[Session] 保存失败: {e}")

    print("\n" + "=" * 60)
    print("全部完成！结果已保存到:", RESULTS_PATH)
    print("=" * 60)


if __name__ == "__main__":
    main()
