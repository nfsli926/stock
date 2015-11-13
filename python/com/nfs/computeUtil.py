# coding=utf-8
#主要进行均线数据的计算
__author__ = 'litao'
import util.dbutil as dbutil
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import tushare as ts
def computeAvgLine(stockNo):
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
        cursor = conn.cursor()

        cursor.execute(sql)

        #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
        #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
        print 'compureAvgLine'
    except Exception,e:
        print e.message
