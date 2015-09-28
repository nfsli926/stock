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

stockDf =ts.get_stock_basics()
sssj = str(stockDf.ix['000001']['timeToMarket']) #上市日期YYYYMMDD
print sssj[0:4]

#print n