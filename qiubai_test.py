#爬虫糗事百科
import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pymysql

start = time.clock()     #计时-开始
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect("localhost", "root", "111111", "python_test",charset="utf8")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
#pageary = []
#for i in range(1,101):
#    pageary.append(i)
def depth_request(ulrid):
    url = 'https://www.qiushibaike.com'+ulrid
    web = requests.get(url, headers=headers)
    web.encoding = 'utf-8'
    soup = BeautifulSoup(web.text, 'lxml')
    content_dom = soup.find('div', attrs={'class': 'col1'})
    author_dom = content_dom.find('div', attrs={'class': 'author clearfix'})
    if author_dom.a:
        author_img = author_dom.a.img['src']
        nickname = author_dom.a.img['alt']
    else:
        author_img = author_dom.img['src']
        nickname = author_dom.img['alt']
    content = content_dom.find('div', attrs={'class': 'content'})
    content = content.get_text()
    start_dom = content_dom.find('div', attrs={'class': 'stats'})
    start = int(start_dom.span.i.string)
    sql = "INSERT INTO qiubai_test (anthor_img,nickname,content,start) VALUES ('%s','%s','%s',%d)" % (author_img,nickname,content.strip(),start)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print('挖取并入库页面',url,'内容')
    except:
        # 如果发生错误则回滚
        print(Exception.message)
        db.rollback()

#while 1:
    #@retry(stop_max_attempt_number=8)  # 设置最大重试次数
    #def make_request(num):
url = 'https://www.qiushibaike.com/text/page/1/'
web = requests.get(url, headers=headers)
web.encoding = 'utf-8'
soup = BeautifulSoup(web.text, 'lxml')
all_li_select = soup.find_all('div', attrs={'class': 'article'})
for r in all_li_select:
    url_dom = r.find('a', attrs={'class': 'contentHerf'})
    geturl = url_dom['href']
    depth_request(geturl)
end = time.clock()
print('用时', end - start, '秒')
# 关闭数据库连接
db.close()


