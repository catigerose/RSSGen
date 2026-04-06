from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed

FILTER_SOURCES = ["智通财经", "华尔街见闻", "格隆汇"]


def should_skip_source(source_text):
    """过滤掉明显的转载源，只保留更适合本项目的内容。"""
    return any(keyword in source_text for keyword in FILTER_SOURCES)


def run():
    website_url = "https://news.futunn.com/main?lang=zh-cn"
    feed_title = "富途牛牛要闻"
    feed_name = "futunn.xml"
    feed_description = "财经新闻与全球市场资讯聚合。"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url, is_dynamic=True, sleep_seconds=3)

    # 页面已改版，原来的 market-wrap 变成了 marketWrap。
    market_wrap = soup.find("div", class_="marketWrap")
    news_list = []
    if market_wrap is not None:
        news_list = market_wrap.find_all("a", class_="market-item list-item")

    for news in reversed(news_list):
        news_url = news["href"]
        if news_url in existing_guids:
            continue

        title_node = news.find("h2", class_="market-item__title")
        footer_node = news.find("div", class_="market-item__footer")
        source_node = news.find("span", class_="footer-source")
        time_node = news.find("span", class_="footer-time")

        news_title = (
            title_node.get_text(strip=True) if title_node is not None else news.get_text(strip=True)
        )
        source_text = source_node.get_text(strip=True) if source_node is not None else ""
        publish_text = time_node.get_text(strip=True) if time_node is not None else ""

        if should_skip_source(source_text):
            continue

        footer_text = footer_node.get_text(" ", strip=True) if footer_node is not None else ""
        news_detail = (
            f"<p>{news_title}</p>"
            f"<p>来源：{source_text or '未知来源'}</p>"
            f"<p>时间：{publish_text or '未知时间'}</p>"
            f"<p>{footer_text}</p>"
        )

        append_entry(
            entries,
            title=news_title,
            content=news_detail,
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
