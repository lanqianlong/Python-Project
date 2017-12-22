#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: adaboost.py
@time: 2016/1/29 0029 下午 10:56
"""
import numpy as np
from dataminer.adaboost.weakclassifier import WeakClassifier
import math


class AdaBoost(object):
    def __init__(self, weaker=WeakClassifier(),positive='i100',negative='i500'):
        self._worker = weaker
        self._weakerClassifers = []
        self._positive=positive
        self._negative=negative




    def train(self, dataArray, labelVector, M=40):
        """

        :param dataArray:
        :param labelVector:
        :param M: maxmiun weaker classifier count
        :return:
        """
        m, n = np.shape(dataArray)
        weightDMatrix = np.mat(np.ones((m, 1)) / m)
        aggPredicate = np.mat(np.zeros((m, 1)))

        for i in range(M):
            oneStump, errorRate, onePredicate = self._worker.train(dataArray, labelVector, weightDMatrix)
            assert errorRate<0.5

            alpha = float(0.5 * np.log((1 - errorRate) / max(errorRate, 1e-16)))
            assert alpha>0
            expon = np.multiply(-1 * alpha * onePredicate, np.mat(labelVector).T)
            Z = np.exp(expon)

            weightDMatrix = np.multiply(weightDMatrix, Z)
            weightDMatrix = weightDMatrix / weightDMatrix.sum()

            oneStump['alpha'] = alpha
            self._weakerClassifers.append(oneStump)

            aggPredicate += onePredicate * alpha

            aggErrors = np.multiply(np.sign(aggPredicate) != np.mat(labelVector).T,
                                    np.ones((m, 1)))
            aggErrorRate = aggErrors.sum() / m
            if aggErrorRate == 0:
                break

    def predicate(self,data):
        translateResult = lambda x:self._positive if x==1 else self._negative
        aggResult=0
        mdata=data
        if isinstance(data,list):
            mdata=np.mat(data)

        for oneStump in self._weakerClassifers:
            oneResult= self._worker.predicate(mdata,
                                              oneStump['colIdx'],
                                              oneStump['splitValue'],
                                              oneStump['cmpOperator'])

            aggResult += oneResult * oneStump['alpha']
        return translateResult(np.sign(aggResult))

if __name__ == '__main__':
    from dataminer.loaddata import loadHealthData

    dataArray, colnames, classArray = loadHealthData()


    ada = AdaBoost()

    ada.train(dataArray, classArray, 40)
    for x in  ada._weakerClassifers:
        print x

    for oneData in dataArray:
        print ada.predicate([oneData[0:4]])