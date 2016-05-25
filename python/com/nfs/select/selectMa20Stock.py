# coding=utf-8
import pandas as pd
import MySQLdb
import python.com.nfs.util.MailUtil as mailutil
import sys

# ========== 从原始csv文件中导入股票数据，以浦发银行sh600000为例

# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
'''
1、循环股票代码
2、最新的一条数据20均线在最高与最低之间
2、取出最新的5条数据
3、最后一条的均线数据大于倒数第二条
4、写入数据库，发送 或者写入df，形成xls文件
5、发送

'''
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    cursor = conn.cursor()
    sql ="select * from stock_basic"
    cursor.execute(sql)
    ma20List = []
    for row in cursor.fetchall():
        stockno = str(row[0])
        stockname = row[1]
        print stockname
        stock_data = pd.read_sql("select * from stock_day_data where code='"+stockno+"'  order by code, date desc limit 5 ",conn)

        if stock_data.iloc[2,10]>=stock_data.iloc[1,10] and stock_data.iloc[1,10]< stock_data.iloc[0,10]:
            print "sssssssssss" +stockno
            ma20List.append([stockno,stockname])

    print ma20List
    content = ""
    for ma in ma20List:
        print ma[0]+ma[1]
        content = content +ma[0]+"，"+ma[1].encode('utf8')
        #print content
    #content = content+"</table></body></html>"
    print content
    mailutil.send_mail("20日均线数据", content, None)

    cursor.close()
    conn.close()

    #stock_data.to_csv('selectma20stock.csv', index=False)
except Exception,e:
    print e.message
