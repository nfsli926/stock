# coding=utf-8
__author__ = 'litao'
import DBUtilNew as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
def importDb():
    flag = 0
    try:
        #首先取出所有股票的代码，然后取得股票的上市时间，根据上市时间按年增加数据，一直进行循环
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        cursor = conn.cursor()
        sql ="select * from stock_basic"
        cursor.execute(sql)
        stockDf =ts.get_stock_basics()
        startImport =  time.localtime(time.time())
        #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
        #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
        for row in cursor.fetchall():
            stockno = str(row[0])
            print stockno
            currentDay = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            end = currentDay
            #dbutil.get_day_data(engine,stockno,end,end)
            dbutil.get_bfq_data(engine,conn,stockno,end,end)
            dbutil.get_day_data(engine,conn,stockno,end,end)

            print "sdfsdf"
            #dbutil.get_five_data(stockno,start,end)
            #ssYear = ssYear+1

           #取得当前的年月，并按年进行循环，插入数据相关数据

        print "import stock data success"
        return flag
    except Exception,e:
         print e.message
    finally:
        return flag


if __name__ == "__main__":
    if importDb():
        print "1111"
    else:
        print "2222！"