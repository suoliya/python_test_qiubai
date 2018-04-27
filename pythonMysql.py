import pymysql

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect("localhost", "root", "111111", "python_test",charset="utf8")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO clear_warter (title,detail,num,shop,price) VALUES ('%s','%s',%f,'%s',%f)" % ('测试','测试xsss',11,'测试内容',1234.45)
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    print(Exception)
    db.rollback()

# 关闭数据库连接
db.close()