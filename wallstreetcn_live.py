#!/usr/bin/env python
# coding: utf-8
from PyRSS2Gen import RSS2
from datetime import datetime
from platform import system
from rss_funcs import get_soup, gen_rssitems, get_rss_path


if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_links = []
    news_titles = []
    news_details = []
    rss_dir = get_rss_path(system())
    is_ajax = True  # 是否为动态页面。对于静态网站：True时也能正常运行，但false会更快更省服务器资源。
    chromedriver_path = rss_dir+'/chromedriver'  # chromedriver的存放位置


rss_path = rss_dir + "/feeds/" + "wallstreetcn_live.xml"  # 生成的RSS存放位置
url = 'https://wallstreetcn.com/live/global'  # 要爬取的页面
rss_title = "华尔街见闻-快讯"  # rss的标题，会显示再rss阅读中
rss_description = "华尔街见闻实时新闻，7*24金融资讯，不仅更快还要你懂，华尔街，财经数据，24小时资讯，7x24快讯，财经资讯，市场直播，黄金，黄金价格，原油，外汇，A股，美股，商品，股市"  # rss的描述


soup = get_soup(url, is_ajax, chromedriver_path)  # 网页的内容，返回bs4的soup文件


# 找到或精确 items位置  ，防止抓到其它版面内容
news_list = soup.find_all("div", class_="live-item")
for news in news_list:
    news_link = news.a.attrs['href']  # 详情页的url
    try:
        news_detail = news.div.div.p.get_text()
    except:
        news_detail = news.div.div.get_text()

    news_title = news_detail  # 新闻的标题

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
