from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from feedgen.feed import FeedGenerator


def parse_date(entry):
    """
    将 RSS 发布时间统一转换为 UTC 时间，方便排序。
    """
    for attr in ("published", "updated"):
        value = getattr(entry, attr, None)

        if value:
            try:
                dt = parsedate_to_datetime(value)

                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)

                return dt.astimezone(timezone.utc)

            except Exception:
                pass

    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def write_feed(all_entries, output_file):

    fg = FeedGenerator()

    fg.title("My RSS Aggregator")
    fg.link(href="https://github.com/azurewaylee/rss")
    fg.description("Generated from OPML")
    fg.language("zh-cn")

    # 按发布时间排序（最新在前）
    all_entries.sort(
        key=lambda x: parse_date(x["entry"]),
        reverse=True
    )

    for item in all_entries:

        entry = item["entry"]

        fe = fg.add_entry()

        # 标题
        fe.title(getattr(entry, "title", ""))

        # 链接 + GUID
        if hasattr(entry, "link"):
            fe.link(href=entry.link)
            fe.guid(entry.link, permalink=True)

        # 描述（优先 summary，其次 content）
        description = ""

        if hasattr(entry, "summary"):
            description = entry.summary
        elif hasattr(entry, "content") and entry.content:
            description = entry.content[0].get("value", "")

        fe.description(description)

        # 发布时间
        fe.pubDate(parse_date(entry))

        # 作者
        if hasattr(entry, "author"):
            fe.author({"name": entry.author})

        # 来源
        fe.category(term=item["source"])

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fg.rss_file(str(output_file), pretty=True)

    print()
    print("=" * 50)
    print("RSS 已生成")
    print(output_file)
    print("=" * 50)