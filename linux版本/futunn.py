#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import PyRSS2Gen
import requests
import time
from bs4 import BeautifulSoup
#from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# # 获取页面的数据、静态、动态的 最终输出结果都是一个soup。

# In[2]:


# 获取  ajax网页 的 内容
def get_soup_ajax(url):        
    chrome_options = Options()#实例化一个chrome浏览器实例对象
    chrome_options.add_argument("headless") #不打开浏览器窗口 运行selenium
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--remote-debugging-port=9222")  # this

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    chrome_options.add_argument('--user-agent=%s' % user_agent)
    
    driver = webdriver.Chrome( executable_path=chromedriver_path, options=chrome_options)#新建driver
    driver.maximize_window() #最大化窗口
    
    driver.get(url) #获取页面内容
    #time.sleep(5)    #等待5s，等待加载完成
       
    page_source = driver.page_source #获取页面源码数据  
    soup = BeautifulSoup(page_source )  #用 BeautifulSoup解析
    driver.close()
    return soup


# In[3]:


#获取静态网页的内容
def get_soup_static(url):
    #请求头
    headers = { "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",}
    ret = requests.get(url,headers=headers)
    ret.encoding = ret.apparent_encoding 
    #time.sleep(1)    
    soup = BeautifulSoup(ret.text, 'html.parser') # 构建beautifulsoup实例
    return soup
    


# In[4]:


# 获取 任何网页的内容，返回bs4的soup文件 
def get_soup(url,is_ajax):
    if is_ajax:
        return get_soup_ajax(url)
    else:
        return get_soup_static(url)


# # 2. 获取详情页的内容做为rss的description，默认使用详情页html的body

# In[5]:


#该函数获取详情页的新闻内容
def get_text(news_link):
    headers = { "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",}
    detialHtml=requests.get(news_link,headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding 
    soup = BeautifulSoup(detialHtml.text, 'html.parser') # 构建beautifulsoup实例
    #news_detail = soup.find("div", class_="main")#获取新闻内容详情
    news_detail = soup.body #直接将详情页body做为新闻详情
    time.sleep(0.5) #间隔时间防止反爬虫
    news_detail =news_detail.text #要转为文本，不然后面会报错
    return news_detail


# # 4.生成RSS的xml文件

# In[6]:


#该函数使用新闻的标题、链接、新闻内容，生成 PyRSS2Gen.RSS2函数所需要的参数 items
def gen_rssitems(news_titles,news_links,news_details):
    pubDate_now =datetime.datetime.now()
    rssitems=[]
    
    for i in range(len(news_titles)):
        rssitem = PyRSS2Gen.RSSItem(
         title = news_titles[i],
         link = news_links[i],

         description = news_details[i],
         #description = news_titles[i],
         pubDate =pubDate_now)
        
        rssitems.append(rssitem)
    return rssitems
        


# In[7]:


if __name__ == '__main__':
    
    #新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles=[]
    news_details = []  
    
    ##############下面的变量 要根据要制作rss的网页进行修改###############################
    rss_path = "/home/futunn.xml" #生成的RSS存放位置    
    chromedriver_path='/root/chromedriver'   #chromedriver的存放位置

    url = 'https://news.futunn.com/main?lang=zh-cn'  #要爬取的页面
    is_ajax = True    #是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    
    rss_title = "富途牛牛-要闻"  #rss的标题，会显示再rss阅读中
    rss_description="财经新闻_最新全球财经资讯报道 - 富途牛牛"  #rss的描述
    soup = get_soup(url,is_ajax) #网页的内容，返回bs4的soup文件 
    
    
    news_list= soup.find_all("li", class_="news-li") # 找到或精确 items位置  ，防止抓到其它版面内容  
  
    for news in news_list:
        news_link = news.a.attrs['href']    #详情页的url        
        news_title = news.a.div.h3.get_text()  #新闻的标题
        news_detail = get_text(news_link)       
        

        ##############上面的变量 要根据要制作rss的网页进行修改###############################
        
        news_links.append(news_link)
        news_titles.append(news_title)
        news_details.append(news_detail)
    
    rss = PyRSS2Gen.RSS2(
    title = rss_title,
    link = url,
    description = rss_description,
    lastBuildDate = datetime.datetime.now(),
    items =gen_rssitems(news_titles,news_links,news_details))
    rss.write_xml(open(rss_path, "w",encoding='UTF-16'))

