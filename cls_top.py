

from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir

if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []

    feed_title = "财联社-头条"  # feed的标题，会显示在feed阅读器中
    feed_description = "财联社深度：重大政策事件及时分析解读。提供准确、快速、权威、专业的事件分析，涵盖新能源汽车、创业板、cpi、供给侧改革等板块，想了解更多财经新闻、股市行情请登陆财联社。"  # feed的描述
    feed_name = "cls_top.xml"  # feed xml文件的的名字
    website_url = 'https://www.cls.cn/depth?id=1000'  # 要爬取的页面
    
    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find_all(
        "div", class_="clearfix b-c-e6e7ea subject-interest-list")  # 找到或精确 items位置
  
    for news in news_list:
        news_url = "https://www.cls.cn"+news.a.attrs['href']  # 详情页的url
        news_title = news.div.div.a.get_text()  # 新闻的标题
        news_detail = news_title

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
        fg.rss_file(feeds_dir + feed_name)  # Write the RSS feed to a file
