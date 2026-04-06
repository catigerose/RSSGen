from datetime import date

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed

SKIP_SECTIONS = {"信息披露", "艺术投资"}


def build_day_prefix(target_day):
    return f"{target_day.year}-{target_day.month:02d}/{target_day.day:02d}/"


def run():
    feed_title = "证券日报"
    feed_description = "证券日报每日重要新闻。"
    feed_name = "zqrb.xml"
    website_url = "http://epaper.zqrb.cn/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    day_prefix = build_day_prefix(date.today())
    index_url = "http://epaper.zqrb.cn/html/" + day_prefix + "node_2.htm"
    index_soup = get_soup(index_url)
    news_urls = []

    section_root = index_soup.find("div", class_="neir")
    tables = section_root.find_all("table", class_="biaoge")[:9] if section_root is not None else []
    for table in tables:
        title_node = table.find("h2")
        section_name = title_node.get_text(strip=True)[2:] if title_node is not None else ""
        if section_name in SKIP_SECTIONS:
            continue

        nested_tables = table.find_all("table")
        if not nested_tables:
            continue
        for link in nested_tables[-1].find_all("a"):
            news_urls.append("http://epaper.zqrb.cn/html/" + day_prefix + link["href"])

    for news_url in news_urls:
        if news_url in existing_guids:
            continue

        detail_soup = get_soup(news_url)
        detail_node = detail_soup.find("div", class_="neiyee")
        if detail_node is None:
            continue

        title_node = detail_node.find("h1")
        news_title = title_node.get_text(strip=True) if title_node is not None else news_url
        append_entry(
            entries,
            title=news_title,
            content=detail_node.decode(),
            link=news_url,
        )
        existing_guids.add(news_url)
        added_entry_count += 1

    persist_feed(
        website_url=website_url,
        feed_title=feed_title,
        feed_description=feed_description,
        feed_name=feed_name,
        entries=entries,
        existing_entry_count=existing_entry_count,
        added_entry_count=added_entry_count,
    )


if __name__ == "__main__":
    run()
