from time import sleep

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def get_content(news_url):
    """抓取文章正文，并在必要时退回到 body。"""
    detail_soup = get_soup(news_url)
    content_node = detail_soup.find("div", class_="main clearfix")
    if content_node is not None:
        news_detail = content_node.decode()
    else:
        news_detail = detail_soup.body.decode() if detail_soup.body else ""

    # 给目标站点留一点间隔，减少连续请求造成的压力。
    sleep(0.5)
    return news_detail


def run():
    feed_title = "新华网要闻"
    feed_description = "新华网重点新闻聚合。"
    feed_name = "xinhua_focus.xml"
    website_url = "http://www.xinhuanet.com/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url)
    focus_list = soup.find("div", id="focusListNews")
    news_list = focus_list.find_all("li") if focus_list is not None else []

    # 前两个元素通常不是正文新闻，因此跳过。
    for news in reversed(news_list[2:]):
        anchor = news.find("a")
        if anchor is None:
            continue

        news_url = anchor["href"]
        if news_url in existing_guids:
            continue

        news_title = news.get_text(strip=True)
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
