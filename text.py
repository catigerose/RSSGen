from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems, get_rss_path
import requests
from bs4 import BeautifulSoup
import time


news_link="https://news.futunn.com/post/21486791?src=3&report_type=market&report_id=220581&futusource=news_headline_list&level=1&data_ticket=89ce2aa3f65f07b2066b3d37f6479e53"
headers = {
    "user_agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/105.0.0.0 Safari/537.36"), }
detialHtml = requests.get(news_link, headers=headers)
detialHtml.encoding = detialHtml.apparent_encoding
soup = BeautifulSoup(detialHtml.text, 'html.parser')  # 构建beautifulsoup实例


news_detail= soup.find("div", class_="main")



news_detail2 = soup.find("div", class_="main")

print(news_detail )




print("---------------------------------------------------------" )

print(news_detail2 )


print(news_detail2 ==news_detail)