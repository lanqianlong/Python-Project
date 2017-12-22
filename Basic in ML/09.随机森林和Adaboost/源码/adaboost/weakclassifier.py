#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: weakclassifier.py
@time: 2016/1/30 0030 下午 1:44
"""
import numpy as np


class WeakClassifier(object):
    def __init__(self):
        pass

    def _stump(self, dataArray, colIdx, splitValue, cmpOperator):
        """
        会把这一列中，与给定的阈值splitValue 比较(cmpOperator)结果为True的设置为-1，其他的都是1
        :param dataArray:
        :param colidx:
        :param splitValue:
        :param cmpOperator: == ,!=
        :return:
        """
        resultArray = np.ones((dataArray.shape[0], 1))

        if cmpOperator == '==':
            resultArray[dataArray[:, colIdx] == splitValue] = -1
        if cmpOperator == '!=':
            resultArray[dataArray[:, colIdx] != splitValue] = -1

        return resultArray

    def train(self, dataArray, labelsVector, weightDMatrix):
        m, n = np.shape(dataArray)

        bestStump = {}
        bestPredicate = None
        minErrorRate = np.inf

        for i in range(n - 1):
            uniqueValues = np.unique(dataArray[:, i])


            for oneValue in uniqueValues:
                for cmpOperaor in ['==', '!=']:
                    stumpResultArray = self._stump(dataArray, i, oneValue, cmpOperaor)

                    errors=np.mat(np.ones((m,1)))
                    errors[stumpResultArray==np.mat(labelsVector).T] = 0
                    errorRate = weightDMatrix.T * errors

                    print 'column {} :cmpOperator {} : splitValue {} : errorRate {}'.format(i,cmpOperaor,oneValue,errorRate)

                    if errorRate<minErrorRate:
                        bestStump['colIdx'] = i
                        bestStump['splitValue'] = oneValue
                        bestStump['cmpOperator'] = cmpOperaor
                        bestPredicate = stumpResultArray.copy()
                        minErrorRate=errorRate

        return bestStump,minErrorRate,bestPredicate

    def predicate(self,data,colIdx,splitValue,cmpOperator):
        return self._stump(data,colIdx,splitValue,cmpOperator)

if __name__=='__main__':
    from dataminer.loaddata import loadHealthData
    import numpy as np

    dataArray,colNames,classLabels = loadHealthData()
    m=dataArray.shape[0]
    weightDMatrix=np.mat(np.ones((m,1))/m)
    weakcls=WeakClassifier()
    bestStump,errorRate,bestPredicate = weakcls.train(dataArray,classLabels,weightDMatrix)
    print bestStump
    print errorRate
