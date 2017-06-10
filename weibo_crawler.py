# -*-coding:utf8-*-

import re
import os
import sys
import codecs
import time
import urllib.request
from bs4 import BeautifulSoup
import requests
from lxml import etree

# 请替换成所要爬取信息的用户ID（见其主页URL）
user_id = 2716993481

# 请替换成自己的cookie
cookie = {"Cookie": "_T_WM=e1327bcb2d98ce2b1bd56179829a82ae; ALF=1499650565; SCF=AqnG5_pouJElPcQk3T0RRkMM_l2eaShCPYhq6vh3fP48L5bjrpZ3IS66BEImcXQCwnWcy0wJWrqHjH151bMhklU.; SUB=_2A250Pz1WDeThGeRJ6lQY-S3Iwz2IHXVXwEMerDV6PUJbktBeLXP-kW1S9VKtMkRgUhSTy2R8nqd_meW0IQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yA5xZvo7QmK9BwG2nDZsa5JpX5o2p5NHD95QES02c1K.0ShnpWs4Dqcj.i--Ri-2piKyhi--Xi-zRiK.Xi--4iK.fi-isi--ci-82iKyh; SUHB=0h1YqCgy6xOWrA; SSOLoginState=1497058566"}
url = 'https://weibo.cn/%d/profile' % user_id

html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = ""
urllist_set = set()
word_count = 1
image_count = 1

print(pageNum, "页")
print('爬虫准备就绪...')
sys.stdout.flush()
step = 0

for page in range(1, pageNum+1):
    try:
        # 获取lxml页面
        url = 'https://weibo.cn/%d/profile?page=%d' % (user_id, page)
        lxml = requests.get(url, cookies=cookie).content

        # 文字爬取
        selector = etree.HTML(lxml)
        content = selector.xpath('//span[@class="ctt"]')
        for each in content:
            text = each.xpath('string(.)')
            text = "%d :" % word_count + text + "\n\n"
            result += text
            word_count += 1

        print(page, '页文字已爬下')
        sys.stdout.flush()

        # 图片爬取
        soup = BeautifulSoup(lxml, "lxml")
        urllist = soup.find_all('a', href=re.compile(r'^https://weibo.cn/mblog/oripic', re.I))
        urllist1 = soup.find_all('a', href=re.compile(r'^https://weibo.cn/mblog/picAll', re.I))
        for imgurl in urllist:
            imgurl['href'] = re.sub(r"amp;", '', imgurl['href'])
            urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
            image_count += 1
            for imgurl_all in urllist1:
                html_content = requests.get(imgurl_all['href'], cookies=cookie).content
                soup = BeautifulSoup(html_content, "lxml")
                urllist2 = soup.find_all('a', href=re.compile(r'^/mblog/oripic', re.I))
                for imgurl in urllist2:
                    imgurl['href'] = 'http://weibo.cn' + re.sub(r"amp;", '', imgurl['href'])
                    urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
                    image_count += 1
                image_count -= 1
        print(page, '页图片已爬下')
    except:
        print(page, 'oops，出错了')

    time.sleep(5)
    if page % 5 == 0:
        print(page, 'sleep')
        sys.stdout.flush()
        time.sleep(100)
        print('正在进行第', step + 1, u'次停顿，防止访问次数过多')

time.sleep(30)

# 请设置成自己的文件存储路径
path = "E:/写字的地方/weibo"
fo = codecs.open(path + "/Personals/%s.txt" % user_id, "w", "utf-8")
fo.write(result)
word_path = path + '/%d' % user_id
print('文字微博爬取完毕')

link = ""
fo2 = codecs.open(path + "/Personals/%s_imageurls.txt" % user_id, "w", "utf-8")
for eachlink in urllist_set:
    link = link + eachlink + "\n"
fo2.write(link)
print('图片链接爬取完毕')

if not urllist_set:
    print('该页面中不存在图片')
else:
    # 下载图片,保存在文件夹
    image_path = path + '/weibo_image'
    if os.path.exists(image_path) is False:
        os.mkdir(image_path)
    x = 1
    for imgurl in urllist_set:
        temp = image_path + '/%s.jpg' % x
        print(u'正在下载第%s张图片' % x)
        try:
            urllib.request.urlretrieve(urllib.request.urlopen(imgurl).geturl(), temp)
        except:
            print(u"该图片下载失败:%s" % imgurl)
        x += 1

print('微博文字爬取完毕，共%d条，保存路径%s' % (word_count, word_path))
print('微博图片爬取完毕，共%d张，保存路径%s' % (image_count - 1, image_path))