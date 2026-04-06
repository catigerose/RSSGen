from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_title = "要闻-每日经济新闻"
    feed_description = "每日经济新闻要闻聚合。"
    feed_name = "nbd.xml"
    website_url = "http://www.nbd.com.cn/columns/3/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url, sleep_seconds=1)
    news_container = soup.find("ul", class_="u-news-list")
    news_list = []
    if news_container is not None:
        news_list = news_container.find_all("li", class_="u-news-title")

    for news in reversed(news_list):
        anchor = news.find("a", href=True)
        if anchor is None:
            continue

        news_url = anchor["href"]
        if news_url in existing_guids:
            continue

        news_title = anchor.get_text(strip=True)
        time_node = news.find("span")
        publish_text = time_node.get_text(strip=True) if time_node is not None else ""

        # 每经详情页当前访问经常超时，这里退回为列表页标题内容，保证 feed 稳定产出。
        news_detail = f"<p>{news_title}</p><p>列表时间：{publish_text or '未知时间'}</p>"
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
