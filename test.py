

import requests
import time
from bs4 import BeautifulSoup








feed_title = "日经中文网"  # feed的标题，会显示在feed阅读器中
feed_description = "日经中文网官方网站。日经中文网是日本经济新闻社的中文财经网站。提供日本、中国、欧美财经金融信息、商务、企业、高科技报道、评论和专栏。"  # feed的描述
feed_name = "nikkei.xml"  # feed xml文件的的名字
url = 'https://cn.nikkei.com'  # 要爬取的页面



        # 请求头
headers = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", 
    "referer": "https://cn.nikkei.com/"}


ret = requests.get(url, headers=headers)
print(ret.status_code)
print(ret.headers)
ret.encoding = ret.apparent_encoding
time.sleep(1)
soup = BeautifulSoup(ret.text, 'html.parser')  # 构建beautifulsoup实例
soup
