# coding=utf-8
#获得市值最低的股票收益的回测
import pandas as pd
import numpy as np
import MySQLdb
import datetime
from sqlalchemy import create_engine
def getStockPool(month):
    #计算每月的股票池
    try:

        stocksql = "select  t4.* from (select t1.name,t1.code,t1.totals*10000*t2.open zsz,t2.open from stock_basics t1 " \
                   "left join (select code ,open from stock_bfq_data " \
                   "where  date =(select min(date) from stock_bfq_data where date like'"+month+"%')) t2 " \
                   "on t1.code=t2.code) t4 where t4.zsz is not  null order by t4.zsz"
        print stocksql
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        stock_data = pd.read_sql(stocksql,conn)
        stock_data.dropna(axis=0)
        stock_data['buysaleflag'] ='0'
        stock_data['yf']=month
        #pd.MultiIndex.from_product(stock_data, names=['yf', 'code'])
        #取得市值最小的100只股票
        stock_data[0:100].to_sql('stock_month_pool', engine, if_exists='append',index=False)

    except Exception ,e:
        print e.message

def setStockPool():
    startYear = 2008
    endYear = 2015
    startMonth =1
    endMonth = 12
    yf = ""
    while startYear<=endYear:
        if startMonth ==13:
            startMonth=1
        while startMonth<=endMonth:
            yfDate = datetime.datetime(startYear,startMonth,1)
            startMonth = startMonth+1
            yf = yfDate.strftime('%Y-%m')
            getStockPool(yf)
        startYear = startYear+1
        print startYear
#初始化股票数据
def init(month):
    print "firstcompute"
    #按月去除股票池中的数据
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    poolSql = "select * from stock_month_pool where yf = '"+month+"' "
    yeSql = "select * from stock_month_sz where yf=(select max(yf) from stock_month_sz)"
    cursor = conn.cursor()
    insertCur = conn.cursor()
    cursor.execute(yeSql)
    totalsz = 0;

    for r in cursor:
       totalsz = r[3]
    cursor.execute(poolSql)
    for poolInfo in cursor:
        code = str(poolInfo[1]) #股票代码
        print code
        open =poolInfo[3]  #开盘价
        #可以购买的数量用10000除open的价格再除以100，四舍五入
        #python下的函数round可以四舍五入，但函数int就只能向下取整数，以下代码可以实现四舍五入
        if totalsz<10000:
            print "zongshizhi <10000"
            buyNum = int(100/open)*100
            totalsz = totalsz-open*buyNum
            insertSql = "insert into stock_month_compute(yf,code,buyprice,buynum) values('"+month+"','"+code+"',"+str(open)+","+str(buyNum)+")"
            insertCur.execute(insertSql)
            conn.commit()
            break
        else:
            buyNum = round(100/open)*100
            print "buynum"+str(buyNum) +code
            totalsz = totalsz-open*buyNum
            insertSql = "insert into stock_month_compute(yf,code,buyprice,buynum) values('"+month+"','"+code+"',"+str(open)+","+str(buyNum)+")"
            print insertSql
            insertCur.execute(insertSql)
            conn.commit()

    print totalsz
    insertSql = "insert into stock_month_sz(yf,ye) values('"+month+"',"+str(totalsz)+")"
    insertCur.execute(insertSql)
    conn.commit()

    cursor.close()
    insertCur.close()
    conn.close
def compute():
    print "compute"
    #1先取出余额
    #2然后取出第一期中不在第二期中的股票，将其卖出
    #将同时在第一期第二期的股票转到第二期，
    #买入第二期中不在第一其中的股票

if __name__ == "__main__":
    print "compute"
    init('2008-01')