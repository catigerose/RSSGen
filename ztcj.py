# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:27:11 2022

@author: catig
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 22:18:53 2022

@author: catig
"""

from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup_static, gen_rssitems, get_rss_path

import time


# 该函数获取详情页的新闻内容
# 该函数获取详情页的新闻内容
def get_text(news_link):
    detail_soup = get_soup_static(news_link)  # 构建beautifulsoup实例
    if detail_soup.find("div", class_="news-body-content"):
        news_detail = detail_soup.find("div", class_="news-body-content").decode()
    else:
        news_detail = detail_soup.body.decode()
    # news_detail = detail_soup.find("div", class_="g-article").decode()
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())

    rss_title = "要闻-智通财经"  # rss的标题，会显示再rss阅读中
    rss_description = "智通财经网，连线全球资本市场，提供最及时的全球财经市场资讯，覆盖港股、美股、A股的资讯、行情、数据、H股，港股公司，香港股市，恒生指数，国企指数，港股开户，蓝筹股，红筹股，AH， 窝轮等"  # rss的描述
    rss_path = rss_dir + "/feeds/" + "ztcj.xml"  # 生成的RSS存放位置
    url = 'https://www.zhitongcaijing.com/?index=yaowen'  # 要爬取的页面
    soup = get_soup_static(url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find(
        "div", class_="home-list-scroll").find_all("div", class_="info-item-content")

    for news in news_list:
        news_link ="https://www.zhitongcaijing.com"+ news.div.a.attrs['href']  # 详情页的url
        news_title = news.div.a.span.get_text()  # 新闻的标题
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
    rss.write_xml(open(rss_path, "w", encoding='UTF-8'),encoding='UTF-8')
