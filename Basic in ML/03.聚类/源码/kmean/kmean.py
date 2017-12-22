#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: kmean.py
@time: 2016/1/24 0024 下午 5:17
"""
import random
from dataminer.mltools.stats.distance import Distance


class KMean(object):
    def __init__(self, k):
        self._data = []
        self._normalizeData = []
        self._memeberOfClusters = []
        self._maxIteration = None

        self._clusterCenters = []
        self._pointChangedNum = 0
        self._k = k
        self._comment = []
        # self._loadIirsDataFile(datafiles)
        # self._normalized()

    def _loadIirsDataFile(self, datafile):
        file = open(datafile)
        for lineIdx, line in enumerate(file):
            columns = line.strip('\n').split(',')[:4]
            floatColumns = map(float, columns)
            self._data.append(floatColumns)
            self._memeberOfClusters.append(lineIdx)
        file.close()

    def loadDataFiles(self, datafilenames, commentId, delimiter=','):
        for oneFile in datafilenames:
            file = open(oneFile)
            lineIdx = 0
            for line in file:
                vector = []
                columns = line.strip('\n').split(delimiter)
                for cid, value in enumerate(columns):
                    if cid == commentId:
                        self._comment.append(value)
                    else:
                        vector.append(float(value))
                self._data.append(vector)
                self._memeberOfClusters.append(lineIdx)
                lineIdx += 1

    def _getColumn(self, colIdx):
        column = [self._data[i][colIdx] for i in range(len(self._data))]
        return column

    def _getColumnMeanAndStd(self, column):
        sumx = 0.0
        sumx2 = 0.0
        for x in column:
            sumx += x
            sumx2 += x ** 2
        n = len(column)
        mean = sumx / n
        d = sumx2 / n - mean ** 2
        std = pow(d, 0.5)

        return (round(mean, 3), round(std, 3))

    def _getColumnMedian(self, column):
        columncopy = list(column)
        columncopy.sort()
        clen = len(columncopy)
        if clen % 2 == 0:
            return (columncopy[clen / 2] + columncopy[clen / 2 - 1]) / 2
        else:
            return columncopy[(clen - 1) / 2]

    def _normalizeOneColumn(self, column):
        cmedian = self._getColumnMedian(column)
        csum = sum([abs(x - cmedian) for x in column]) * 1.0
        asd = round(csum / len(column), 3)

        result = [round((x - cmedian) / asd, 3) for x in column]
        return result

    def normalized(self, normalize=False):
        if not normalize:
            self._normalizeData = self._data
        else:
            cols = len(self._data[0])
            rows = len(self._data)

            self._normalizeData = [[0] * cols for i in range(rows)]

            for i in range(len(self._data[0])):
                oneColumn = self._getColumn(i)
                result = self._normalizeOneColumn(oneColumn)

                for rowidx, value in enumerate(result):
                    self._normalizeData[rowidx][i] = result[rowidx]

    def _initializeCenters(self):
        randLineIdx = random.sample(range(len(self._data)), self._k)
        for lIdx in randLineIdx:
            self._clusterCenters.append(self._normalizeData[lIdx])

    def _selectCloestToCenters(self,point,centers):
        result = Distance.computeEuDistance(point,centers[0])
        for center in centers[1:]:
            distance=Distance.computeEuDistance(point,center)
            if distance < result:
                result=distance
        return result
    def _initailizeCentersByRoulette(self):
        self._clusterCenters=[]
        total=0
        firstCenter=random.choice(range(len(self._data)))
        self._clusterCenters.append(self._normalizeData[firstCenter])

        for i in range(self._k-1):
            weights = [self._selectCloestToCenters(x,self._clusterCenters) for x in self._data]
            total=sum(weights)
            weights = [w/total for w in weights]
            num = random.random()
            total=0.0
            x=-1
            while total<num:
                x+=1
                total += weights[x]
            self._clusterCenters.append(self._normalizeData[x])


    def _updateCenter(self):
        newClusterCenter = [[0] * len(self._normalizeData[0]) for i in range(self._k)]
        clusertMemberCnt = [0] * self._k
        for lineIdx, oneLine in enumerate(self._normalizeData):
            clusertMemberCnt[self._memeberOfClusters[lineIdx]] += 1
            for colIdx, oneColumn in enumerate(oneLine):
                newClusterCenter[self._memeberOfClusters[lineIdx]][colIdx] += oneColumn

        for i in range(self._k):
            for j in range(len(newClusterCenter[0])):
                self._clusterCenters[i][j] = newClusterCenter[i][j] * 1.0 / clusertMemberCnt[i]

    def _assignPointToClusters(self):
        self._pointChangedNum = 0
        for lineIdx, oneLine in enumerate(self._normalizeData):
            minDistance = 9999999
            clusterIdx = -1
            for centerIdx, oneCenter in enumerate(self._clusterCenters):
                distance = Distance.computeEuDistance(oneLine, oneCenter)
                if distance < minDistance:
                    clusterIdx = centerIdx
                    minDistance = distance
            if clusterIdx != self._memeberOfClusters[lineIdx]:
                self._memeberOfClusters[lineIdx] = clusterIdx
                self._pointChangedNum += 1

    def kCluster(self):
        changed = True
        # self._initializeCenters()
        self._initailizeCentersByRoulette()
        while changed:
            self._assignPointToClusters()
            if self._pointChangedNum < 2:
                changed = False
            else:
                self._updateCenter()
                changed = True

    def getMemberClusers(self):
        return self._memeberOfClusters
