from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_title = "要闻-智通财经"
    feed_description = "智通财经要闻聚合。"
    feed_name = "ztcj.xml"
    website_url = "https://www.zhitongcaijing.com/?index=yaowen"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url, is_dynamic=True)
    content_root = soup.find("div", class_="home-list-scroll")
    news_list = (
        content_root.find_all("div", class_="info-item-content")
        if content_root is not None
        else []
    )

    for news in reversed(news_list):
        news_url = "https://www.zhitongcaijing.com" + news.div.a["href"]
        if news_url in existing_guids:
            continue

        news_title = news.div.a.span.get_text(strip=True)
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
