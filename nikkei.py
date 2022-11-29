# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 17:33:51 2022

@author: catig
"""

from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir

# 该函数获取详情页的新闻内容
def get_content(news_url):
    soup = get_soup(website_url+news_url)
    content = soup.find("div","newsText fix").decode()
    if soup.find("div","pagenavbar"):
        othter_pages = soup.find("div","pagenavbar").find_all("span")[1:-1]
        for page in othter_pages:
            next_soup = get_soup(website_url+page.a.attrs['href'])
            next_content=next_soup.find("div","newsText fix").decode()
            content +=next_content

 
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return content


if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []
    feed_title = "日经中文网"  # feed的标题，会显示在feed阅读器中
    feed_description = "日经中文网官方网站。日经中文网是日本经济新闻社的中文财经网站。提供日本、中国、欧美财经金融信息、商务、企业、高科技报道、评论和专栏。"  # feed的描述
    feed_name = "nikkei.xml"  # feed xml文件的的名字
    website_url = 'https://cn.nikkei.com'  # 要爬取的页面
    
    
    soup = get_soup(website_url)
    soup = soup.find("div",class_="column-2 mainContent")   #左侧新闻
    
    news_list =[]  #用于汇集所有新闻
    
    news_list.append(soup.find("div",class_="indexTopNews fix mB5").find("dt")) #top news第一个新闻
    
    top_news = soup.find("div",class_="indexTopNews fix mB5").find("ul").find_all("li")   
    news_list.extend(top_news) #top news
    
    focus = soup.find("div",class_="fix pR15").find("div",class_="column-1 frt").find_all("dl",class_="newsContent01")[0].find_all("dt")
    news_list.extend(focus)  #聚焦板块
    
    column = soup.find("div",class_="fix pR15").find("div",class_="column-1 frt").find_all("dl",class_="newsContent01")[1].find_all("dt")
    news_list.extend(column)  #专栏板块
    
    
    for news in news_list:
        news_url = news.a.attrs['href']  # 详情页的url
        news_title = news.a.get_text()  # 新闻的标题
        news_detail = get_content(news_url)

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
        fg.atom_file(feeds_dir + feed_name)  # Write the ATOM feed to a file
    else:
        fg.rss_file(feeds_dir + feed_name)  # Write the RSS feed to a file