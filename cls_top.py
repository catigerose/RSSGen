from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems, get_rss_path


# 该函数获取详情页的新闻内容



# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
    is_ajax = True  # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置

    rss_title = "财联社-头条"  # rss的标题，会显示再rss阅读中
    rss_description = "财联社深度：重大政策事件及时分析解读。提供准确、快速、权威、专业的事件分析，涵盖新能源汽车、创业板、cpi、供给侧改革等板块，想了解更多财经新闻、股市行情请登陆财联社。"  # rss的描述
    rss_path = rss_dir + "/feeds/" + "cls_top.xml"  # 生成的RSS存放位置
    url = 'https://www.cls.cn/depth?id=1000'  # 要爬取的页面
    soup = get_soup(url, is_ajax, chromedriver_path)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find_all(
        "div", class_="clearfix b-c-e6e7ea subject-interest-list")  # 找到或精确 items位置
    #print(news_list )
    for news in news_list:
        news_link = "https://www.cls.cn"+news.a.attrs['href']  # 详情页的url
        news_title = news.div.div.a.get_text()  # 新闻的标题
        news_detail = news_title

        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)
    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems(news_titles, news_links, news_details))
    rss.write_xml(open(rss_path, "w", encoding='UTF-16'))
