from pathlib import Path
import listparser


def load_opml(opml_path):
    result = listparser.parse(opml_path)

    if not result.feeds:
        print("没有找到任何 RSS 订阅。")
        return

    print(f"共发现 {len(result.feeds)} 个 RSS 订阅：\n")

    for i, feed in enumerate(result.feeds, start=1):
        title = feed.title or "(无标题)"
        url = feed.url

        print(f"{i}. {title}")
        print(f"   {url}")
        print()
