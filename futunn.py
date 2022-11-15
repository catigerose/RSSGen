#!/usr/bin/env python
# coding: utf-8
from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup,gen_rssitems,get_rss_path
import requests
from bs4 import BeautifulSoup
import time


#该函数获取详情页的新闻内容
def get_text(news_link):
    headers = { "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",}
    detialHtml=requests.get(news_link,headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding 
    soup = BeautifulSoup(detialHtml.text, 'html.parser') # 构建beautifulsoup实例
    if soup.find("div", class_="main"):#获取新闻内容详情
        news_detail = soup.find("div", class_="main")
    else:        
        news_detail = soup.body #直接将详情页body做为新闻详情
        #news_detail = soup #直接将详情页body做为新闻详情

    time.sleep(1) #间隔时间防止反爬虫
    news_detail =news_detail.text #要转为文本，不然后面会报错
    return news_detail


# # 4.生成RSS的xml文件
if __name__ == '__main__':
    
    #新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles=[]
    news_details = []  
    rss_dir = get_rss_path(system())
    is_ajax = True    #是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'   #chromedriver的存放位置

    url = 'https://news.futunn.com/main?lang=zh-cn'  #要爬取的页面   
    rss_title = "富途牛牛要闻"  #rss的标题，会显示再rss阅读中
    rss_path =rss_dir+ "/feeds/"+      "futunn.xml" #生成的RSS存放位置
    rss_description="财经新闻_最新全球财经资讯报道 - 富途牛牛"  #rss的描述

    soup = get_soup(url,is_ajax,chromedriver_path) #网页的内容，返回bs4的soup文件    
    
    news_list= soup.find_all("li", class_="news-li") # 找到或精确 items位置  ，防止抓到其它版面内容  
  
    for news in news_list:
        news_link = news.a.attrs['href']    #详情页的url        
        news_title = news.a.div.h3.get_text()  #新闻的标题
        news_detail = get_text(news_link)       
        #news_detail = news_title 




        
        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)    
    rss = RSS2(
    title = rss_title,
    link = url,
    description = rss_description,
    lastBuildDate = datetime.now(),
    items =gen_rssitems(news_titles,news_links,news_details))
    rss.write_xml(open(rss_path, "w",encoding='UTF-16'))

