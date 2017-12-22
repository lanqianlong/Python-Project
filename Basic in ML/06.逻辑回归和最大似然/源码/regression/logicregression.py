#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: logicregression.py
@time: 2016/2/13 0013 上午 10:21
"""
import math
import numpy as np
class LogisticRegression(object):
    def __init__(self):
        self.weight=None

    def sigmod(self,x):
        return 1.0/(1.0+math.exp(-x))

    def gradientAscent(self,data,lables):
        x=np.mat(data)
        y=np.mat(lables).transpose()
        m,n=np.shape(x)
        alpha = 0.001
        step = 1000
        weight = np.ones((n,1))
        for i in range(step):
            h=self.sigmod(x*weight)
            error=(y-h)
            weight= weight + alpha * x.transpose()*error

    def predict(self,x):
        prob = self.sigmod(np.dot(x,self.weight))
        if prob > 0.5 :
            return 1.0
        else :
            return 0.0
