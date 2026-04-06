from time import sleep

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def get_content(news_url):
    detail_soup = get_soup(news_url)
    content_node = detail_soup.find("div", id="content_area")
    news_detail = (
        content_node.decode() if content_node is not None else detail_soup.body.decode() if detail_soup.body else ""
    )
    sleep(0.5)
    return news_detail


def run():
    feed_name = "xwlb.xml"
    website_url = "http://tv.cctv.com/lm/xwlb/"
    feed_title = "新闻联播"
    feed_description = "央视《新闻联播》节目内容聚合。"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url, is_dynamic=True)
    list_node = soup.find("ul", id="content")
    news_list = list_node.find_all("li") if list_node is not None else []

    for news in reversed(news_list[1:]):
        news_url = news.a["href"]
        if news_url in existing_guids:
            continue

        news_title = news.a.get("title", "").strip()
        news_detail = get_content(news_url)
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
