# coding=utf-8
__author__ = 'litao'
from sqlalchemy import create_engine
import tushare as ts

try:

    df = ts.get_hist_data('600848')
    engine = create_engine('mysql://root:123456@127.0.0.1/stock?charset=utf8')
    df.insert(0,'code','600848')
    #df.to_sql('hist_data',engine,if_exists='append')
    df = ts.get_stock_basics()
    df.to_csv('d:\\stock_basic.csv')
    #df.to_sql('stock_basics',engine,if_exists='append')



except Exception,e:
    print e
