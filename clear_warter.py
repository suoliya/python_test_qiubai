#爬虫京东净水机查看比较受欢迎的品牌

import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pymysql
import re
start = time.clock()     #计时-开始


url = 'https://search.jd.com/Search?keyword=%E5%87%80%E6%B0%B4%E5%99%A8&enc=utf-8&wq=%E5%87%80%E6%B0%B4%E5%99%A8&pvid=96dd18d77fa44dceab891920fb4888f5'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
web = requests.get(url, headers=headers)
web.encoding = 'utf-8'
soup = BeautifulSoup(web.text,'lxml')
all_li_select = soup.find_all('li', attrs={'class': 'gl-item'})

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect("localhost", "root", "111111", "python_test",charset="utf8")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
for r in all_li_select:
    dom = r.find_all('div',attrs={'class':'gl-i-wrap'})
    price_dom = dom[0].find('div',attrs={'class':'p-price'})
    name_dom = dom[0].find('div', attrs={'class': 'p-name'})
    commit_dom = dom[0].find('div', attrs={'class': 'p-commit'})
    shop_dom = dom[0].find('div', attrs={'class': 'p-shop'})
    price = float(price_dom.strong.i.get_text())
    url = name_dom.a['href']
    title = name_dom.em.get_text()
    detail = name_dom.a['title']
    commit_str =commit_dom.strong.get_text()
    commit = re.findall(r"\d+\.?\d*",commit_str)[0]
    if commit_str.find('万') >=1:
        commit = float(commit)*10000
    commit = int(commit)
    shop = shop_dom.a.get_text()
    sql = "INSERT INTO clear_warter (title,detail,num,shop,price,url) VALUES ('%s','%s',%d,'%s',%f,'%s')" % (title,detail,commit,shop,price,url)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print(Exception.message)
        db.rollback()
end = time.clock()
print('用时',end-start,'秒')
# 关闭数据库连接
db.close()






