# coding=utf-8
#2015年9月25创建
__author__ = 'litao'
import time
import datetime
import calendar as cal
#此处主要编写关于时间的相关函数并作整理
def get_next_day(mydate):
    time1 = datetime.datetime.strptime(mydate,'%Y-%m-%d')+datetime.timedelta(hours=24)
    currentday = time.strftime('%Y-%m-%d',time.localtime(time.mktime(time1.timetuple())))
    return  currentday
def get_pre_month():
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    lastMonth = first - datetime.timedelta(days=1)
    pre_month = time.strftime('%Y-%m',time.localtime(time.mktime(lastMonth.timetuple())))
    return  pre_month
def convertDate(sssj):
    timeArray = time.strptime(sssj, "%Y%m%d")
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
def get_next_month(currentMonth):
    print int(currentMonth[5:])
    d = cal.monthrange(int(currentMonth[0:4]),int(currentMonth[5:]))
    currentMonth_last_day = datetime.date(day=d[1],month=int(currentMonth[5:]), year=int(currentMonth[0:4]))
    next_Month = currentMonth_last_day + datetime.timedelta(days=1)
    next_Month = time.strftime('%Y-%m',time.localtime(time.mktime(next_Month.timetuple())))
    return  next_Month

if __name__ == "__main__":
    if get_next_month('2016-01'):
        print "1111"
    else:
        print "2222！"



