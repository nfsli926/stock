# coding=utf-8
# 2015年9月25创建
__author__ = 'litao'
from sqlalchemy import create_engine
import tushare as ts
import urllib
import urllib2
import re
import sys
import csv
import MySQLdb
import tushare as ts
import datetime
import time
import DateUtil as dateutil
# 导入股票前复权数据
#code:string,股票代码 e.g. 600848
#start:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
#end:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
#autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
#index:Boolean，是否是大盘指数，默认为False
#retry_count : int, 默认3,如遇网络等问题重复执行的次数
#pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
#返回值说明：
#date : 交易日期 (index)
#open : 开盘价
#high : 最高价
#close : 收盘价
#low : 最低价
#volume : 成交量
#amount : 成交金额
def get_qfq_date(code,start,end):
    try:
        df = ts.get_h_data(code,start,end)
        print start+end
        if df is None:
            print "qfq df is none"
        else:
            engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
            df.insert(0,'code',code)
            df.to_sql('stock_qfq_data', engine, if_exists='append')
            print  code + " qfq success"
    except Exception,e:
        print e.message
# 导入股票的不复权的历史数据
#code:string,股票代码 e.g. 600848
#start:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
#end:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
#autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
#index:Boolean，是否是大盘指数，默认为False
#retry_count : int, 默认3,如遇网络等问题重复执行的次数
#pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
#返回值说明：
#date : 交易日期 (index)
#open : 开盘价
#high : 最高价
#close : 收盘价
#low : 最低价
#volume : 成交量
#amount : 成交金额
def get_bfq_data(code,startdate,enddate):
    try:
        print "sdfsdf"
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        print startdate+enddate
        df = ts.get_h_data(code,start=startdate,end=enddate,autype='None')
        if df is None :
            print " day df is none"
        else:
            df.insert(0,'code',code)
            df.to_sql('stock_bfq_data', engine, if_exists='append')
    except Exception,e:
        e.message

# 获得股票的日分笔数据
def get_day_data(code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='D')
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        if df is None:
            print " day df is none"

        else:
            df.insert(0,'code',code)
            df.to_sql('stock_day_data', engine, if_exists='append')

    except Exception,e:
        print e.message

# 获得股票的周分笔数据
def get_week_data(code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='W')
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.insert(0,'code',code)
        df.to_sql('stock_week_data', engine, if_exists='append')
        print  code + " week success"
    except Exception,e:
        print e.message
# 获得股票的月分笔数据
def get_month_data(code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='M')
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.insert(0,'code',code)
        df.to_sql('stock_month_data', engine, if_exists='append')
        print  code + " month success"
    except Exception,e:
        print e.message
# 获得股票的月分笔数据
def get_five_data(code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='5')
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.insert(0,'code',code)
        df.to_sql('stock_five_data', engine, if_exists='append')
        print  code + " five success"
    except Exception,e:
        print e.message
# 获得行业分类
def get_industry_classified():
    try:
        df = ts.get_industry_classified();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('industry_classified', engine, if_exists='append')
    except Exception, e:
        e.message
#ts.get_hist_data('sh'）#获取上证指数k线数据，其它参数与个股一致，下同
#ts.get_hist_data('sz'）#获取深圳成指k线数据
#ts.get_hist_data('hs300'）#获取沪深300指数k线数据
#ts.get_hist_data('sz50'）#获取上证50指数k线数据
#ts.get_hist_data('zxb'）#获取中小板指数k线数据
#ts.get_hist_data('cyb'）#获取创业板指数k线数据



# 获得概念分类
def get_concept_classified():
    try:
        df = ts.get_concept_classified();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('concept_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得地域分类
def get_area_classified():
    try:
        df = ts.get_area_classified();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('area_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得中小板分类

# 获得创业板分类
# 获得风险警示板分类
def get_st_classified():
    try:
        df = ts.get_st_classified();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('st_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 沪深300成分及权重
def get_hs300s():
    try:
        df = ts.get_hs300s();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('hs300s', engine, if_exists='append')
    except Exception, e:
        e.message


# 上证50成分股
def get_sz50s():
    try:
        df = ts.get_sz50s();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('sz50s', engine, if_exists='append')
    except Exception, e:
        e.message


# 中证500成分股
def get_zz500s():
    try:
        df = ts.get_zz500s();
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        # df.insert(0,'code','600848')
        df.to_sql('zz500s', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得股票的基本数据--业绩报表
# 获取2014年第3季度的业绩报表数据
# ts.get_report_data(2014,3)
def get_report_data(year, quarter):
    try:
        df = ts.get_report_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('report_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 获得股票的基本数据--盈利能力
def get_profit_data(year, quarter):
    try:
        df = ts.get_profit_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('profit_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 获得股票的基本数据--营运能力
def get_operation_data(year, quarter):
    try:
        df = ts.get_operation_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('operation_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 获得股票的基本数据--成长能力
def get_growth_data(year, quarter):
    try:
        df = ts.get_growth_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('growth_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 获得股票的基本数据--偿债能力
def get_debtpaying_data(year, quarter):
    try:
        df = ts.get_debtpaying_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('debtpaying_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 获得股票的基本数据--现金流量
def get_cashflow_data(year, quarter):
    try:
        df = ts.get_cashflow_data(year, quarter)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('cashflow_data', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message

# 获取宏观经济数据 -存款利率
def get_deposit_rate():
    try:
        df = ts.get_deposit_rate()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('deposit_rate', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 获取宏观经济数据 -贷款利率
def get_loan_rate():
    try:
        df = ts.get_loan_rate()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('loan_rate', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message

# 获取宏观经济数据 -存款准备金绿
def get_rrr(year, quarter):
    try:
        df = ts.get_rrr()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('rrr', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 获取宏观经济数据 -货币供应量
def get_money_supply():
    try:
        df = ts.get_money_supply()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('money_supply', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 获取宏观经济数据 -国内生产总值（年度）
def get_gdp_year():
    try:
        df = ts.get_gdp_year()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('gdp_year', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 获取宏观经济数据 -国内生产总值（季度）
def get_gdp_quarter():
    try:
        df = ts.get_gdp_quarter()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('gdp_quarter', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 三大需求对gdp贡献
def get_gdp_for():
    try:
        df = ts.get_gdp_for()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('gdp_for', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 三大需求对gdp拉动
def get_gdp_pull():
    try:
        df = ts.get_gdp_pull()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('gdp_pull', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 三大产业贡献率
def get_gdp_contrib():
    try:
        df = ts.get_gdp_contrib()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('gdp_contrib', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 居民价格消费指数
def get_cpi():
    try:
        df = ts.get_cpi()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('cpi', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 工业品出厂价格指数
def get_ppi():
    try:
        df = ts.get_ppi()
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('ppi', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 龙虎榜数据
def get_top_list(date):
    try:
        df = ts.top_list(date)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('top_list', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 每日龙虎榜数据
def cap_tops(days,retry_count,pause):
    try:
        df = ts.cap_tops(days,retry_count,pause)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('cap_tops', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message


# 个股上榜统计
def cap_tops(days,retry_count,pause):
    try:
        df = ts.cap_tops(days,retry_count,pause)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('cap_tops', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 营业部上榜统计
def broker_tops(days,retry_count,pause):
    try:
        df = ts.broker_tops(days,retry_count,pause)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('broker_tops', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 机构席位追踪
def inst_tops(days,retry_count,pause):
    try:
        df = ts.inst_tops(days,retry_count,pause)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('inst_tops', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message
# 机构成交明细
def inst_detail(retry_count,pause):
    try:
        df = ts.inst_detail(retry_count,pause)
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        df.to_sql('inst_detail', engine, if_exists='append')
        print "message"
    except Exception, e:
        e.message

#获得日k线数据中一直股票的最大时间
def get_day_maxdate(stockno):
    try:
        sql = "select max(date) maxdate from stock_day_data where code='"+stockno+"'"
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        #df.to_sql('inst_detail', engine, if_exists='append')

        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得周线线数据中股票的最大时间
def get_week_maxdate(stockno):
    try:
        sql = "select max(date) maxdate from stock_week_data where code='"+stockno+"'"
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        #df.to_sql('inst_detail', engine, if_exists='append')

        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得月K线数据中一直股票的最大时间
def get_month_maxdate(stockno):
    try:
        sql = "select max(date) maxdate from stock_month_data where code='"+stockno+"'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得前复权数据中一直股票的最大时间
def get_qfq_maxdate(stockno):
    try:
        sql = "select max(date) maxdate from stock_qfq_data where code='"+stockno+"'"
        engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
        #df.to_sql('inst_detail', engine, if_exists='append')

        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0][0:10]
        cursor.close()
        conn.close
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得不复权stock_bfq_data表中的一只股票的最大时间
def get_bfq_maxdate(stockno):
    try:
        sql = "select max(transdate) maxdate from stock_bfq_data where code='"+stockno+"'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]

        cursor.close()
        conn.close
        if len(maxdate)>10:
            maxdate=maxdate[0:10]
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message

#399001 深圳成指
#399006 创业扳指
#399005 中小板指
#399300 沪深300
#000001
#获得深圳成指的最大时间
def get_szcz_maxdate():
    try:
        sql = "select max(date) maxdate from stock_index_data where code='399001'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if len(maxdate)>10:
           maxdate=maxdate[0:10]
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得创业板指数的最大时间
def get_cybz_maxdate():
    try:
        sql = "select max(date) maxdate from stock_index_data where code='399006'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if len(maxdate)>10:
           maxdate=maxdate[0:10]
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得中小板指数的最大时间
def get_zxbz_maxdate():
    try:
        sql = "select max(date) maxdate from stock_index_data where code='399005'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if len(maxdate)>10:
           maxdate=maxdate[0:10]
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得沪深300指数的最大时间
def get_hs300_maxdate():
    try:
        sql = "select max(date) maxdate from stock_index_data where code='399300'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if len(maxdate)>10:
           maxdate=maxdate[0:10]
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得上证指数的最大时间
def get_szzs_maxdate():
    try:
        sql = "select max(date) maxdate from stock_index_data where code='000001'"
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock')
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        conn.close
        if len(maxdate)>10:
           maxdate=maxdate[0:10]
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message