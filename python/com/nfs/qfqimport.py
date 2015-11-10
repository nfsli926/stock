# coding=utf-8
__author__ = 'litao'
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
try:
    #首先取出所有股票的代码，然后取得股票的上市时间，根据上市时间按年增加数据，一直进行循环
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"
    cursor.execute(sql)
    stockDf =ts.get_stock_basics()
    print time.localtime(time.time())
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
    for row in cursor.fetchall():
        stockno = str(row[0])
        print stockno
        #获得上市时间
        sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
        ssYear =int(sssj[0:4])
        print ssYear
        currentYear = int(time.strftime('%Y',time.localtime(time.time())))
        print currentYear
        while ssYear<=currentYear:
            start = str(ssYear)+"-01-01"
            end = str(ssYear)+"-12-31"
            dbutil.get_qfq_date(stockno,start,end)
            print str(ssYear)+"年"+stockno+"导入成功"
            ssYear = ssYear+1


except Exception,e:
    e.message
