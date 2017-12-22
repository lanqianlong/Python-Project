#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: knnclassfier.py
@time: 2016/1/19 0019 下午 2:46
"""

from dataminer.baseClassifier.baseClassifier import BaseClassifier
from dataminer.mltools.stats.distance import Distance
import operator
class KNNClassifier(BaseClassifier):
    def __init__(self,traingfilesname,fieldsrols,delimiter,k=10):
        super(KNNClassifier,self).__init__(traingfilesname,fieldsrols,delimiter)
        self.k=k



    def _findNearestNeighbor(self,item):
        neighbors=[]
        for idx,onerecord in enumerate(self._data['prop']):
            distance=Distance.computeManhattanDistance(onerecord,item)
            neighbors.append([idx,distance,self._data['class'][idx]])

        neighbors.sort(key=lambda x:x[1])

        nearestk={}
        for i in range(self.k):
            nearestk.setdefault(neighbors[i][2],0)
            nearestk[neighbors[i][2]]+=1

        return nearestk

    def predicate(self,item):
        nearestk=self._findNearestNeighbor(item)
        ps=sorted(nearestk.items(),key=lambda x:x[1],reverse=True)
        return ps[0][0]
