# coding=utf-8
__author__ = 'litao'
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
import BeautifulSoup
try:
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock where stockno like\'00%\' or stockno like\'60%\' or stockno like\'3%\'"
    cursor.execute(sql)
    #通过循环获得股票的基本信息并写入到数据库中，并实现定义好股票的相关基本信息与数据库的字段相对应
    for row in cursor.fetchall():

        print row[0],row[1].decode("utf8")
        stockno = str(row[1])
        if stockno.startswith("6"):
            stockURL = "http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code=sh"+ stockno
        else:
            stockURL = "http://f10.eastmoney.com/f10_v2/CompanySurvey.aspx?code=sz"+ stockno
        #读取页面的信息
        request = urllib2.Request(stockURL)
        response = urllib2.urlopen(request)
        stockContent =  response.read()
        #进行解析相关的页面数据 根据id的相关信息提取相关大块的数据，在通过正则表达式获得具体的内容并进行解析
        companyname =  ""  #公司名称
        name = ""          #曾用名
        url = ""           #公司网址
        zyyw = ""          #主营业务
        cpmc = ""          #产品名称
        kggd = ""          #控股股东
        sjkzr = ""         #实际控制人
        zzkzr = ""         #最终控制人

        dsz = ""           #董事长
        dm = ""            #董秘
        frdb = ""          #法人代表
        zjl = ""           #总经理
        ssds = ""          #所属地市
        sssj = ""
        soup = BeautifulSoup.BeautifulSoup(stockContent)
        detail = soup.findAll(id="Table0")
        #print detail
        trContent = detail[0].findAll("tr")
        companyname = trContent[0].findAll("td")[0].text
        name =  trContent[2].findAll("td")[0].text
        zyyw =  trContent[6].findAll("td")[1].text
        url =  trContent[11].findAll("td")[1].text
        ssds =  trContent[13].findAll("td")[0].text

        dsz =  trContent[8].findAll("td")[1].text
        dm =  trContent[8].findAll("td")[0].text
        frdb =  trContent[7].findAll("td")[1].text
        zjl =  trContent[7].findAll("td")[0].text
        print companyname + ssds + dsz + zjl
        #获取上市时间
        tableContent = soup.findAll("table")
        sssj = tableContent[1].findAll("tr")[0].findAll("td")[1].text
        print sssj
        updateSQL = "update stock set sssj=\'"+sssj +"\',companyname=\'"+companyname+"\',name=\'"+name+"\',zyyw=\'"+zyyw+"\',url=\'"+url+"\',ssds=\'"+ssds+"\' where stockno=\'"+stockno+"\'"
        cursor.execute(updateSQL)
        conn.commit()



            #div的class = content是发行相关的数据


        #下一步进行查询相关数据


    cursor.close()


except Exception,e:
    print e.message
    print e