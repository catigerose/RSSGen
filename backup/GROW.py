from feed_funcs import append_entry, feeds_dir, get_entrys, get_soup, persist_feed


def get_article_content(news_url):
    detail_soup = get_soup(news_url, is_dynamic=True)
    content_node = detail_soup.find("ul", class_="wp-block-list")
    return content_node.decode() if content_node is not None else (
        detail_soup.body.decode() if detail_soup.body else ""
    )


if __name__ == "__main__":
    feed_title = "思睿中国策略研究"
    feed_description = "思睿投资中国策略研究栏目聚合。"
    feed_name = "GROW.xml"
    website_url = "https://grow-investment-group.com/category/%e4%b8%ad%e5%9b%bd%e7%ad%96%e7%95%a5%e7%a0%94%e7%a9%b6/"

    feed_path = feeds_dir + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(feed_path)
    old_count = len(guids)
    new_count = 0

    main_soup = get_soup(website_url, is_dynamic=True)
    main_node = main_soup.find("main")
    list_node = main_node.find("ul") if main_node is not None else None
    news_list = list_node.find_all("li") if list_node is not None else []

    for news in reversed(news_list):
        news_url = news.div.h3.a["href"]
        if news_url in guids:
            continue

        news_title = news.div.h3.a.get_text(strip=True)
        news_date = news.div.find("div", class_="wp-block-post-date").time.get_text(strip=True)
        news_detail = get_article_content(news_url) + "\n" + news_date
        append_entry(
            titles,
            contents,
            links,
            guids,
            updateds,
            publisheds,
            title=f"{news_title} {news_date}",
            content=news_detail,
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
