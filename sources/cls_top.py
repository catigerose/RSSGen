from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_title = "财联社头条"
    feed_description = "财联社深度内容与重点头条聚合。"
    feed_name = "cls_top.xml"
    website_url = "https://www.cls.cn/depth?id=1000"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    # 财联社该页由前端渲染，需使用 Selenium 获取完整内容。
    soup = get_soup(website_url, is_dynamic=True)
    news_list = soup.find_all(
        "div", class_="clearfix b-c-e6e7ea subject-interest-list"
    )

    # 旧数据在前，新数据在后，便于后续直接追加。
    for news in reversed(news_list):
        news_url = "https://www.cls.cn" + news.a["href"]
        if news_url in existing_guids:
            continue

        news_title = news.div.div.a.get_text(strip=True)
        append_entry(
            entries,
            title=news_title,
            content=news_title,
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
