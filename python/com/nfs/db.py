# coding=utf-8
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"
    cursor.execute(sql)
    stockDf =ts.get_stock_basics()
    print time.localtime(time.time())
    engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
    #df = pd.read_sql("select * from stock_day_report_copy where importdate='2015-11-27' order by sshy,ltg,zgb",conn)
    #df.rename(columns={'stockno':'股票代码','stockname':'股票名称','sshy':'所属杨业','sjgn':'涉及概念','brspj':'本日收盘价','syspj':'上月收盘价','ltg':'流通股','zgb':'总股本','jlr':'净利润','yysr':'营业收入','mgjzc':'每股净资产','mgsy':'每股收益','jlrzzl':'净利润增长率','mgxjl':'每股现金流','mggjj':'每股公积金','mgwfplr':'每股未分配利润','dtsyl':'动态市盈率','sjl':'市净率','ltsz':'流通市值','zsz':'总市值','jjsj':'解禁时间','mlv':'毛利率','jlv':'净利率','roe':'ROE','fzl':'负债率','importdate':'导入日期','sssj':'上市时间','cplx':'产品类型','ssdy':'所属地域','lrzy':'利润总额','tenholder':'十大持股人','gdrs':'股东人数'}, inplace=True)
    #print df
        #首先执行相关数据导入操作
    #df.to_csv('d:/2015-11-27.csv',encoding='gbk', index=False)
    #print "ddddddddddd"

    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
    for row in cursor.fetchall():
        stockno = str(row[0])
        print stockno
        #获得上市时间
        sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
        ssYear =int(sssj[0:4])
        print sssj




        df = ts.get_hist_data(stockno,start='2015-11-27',end='2015-11-27',ktype='D')

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