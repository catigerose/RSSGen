
from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':



    # 该部分变量每个feed均不同，且必须填写。
    feed_name = "wallstreetcn_live.xml"  # feed xml文件的的名字
    website_url = 'https://wallstreetcn.com/live/global'  # 要爬取的页面，也是feed的link
    feed_title = "华尔街见闻-快讯"  # feed的标题，会显示在feed阅读器中
    feed_description = "华尔街见闻实时新闻，7*24金融资讯，不仅更快还要你懂，华尔街，财经数据，24小时资讯，7x24快讯，财经资讯，市场直播，黄金，黄金价格，原油，外汇，A股，美股，商品，股市"  # feed的描述  
    
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(  feed_path)
    new_nums = 0
    old_nums = len(guids)
    
    # 该部分为爬虫模块，不同feed一般不一样 
    soup = get_soup(website_url,is_dynamic=True)  # 网页的内容，返回bs4的soup文件   
    news_list = soup.find_all("div", class_="live-item") # 找到或精确 items位置  ，避免抓到其它版面内容
    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news.a.attrs['href']  # 详情页的url
        guid = news_url
        try:
            news_detail = news.div.div.p.get_text()
        except:
            news_detail = news.div.div.get_text()

        news_title = news_detail  # 新闻的标题

        if guid not in guids:
            try:
                news_detail = news.div.div.p.get_text()
            except:
                news_detail = news.div.div.get_text()

            news_title = news_detail  # 新闻的标题
            new_nums += 1
            titles.append(news_title)
            contents.append(news_detail)
            links.append(news_url)
            guids.append(guid)
            updateds.append(datetime.now(tz))
            publisheds.append(datetime.now(tz))
    truc = min(old_nums,new_nums) # 保证不漏掉新的内容，没有feed文件则新的全部写入，及限制entry数目
    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles
    fg = gen_fg(website_url, feed_title, feed_description, feed_url, 
                titles, 
                contents,
                links,
                guids,
                updateds,
                publisheds,
                truc)
    fg.atom_file(feed_path)  # Write the ATOM feed to a file