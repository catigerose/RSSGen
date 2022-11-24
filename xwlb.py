# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 01:27:11 2022

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
    detail_soup = get_soup_static(news_link) # 构建beautifulsoup实例  
    if detail_soup.find("div", class_="content_area"):
        news_detail = detail_soup.find("div", class_="content_area").decode()
    else:   
        news_detail = detail_soup.body.decode()
    #news_detail = detail_soup.find("div", class_="g-article").decode()   
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail

# # 4.生成RSS的xml文件
if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
   


    rss_title = "新闻联播"  # rss的标题，会显示再rss阅读中
    rss_description = "《新闻联播》是中国中央电视台每日晚间播出的一档新闻节目，被称为“中国政坛的风向标”，节目宗旨为“宣传党和政府的声音，传播天下大事”。"  # rss的描述
    rss_path = rss_dir + "/feeds/" + "xwlb.xml"  # 生成的RSS存放位置
    url = 'http://tv.cctv.com/lm/xwlb/'  # 要爬取的页面
    soup = get_soup_static(url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find("div",class_="column_wrapper").find("ul",class_="rililist newsList").find_all("li")
    

    for news in news_list[1:]:
        news_link = news.a.attrs['href']  # 详情页的url
        news_title = news.a.attrs['title']# 新闻的标题
        news_detail= get_text(news_link)

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
