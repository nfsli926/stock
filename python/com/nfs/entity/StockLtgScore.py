# coding=utf-8
__author__ = 'litao'
class stockltgscore(object):
    #股票代码
    code = ''
    #统计时间
    scoredate = ''
    #价格因子
    priceitem = 0
    #流通盘因子
    ltpitem = 0.0
    #业绩因子
    yjitem = 0.0
    #净资产因子
    jzcitem = 0.0
    #总股本因子
    zgbitem = 0.0
    #得分
    score = 0.0
    #所属行业
    sshy = ''
    #流通盘分类
    ltgfl = ''


    def setCode(self,code):
        self.code = code
    def setScoredate(self,scoredate):
        self.scoredate = scoredate
    def setPriceitem(self,priceitem):
        self.priceitem = priceitem

    def setLtpitem(self,ltpitem):
        self.ltpitem = ltpitem
    def setYjitem(self,yjitem):
        self.yjitem = yjitem
    def setJzcitem(self,jzcitem):
        self.jzcitem = jzcitem
    def setZgbitem(self,zgbitem):
        self.zgbitem = zgbitem
    def setScoreitem(self,score):
        self.score = score
    def setSshyitem(self,sshy):
        self.sshy = sshy
    def setltgfl(self,ltgfl):
        self.ltgfl = ltgfl
    #设置相关的get方法
    def getCode(self):
        return self.code
    def getScoredate(self):
        return self.scoredate
    def getPriceitem(self):
        return self.priceitem
    def getLtpitem(self):
        return self.ltpitem
    def getYjitem(self):
        return self.yjitem
    def getJzcitem(self):
        return self.jzcitem
    def getZgbitem(self):
        return self.zgbitem
    def getScore(self):
        return self.score
    def getSshy(self):
        return self.sshy
    def getLtgfl(self):
        return self.ltgfl



