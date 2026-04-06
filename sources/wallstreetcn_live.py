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
    feed_name = "wallstreetcn_live.xml"
    website_url = "https://wallstreetcn.com/live/global"
    feed_title = "华尔街见闻快讯"
    feed_description = "华尔街见闻实时新闻与 7x24 金融资讯。"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    api_url = (
        "https://api-one-wscn.awtmt.com/apiv1/content/lives?"
        "channel=global-channel&client=pc&limit=40&first_page=true&accept=live%2Cvip-live"
    )
    response = get_json(api_url)
    news_list = response["data"]["items"]

    for news in reversed(news_list):
        news_url = news["uri"]
        if news_url in existing_guids:
            continue

        news_detail = news["content_text"]
        news_title = news["title"] or news_detail
        publish_time = datetime.fromtimestamp(news["display_time"], SHANGHAI_TZ)
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
