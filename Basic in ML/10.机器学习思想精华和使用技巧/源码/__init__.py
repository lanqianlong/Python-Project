#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: __init__.py.py
@time: 2016/2/9 0009 下午 6:07
"""
import numpy as np
def ArmijoBacktrack(fun,d,x,alpha,c=0.3):
    """

    :param fun: 目标函数，是个函数
    :param d: 当前点x处的导数，因为要寻找的是当前点处的最佳学习速率alpha，当前点的梯度是固定的，是个值，向量
    :param x: 当前点，向量
    :param alpha: 初始学习速率
    :param c: 参数c
    :return: 返回找到的学习速率
    """
    now=fun(x)
    nextv=fun(x-alpha*d)

    count=50
    while nextv < now and count>0:
        """
        寻找最大的alpha
        """
        alpha = alpha*2
        nextv=fun(x-alpha*d)
        count -=1

    iterstep=50
    slope=np.dot(d,d)
    while nextv > now - slope * c * alpha and iterstep>0:
        """
        折半搜索
        """
        alpha=alpha/2
        nextv=fun(x-alpha*d)
        iterstep-=1
    return alpha



def GradientDescent(fun,dfun,x,alpha,itersteps):
    for i in range(itersteps):
        d=dfun(x)
        x-= d * alpha
        print fun(x)

def ArmijoGradientDescent(fun,dfun,x,alpha,itersteps):
    for i in range(itersteps):
        d=dfun(x)
        alpha=ArmijoBacktrack(fun,d,x,alpha)
        x-=d*alpha
        print '{},{}'.format(alpha,fun(x))

def fun1(args):
    """
    x^2+y^4+z^6
    :param args:
    :return:
    """
    return args[0]**2+args[1]**4+args[2]**6

def dgfun1(args):
    """
    x^2+y^4+z^6
    :param args:
    :return:
    """
    return np.array([2*args[0],4*args[1]**3,6*args[2]**5])

if __name__=='__main__':
    args=np.array([3,2,2],dtype=float)


    # GradientDescent(fun1,dgfun1,args,0.01,1000)
    ArmijoGradientDescent(fun1,dgfun1,args,0.01,1000)

    # print fun1(args)
    # print 9+16+64
    # print dgfun1(args)
    #print ArmijoBacktrack(fun1,d,args,0.1)
    # ArmijoBacktrack(fun1,dgfun1,args,0.001)
    # GradientDescent(fun1,dgfun1,args,0.001,10000)

    # d=dgfun1(args)