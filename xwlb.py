import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rss_funcs import  gen_rssitems, get_rss_path
from PyRSS2Gen import RSS2
from platform import system


if __name__ == '__main__':
    
    
    
    
    rss_dir = get_rss_path(system())
    



    rss_title = "新闻联播文字版"  # rss的标题，会显示再rss阅读中
    rss_path = rss_dir + "/feeds/" + "xwlb.xml"  # 生成的RSS存放位置
    rss_description = "新闻联播文字版,央视新闻联播文字稿子,今天中央新闻联播直播完整版,中央电视台cctv新闻联播,新聞联播"  # rss的描述

    url = "https://cn.govopendata.com/xinwenlianbo/"
    
    headers = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                   }
    abstact_html = requests.get(url, headers=headers)
    abstact_html.encoding = abstact_html.apparent_encoding
    soup = BeautifulSoup(abstact_html.text, 'html.parser') 
    
    
    new1 = soup.find("table",class_="table table-bordered").find("tr").td
    
    latsest_news_url = "https://cn.govopendata.com"+new1.a.attrs['href'] 
    
    abstacts = new1.ul.decode()
    
    title = new1.a.get_text()
    
    
    detialHtml = requests.get(latsest_news_url, headers=headers)
    detialHtml.encoding = detialHtml.apparent_encoding
    soup = BeautifulSoup(detialHtml.text, 'html.parser') 
    
    
    detail = soup.find("div",class_="col-md-9 col-sm-12 heti").decode()
    
    news_links=[url,latsest_news_url]
    news_titles=[title,title ]
    news_details =[abstacts ,detail ]

    rss = RSS2(
        title=rss_title,
        link=url,
        description=rss_description,
        lastBuildDate=datetime.now(),
        items=gen_rssitems(news_titles, news_links, news_details))
    rss.write_xml(open(rss_path, "w", encoding='UTF-16'))

