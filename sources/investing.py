from datetime import datetime

import feedparser

from feed_funcs import (
    FEEDS_DIR,
    SHANGHAI_TZ,
    append_entry,
    get_entries,
    persist_feed,
)

FEED_CONFIGS = [
    {
        "feed_title": "外汇新闻-英为财情",
        "feed_description": "外汇新闻快讯与实时资讯。",
        "feed_name": "forex_news.xml",
        "website_url": "https://cn.investing.com/news/forex-news",
        "rss_url": "https://cn.investing.com/rss/news_1.rss",
    },
    {
        "feed_title": "股市新闻-英为财情",
        "feed_description": "股市新闻与市场动态。",
        "feed_name": "stock_market_news.xml",
        "website_url": "https://cn.investing.com/news/stock-market-news",
        "rss_url": "https://cn.investing.com/rss/news_25.rss",
    },
    {
        "feed_title": "经济新闻-英为财情",
        "feed_description": "经济新闻与宏观资讯。",
        "feed_name": "economy_investing.xml",
        "website_url": "https://cn.investing.com/news/economy",
        "rss_url": "https://cn.investing.com/rss/news_14.rss",
    },
    {
        "feed_title": "全球宏观经济指标-英为财情",
        "feed_description": "宏观经济指标新闻与数据解读。",
        "feed_name": "economic_indicators.xml",
        "website_url": "https://cn.investing.com/news/economic-indicators",
        "rss_url": "https://cn.investing.com/rss/news_95.rss",
    },
    {
        "feed_title": "期货新闻-英为财情",
        "feed_description": "商品、股指、外汇期货资讯。",
        "feed_name": "commodities_news.xml",
        "website_url": "https://cn.investing.com/news/commodities-news",
        "rss_url": "https://cn.investing.com/rss/news_11.rss",
    },
]


def parse_entry_time(entry):
    """Investing 官方 RSS 提供的是无时区时间，这里统一按上海时区写入。"""
    published_parsed = getattr(entry, "published_parsed", None)
    if published_parsed is None:
        return datetime.now(SHANGHAI_TZ)
    return SHANGHAI_TZ.localize(datetime(*published_parsed[:6]))


def build_entry_content(entry):
    """官方 RSS 只提供标题和链接，因此正文退化为标题摘要。"""
    title = getattr(entry, "title", "").strip()
    link = getattr(entry, "link", "").strip()
    return f'<p>{title}</p><p><a href="{link}">{link}</a></p>'


def fetch_entries(rss_url):
    feed = feedparser.parse(rss_url)
    if getattr(feed, "bozo", False):
        raise ValueError(f"RSS 解析失败: {getattr(feed, 'bozo_exception', 'unknown error')}")
    return list(getattr(feed, "entries", []))


def run():
    for config in FEED_CONFIGS:
        feed_name = config["feed_name"]
        website_url = config["website_url"]
        entries = get_entries(FEEDS_DIR / feed_name)
        existing_guids = {entry.guid for entry in entries}
        existing_entry_count = len(entries)
        added_entry_count = 0

        news_entries = fetch_entries(config["rss_url"])
        for entry in reversed(news_entries):
            news_url = getattr(entry, "link", "").strip()
            if not news_url or news_url in existing_guids:
                continue

            news_title = getattr(entry, "title", "").strip() or news_url
            publish_time = parse_entry_time(entry)
            append_entry(
                entries,
                title=news_title,
                content=build_entry_content(entry),
                link=news_url,
                updated=publish_time,
                published=publish_time,
            )
            existing_guids.add(news_url)
            added_entry_count += 1

        persist_feed(
            website_url=website_url,
            feed_title=config["feed_title"],
            feed_description=config["feed_description"],
            feed_name=feed_name,
            entries=entries,
            existing_entry_count=existing_entry_count,
            added_entry_count=added_entry_count,
        )


if __name__ == "__main__":
    run()
