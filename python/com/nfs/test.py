# coding=utf-8
__author__ = 'litao'
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
import datetime
import time
from bs4 import BeautifulSoup
try:

       #print time.localtime(time.time())-datetime.timedelta(month=1)

    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    lastMonth = first - datetime.timedelta(days=1)


    print time.strftime('%Y-%m',time.localtime(time.mktime(lastMonth.timetuple())))
      # time1 = datetime.datetime.strptime(time.localtime(time.time()),'%Y-%m-%d')-datetime.timedelta(month=1)
       #currentday = time.strftime('%Y-%m',time.localtime(time.mktime(time1.timetuple())))
      # print currentday
except Exception,e:
    print e.message
    print e