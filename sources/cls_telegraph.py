from hashlib import md5

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed


def run():
    feed_name = "cls_telegraph.xml"
    website_url = "https://www.cls.cn/telegraph/"
    feed_title = "财联社电报"
    feed_description = "财联社电报中心，A股 24 小时电报与财经快讯。"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    soup = get_soup(website_url, is_dynamic=True)
    news_list = soup.find_all("div", class_="clearfix p-r l-h-26p")

    # 快讯没有稳定详情页时，用正文内容生成伪唯一链接。
    for news in reversed(news_list):
        content_wrapper = news.find_all("span")[1].div
        news_detail = content_wrapper.get_text(strip=True)
        guid = website_url + md5(news_detail.encode("utf-8")).hexdigest()
        if guid in existing_guids:
            continue

        strong_tag = content_wrapper.find("strong")
        news_title = strong_tag.get_text(strip=True) if strong_tag else news_detail
        append_entry(
            entries,
            title=news_title,
            content=news_detail,
            link=guid,
        )
        existing_guids.add(guid)
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
