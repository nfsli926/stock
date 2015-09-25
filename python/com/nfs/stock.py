# coding=utf-8
__author__ = 'litao'
#获得股票的代码及名称
#20150828先获得第一页中的table，重点在编写正则表达式
import urllib
import urllib2
import re
import sys
import csv
import BeautifulSoup
import MySQLdb
try:
     page = 1
     last = 72
     conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
     cursor = conn.cursor()


     while page<last:
        url = "http://vip.stock.finance.sina.com.cn/q/go.php/vIR_CustomSearch/index.phtml?sr_p=-1&p="+str(page)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content =  response.read()
        soup = BeautifulSoup.BeautifulSoup(content)
        csvout  = csv.writer(sys.stdout)
        i=0

        for table in soup.findAll('table'):
            i=0
            for row in table.findAll('tr'):
                #将第一行排除出去
                if i==0:
                    i = i+1
                    continue
                else:
                    tdcontent = row.findAll('td')
                    stockno = tdcontent[0].text.encode("raw_unicode_escape").decode('string_escape')
                    stockname = tdcontent[1].text.encode("raw_unicode_escape").decode('string_escape')
                    print stockno+stockname
                    sql = "insert into stock (stockno,stockname) values(\'"+stockno+"\',\'"+stockname+"\')"
                    #cursor.execute(sql)

        page = page+1
     conn.commit()





                    #在此处增加对于数据库的写操作，讲股票代码以及名称写入到数据库20150901准备编写




    #pattern = re.compile('<table class="list_table.*?>(.*?)</table>',re.S)
    #items = re.findall(pattern,content)
    #print items[0]
    #for row in




except Exception,e:
    print e


