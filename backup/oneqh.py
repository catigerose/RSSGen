from urllib.parse import urljoin

from feed_funcs import append_entry, feeds_dir, get_entrys, get_soup, persist_feed


if __name__ == "__main__":
    feed_name = "1qh_live.xml"
    website_url = "https://www.1qh.cn/kx"
    feed_title = "一期货快讯"
    feed_description = "一期货快讯频道与期货市场实时资讯。"

    feed_path = feeds_dir + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(feed_path)
    old_count = len(guids)
    new_count = 0

    soup = get_soup(website_url, is_dynamic=True)
    content_node = soup.find("ul", id="kx-content")
    news_list = content_node.find_all("li") if content_node is not None else []

    for news in reversed(news_list):
        guid = news.get("id")
        if not guid or guid in guids:
            continue

        anchor = news.find("a")
        if anchor is None:
            continue

        news_url = urljoin(website_url, anchor["href"])
        news_detail = anchor.get_text(strip=True)
        append_entry(
            titles,
            contents,
            links,
            guids,
            updateds,
            publisheds,
            title=news_detail,
            content=news_detail,
            link=news_url,
            guid=guid,
        )
        new_count += 1

    persist_feed(
        website_url=website_url,
        feed_title=feed_title,
        feed_description=feed_description,
        feed_name=feed_name,
        titles=titles,
        contents=contents,
        links=links,
        guids=guids,
        updateds=updateds,
        publisheds=publisheds,
        old_count=old_count,
        new_count=new_count,
    )
