#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import PyRSS2Gen
import requests
import time
from bs4 import BeautifulSoup
from datetime import date


# # 1. 获取今天的日期（年，月，日） 

# In[14]:


today = date.today()


# In[15]:


year= today.year
month =today.month 
day= today.day
weekday =today.weekday()


# In[16]:


str_today = '{}-{}/{}'.format(year, month, day)#拼接成url需要的格式
str_today


# # 2.生成要爬取的url组

# In[17]:


domain = "http://paper.people.com.cn/rmrb/html/"+str_today +"/nbs.D110000renmrb_"  #url前面公用的域名


# In[18]:


spaces1 = ["01.htm","02.htm","03.htm","04.htm","05.htm","06.htm","07.htm","08.htm","09.htm","10.htm","14.htm","17.htm"] #工作日新闻版面类别
spaces2 = ["01.htm","02.htm","03.htm","04.htm","05.htm"] #周末新闻版面类别

if weekday in [5,6]:
    spaces = spaces2 
else:
    spaces = spaces21

urls =[]

for space in spaces:    
   urls.append(domain + space) 


# In[19]:


urls


# # 3. 爬取版面内的新闻

# In[7]:


#请求头
headers = { "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}


# In[8]:


domain2 = "http://paper.people.com.cn/rmrb/html/2022-11/11/"  #详情页的域名


# In[9]:


#获取详情页的新闻内容
def get_text(news_link):
    detialHtml=requests.get(news_link,headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding 
    return detialHtml.text


# In[10]:


#新闻标题、详情页、新闻内容链接 存入数组中
news_links = []
news_titles=[]
news_details = []
for url in urls:
    ret = requests.get(url,headers=headers)
    ret.encoding = ret.apparent_encoding 
    time.sleep(1)    
    soup = BeautifulSoup(ret.text, 'html.parser') # 构建beautifulsoup实例
    
    news_list = soup.find("ul", class_="news-list").find_all ("a")#获取新闻列表
    
    for news in  news_list:
        news_link = domain2 + news.attrs['href']   #详情页的url        
        news_title = news.get_text()  #新闻的标题
        news_detail = get_text(news_link)
        
        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)


# # 4.生成RSS的xml文件

# In[14]:


#该函数使用新闻的标题、链接、新闻内容，生成 PyRSS2Gen.RSS2函数所需要的参数 items
def gen_rssitems(news_titles,news_links,news_details):
    pubDate_now =datetime.datetime.now()
    rssitems=[]
    
    for i in range(len(news_titles)):
        rssitem = PyRSS2Gen.RSSItem(
         title = news_titles[i],
         link = news_links[i],

         #description = news_details[i],
         description = news_titles[i],
         pubDate =pubDate_now)
        
        rssitems.append(rssitem)
    return rssitems
        


# In[ ]:


if __name__ == '__main__':
    rss = PyRSS2Gen.RSS2(
    title = "feed of renmrb",
    link = "http://paper.people.com.cn/",
    description = " everyday's news of renmrb ",


    lastBuildDate = datetime.datetime.now(),

    items =gen_rssitems(news_titles,news_links,news_details))
    rss.write_xml(open("renmrb.xml", "w",encoding='UTF-16'))
    

