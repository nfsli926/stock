# coding=utf-8
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
cursor = conn.cursor()
#n = cursor.execute("select max(date) maxdate from stock_month_data where code='000061'")
#for r in cursor:
#    print r[0]


#df = ts.get_h_data("300001")
#engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
#df.insert(0,'code','300001')
#print df.dtypes
#print df['code']
#df.to_sql('stock_qfq_data', engine, if_exists='append')
print  "000061" + "success"

        #获得tushaure的数据
        #df = ts.get_hist_data("000061",ktype='M')
        #engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        #df.insert(0,'code','000061')
        #df.to_sql('stock_month_data', engine, if_exists='append')
        #追加数据到现有表
        #df.to_sql('tick_data',engine,if_exists='append')
        #print n
try:
        sql = "select max(date) maxdate from stock_qfq_data where code='000061'"
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        #df.to_sql('inst_detail', engine, if_exists='append')

        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0][0:10]
             print maxdate
        cursor.close()
        conn.close

except Exception,e:
        print e.message
print time.strftime('%Y-%m-%d',time.localtime(time.time()))