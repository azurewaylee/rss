from pathlib import Path

from opml_reader import load_opml
from rss_fetcher import fetch_all
from deduplicator import deduplicate
from feed_writer import write_feed
from config import OUTPUT_FILE


def main():

    root = Path(__file__).resolve().parent.parent

    opml_file = root / "feeds" / "subscriptions.opml"

    feeds = load_opml(opml_file)

    print("=" * 60)
    print("RSS Aggregator")
    print("=" * 60)

    print(f"共发现 {len(feeds)} 个 RSS")

    print()

    all_entries = fetch_all(feeds)

    print()

    print(f"下载完成，共 {len(all_entries)} 篇文章")

    print()

    all_entries = deduplicate(all_entries)

    print(f"去重后剩余 {len(all_entries)} 篇")

    print()

    output = root / OUTPUT_FILE

    write_feed(all_entries, output)

    print()

    print("全部完成！")


if __name__ == "__main__":
    main()