# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 21:36:44 2022

@author: catig
"""


from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir,get_entrys,tz
from datetime import datetime

if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []
    
    # entry必须使用url作为唯一性的id，相同id entry rss阅读不会再抓取。
    #直播类网站可能没有url，使用detail生成hash制作伪url。
    from hashlib import md5
    hash_details = []

    feed_name = "futunn_live.xml"  # feed xml文件的的名字
    website_url = 'https://news.futunn.com/main/live?lang=zh-cn/'  # 要爬取的页面
    feed_title = "富途牛牛-直播"  # feed的标题，会显示在feed阅读器中
    feed_description = "7×24小时全球实时财经新闻快讯 - 富途牛牛"  # feed的描述
    
    titles,contents,links,guids,updateds,publisheds = get_entrys(feeds_dir+ feed_name)
    len(guids)
    soup = get_soup(website_url,1)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("li", style="cursor: pointer;")
    
    nums = 0

    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles   
    fg = gen_fg(
        website_url,
        feed_title,
        feed_description,
        feeds_url + feed_name,
        
        titles[nums:],
        contents[nums:],
        links[nums:],
        guids[nums:],
        updateds[nums:],
        publisheds[nums:])     
    

    if use_atom:
        fg.atom_file(feeds_dir+ feed_name)  # Write the ATOM feed to a file
    else:
        fg.rss_file(feeds_dir+ feed_name)  # Write the RSS feed to a file

