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
import pandas as pd
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
def get_qfq_date(engine,conn,code,start,end):
    try:
        startDate = get_day_maxdate(conn,code)
        df = ts.get_h_data(code,startDate,end)
        if df is None:
            print "qfq df is none"
        else:
            df.insert(0,'code',code)
            df.to_sql('stock_qfq_data', engine, if_exists='append')
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
def get_bfq_data(engine,conn,code,startdate,enddate):
    try:
        startdate = get_bfq_maxdate(conn,code)
        print startdate + "ssssssssss"
        df = ts.get_h_data(code,autype=None,start=startdate,end=enddate)
        print df
        if df is None or df.__len__()==0:
            print " day df is none"
        else:
            df.insert(0,'code',code)
            #df.rename(columns={'date':'transdate'}, inplace=True)
            df.to_sql('stock_bfq_data', engine, if_exists='append')
    except Exception,e:
        e.message

# 获得股票的日分笔数据
def get_day_data(engine,conn,code,startdate,enddate):
    flag = 0
    try:
        startdate = get_day_maxdate(conn,code)
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='D')
        if df is None or df.__len__()==0:
            print " day df is none"

        else:
            df.insert(0,'code',code)
            df.to_sql('stock_day_data', engine, if_exists='append')
            flag = 1
    except Exception,e:
        print e.message
    finally:
        return flag
# 获得股票的周分笔数据
def get_week_data(engine,conn,code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='W')
        df.insert(0,'code',code)
        df.to_sql('stock_week_data', engine, if_exists='append')
    except Exception,e:
        print e.message
# 获得股票的月分笔数据
def get_month_data(engine,conn,code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='M')
        df.insert(0,'code',code)
        df.to_sql('stock_month_data', engine, if_exists='append')
    except Exception,e:
        print e.message
# 获得股票的月分笔数据
def get_five_data(engine,conn,code,startdate,enddate):
    try:
        df = ts.get_hist_data(code,start=startdate,end=enddate,ktype='5')
        df.insert(0,'code',code)
        df.to_sql('stock_five_data', engine, if_exists='append')
    except Exception,e:
        print e.message
# 获得行业分类
def get_industry_classified(engine):
    try:
        df = ts.get_industry_classified()
        df.to_sql('industry_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得概念分类
def get_concept_classified(engine):
    try:
        df = ts.get_concept_classified()
        df.to_sql('concept_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得地域分类
def get_area_classified(engine):
    try:
        df = ts.get_area_classified();
        df.to_sql('area_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 获得中小板分类

# 获得创业板分类
# 获得风险警示板分类
def get_st_classified(engine):
    try:
        df = ts.get_st_classified();
        df.to_sql('st_classified', engine, if_exists='append')
    except Exception, e:
        e.message


# 沪深300成分及权重
def get_hs300s(engine):
    try:
        df = ts.get_hs300s();
        df.to_sql('hs300s', engine, if_exists='append')
    except Exception, e:
        e.message


# 上证50成分股
def get_sz50s(engine):
    try:
        df = ts.get_sz50s();
        df.to_sql('sz50s', engine, if_exists='append')
    except Exception, e:
        e.message


# 中证500成分股
def get_zz500s(engine):
    try:
        df = ts.get_zz500s();
        df.to_sql('zz500s', engine, if_exists='append')
    except Exception, e:
        e.message




# 获取宏观经济数据 -存款利率
def get_deposit_rate(engine):
    try:
        df = ts.get_deposit_rate()
        df.to_sql('deposit_rate', engine, if_exists='append')
    except Exception, e:
        e.message
# 获取宏观经济数据 -贷款利率
def get_loan_rate(engine,):
    try:
        df = ts.get_loan_rate()
        df.to_sql('loan_rate', engine, if_exists='append')
    except Exception, e:
        e.message

# 获取宏观经济数据 -存款准备金绿
def get_rrr(engine,year, quarter):
    try:
        df = ts.get_rrr()
        df.to_sql('rrr', engine, if_exists='append')
    except Exception, e:
        e.message
# 获取宏观经济数据 -货币供应量
def get_money_supply(engine,):
    try:
        df = ts.get_money_supply()
        df.to_sql('money_supply', engine, if_exists='append')
    except Exception, e:
        e.message
# 获取宏观经济数据 -国内生产总值（年度）
def get_gdp_year(engine):
    try:
        df = ts.get_gdp_year()
        df.to_sql('gdp_year', engine, if_exists='append')
    except Exception, e:
        e.message
# 获取宏观经济数据 -国内生产总值（季度）
def get_gdp_quarter(engine):
    try:
        df = ts.get_gdp_quarter()
        df.to_sql('gdp_quarter', engine, if_exists='append')
    except Exception, e:
        e.message
# 三大需求对gdp贡献
def get_gdp_for(engine):
    try:
        df = ts.get_gdp_for()
        df.to_sql('gdp_for', engine, if_exists='append')
    except Exception, e:
        e.message
# 三大需求对gdp拉动
def get_gdp_pull(engine):
    try:
        df = ts.get_gdp_pull()
        df.to_sql('gdp_pull', engine, if_exists='append')
    except Exception, e:
        e.message
# 三大产业贡献率
def get_gdp_contrib(engine):
    try:
        df = ts.get_gdp_contrib()
        df.to_sql('gdp_contrib', engine, if_exists='append')
    except Exception, e:
        e.message
# 居民价格消费指数
def get_cpi(engine):
    try:
        df = ts.get_cpi()
        df.to_sql('cpi', engine, if_exists='append')
    except Exception, e:
        e.message
# 工业品出厂价格指数
def get_ppi(engine):
    try:
        df = ts.get_ppi()
        df.to_sql('ppi', engine, if_exists='append')
    except Exception, e:
        e.message


# 龙虎榜数据
def get_top_list(engine,date):
    try:
        df = ts.top_list(date)
        df.to_sql('top_list', engine, if_exists='append')
    except Exception, e:
        e.message
# 每日龙虎榜数据
def cap_tops(engine,days,retry_count,pause):
    try:
        df = ts.cap_tops(days,retry_count,pause)
        df.to_sql('cap_tops', engine, if_exists='append')
    except Exception, e:
        e.message


# 个股上榜统计
def cap_tops(engine,days,retry_count,pause):
    try:
        df = ts.cap_tops(days,retry_count,pause)
        df.to_sql('cap_tops', engine, if_exists='append')
    except Exception, e:
        e.message
# 营业部上榜统计
def broker_tops(engine,days,retry_count,pause):
    try:
        df = ts.broker_tops(days,retry_count,pause)
        df.to_sql('broker_tops', engine, if_exists='append')
    except Exception, e:
        e.message
# 机构席位追踪
def inst_tops(engine,days,retry_count,pause):
    try:
        df = ts.inst_tops(days,retry_count,pause)
        df.to_sql('inst_tops', engine, if_exists='append')
    except Exception, e:
        e.message
# 机构成交明细
def inst_detail(engine,retry_count,pause):
    try:
        df = ts.inst_detail(retry_count,pause)
        df.to_sql('inst_detail', engine, if_exists='append')
    except Exception, e:
        e.message
# 获得指定季度的业绩报告数据，去掉重复值
def get_report_data(conn,engine,year,quarter):
    try:
        print "report data"
        df = ts.get_report_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_report_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()
        df.to_sql('stock_report_data', engine, if_exists='append',index=False)
    except Exception, e:
        print e.message
# 获得指定季度的盈利能力,去掉重复值
def get_profit_data(conn,engine,year,quarter):
    try:
        df = ts.get_profit_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_profit_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        print df
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()
        df.to_sql('stock_profit_data', engine, if_exists='append',index=False)
    except Exception, e:
        e.message
# 获得指定季度的营运能力数据，,去掉重复值
def get_operation_data(conn,engine,year,quarter):
    try:
        df = ts.get_operation_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_operation_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()

        df.to_sql('stock_operation_data', engine, if_exists='append',index=False)
    except Exception, e:
        e.message
# 获得指定季度的成长能力数据，,去掉重复值
def get_growth_data(conn,engine,year,quarter):
    try:
        df = ts.get_growth_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_growth_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()

        df.to_sql('stock_growth_data', engine, if_exists='append',index=False)
    except Exception, e:
        e.message
# 获得指定季度的偿债能力数据，,去掉重复值
def get_debtpaying_data(conn,engine,year,quarter):
    try:
        df = ts.get_debtpaying_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_debtpaying_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()

        df.to_sql('stock_debtpaying_data', engine, if_exists='append',index=False)
    except Exception, e:
        e.message
# 获得指定季度的现金流量表能力数据，,去掉重复值
def get_cashflow_data(conn,engine,year,quarter):
    try:
        df = ts.get_cashflow_data(year,quarter)
        reportDF = pd.read_sql("select * from stock_cashflow_data where year='"+str(year)+"' and quarter='"+str(quarter)+"'",conn)
        df.insert(0,'year',year)
        df.insert(0,'quarter',quarter)
        df.append(reportDF)
        df.drop_duplicates()

        df.to_sql('stock_cashflow_data', engine, if_exists='append',index=False)
    except Exception, e:
        e.message

#获得日k线数据中一直股票的最大时间
def get_day_maxdate(conn,stockno):
    try:
        sql = "select max(date) maxdate from stock_day_data where code='"+stockno+"'"
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            print sssj
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得周线线数据中股票的最大时间
def get_week_maxdate(conn,stockno):
    try:
        sql = "select max(date) maxdate from stock_week_data where code='"+stockno+"'"

        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得月K线数据中一直股票的最大时间
def get_month_maxdate(conn,stockno):
    try:
        sql = "select max(date) maxdate from stock_month_data where code='"+stockno+"'"
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0]
        cursor.close()

        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得前复权数据中一直股票的最大时间
def get_qfq_maxdate(conn,stockno):
    try:
        sql = "select max(date) maxdate from stock_qfq_data where code='"+stockno+"'"
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        for r in cursor:
             maxdate = r[0][0:10]
        cursor.close()
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
#获得不复权stock_bfq_data表中的一只股票的最大时间
def get_bfq_maxdate(conn,stockno):
    try:
        sql = "select max(date) maxdate from stock_bfq_data where code='"+stockno+"'"
        cursor = conn.cursor()
        n = cursor.execute(sql)
        maxdate = ''
        print n
        for r in cursor:
             if r[0] is None:
                 print "r is none"
                 maxdate=''
             else:
                print "bfq_max_date"
                maxdate = r[0][0:10]
                print "bfq_max_date1"
        cursor.close()
        if maxdate=='':
            stockDf =ts.get_stock_basics()
            sssj = str(stockDf.ix[stockno]['timeToMarket']) #上市日期YYYYMMDD
            print sssj
            return  dateutil.convertDate(sssj)
        return dateutil.get_next_day(maxdate)
    except Exception,e:
        print e.message
