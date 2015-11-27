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
import com.nfs.util.DayReportUtil as dayreport
import com.nfs.util.MailUtil as mailutil
import com.nfs.util.ImportUtil as importutil
try:
    print "generateDayReport"
    #init
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    #获得股票交易数据
    importdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #importutil.importDb()

    #importdate='2015-11-26'
    #生成每日的股票报表----
    dayreport.dayreport_generate(importdate)
    #导出文件
    print "genereate Day Report success"


except Exception,e:
    print e.message
