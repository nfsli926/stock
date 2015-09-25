# coding=utf-8
__author__ = 'litao'
from sqlalchemy import create_engine
import tushare as ts
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock where stockno like\'00%\' or stockno like\'60%\' or stockno like\'3%\'"
    engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
    cursor.execute(sql)
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    for row in cursor.fetchall():
        stockno = str(row[1])
        print stockno
        print ts.get_hist_data(stockno)
        cursor.close()
    conn.commit()
except Exception,e:
    print e.message
    print e



