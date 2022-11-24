#!/usr/bin/env python
# coding: utf-8
from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems, get_rss_path


# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
    is_ajax = True  # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置

    rss_path = rss_dir + "/feeds/" + "futunn_live.xml"  # 生成的RSS存放位置
    url = 'https://news.futunn.com/main/live?lang=zh-cn'  # 要爬取的页面
    rss_title = "富途牛牛-直播"  # rss的标题，会显示再rss阅读中
    rss_description = "7×24小时全球实时财经新闻快讯 - 富途牛牛"  # rss的描述

    soup = get_soup(url, is_ajax, chromedriver_path)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("li", style="cursor: pointer;")
    for news in news_list:
        news_link = url  # 详情页的url
        news_detail = news.p.decode()  +"   "+news.span.decode()  

        if news.h3.get_text() == '':
            news_title = news.p.get_text()
        else:
            news_title = news.h3.get_text()  # 新闻的标题

        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)
    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems(news_titles, news_links, news_details))
    rss.write_xml(open(rss_path, "w", encoding='UTF-8'),encoding='UTF-8')
