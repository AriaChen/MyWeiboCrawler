# MyWeiboCrawler
PC 端的微博是 Ajax 动态加载，难于操作。这里爬取[新浪微博移动端](https://weibo.cn/)，简单很多。

### 参考代码：
* [用Python写一个简单的微博爬虫](http://python.jobbole.com/84349/)
* [Python 爬虫爬取指定用户微博图片及内容，并进行微博分类及使用习惯分析，生成可视化图表](http://www.cnblogs.com/dmyu/p/6034634.html)

### 环境：
* Python 3.5
* 系统：Windows
* 依赖库：re, os, sys, codecs, time, urllib, bs4, requests, lxml

### 需替换的部分：
* **user_id**：用户主页URL中数字
* **cookie**：
	* Chrome 浏览器中：
		* 打开https://weibo.cn/
		* F12，选 Network 栏，勾上 Preserve log
		* 登录微博
		* 找到m.weibo.cn->Headers->Cookie

	cookie有效期大约为一天，**随时可能更新。**

	遇“index out of range”报错，需查看cookie设置。

* **如只需原创微博内容**,将代码中 'https://weibo.cn/%d/profile?page=%d' 改为 'https://weibo.cn/u/%d?filter=1&page=%d'


## 注意：使用爬虫有封号风险。
* 可注册小号登录获取 cookie 并运行程序
* 可自行修改 sleep 时间
