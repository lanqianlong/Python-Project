#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: distance.py
@time: 2016/1/18 0018 上午 11:06
"""


class Distance(object):
    @staticmethod
    def computeManhattanDistance(vector1,vector2,q=1):

        """

        :param vector1: [1,2,3,45,6]
        :param vector2: [1,2,4,56,7]
        :return:
        """
        distance=0.
        n=len(vector1)
        for i in range(n):
            distance +=pow(abs(vector1[i]-vector2[i]),q)
        return round(pow(distance,1.0/q),5)
    @staticmethod
    def computeEuDistance(vector1,vector2):
        return Distance.computeManhattanDistance(vector1,vector2,2)