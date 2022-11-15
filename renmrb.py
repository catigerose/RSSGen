#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
from rss_funcs import get_soup,gen_rssitems,get_rss_path
from PyRSS2Gen import RSS2
from platform import system











#该函数获取详情页的新闻内容
def get_text(news_link):
    headers = { "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}
    detialHtml=requests.get(news_link,headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding 
    soup = BeautifulSoup(detialHtml.text, 'html.parser') # 构建beautifulsoup实例
    news_detail = soup.find("div", class_="article")#获取新闻内容详情
    news_detail =news_detail.text
    return news_detail





        




if __name__ == '__main__':
    #新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles=[]
    news_details = []  
    rss_dir = get_rss_path(system())
    is_ajax = False    #是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'   #chromedriver的存放位置






    rss_title = "人民日报" #rss的标题，会显示再rss阅读中
    rss_description="人民日报每日重要新闻"  #rss的描述
    rss_path =rss_dir+ "/feeds/"+      "renmrb.xml" #生成的RSS存放位置
    url = "http://paper.people.com.cn/"  #要爬取的页面  


    # 1. 获取今天的日期（年，月，日） 
    today = date.today()
    year= today.year
    month =today.month 
    day= today.day
    weekday =today.weekday()#周末排版不一样
    str_today = '{}-{}/{}/'.format(year, month, day)#拼接成url需要的格式
    #str_today



    #2. 获取每个版面的链接
    domain = "http://paper.people.com.cn/rmrb/html/"+str_today  #url和新闻详情页 前面公用的域名
    spaces1 = ["01.htm","02.htm","03.htm","04.htm","05.htm","06.htm","07.htm","08.htm","09.htm","10.htm","14.htm","17.htm"] #工作日新闻版面类别
    spaces2 = ["01.htm","02.htm","03.htm","04.htm","05.htm"] #周末新闻版面类别
    if weekday in [5,6]:
        spaces = spaces2 
    else:
        spaces = spaces1
    urls =[]
    for space in spaces:    
       urls.append(domain+"nbs.D110000renmrb_"  + space) 



    #3. 获取新闻内容

    for url0 in urls:   

        soup = get_soup(url0,is_ajax,chromedriver_path) #网页的内容，返回bs4的soup文件
        news_list = soup.find("ul", class_="news-list").find_all ("a")#获取新闻列表
        for news in  news_list:
            news_link = domain + news.attrs['href']   #详情页的url        
            news_title = news.get_text()  #新闻的标题
            news_detail = get_text(news_link)

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






