
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir

def get_content(news_url):
    detail_soup = get_soup(news_url)  # 构建beautifulsoup实例
    if detail_soup.find("div","main clearfix"):
        news_detail = detail_soup.find("div","main clearfix").decode()
    else:
        news_detail=detail_soup.body.decode()
    # news_detail = detail_soup.find("div", class_="g-article").decode()
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    feed_title = "新华网_要闻"  # feed的标题，会显示在feed阅读器中
    feed_description = "中国主要重点新闻网站,依托新华社遍布全球的采编网络,记者遍布世界100多个国家和地区,地方频道分布全国31个省市自治区,每天24小时同时使用6种语言滚动发稿,权威、准确、及时播发国内外重要新闻和重大突发事件,受众覆盖200多个国家和地区,发展论坛是全球知名的中文论坛。"  # rss的描述
    feed_name = "xinhua_focus.xml"  # feed xml文件的的名字
    website_url = 'http://www.xinhuanet.com/'  # 要爬取的页面
    soup = get_soup(website_url)  # 网页的内容，返回bs4的soup文件

    news_list = soup.find(
        "div", id="focusListNews").find_all("li")

    for news in news_list:
        news_url = news.span.a.attrs['href']  # 详情页的url
        
        news_title = news.span.get_text()  # 新闻的标题
        news_detail = get_content(news_url)

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
        fg.rss_file(feeds_dir+ feed_name)  # Write the RSS feed to a file

