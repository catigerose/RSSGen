from datetime import date, timedelta

import requests

from feed_funcs import (
    DEFAULT_HEADERS,
    FEEDS_DIR,
    append_entry,
    get_entries,
    get_soup,
    persist_feed,
)

WEEKDAY_SPACES = [
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
    "14.html",
    "17.html",
]
WEEKEND_SPACES = ["01.html", "02.html", "03.html", "04.html", "05.html"]
FILTER_STRINGS = ["责编", "图片报道", "广告"]


def resolve_latest_day():
    """优先抓取当天版面；若当天尚未发布，则回退到昨天。"""
    today = date.today()
    candidate_url = build_day_index_url(today)
    response = requests.get(candidate_url, headers=DEFAULT_HEADERS, timeout=10)
    return today if response.status_code != 404 else today - timedelta(days=1)


def build_day_index_url(target_day):
    return (
        "http://paper.people.com.cn/rmrb/pc/layout/"
        f"{target_day.year}{target_day.month:02d}/{target_day.day:02d}/node_01.html"
    )


def build_page_urls(target_day):
    """根据日期生成当日所有版面地址。"""
    day_prefix = f"{target_day.year}{target_day.month:02d}/{target_day.day:02d}/"
    domain = f"http://paper.people.com.cn/rmrb/pc/layout/{day_prefix}"
    spaces = WEEKEND_SPACES if target_day.weekday() in (5, 6) else WEEKDAY_SPACES
    return domain, [domain + "node_" + space for space in spaces]


def should_skip_title(title):
    """过滤广告、责编等不需要进入 RSS 的条目。"""
    return any(flag in title for flag in FILTER_STRINGS)


def run():
    feed_title = "人民日报"
    feed_description = "人民日报每日重点新闻。"
    feed_name = "renmrb.xml"
    website_url = "http://paper.people.com.cn/"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    latest_day = resolve_latest_day()
    domain, page_urls = build_page_urls(latest_day)

    for page_url in page_urls:
        soup = get_soup(page_url)
        news_container = soup.find("ul", class_="news-list")
        if news_container is None:
            continue

        for news in news_container.find_all("a"):
            news_title = news.get_text(strip=True)
            if not news_title or should_skip_title(news_title):
                continue

            news_url = domain + news["href"]
            if news_url in existing_guids:
                continue

            detail_soup = get_soup(news_url)
            article = detail_soup.find("div", class_="article")
            if article is None:
                continue

            append_entry(
                entries,
                title=news_title,
                content=article.decode(),
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
