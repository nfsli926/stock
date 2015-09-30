# coding=utf-8
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts

#数据库查询功能
#conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
#cursor = conn.cursor()
#n = cursor.execute("select * from cj")

df = ts.get_hist_data("000061",ktype='M')
engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')

df.insert(0,'code','000061')
df.to_sql('stock_month_data', engine, if_exists='append')

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')

#print n