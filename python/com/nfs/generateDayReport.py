# coding=utf-8
#生成每日的报表
#1、执行相关任务，将数据存入到数据库中
#2、读取相关数据
#3、写入excel文件
#4、发送电子邮件
#5、每天定期执行
#6、优化整个操作，尽量减少读取同花顺的时间
#7、判断解禁时间，并重点标红
__author__ = 'litao'
from sqlalchemy import create_engine
import tushare as ts
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
import tushare as ts
import datetime
import time
import util.DateUtil as dateutil
import xlrd
import win32com.client as win32
import pandas as pd
app = "Excel"
try:
    print "generateDayReport"
    #init
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    df = pd.read_sql("select * from stock_day_report where importdate='2015-11-11' order by sshy,ltg,zgb",conn)
    print df
    #首先执行相关数据导入操作
    df.to_csv('d:/20151111.csv',encoding='gbk', index=False)



except Exception,e:
    print e.message
