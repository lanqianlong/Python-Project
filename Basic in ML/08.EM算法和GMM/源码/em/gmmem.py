#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: gmmem.py
@time: 2016/3/13 0013 下午 4:08
"""
import numpy as np
import math
import copy
class GMM(object):
    def __init__(self,data,k,mus,sigmas,maxiter=1000,epsilon=0.0000001):
        self._data=data
        self._k=k
        self._data=data
        self._distribs = np.zeros((k,len(data)))
        self._sigmas = sigmas
        self._mus= mus
        self._maxiter=maxiter
        self._epsilon=epsilon

    def guass(self,x,sigma,mu):
        exponent = math.exp(-(math.pow(x-mu,2)/(2*math.pow(sigma,2))))
        return (1 / (math.sqrt(2*math.pi) * sigma)) * exponent

    def e_step(self):
        for i,onedata in enumerate(self._data):
            sump=0.
            for j,oneclass in enumerate(range(self._k)):
                p=self.guass(onedata,self._sigmas[j],self._mus[j])
                self._distribs[j,i]=p
                sump+=p
            for j in range(self._k):
                self._distribs[j,i] = self._distribs[j,i] / sump
        # print self._distribs


    def m_step(self):
        print self._sigmas
        print self._mus
        sum_x=[0.0] * self._k
        sum_n=[0.0] * self._k
        # sum_x_square = [0.0] * self._k
        for idx in range(len(self._data)):
            for i in range(self._k):
                x = self._distribs[i,idx] * self._data[idx]
                sum_x[i] += x
                sum_n[i] += self._distribs[i,idx]
                # sum_x_square[i] += self._distribs[i,idx] * math.pow(x,2)
        for i in range(self._k):
            self._mus[i] = sum_x[i] / sum_n[i]
            # self._sigmas[i] = math.sqrt(sum_x_square[i] / sum_n[i] - math.pow(self._mus[i],2))

        for i in range(self._k):
            sum_s=0.0
            for idx in range(len(self._data)):
                dev= self._distribs[i,idx] * self._data[idx] - self._mus[i]
                dev2= math.pow(dev,2) * self._distribs[i,idx]
                sum_s+= dev2
            self._sigmas[i]=math.sqrt(sum_s/sum_n[i])
            # x1=sum_x_square[i]/sum_n[i]
            # x2=x1-math.pow(self._mus[i],2)
            # x3=math.sqrt(x2)



            # self._sigmas=math.pow(sum_x_square[i]/sum_n[i] - math.pow(self._mus[i],2),0.5)

        print self._sigmas
        print self._mus
        print '*************************'

    def train(self):
        for step  in range(self._maxiter):
            old_mu=copy.deepcopy(self._mus)
            self.e_step()
            self.m_step()
            err=0.0
            for i in range(self._k):
                err += abs(old_mu[i] - self._mus[i])
            if err <self._epsilon:
                print '迭代 %d' % step
                break

        print self._distribs



def prepareData(n,mu,sigma):
    data=np.zeros((1,n))
    z=np.random.normal(size=n)
    data=z*sigma + mu
    return data

if __name__=='__main__':

    datasize=[10,20,30]
    mus = [175.0 , 155.0 , 0.80]
    sigmas=[2.0 , 2.0, 2.0]
    data=np.zeros((2,sum(datasize)))
    sn = 0
    for id,n in enumerate(datasize):
        x1=prepareData(n,mus[id],sigmas[id])
        data[0,sn:sn+n] = x1
        data[1,sn:sn+n] =id
        sn += n

    # print data
    mus2=[140.0,190.0,.4]
    gmm=GMM(data[0,:],len(mus),mus2,sigmas)
    gmm.train()





