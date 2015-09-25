# coding=utf-8
import MySQLdb

#数据库查询功能
conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
cursor = conn.cursor()
n = cursor.execute("select * from cj")
print n