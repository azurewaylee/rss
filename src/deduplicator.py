def deduplicate(entries):
    """
    根据文章链接去重
    """

    result = []

    seen = set()

    for item in entries:

        entry = item["entry"]

        link = getattr(entry, "link", None)

        if not link:
            continue

        if link in seen:
            continue

        seen.add(link)

        result.append(item)

    return result