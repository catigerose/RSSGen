from feed_funcs import append_entry, feeds_dir, get_entrys, get_soup, persist_feed

ADVISER_CONFIGS = [
    (231729, "光大期货"),
    (273399, "中信建投期货"),
    (241263, "平安期货"),
    (241737, "长城证券期货"),
    (225389, "徽商期货"),
    (268767, "广州期货"),
    (263711, "华创期货"),
    (238420, "钱多多团队"),
    (215408, "南华期货"),
]


if __name__ == "__main__":
    for adviser_id, adviser_name in ADVISER_CONFIGS:
        website_url = f"http://t.10jqka.com.cn/circle/{adviser_id}/"
        feed_name = f"{adviser_id}.xml"
        feed_title = f"{adviser_name}-同花顺投顾"
        feed_description = f"{adviser_name}-同花顺投顾平台内容聚合。"

        feed_path = feeds_dir + feed_name
        titles, contents, links, guids, updateds, publisheds = get_entrys(feed_path)
        old_count = len(guids)
        new_count = 0

        soup = get_soup(website_url, is_dynamic=True)
        post_list = soup.find("ul", class_="postlist-ul")
        news_list = (
            post_list.find_all("li", class_="post-single clearfix")
            if post_list is not None
            else []
        )

        for item in reversed(news_list):
            anchor = item.find("a")
            if anchor is None:
                continue

            news_url = anchor["href"]
            if news_url in guids:
                continue

            title_node = anchor.find("div", class_="post-title")
            news_title = title_node.get_text(strip=True) if title_node else anchor.get_text(strip=True)
            append_entry(
                titles,
                contents,
                links,
                guids,
                updateds,
                publisheds,
                title=news_title,
                content=news_title,
                link=news_url,
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
