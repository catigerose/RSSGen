from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_title = "华尔街见闻最新资讯"
    feed_description = "华尔街见闻全球快讯与新闻聚合。"
    feed_name = "wallstreet_news.xml"
    website_url = "https://wallstreetcn.com/news/global"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    page_soup = get_soup(website_url, is_dynamic=True, sleep_seconds=3)
    article_list = page_soup.find("div", class_="article-list")
    news_list = []
    if article_list is not None:
        news_list = article_list.find_all("div", class_="article-entry list-item")

    for news in reversed(news_list):
        title_link = news.find("a", class_="article-link title")
        if title_link is None:
            continue

        news_url = title_link["href"]
        if news_url in existing_guids:
            continue

        news_title = title_link.get_text(strip=True)
        summary_node = news.find("div", class_="content")
        author_node = news.find("div", class_="author")
        time_node = news.find("time", class_="time")

        summary_text = summary_node.get_text(" ", strip=True) if summary_node is not None else ""
        author_text = author_node.get_text(strip=True) if author_node is not None else ""
        time_text = time_node.get_text(strip=True) if time_node is not None else ""

        # 列表页已经有标题、摘要、作者和时间，直接使用它们可避免逐篇详情页拉取过慢。
        news_detail = (
            f"<p>{summary_text or news_title}</p>"
            f"<p>作者：{author_text or '未知作者'}</p>"
            f"<p>时间：{time_text or '未知时间'}</p>"
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
