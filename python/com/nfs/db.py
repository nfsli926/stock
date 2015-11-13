# coding=utf-8
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"
    cursor.execute(sql)
    stockDf =ts.get_stock_basics()
    print time.localtime(time.time())
    engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
    for row in cursor.fetchall():
        stockno = str(row[0])
        print stockno
        #获得上市时间
        sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
        ssYear =int(sssj[0:4])
        print sssj
        df = ts.get_hist_data(stockno,start='2015-11-11',end='2015-11-13',ktype='D')

        #df = ts.get_h_data(stockno,autype=None,start='2015-11-13',end='2015-11-13')
        print df

        if df is None:
           print "asdfasdf"
        else:
           print "asdfasd1"
           df.insert(0,'code',stockno)
           df.to_sql('stock_day_data', engine, if_exists='append')
           print time.strftime('%Y-%m-%d',time.localtime(time.time()))
except Exception,e:
   print  e.message