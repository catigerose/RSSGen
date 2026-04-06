from datetime import date, timedelta

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed

FILTER_STRINGS = ["责编", "图片报道", "广告", "图片新闻", "来稿邮箱", "公益", "邮箱"]
SPACES = [
    "01.html",
    "02.html",
    "03.html",
    "04.html",
    "05.html",
    "06.html",
    "07.html",
    "08.html",
    "09.html",
    "10.html",
    "11.html",
    "12.html",
]


def should_skip_title(title):
    return any(flag in title for flag in FILTER_STRINGS)


def run():
    feed_title = "经济日报"
    feed_description = "经济日报每日重要新闻。"
    feed_name = "jjrb.xml"
    website_url = "http://paper.ce.cn/pc/layout/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    target_day = date.today() - timedelta(days=1)
    day_prefix = f"{target_day.year}{target_day.month:02d}/{target_day.day:02d}/"
    domain = "http://paper.ce.cn/pc/layout/" + day_prefix
    page_urls = [domain + "node_" + space for space in SPACES]

    for page_url in page_urls:
        soup = get_soup(page_url)
        article_list = soup.find("ul", id="articlelist")
        if article_list is None:
            continue

        for news in article_list.find_all("a"):
            news_title = news.get_text(strip=True)
            if not news_title or should_skip_title(news_title):
                continue

            news_url = "http://paper.ce.cn/pc" + news["href"][8:]
            if news_url in existing_guids:
                continue

            detail_soup = get_soup(news_url)
            detail_node = detail_soup.find("div", class_="detail-art")
            if detail_node is None:
                continue

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
