
from datetime import datetime
from PyRSS2Gen import RSSItem
import requests
import time
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# # 获取页面的数据、静态、动态的 最终输出结果都是一个soup。


# 获取  ajax网页 的 内容
def get_soup_ajax(url, chromedriver_path):
    options = Options()  # 实例化一个chrome浏览器实例对象
    options.add_argument("headless")  # 不打开浏览器窗口 运行selenium
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--remote-debugging-port=9222")  # this

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    options.add_argument('--user-agent=%s' % user_agent)

    # 函数更新，使用service传参数，解决警告 DeprecationWarning: executable_path has been deprecated, please pass in a Service object
    s = Service(chromedriver_path)
    driver = Chrome(service=s, options=options)  # 新建driver
    driver.maximize_window()  # 最大化窗口

    driver.get(url)  # 获取页面内容
    time.sleep(5)  # 等待5s，等待加载完成

    page_source = driver.page_source  # 获取页面源码数据
    soup = BeautifulSoup(page_source, features="lxml")  # 用 BeautifulSoup解析
    driver.close()
    return soup


# 获取静态网页的内容
def get_soup_static(url):
    # 请求头
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }
    ret = requests.get(url, headers=headers)
    ret.encoding = ret.apparent_encoding
    time.sleep(1)
    soup = BeautifulSoup(ret.text, 'html.parser')  # 构建beautifulsoup实例
    return soup


# 获取 任何网页的内容，返回bs4的soup文件
def get_soup(url, is_ajax, chromedriver_path):
    if is_ajax:
        return get_soup_ajax(url, chromedriver_path)
    else:
        return get_soup_static(url)


# 该函数使用新闻的标题、链接、新闻内容，生成 PyRSS2Gen.RSS2函数所需要的参数 items
def gen_rssitems(news_titles, news_links, news_details):
    pubDate_now = datetime.now()
    rssitems = []

    for i in range(len(news_titles)):
        rssitem = RSSItem(
            title=news_titles[i],
            link=news_links[i],

            description=news_details[i],
            #description = news_titles[i],
            pubDate=pubDate_now)

        rssitems.append(rssitem)
    return rssitems

# 获取当前工作目录


def get_rss_path(platform_system):
    if platform_system == 'Linux':
        rss_path = "/home/rss"
    elif platform_system == 'Windows':
        rss_path = "."
    else:
        print("waring： platform.system is not linux or windows")
        rss_path = "."
    return rss_path
