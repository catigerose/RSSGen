
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir



if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    
    feed_title = "外汇新闻-英为财情"  # feed的标题，会显示在feed阅读器中
    feed_description = "外汇新闻快讯_外汇实时新闻资讯网_英为财情Investing.com"  # feed的描述
    feed_name =  "forex_news.xml"  # feed xml文件的的名字
    website_url = 'https://cn.investing.com/news/forex-news'  # 要爬取的页面
    soup = get_soup(website_url,1).find(
        "section", id="leftColumn")  # 网页的内容，返回bs4的soup文件
    news_list = soup.find_all(
        "article", class_="js-article-item articleItem")  # 找到或精确 items位置

    for news in news_list:
        news_url = "https://cn.investing.com"+news.a.attrs['href']  # 详情页的url
        news_title = news.div.a.get_text()  # 新闻的标题
        # print(news_title)
        #news_detail = get_soup(news_url,True, chromedriver_path).find("div", class_="WYSIWYG articlePage").decode()
        news_detail = news.div.get_text()

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
         fg.atom_file(feeds_dir+ feed_name)  # Write the ATOM feed to a file
    else:
         fg.feed_file(feeds_dir+ feed_name)  # Write the RSS feed to a file

