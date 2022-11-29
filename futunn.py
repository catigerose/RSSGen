
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir

# 该函数获取详情页的新闻内容
def get_content(news_url):

    detail_soup = get_soup(news_url)   # 构建beautifulsoup实例
    if detail_soup.find("div", id="content"):  # 获取新闻内容详情
        news_detail = detail_soup.find("div", id="content").decode()
    else:
        news_detail = detail_soup.body.decode()  # 直接将详情页body做为新闻详情

    if detail_soup.find("div", class_="ftEditor"):  # 获取新闻内容详情
        source = detail_soup.find("div", class_="ftEditor").get_text()
    else:
        source = "未显示来源"  # 直接将详情页body做为新闻详情
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail, source



if __name__ == '__main__':

    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    website_url = 'https://news.futunn.com/main?lang=zh-cn'  # 要爬取的页面
    feed_title = "富途牛牛要闻"  # feed的标题，会显示在feed阅读器中
    feed_name =  "futunn.xml"  # feed xml文件的的名字
    feed_description = "财经新闻_最新全球财经资讯报道 - 富途牛牛"  # feed的描述

    soup = get_soup(website_url,1)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("li", class_="news-li")

    # 40条即可，提高抓取频率，减少抓取数量
    for news in news_list[:40]:
        news_url = news.a.attrs['href']  # 详情页的url
        news_title = news.a.div.h3.get_text()  # 新闻的标题
        news_detail, source = get_content(news_url)

        # 过滤一些报道
        filter_strings = ["智通财经", "华尔街见闻", "格隆汇"]
        filter_results = []
        for str in filter_strings:
            filter_result = source.find(str) == -1
            filter_results.append(filter_result)

        if False in filter_results:
            pass
        else:

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

