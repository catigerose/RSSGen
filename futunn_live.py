
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir


if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    feed_name = "futunn_live.xml"  # feed xml文件的的名字
    website_url = 'https://news.futunn.com/main/live?lang=zh-cn'  # 要爬取的页面
    feed_title = "富途牛牛-直播"  # feed的标题，会显示在feed阅读器中
    feed_description = "7×24小时全球实时财经新闻快讯 - 富途牛牛"  # feed的描述

    soup = get_soup(website_url,1)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("li", style="cursor: pointer;")
    for news in news_list:
        news_url = website_url  # 详情页的url
        news_detail = news.p.decode()  +"   "+news.span.decode()  

        if news.h3.get_text() == '':
            news_title = news.p.get_text()
        else:
            news_title = news.h3.get_text()  # 新闻的标题

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
        guids=news_titles)     
    
    use_atom = 0
    if use_atom:
        fg.atom_file(feeds_dir+ feed_name)  # Write the ATOM feed to a file
    else:
        fg.rss_file(feeds_dir+ feed_name)  # Write the RSS feed to a file

