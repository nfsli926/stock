# coding=utf-8
__author__ = 'litao'
import util.dbutil as dbutil

try:
    dbutil.get_qfq_date('000002')
except Exception,e:
    e.message
