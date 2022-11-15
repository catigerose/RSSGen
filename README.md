# gen_rss_py
使用python制作RSS订阅源
	RSS介绍：https://cyber.harvard.edu/rss/
	an acronym for Really Simple Syndication.RSS is a dialect of XML. All RSS files must conform to the XML 1.0 specification, as published on the World Wide Web Consortium (W3C) website.
	
	
	
	
	1. rss本质是一个xml文件，不但符合xml格式要求，另外需要满足RSS的协议要求。

	2. RSS订阅链接本质上是一个  RSS文件的 URI。一般通过搭建http服务器实现。

	3. RSS文件会改变其内容，客户端定时抓取，以实现“推送消息”的功能。

	4. RSS 生成器 的作用就是 修改、更新xml文件

	5. RSS服务器定时获取RSS的更新内容，并保存。 
该服务器可以是本地客户端、服务器提高商如inoreader，或自行搭建的RSS服务如tiny tiny rss。
云端的rss服务可以实现24小时抓取，其中tiny rss可自行设定更新时间，inoreader免费版无法定制更新时间，本地客户端如不24小时后台运行，可能会漏掉信息。

	6. RSS阅读器具有附加功能如全文阅读等  其可使用RSS服务商的api端口，其也可做本地RSS服务器，

无论是官方RSS，RSShub，https://politepol.com/en/ 、huginn、python ，其整体运行框架均是如此。![image](https://user-images.githubusercontent.com/67047102/201942566-96c7786a-69b3-4146-b81d-e8ce3fa6fa5b.png)
