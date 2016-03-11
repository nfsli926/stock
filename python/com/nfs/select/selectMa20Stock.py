# coding=utf-8
import pandas as pd
import MySQLdb

# ========== 从原始csv文件中导入股票数据，以浦发银行sh600000为例

# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='stock',charset="utf8")
selectdate = "2016-03-09"
stock_data = pd.read_sql("select * from stock_day_data where ma20 between open and close and date='"+selectdate+"' ",conn)
#stock_data = pd.read_csv('stock data/sh600000.csv', parse_dates=[1])
print stock_data

# 将数据按照交易日期从远到近排序
stock_data.sort('code', inplace=True)

stock_data.to_csv('selectma20stock.csv', index=False)