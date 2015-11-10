# coding=utf-8
__author__ = 'litao'
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
from bs4 import BeautifulSoup
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock where stockno like\'00%\' or stockno like\'60%\' or stockno like\'3%\'"
    cursor.execute(sql)
    #获得同花顺的相关数据
    stockno = '' #股票代码
    stockname = '' #股票名称
    #http://stockpage.10jqka.com.cn/realHead_v2.html#hs_600061
    url = "http://stockpage.10jqka.com.cn/realHead_v2.html#hs_600061"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content =  response.read()
    print content
    #print content
    soup = BeautifulSoup(content,"lxml")
    csvout  = csv.writer(sys.stdout)
    print soup.name
    i=0
    for content1 in soup.find_all("ul", class_="new_trading fl"):
        print '11111111111'
        print content1
    print 'aaaa'


    cursor.close()


except Exception,e:
    print e.message
    print e