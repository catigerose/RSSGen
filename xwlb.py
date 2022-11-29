#!/usr/bin/env python
# coding: utf-8

from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url,feeds_dir

def get_content(news_url):
    detail_soup = get_soup(news_url) # 构建beautifulsoup实例  
    if detail_soup.find("div", class_="content_area"):
        news_detail = detail_soup.find("div", class_="content_area").decode()
    else:   
        news_detail = detail_soup.body.decode()
    #news_detail = detail_soup.find("div", class_="g-article").decode()      
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail

if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []
   

    # 该部分变量每个feed均不同，且必须填写。
    feed_name = "xwlb.xml"  # feed xml文件的的名字
    website_url = 'http://tv.cctv.com/lm/xwlb/'  # 要爬取的页面，也是feed的link       
    feed_title = "新闻联播"  # rss的标题，会显示再rss阅读中
    feed_description = "《新闻联播》是中国中央电视台每日晚间播出的一档新闻节目，被称为“中国政坛的风向标”，节目宗旨为“宣传党和政府的声音，传播天下大事”。"  # rss的描述

     # 该部分为爬虫模块，不同feed一般不一样 
    soup = get_soup(website_url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find("div",class_="column_wrapper").find("ul",class_="rililist newsList").find_all("li")
    
    for news in news_list[1:]:
        news_url = news.a.attrs['href']  # 详情页的url
        news_title = news.a.attrs['title']# 新闻的标题
        news_detail= get_content(news_url)

 
        news_urls.append(news_url)
        news_titles.append(news_title)
        news_details.append(news_detail)   
        
    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles   
    fg = gen_fg(
        website_url,
        feed_title,
        feed_description,
        news_urls,
        news_titles,
        news_details,
        feed_url=feeds_url + feed_name,
        guids="news_urls")     

    if use_atom:
        fg.atom_file(feeds_dir+ feed_name)  # Write the ATOM feed to a file
    else:
        fg.rss_file(feeds_dir+ feed_name)  # Write the RSS feed to a file
