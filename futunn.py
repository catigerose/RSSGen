#!/usr/bin/env python
# coding: utf-8
from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems, get_rss_path
import requests
from bs4 import BeautifulSoup
import time


# 该函数获取详情页的新闻内容
def get_text_source(news_link):
    headers = {
        "user_agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/105.0.0.0 Safari/537.36"), }
    detialHtml = requests.get(news_link, headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding
    detail_soup = BeautifulSoup(
        detialHtml.text, 'html.parser')  # 构建beautifulsoup实例
    if detail_soup.find("div", id="content"):  # 获取新闻内容详情
        news_detail = detail_soup.find("div", id="content").decode()
    else:
        news_detail = detail_soup.body.decode() # 直接将详情页body做为新闻详情

    if detail_soup.find("div", class_="ftEditor"):  # 获取新闻内容详情
        source = detail_soup.find("div", class_="ftEditor").get_text()
    else:
        source = "未显示来源"  # 直接将详情页body做为新闻详情

    time.sleep(1)  # 间隔时间防止反爬虫
    return news_detail, source


#  4.生成RSS的xml文件
if __name__ == '__main__':

    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
    is_ajax = True  # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置

    url = 'https://news.futunn.com/main?lang=zh-cn'  # 要爬取的页面
    rss_title = "富途牛牛要闻"  # rss的标题，会显示再rss阅读中
    rss_path = rss_dir + "/feeds/" + "futunn.xml"  # 生成的RSS存放位置
    rss_description = "财经新闻_最新全球财经资讯报道 - 富途牛牛"  # rss的描述

    soup = get_soup(url, is_ajax, chromedriver_path)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("li", class_="news-li")

    # 40条即可，提高抓取频率，减少抓取数量
    for news in news_list[:40]:
        news_link = news.a.attrs['href']  # 详情页的url
        news_title = news.a.div.h3.get_text()  # 新闻的标题
        news_detail, source = get_text_source(news_link)

        # 过滤一些报道
        filter_strings = ["智通财经", "华尔街见闻"]
        filter_results = []
        for str in filter_strings:
            filter_result = source.find(str) == -1
            filter_results.append(filter_result)

        if False in filter_results:
            pass
        else:

            news_links.append(news_link)
            news_titles.append(news_title)
            news_details.append(news_detail)
    # print(len(news_links))
    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems(news_titles, news_links, news_details))
    rss.write_xml(open(rss_path, "w", encoding='UTF-16'))
