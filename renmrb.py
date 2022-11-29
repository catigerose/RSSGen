
from feed_funcs import use_atom,  get_soup, gen_fg, feeds_url, feeds_dir
from datetime import date

if __name__ == '__main__':
    # 新闻标题、详情页、新闻内容链接 存入数组中
    news_urls = []
    news_titles = []
    news_details = []


    feed_title = "人民日报"  # feed的标题，会显示在feed阅读器中
    feed_description = "人民日报每日重要新闻"  # feed的描述
    feed_name =   "renmrb.xml"  # feed xml文件的的名字
    website_url = "http://paper.people.com.cn/"  # 要爬取的页面
    


    # 1. 获取今天的日期（年，月，日）
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    weekday = today.weekday()  # 周末排版不一样
    str_today = '{}-{}/{}/'.format(year, month, day)  # 拼接成url需要的格式
    # str_today
    # 2. 获取每个版面的链接
    domain = "http://paper.people.com.cn/rmrb/html/"+str_today  # url和新闻详情页 前面公用的域名
    spaces1 = ["01.htm", "02.htm", "03.htm", "04.htm", "05.htm", "06.htm",
               "07.htm", "08.htm", "09.htm", "10.htm", "14.htm", "17.htm"]  # 工作日新闻版面类别
    spaces2 = ["01.htm", "02.htm", "03.htm", "04.htm", "05.htm"]  # 周末新闻版面类别
    if weekday in [5, 6]:
        spaces = spaces2
    else:
        spaces = spaces1
    urls = []
    for space in spaces:
        urls.append(domain+"nbs.D110000renmrb_" + space)
    # 3. 获取新闻内容
    for url0 in urls:
        
        
        
        

        soup = get_soup(url0, 1)  # 网页的内容，返回bs4的soup文件
        news_list = soup.find("ul", class_="news-list").find_all("a")  # 获取新闻列表
        for news in news_list:


            news_title = news.get_text()  # 新闻的标题
            
            # 过滤一些报道
            filter_strings =["责编","图片报道","广告"]
            filter_results=[]
            for str in filter_strings:
                filter_result=  news_title.find(str)==-1
                filter_results.append(filter_result)
                
        
            if False in filter_results :
                pass
            else:
                
                
                
                news_url = domain + news.attrs['href']  # 详情页的url
                news_detail = get_soup(news_url).find("div", class_="article").decode()  # 获取新闻内容详情             
    
                
    
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

