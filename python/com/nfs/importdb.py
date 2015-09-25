# coding=utf-8
__author__ = 'litao'
import util.dbutil as dbutil

try:
    dbutil.get_cpi()
except Exception,e:
    e.message
