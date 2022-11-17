# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 18:15:54 2022

@author: catig
"""

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
    is_ajax = True # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置

    
    rss_title = "经济新闻-英为财情"  # rss的标题，会显示再rss阅读中
    rss_description = "经济新闻_每日经济新闻快讯_英为财情Investing.com"  # rss的描述
    rss_path = rss_dir + "/feeds/" + "economy_investing.xml"  # 生成的RSS存放位置
    url = 'https://cn.investing.com/news/economy'  # 要爬取的页面
    soup = get_soup(url, is_ajax, chromedriver_path).find(
        "section", id="leftColumn")  # 网页的内容，返回bs4的soup文件
    news_list = soup.find_all(
        "article", class_="js-article-item articleItem")  # 找到或精确 items位置

    for news in news_list:
        news_link = "https://cn.investing.com"+news.a.attrs['href']  # 详情页的url
        news_title = news.div.get_text()  # 新闻的标题
        # print(news_title)
        #news_detail = get_soup(news_link,True, chromedriver_path).find("div", class_="WYSIWYG articlePage").decode()
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