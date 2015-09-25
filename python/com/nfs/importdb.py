# coding=utf-8
__author__ = 'litao'
import util.dbutil as dbutil
import re
import sys
import csv
import MySQLdb
try:
    #首先取出所有股票的代码，然后取得股票的上市时间，根据上市时间按年增加数据，一直进行循环
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock where stockno like\'00%\' or stockno like\'60%\' or stockno like\'3%\'"
    cursor.execute(sql)
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    for row in cursor.fetchall():
        stockno = str(row[1])
        #获得上市时间
        dbutil.get_qfq_date(stockno)
except Exception,e:
    e.message
