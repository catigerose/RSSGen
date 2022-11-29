
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url,feeds_dir

if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    feed_name = "cls_telegraph.xml"  # feed xml文件的的名字
    website_url = 'https://www.cls.cn/telegraph'  # 要爬取的页面
    feed_title = "财联社电报"  # feed的标题，会显示在feed阅读器中
    feed_description = "财联社电报中心，A股24小时电报。为投资者提供专业的上市公司动态、股市资讯、股票行情、财经新闻、今日股市行情、创业板、新能源汽车、板块投资资讯。"  # feed的描述


    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件
    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("div", class_="clearfix p-r l-h-26p")
    for news in news_list:
        news=news.find_all("span")[1].div
        
        news_url = website_url  # 详情页的url
        news_detail = news.get_text()
        
        if news.strong :
            news_title = news.strong.get_text()
        else:
            news_title = news_detail # 新闻的标题

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

    if use_atom:
        fg.atom_file(feeds_dir+ feed_name)  # Write the ATOM feed to a file
    else:
        fg.rss_file(feeds_dir+ feed_name)  # Write the RSS feed to a file        


