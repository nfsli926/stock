# coding=utf-8
# 2015年9月25创建
__author__ = 'litao'
try:
    print "testString"
    hy = '医药生物 — 生物制品'.decode("utf-8")
    print hy
    index = hy.index('—')-4
    print index

    print hy[0:index]
except Exception, e:
     print e.message