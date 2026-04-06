from datetime import datetime

from feed_funcs import (
    FEEDS_DIR,
    SHANGHAI_TZ,
    append_entry,
    get_entries,
    get_json,
    persist_feed,
)


def run():
    feed_name = "futunn_live.xml"
    website_url = "https://news.futunn.com/main/live?lang=zh-cn/"
    feed_title = "富途牛牛快讯"
    feed_description = "7x24 小时全球实时财经新闻快讯。"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    api_url = "https://news.futunn.com/news-site-api/main/get-flash-list?pageSize=30"
    response = get_json(api_url)
    news_list = response["data"]["data"]["news"]

    for news in reversed(news_list):
        news_url = f"https://news.futunn.com/flash/{news['id']}"
        if news_url in existing_guids:
            continue

        news_detail = news["content"]
        news_title = news["title"] or news_detail
        publish_time = datetime.fromtimestamp(int(news["time"]), SHANGHAI_TZ)
        append_entry(
            entries,
            title=news_title,
            content=news_detail,
            link=news_url,
            updated=publish_time,
            published=publish_time,
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
