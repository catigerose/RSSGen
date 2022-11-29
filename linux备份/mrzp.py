# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:54:08 2022

@author: catig
"""

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


# 该函数获取详情页的新闻内容
# 该函数获取详情页的新闻内容




from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup_static, gen_rssitems, get_rss_path
import time
def get_text(news_link):
    detail_soup = get_soup_static(news_link)  # 构建beautifulsoup实例
    news_detail = detail_soup.find("div", class_="news-body-content").decode()
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

    rss_title = "每日猪评"  # rss的标题，会显示再rss阅读中
    rss_description = "中国养猪网每日猪评页面提供每天的猪评信息,给养殖户最新最好的养猪信息。"  # rss的描述
    rss_path = rss_dir + "/feeds/" + "mrzp.xml"  # 生成的RSS存放位置
    url = 'https://zhujia.zhuwang.cc/zhuping.shtml'  # 要爬取的页面
    soup = get_soup_static(url)  # 网页的内容，返回bs4的soup文件

    news_list = soup.find(
        "div", class_="right news").find_all("div", class_="list")
    for news in news_list[:2]:
        news_link = news.find(
            "div", class_="morezp").a.attrs['href']  # 详情页的url
        news_title = news.h2.get_text()  # 新闻的标题
        news_detail = news.find("div", class_="f14 info").p.get_text()

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
