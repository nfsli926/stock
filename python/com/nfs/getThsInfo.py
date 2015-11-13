# coding=utf-8
__author__ = 'litao'
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
import time
import util.DateUtil as dateutil
from bs4 import BeautifulSoup
import com.nfs.test.mailtest as mailtest
import pandas as pd
try:
    starttime = time.localtime(time.time())
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"

    cursor.execute(sql)
    for stockrow in cursor.fetchall():
        stockno = stockrow[0]
        stockname=stockrow[1]
        print stockno+stockname
    #获得同花顺的相关数据
    #在这个地方增加循环的操作

        #http://stockpage.10jqka.com.cn/realHead_v2.html#hs_600061
        url = "http://stockpage.10jqka.com.cn/"+stockno
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content =  response.read()

        soup = BeautifulSoup(content,"lxml")
        csvout  = csv.writer(sys.stdout)
        ###获得主营业务
        request = urllib2.Request("http://stockpage.10jqka.com.cn/"+stockno+"/operate/")
        response = urllib2.urlopen(request)
        contentZyyw =  response.read()
        soupZyyw = BeautifulSoup(contentZyyw,"lxml")
        csvout1  = csv.writer(sys.stdout)
        cplxTag = soupZyyw.find("ul",class_="main_intro_list")
        if cplxTag==None:
            cplx = ""
        else:
            cplx =  cplxTag.li.p.text
        print cplx
        sshySql= "select * from stock_industry_classified where code=\'"+stockno+"\' "
        cursor.execute(sshySql)
        sshy = ""
        for rowSshy in cursor.fetchall():
            sshy =  rowSshy[3]

        importdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))


        #取得股票的相关公司信息
        #股票代码，股票名称
        #所属地域
        #涉及概念
        #主营业务
        #上市时间
        #每股净资产
        #每股收益
        #净利润
        #净利润增长率
        #营业收入
        #每股现金流
        #每股公积金
        #每股未分配利润
        #总股本
        #流通股
        #所属行业通过在http://stockpage.10jqka.com.cn/600062/company/获得
        #市盈率 市净率现在的数据获取不到
        #利润总额流通市值，总市值去不了
        #限售解禁http://stockpage.10jqka.com.cn/000001/holder/#liftban
        for content1 in soup.find_all("dl", class_="company_details"):
            #获得主营业务
            #http://stockpage.10jqka.com.cn/002229/operate/

            #获得相关信息
            for details in content1.find_all("dt"):
                if details.string==unicode("所属地域：","utf-8"):
                    ssdy = details.next_sibling.next_sibling.string
                    print details.string+ssdy
                elif details.string==unicode("涉及概念：","utf-8"):
                    sjgn = details.next_sibling.next_sibling["title"]
                    print sjgn
                elif details.string==unicode("主营业务：","utf-8"):
                    zyyw = details.next_sibling.next_sibling.string
                    print zyyw
                elif details.string==unicode("上市日期：","utf-8"):
                    sssj = details.next_sibling.next_sibling.string
                    print sssj
                elif details.string==unicode("每股净资产：","utf-8"):
                    mgjzc = details.next_sibling.next_sibling.string[:-1]
                    print mgjzc[:-1]
                elif details.string==unicode("每股收益：","utf-8"):
                    mgsy = details.next_sibling.next_sibling.string[:-1]
                    print mgsy[:-1]
                elif details.string==unicode("净利润：","utf-8"):
                    jlr = details.next_sibling.next_sibling.string[:-2]
                    print jlr[:-2]
                elif details.string==unicode("净利润增长率：","utf-8"):
                    jlrzzl = details.next_sibling.next_sibling.string[:-1]
                    print jlrzzl[:-1]
                elif details.string==unicode("营业收入：","utf-8"):
                    yysr = details.next_sibling.next_sibling.string[:-1]
                    print yysr[:-1]
                elif details.string==unicode("每股现金流：","utf-8"):
                    mgxjl = details.next_sibling.next_sibling.string[:-1]
                    print mgxjl[:-1]
                elif details.string==unicode("每股公积金：","utf-8"):
                    mggjj = details.next_sibling.next_sibling.string[:-1]
                    print mggjj[:-1]
                elif details.string==unicode("每股未分配利润：","utf-8"):
                    mgwfplr = details.next_sibling.next_sibling.string[:-1]
                    print mgwfplr[:-1]
                elif details.string==unicode("总股本：","utf-8"):
                    zgb = details.next_sibling.next_sibling.string[:-1]
                    print zgb[:-1]
                elif details.string==unicode("流通股：","utf-8"):
                    ltg = details.next_sibling.next_sibling.string[:-1]
                    print ltg[:-1]
        #从东方财富抓取数据
        if stockno[0:2]=="60":
            dfUrl = "http://quote.eastmoney.com/sh"+stockno+".html"
        else:
            dfUrl = "http://quote.eastmoney.com/sz"+stockno+".html"
        request = urllib2.Request(dfUrl)
        response = urllib2.urlopen(request)
        dfcontent =  response.read()

        dfSoup = BeautifulSoup(dfcontent,"lxml")
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
        hxTableTag = dfSoup.find("table",id="rtp2")
        if hxTableTag!=None:
            trContent = hxTableTag.find_all("tr")
            dtsyl = trContent[0].find_all("td")[1].text[6:]
            sjl = trContent[1].find_all("td")[1].text[4:]
            mlv = trContent[4].find_all("td")[0].text[4:][:-1]
            jlv = trContent[4].find_all("td")[1].text[4:][:-1]
            roe = trContent[5].find_all("td")[0].text[4:][:-1]
            fzl = trContent[5].find_all("td")[1].text[4:][:-1]
            zsz = trContent[6].find_all("td")[1].text[3:][:-1]
            ltsz = trContent[7].find_all("td")[1].text[3:][:-1]
            print "jlv" +trContent[4].find_all("td")[1].text[4:]
        #获得解禁时间
        jjSql = "select min(jjsj) jjsj from stock_jjsj where stockno='"+stockno+"' and jjsj>='"+importdate+"'"
        cursor.execute(jjSql)
        jjRow = cursor.fetchone()
        print jjRow
        if jjRow[0] ==None:
           jjsj = ""
        else:
           jjsj = jjRow[0]
        #获得上月收盘价
        #获得本日收盘价
        #获得上个月
        pre_month = dateutil.get_pre_month()
        print pre_month
        syspjSQL ="select * from stock_day_data where date=(select max(date) from stock_day_data where code='"+stockno+"' and left(date,7)='"+pre_month+"') and code='"+stockno+"' "
        brspjSQL = "select * from stock_day_data where date like'"+importdate+"%' and code='"+stockno+"'"
        cursor.execute(syspjSQL)
        syspjRow = cursor.fetchone()
        print syspjRow
        if syspjRow==None:
            print syspj
            syspj = ""
        else:
            syspj = str(syspjRow[4])
        print syspj
        #本日收盘价
        cursor.execute(brspjSQL)
        brspjRow = cursor.fetchone()
        print brspjRow
        if None==brspjRow:
            print "brspj"
            brspj = ""
        else:
            brspj = str(brspjRow[4])
        insertsql = "insert into stock_day_report (stockno,stockname,importdate,ssdy,sjgn,cplx,sshy,sssj,mgjzc,mgsy,jlr,jlrzzl,yysr,mgxjl,mggjj,mgwfplr,zgb,ltg," \
                    "zsz,ltsz,sjl,dtsyl," \
                    "mlv,jlv,roe,fzl,jjsj,syspj,brspj" \
                    ")             " \
                    "values(\'"+stockno+"\',\'"+stockname+"\',\'"+importdate+"\',\'"+ssdy+"\',\'"+sjgn+"\',\'"+cplx+"\',\'"+sshy+"\',\'"+sssj+"\',\'"+mgjzc+"\',\'"+mgsy+"\',\'"+jlr+"\',\'"+jlrzzl+"\',\'"+yysr+"\',\'"+mgxjl+"\',\'"+mggjj+"\',\'"+mgwfplr+"\',\'"+zgb+"\',\'"+ltg+"\'," \
                    "\'"+zsz+"\',\'"+ltsz+"\',\'"+sjl+"\',\'"+dtsyl+"\',\'"+mlv+"\',\'"+jlv+"\',\'"+roe+"\',\'"+fzl+"\',\'"+jjsj+"\',\'"+syspj+"\',\'"+brspj+"\')"
        print insertsql
        cursor.execute(insertsql)
        conn.commit()
    cursor.close()


    df = pd.read_sql("select * from stock_day_report where importdate='2015-11-13' order by sshy,ltg,zgb",conn)
    print df
    #首先执行相关数据导入操作
    df.to_csv('d:/20151113.csv',encoding='gbk', index=False)
    if mailtest.send_mail("测试信", "我的博客欢迎您：http://www.linuxidc.com/", r"d:/20151113.csv"):
        print "1111"
    else:
        print "2222！"


except Exception,e:
    print e.message
    print e