# coding=utf-8
#获得市值最低的股票收益的回测
import pandas as pd
import numpy as np
import MySQLdb
import datetime
from sqlalchemy import create_engine
import time
import datetime
import calendar as cal

def get_next_month(currentMonth):
    d = cal.monthrange(int(currentMonth[0:4]),int(currentMonth[5:]))
    currentMonth_last_day = datetime.date(day=d[1],month=int(currentMonth[5:]), year=int(currentMonth[0:4]))
    next_Month = currentMonth_last_day + datetime.timedelta(days=1)
    next_Month = time.strftime('%Y-%m',time.localtime(time.mktime(next_Month.timetuple())))
    return  next_Month

def getStockPool(month):
    #计算每月的股票池
    try:

        stocksql = "select  t4.* from (select t1.name,t1.code,t1.totals*10000*t2.open zsz,t2.open from (select * from stock_basics where  code like '00%' ) t1 " \
                   "left join (select code ,open from stock_bfq_data " \
                   "where   date =(select min(date) from stock_bfq_data where date like'"+month+"%' and code like '00%')) t2 " \
                   "on t1.code=t2.code) t4 where t4.zsz is not  null  order by t4.zsz"
        print stocksql
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        stock_data = pd.read_sql(stocksql,conn)
        stock_data.dropna(axis=0)
        stock_data['buysaleflag'] ='0'
        stock_data['yf']=month
        print month
        #pd.MultiIndex.from_product(stock_data, names=['yf', 'code'])
        #取得市值最小的100只股票
        stock_data[0:10].to_sql('stock_month_pool', engine, if_exists='append',index=False)
        print "stock_pool success" +month

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
    print "余额====" +str(totalsz)
    cursor.execute(poolSql)
    for poolInfo in cursor:
        code = str(poolInfo[1]) #股票代码
        print code
        open =poolInfo[3]  #开盘价
        #可以购买的数量用10000除open的价格再除以100，四舍五入
        #python下的函数round可以四舍五入，但函数int就只能向下取整数，以下代码可以实现四舍五入
        if totalsz<10000 and totalsz>=0:
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
            print "余额====" +str(totalsz)
            insertSql = "insert into stock_month_compute(yf,code,buyprice,buynum) values('"+month+"','"+code+"',"+str(open)+","+str(buyNum)+")"
            insertCur.execute(insertSql)
            conn.commit()

    print "总余额====" +str(totalsz)
    insertSql = "insert into stock_month_sz(yf,ye) values('"+month+"',"+str(totalsz)+")"
    insertCur.execute(insertSql)
    conn.commit()

    cursor.close()
    insertCur.close()
    conn.close
def compute():
    print "compute"
    start_month='2008-01'
    init(start_month)
    end_month = '2015-12'
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
    engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
    cursor = conn.cursor()
    saleCur = conn.cursor()
    insertCur = conn.cursor()

    while start_month<end_month:
        current_month = start_month
        print current_month
        totalsz = 0.0
        next_month = get_next_month(current_month)
        print next_month
        #在stock_month_sz中取出余额
        yeSql = "select * from stock_month_sz where yf='"+current_month+"'"
        cursor.execute(yeSql)

        for r in cursor:
            totalsz = r[3]
        print "当前余额为 " +str(totalsz)
        #取出同时在第一次与第二月股票池的股票，将其月份数据修改为第二月的数据
        two_month_sql = "select * from stock_month_compute where yf='"+current_month+"' and code in(select code from stock_month_pool where yf='"+next_month+"' )"
        firstMonth = pd.read_sql("select * from stock_month_compute",conn)


        stock_data = pd.read_sql(two_month_sql,conn)
        stock_data['yf'] = next_month
        stock_data.to_sql('stock_month_compute', engine, if_exists='append',index=False)



        #将在当前月中，不在下一个月中的股票卖出,并计算总市值的数据,卖出股票价格需要在别的表中获得，股票池中没有数据
        two_month_sql = "select * from stock_month_compute where yf='"+current_month+"' and code not in(select code from stock_month_pool where yf='"+next_month+"' )"
        cursor.execute(two_month_sql)
        for r in cursor:
            code = r[1]
            buyprice = r[2]
            saleSQL="select * from stock_bfq_data where code='"+code+"' and date=(select min(date) from stock_bfq_data where code='"+code+"' and date like '"+next_month+"%')"
            saleCur.execute(saleSQL)
            salePrice = 0.0
            for saleR in  saleCur:
                salePrice = saleR[3]

            buynum = r[4]
            totalsz = totalsz +salePrice*buynum
        print "总市值为" +str(totalsz)
        #用余额购买股票池的股票
        #查询出相关股票
        two_month_sql = "select * from stock_month_pool where yf='"+next_month+"' and code not in(select code from stock_month_pool where yf='"+current_month+"' )"
        cursor.execute(two_month_sql)
        for r in cursor:
            code = r[1]
            open = r[3]
            if totalsz<10000 and totalsz>=0:
                print "zongshizhi <10000"
                buyNum = int(totalsz/(100*open))*100
                print "购买股票" +str(code) +"购买价格"+str(open)+"购买数量" +str(buyNum)
                if totalsz>open*buyNum:
                    totalsz = totalsz-open*buyNum
                    print "buynum"+str(buyNum) +code
                    insertSql = "insert into stock_month_compute(yf,code,buyprice,buynum) values('"+next_month+"','"+code+"',"+str(open)+","+str(buyNum)+")"
                    insertCur.execute(insertSql)
                    print "购买后余额" +str(totalsz)
                    conn.commit()
                    break
                else:
                    break
            else:

                buyNum = round(100/open)*100
                print "购买股票" +str(code) +"购买价格"+str(open)+"购买数量" +str(buyNum)
                totalsz = totalsz-open*buyNum
                insertSql = "insert into stock_month_compute(yf,code,buyprice,buynum) values('"+next_month+"','"+code+"',"+str(open)+","+str(buyNum)+")"
                insertCur.execute(insertSql)
                conn.commit()
                print "购买后余额" +str(totalsz)

        #插入余额表
        insertSql = "insert into stock_month_sz(yf,ye) values('"+next_month+"',"+str(totalsz)+")"
        insertCur.execute(insertSql)
        #updateSQL = "update stock_month_compute t1 set buyprice=(select open from stock_month_pool t2 where t1.code=t2.code and t1.yf=t2.yf and t1.yf='"+next_month+"')"
        #insertCur.execute(updateSQL)
        #conn.commit()


        conn.commit()
        #循环start——month
        start_month = next_month






    #1先取出余额
    #2然后取出第一期中不在第二期中的股票，将其卖出
    #将同时在第一期第二期的股票转到第二期，
    #买入第二期中不在第一其中的股票

if __name__ == "__main__":
    print "compute"
    setStockPool()
    #init('2008-01')
    compute()
    print "end compute"