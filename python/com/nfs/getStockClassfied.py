# coding=utf-8
#获得股票的行业分类
__author__ = 'litao'
import util.dbutil as dbutil
import urllib
import urllib2
import re
import sys
import csv
import time
import MySQLdb
from sqlalchemy import create_engine
import util.DateUtil as dateutil
from bs4 import BeautifulSoup
import tushare as ts
try:
    #首先取出所有股票的代码，然后取得股票的上市时间，根据上市时间按年增加数据，一直进行循环
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"
    cursor.execute(sql)
    stockDf =ts.get_stock_basics()
    startImport =  time.localtime(time.time())
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    #通过循环获取当前股票的最大时间，然后利用最大时间与与当前时间设置差值，进行导入数据
    for row in cursor.fetchall():
    #if 1==1:
        stockno = str(row[0])
        #stockno = '000851'
        print stockno
        url = "http://stockpage.10jqka.com.cn/"+stockno+"/company/"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content =  response.read()
        soup = BeautifulSoup(content,"lxml")
        #获得同花顺中股票分类代码
        detailDiv = soup.find("div",id="detail")
        if detailDiv is not  None:
            trContent = detailDiv.find("table",class_="m_table").find_all("tr")
            print trContent
            hyflTag =  trContent[1].find_all("td")[1].text[5:].strip()
            print hyflTag
            cursor.execute("select * from stock_industry_classified where code='"+stockno+"'")
            row = cursor.fetchone()
            if row is None:
                cursor.execute("insert into stock_industry_classified (code,name,c_name) values('"+stockno+"','','"+hyflTag+"')")
                cursor.execute(updateSQL)
            updateSQL = "update stock_industry_classified set c_name='"+hyflTag+"' where code='"+stockno+"' "
            cursor.execute(updateSQL)
            conn.commit()
        else:
            continue


except Exception,e:
    print e.message
