# coding=utf-8
#获得东方财富的相关数据
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
    sql ="select * from stock_basic"
    cursor.execute(sql)
    #获得同花顺的相关数据
    #在这个地方增加循环的操作
    stockno = '600061' #股票代码
    stockname = '' #股票名称
    #http://stockpage.10jqka.com.cn/realHead_v2.html#hs_600061
    if stockno[0:2]=="60":
        url = "http://quote.eastmoney.com/sh"+stockno+".html"
    else:
        url = "http://quote.eastmoney.com/sz"+stockno+".html"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content =  response.read()

    soup = BeautifulSoup(content,"lxml")
    csvout  = csv.writer(sys.stdout)
    ###获得主营业务
    #取得价格信息
    #收盘价格
    #开盘价格
    #最高价格
    #最低价格
    #昨日收盘
    #成交量
    #市盈率
    #市净率
    #成交额
    #总市值
    #流通市值
    #roe
    hxTableTag = soup.find("table",id="rtp2")
    if hxTableTag!=None:
        trContent = hxTableTag.find_all("tr")
        peDynamic = trContent[0].find_all("td")[1].text[6:]
        mlv = trContent[4].find_all("td")[0].text[4:][:-1]
        roe = trContent[5].find_all("td")[0].text[4:][:-1]
        zsz = trContent[6].find_all("td")[1].text[3:][:-1]
        ltsz = trContent[7].find_all("td")[1].text[3:][:-1]

        print "pe" + peDynamic +"mlv"+mlv +"roe"+roe + "zsz"+zsz +"ltsz" +ltsz
    jrspj = soup.find("strong",id="price9") #今日收盘价
    print jrspj


    #今日开盘价
    jrkpj = soup.find("td",id="gt1").text #今日开盘价
    #今日最高价
    jrzgj = soup.find("td",id="gt2").text #今日最高价
    #换手率
    hsl = soup.find("td",id="gt4").text #换手率
    #成交量
    cjl = soup.find("td",id="gt5").text #成交量
    #昨日收盘
    zrsp =soup.find("td",id="gt8").text #昨日收盘
    #今日最低价
    jrzdj = soup.find("td",id="gt9").text #今日最低价
    #量比
    lb = soup.find("td",id="gt11").text #量比
    #成交额
    jrspj = soup.find("td",id="gt12").text #成交额
    syl = soup.find("td",id="gt6").text #市盈率
    sjl = soup.find("td",id="gt13").text #市净率
    zsz = soup.find("td",id="gt7").text[:-1] #总市值[:-1]
    ltsz = soup.find("td",id="gt14").text[:-1] #流通市值
    print "ltsz " +ltsz


























    cursor.close()


except Exception,e:
    print e.message
    print e