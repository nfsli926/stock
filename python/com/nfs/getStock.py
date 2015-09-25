# coding=utf-8
__author__ = 'litao'
import urllib
import urllib2
import re
import sys
import csv
import BeautifulSoup
import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    url = "http://quote.eastmoney.com/stocklist.html"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content =  response.read()
    #print content
    soup = BeautifulSoup.BeautifulSoup(content)
    csvout  = csv.writer(sys.stdout)
    i=0
    for liStr in soup.findAll('li'):
        #print liStr
        for aStr in liStr.findAll('a'):
            if aStr.find('\(')==-1:
                print "111111111111111"
            else:
                stock =aStr.text.encode("unicode_escape").decode('string_escape')
                #print stock
                stocknoStr = re.findall("[^(]+(?=[)])",stock)
                if len(stocknoStr)==1:
                    stockno = stocknoStr[0]
                    stockname = stock[0:-8].decode("gbk").encode("utf-8")
                    print stockno+stockname
                    sql = "insert into stock (stockno,stockname) values(\'"+stockno+"\',\'"+stockname+"\')"
                    print sql
                    cursor.execute(sql)


       # print li.findAll("a")[0].text
        #print i
        i=i+1
    conn.commit()

except Exception,e:
    print e
