from urllib.parse import urljoin

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_title = "中国宏观经济论坛（CMF）"
    feed_description = "中国人民大学中国宏观经济论坛（CMF）内容聚合。"
    feed_name = "cmf.xml"
    website_url = "http://ier.ruc.edu.cn/index.htm"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url)
    news_container = soup.find("ul", class_="news_content")
    news_list = news_container.find_all("li") if news_container is not None else []

    for news in reversed(news_list):
        anchor = news.find_all("a")[-1]
        news_url = urljoin(website_url, anchor["href"])
        if news_url in existing_guids:
            continue

        news_title = anchor.get_text(strip=True)
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
