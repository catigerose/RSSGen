# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 22:18:53 2022

@author: catig
"""

from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup_static, gen_rssitems, get_chromedriver_feeds_path

import time


# 该函数获取详情页的新闻内容
# 该函数获取详情页的新闻内容
def get_text(news_link):
    detail_soup = get_soup_static(news_link)  # 构建beautifulsoup实例
    if detail_soup.find("div","main clearfix"):
        news_detail = detail_soup.find("div","main clearfix").decode()
    else:
        news_detail=detail_soup.body.decode()
    # news_detail = detail_soup.find("div", class_="g-article").decode()
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []

    chromedriver_path, feeds_dir = get_chromedriver_feeds_path(system())# chromedriver的存放位置

    rss_title = "新华网_要闻"  # rss的标题，会显示再rss阅读中
    rss_description = "中国主要重点新闻网站,依托新华社遍布全球的采编网络,记者遍布世界100多个国家和地区,地方频道分布全国31个省市自治区,每天24小时同时使用6种语言滚动发稿,权威、准确、及时播发国内外重要新闻和重大突发事件,受众覆盖200多个国家和地区,发展论坛是全球知名的中文论坛。"  # rss的描述
    feed_path = feeds_dir + "xinhua_focus.xml"  # 生成的RSS存放位置
    url = 'http://www.xinhuanet.com/'  # 要爬取的页面
    soup = get_soup_static(url)  # 网页的内容，返回bs4的soup文件

    news_list = soup.find(
        "div", id="focusListNews").find_all("li")

    for news in news_list:
        news_link = news.span.a.attrs['href']  # 详情页的url
        
        news_title = news.span.get_text()  # 新闻的标题
        news_detail = get_text(news_link)

        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)
    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems(news_titles, news_links, news_details))
    rss.write_xml(open(feed_path, "w", encoding='UTF-8'),encoding='UTF-8')
