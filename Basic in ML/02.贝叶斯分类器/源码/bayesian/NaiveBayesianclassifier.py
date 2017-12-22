#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: NaiveBayesianclassifier.py
@time: 2016/1/21 0021 下午 10:19
"""
from dataminer.baseClassifier.baseClassifier import BaseClassifier


class NativeBayesianClassifier(BaseClassifier):
    def __init__(self, datafilename, fieldroles, delimiter):
        super(NativeBayesianClassifier, self).__init__(datafilename, fieldroles, delimiter)
        self._postProb = dict()  # 条件概率，后验概率 P(B|A)
        self._priorProb = dict()  # 先验概率 P(A)
        self._classStats=dict()
        self._categroyPropStatsByClass = dict()

        """
        {
            'class1':{
                col1:{
                        value1:10,
                        value2:20,
                        value3:30
                 },
                col2:{
                        value1:10,
                        value2:20,
                        value3:30
                }
            },
            'class2':{
            }
        }
        """

    def _baseStat(self):
        for idx, rcdClass in enumerate(self._data['class']):
            self._categroyPropStatsByClass.setdefault(rcdClass, {})
            self._classStats.setdefault(rcdClass,0)
            self._classStats[rcdClass] +=1
            for fieldIdx, fieldValue in enumerate(self._data['prop'][idx]):
                self._categroyPropStatsByClass[rcdClass].setdefault(fieldIdx, {})
                self._categroyPropStatsByClass[rcdClass][fieldIdx].setdefault(fieldValue, 0)
                self._categroyPropStatsByClass[rcdClass][fieldIdx][fieldValue] += 1


    def _computePriorProbability(self):
        recordsCnt=len(self._data['class'])
        for rcdClass,cnt in self._classStats.items():
            self._priorProb.setdefault(rcdClass,round(cnt*1./recordsCnt,2))


    def _computePostProbablity(self):
        for oneClass,classStats in self._categroyPropStatsByClass.items():
            self._postProb.setdefault(oneClass,{})
            thisClassCnt=self._classStats[oneClass]
            for oneColumn,valueStats in classStats.items():
                self._postProb[oneClass].setdefault(oneColumn,{})
                for oneValue,valueCnt in valueStats.items():
                    self._postProb[oneClass][oneColumn].setdefault(oneValue,round(valueCnt*1./thisClassCnt,3))




    def trainingModel(self):
        self._baseStat()
        self._computePriorProbability()
        self._computePostProbablity()

    def predicate(self,item):
        result=[]
        for oneClass,priorProp in self._priorProb.items():
            prop = priorProp
            for idx,fieldValue in enumerate(item):
                conditionProp = self._postProb[oneClass][idx].get(fieldValue,0)
                if conditionProp != 0:
                    prop = prop * conditionProp
            result.append((oneClass,prop))

        result.sort(key=lambda x:x[1],reverse=True)
        return result


