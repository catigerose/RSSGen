from urllib.parse import urljoin

from feed_funcs import FEEDS_DIR, append_entry, get_entries, get_soup, persist_feed

WEBSITE_URL = "https://www.stats.gov.cn/sj/sjjd/"


def get_article_content(news_url, href):
    """修正正文中的相对图片路径，保证 RSS 阅读器可直接加载。"""
    detail_soup = get_soup(news_url)
    content_node = detail_soup.find("div", class_="mobile-news-content")
    if content_node is None:
        return detail_soup.body.decode() if detail_soup.body else ""

    base_url = urljoin(WEBSITE_URL, href.split("/")[1] + "/")
    return content_node.decode().replace('src="./', f'src="{base_url}')


def run():
    feed_title = "数据解读-国家统计局"
    feed_description = "国家统计局数据解读栏目聚合。"
    feed_name = "sjjd.xml"

    entries = get_entries(FEEDS_DIR / feed_name)
    existing_guids = {entry.guid for entry in entries}
    existing_entry_count = len(entries)
    added_entry_count = 0

    page_soup = get_soup(WEBSITE_URL, is_dynamic=True)
    list_node = page_soup.find("div", class_="list-content")
    news_list = list_node.find_all("li") if list_node is not None else []

    for news in reversed(news_list):
        href = news.a["href"]
        news_url = urljoin(WEBSITE_URL, href[2:])
        if news_url in existing_guids:
            continue

        news_title = news.a.get("title", "").strip()
        news_detail = get_article_content(news_url, href)
        append_entry(
            entries,
            title=news_title,
            content=news_detail,
            link=news_url,
        )
        existing_guids.add(news_url)
        added_entry_count += 1

    persist_feed(
        website_url=WEBSITE_URL,
        feed_title=feed_title,
        feed_description=feed_description,
        feed_name=feed_name,
        entries=entries,
        existing_entry_count=existing_entry_count,
        added_entry_count=added_entry_count,
    )


if __name__ == "__main__":
    run()
