#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: __init__.py.py
@time: 2016/1/29 0029 下午 10:57
"""

import os
import numpy as np


def getFileName(filename):
    basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    datadir = os.path.join(basedir, 'data')
    datafile = os.path.join(datadir, filename)
    return datafile


def getFileData(filename, coldescriptor, positive=None, negative=None, delimiter=','):
    """

    :param filename:
    :param coldescriptor: [(columnname,type),(columnname,type)]
     type catprop,floatprop,class
    :param positive 分类数据中用于正例的值，作为1
    :param negative 分类数据中用于负例的值，作为-1
    :return: data,columnnames,proptypes
    """

    data = []
    classArry=[]
    absfilename = getFileName(filename)
    file = open(absfilename)
    for line in file:
        columns = line.strip('\n').split(delimiter)
        vector = []
        cls = None
        for idx, value in enumerate(columns):
            if coldescriptor[idx][1] == 'catprop':
                vector.append(value)
            elif coldescriptor[idx][1] == 'floatprop':
                vector.append(float(value))
            elif coldescriptor[idx][1] == 'class':
                cls = value
                if positive and value == positive:
                    cls = 1.0
                if negative and value == negative:
                    cls = -1.0
        vector.append(cls)
        data.append(vector)
        classArry.append(cls)

    columnnames = [elem[0] for elem in coldescriptor]
    columntypes = [elem[1] for elem in coldescriptor]

    dataarr = np.array(data)

    return dataarr, columnnames,classArry


cds1 = [(u'年龄', 'catprop'), (u'收入层次', 'catprop'),
        (u'学生', 'catprop'), (u'信用评级', 'catprop'),
        (u'购买', 'class')]
loadBuyComputerData = lambda: getFileData('buyComputer.data', cds1)
loadBuyComputerData2 = lambda: getFileData('buyComputer2.data', cds1)
cds2 = [('c1', 'catprop'), ('c2', 'catprop'),
        ('c2', 'catprop'), ('c4', 'catprop'),
        ('buy', 'class')]
loadHealthData = lambda: getFileData('health.data', cds2,positive='i100',negative='i500')

if __name__ == '__main__':
    # data,cols,coltype = loadBuyComputerData()
    # print data
    # print cols
    # print coltype
    #
    data, cols, coltype = loadHealthData()
    print data
    print type(data),data.shape
    print cols
    print coltype
