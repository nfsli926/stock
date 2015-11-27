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
    #df.rename(columns={'$a': 'a', '$b': 'b'}, inplace=True)
    df.rename(columns={'stockno':'股票代码','stockname':'股票名称','sshy':'所属杨业','sjgn':'涉及概念','brspj':'本日收盘价','syspj':'上月收盘价','ltg':'流通股','zgb':'总股本','jlr':'净利润','yysr':'营业收入','mgjzc':'每股净资产','mgsy':'每股收益','jlrzzl':'净利润增长率','mgxjl':'每股现金流','mggjj':'每股公积金','mgwfplr':'每股未分配利润','dtsyl':'动态市盈率','sjl':'市净率','ltsz':'流通市值','zsz':'总市值','jjsj':'解禁时间','mlv':'毛利率','jlv':'净利率','roe':'ROE','fzl':'负债率','importdate':'导入日期','sssj':'上市时间','cplx':'产品类型','ssdy':'所属地域','lrzy':'利润总额','tenholder':'十大持股人','gdrs':'股东人数'}, inplace=True)
    print df
    #df.to_csv('d:\\stock_basic.csv')
    #df.to_sql('stock_basics',engine,if_exists='append')



except Exception,e:
    print e
