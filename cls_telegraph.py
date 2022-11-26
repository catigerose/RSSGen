#!/usr/bin/env python
# coding: utf-8
from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems_live, get_rss_path


# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
    is_ajax = True  # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置

    rss_path = rss_dir + "/feeds/" + "cls_telegraph.xml"  # 生成的RSS存放位置
    url = 'https://www.cls.cn/telegraph'  # 要爬取的页面
    rss_title = "财联社电报"  # rss的标题，会显示再rss阅读中
    rss_description = "财联社电报中心，A股24小时电报。为投资者提供专业的上市公司动态、股市资讯、股票行情、财经新闻、今日股市行情、创业板、新能源汽车、板块投资资讯。"  # rss的描述

    soup = get_soup(url, is_ajax, chromedriver_path)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    #print(soup.prettify())
    news_list = soup.find_all("div", class_="clearfix p-r l-h-26p")

    for news in news_list:
        news=news.find_all("span")[1].div
        
        news_link = url  # 详情页的url
        news_detail = news.get_text()
        
        if news.strong :
            news_title = news.strong.get_text()
        else:
            news_title = news_detail # 新闻的标题

        

        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)
    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems_live(news_titles, news_links, news_details))
    rss.write_xml(open(rss_path, "w", encoding='UTF-8'),encoding='UTF-8')
