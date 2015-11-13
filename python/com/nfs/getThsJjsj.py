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
    sql ="select * from stock_basic where code not in (select stockno from stock_jjsj)"
    cursor.execute(sql)
    for row in cursor.fetchall():

        print row[0]
        stockno = str(row[0].decode("utf8"))
        #获得解禁时间业务逻辑建议放到单独一张表进行处理，并根据距离当前最近的时间取出

        request = urllib2.Request("http://stockpage.10jqka.com.cn/"+stockno+"/holder/#liftban")
        response = urllib2.urlopen(request)
        contentJjsj =  response.read()
        soupJjsj = BeautifulSoup(contentJjsj,"lxml")
        csvout1  = csv.writer(sys.stdout)
        jjTable = soupJjsj.find("div",id="liftban")
        if jjTable == None:
            continue
        else:
            for trContent in  soupJjsj.find("div",id="liftban").find("table").find("tbody").find_all("tr"):
                jjsj = trContent.find("th").text
                tdContent = trContent.find_all("td")
                jjgfs = tdContent[0].text
                drspj = tdContent[1].text
                jjsz = tdContent[2].text
                jjgzb = tdContent[3].text
                jjgflx = tdContent[4].text
                print stockno + jjsj + jjgfs+drspj+jjsz+jjgzb+jjgflx
                sql = "insert into stock_jjsj (stockno,jjsj,jjgfs,drspj,jjsz,jjgzb,jjgflx) values(\'"+stockno+"\',\'"+jjsj+"\',\'"+jjgfs+"\',\'"+drspj+"\',\'"+jjsz+"\',\'"+jjgzb+"\',\'"+jjgflx+"\')"
                print sql
                cursor.execute(sql)
                conn.commit()
    cursor.close()
    conn.close
except Exception,e:
    print e.message
    print e