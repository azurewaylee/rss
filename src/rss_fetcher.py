from concurrent.futures import ThreadPoolExecutor, as_completed
import feedparser

from config import MAX_ARTICLES_PER_FEED, MAX_WORKERS


def fetch_one(feed):
    """
    下载一个 RSS
    """
    print(f"下载：{feed['title']}")

    rss = feedparser.parse(feed["url"])

    articles = []

    if getattr(rss, "bozo", False):
        print(f"  ⚠ 解析警告：{feed['title']}")

    for entry in rss.entries[:MAX_ARTICLES_PER_FEED]:

        articles.append({
            "source": feed["title"],
            "entry": entry
        })

    return articles


def fetch_all(feeds):
    """
    并发下载所有 RSS
    """
    all_entries = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(fetch_one, feed): feed
            for feed in feeds
        }

        for future in as_completed(futures):

            try:
                articles = future.result()

                all_entries.extend(articles)

            except Exception as e:

                feed = futures[future]

                print(f"下载失败：{feed['title']}")

                print(e)

    return all_entries