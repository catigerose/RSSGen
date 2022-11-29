from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir


def get_text(news_url):
    detail_soup = get_soup(news_url)  # 构建beautifulsoup实例
    if detail_soup.find("div", class_="news-body-content"):
        news_detail = detail_soup.find(
            "div", class_="news-body-content").decode()
    else:
        news_detail = detail_soup.body.decode()
    # news_detail = detail_soup.find("div", class_="g-article").decode()
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []

    feed_title = "要闻-智通财经"  # feed的标题，会显示在feed阅读器中
    feed_description = "智通财经网，连线全球资本市场，提供最及时的全球财经市场资讯，覆盖港股、美股、A股的资讯、行情、数据、H股，港股公司，香港股市，恒生指数，国企指数，港股开户，蓝筹股，红筹股，AH， 窝轮等"  # rss的描述
    feed_name = "ztcj.xml"  # feed xml文件的的名字
    website_url = 'https://www.zhitongcaijing.com/?index=yaowen'  # 要爬取的页面
    soup = get_soup(website_url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find(
        "div", class_="home-list-scroll").find_all("div", class_="info-item-content")

    for news in news_list:
        news_url = "https://www.zhitongcaijing.com" + \
            news.div.a.attrs['href']  # 详情页的url
        news_title = news.div.a.span.get_text()  # 新闻的标题
        news_detail = get_text(news_url)

        news_urls.append(news_url)
        news_titles.append(news_title)
        news_details.append(news_detail)
    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles
    fg = gen_fg(
        website_url,
        feed_title,
        feed_description,
        news_urls,
        news_titles,
        news_details,
        feed_url=feeds_url + feed_name,
        guids="news_urls")

    if use_atom:
        fg.atom_file(feeds_dir + feed_name)  # Write the ATOM feed to a file
    else:
        fg.feed_file(feeds_dir + feed_name)  # Write the RSS feed to a file
