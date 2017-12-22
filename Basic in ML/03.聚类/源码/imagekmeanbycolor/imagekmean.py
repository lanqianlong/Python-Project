#!/usr/bin/python
# encoding: utf-8


"""
@author: 大圣
@contact: excelchart@sina.cn
@file: imagekmean.py
@time: 2016/1/26 0026 下午 10:23
"""

import colorsys
from PIL import Image
import numpy as np
import os
from dataminer.kmean.kmean import  KMean
import shutil
class ImagesCluster(object):
    def __init__(self,imagedir,k):
        self._imageDir=imagedir
        self._image2VectorDir=os.path.join(imagedir,'image2vector')
        if not os.path.isdir(self._image2VectorDir):
            os.mkdir(self._image2VectorDir)
        self._imageVectorsFile=os.path.join(self._image2VectorDir,'images.txt')
        self._k=k
        for i in range(self._k):
            clusterDir=os.path.join(self._imageDir,'cluster-{}'.format(i))
            if not os.path.isdir(clusterDir):
                os.mkdir(clusterDir)

    def _loadImages(self):
        images = os.listdir(self._imageDir)
        imagesfiles=[os.path.join(self._imageDir,image) for image in images]
        return imagesfiles

    def _hsv2L(self,h,s,v):
        QH=0
        if (h<=20) or (h>315):
            QH=0
        if (h>20 and h<=40):
            QH=1
        if (h>40 and h<=75):
            QH=2
        if (h>75 and h<=155):
            QH=3
        if (h>155 and h<=190):
            QH=4
        if (h>190 and h<=271):
            QH=5
        if (h>271 and h<=295):
            QH=6
        if (h>295 and h<=315):
            QH=7

        QS = 0
        if (s>=0 and s<=0.2):
            QS=0
        if (s>0.2 and s<=0.7):
            QS=1
        if (s>0.7 and s<=1.0):
            QS=2

        QV = 0
        if (v>=0 and v<=0.2):
            QV=0
        if (v>0.2 and v<=0.7):
            QV=1
        if (v>0.7 and v<=1.0):
            QV=2

        L=9*QH+3*QS+QV
        assert L>=0 and L<=71
        return L


    def _getImageColorVector(self,image):
        originImage=Image.open(image)
        ndarr= np.array(originImage.convert('RGB'))
        rowcnt = ndarr.shape[0]
        colcnt=ndarr.shape[1]
        colors=ndarr.shape[2]

        LVector =  [0] * 12

        for oneRow in range(rowcnt):
            for oneCol in range(colcnt):
                r,g,b=ndarr[oneRow][oneCol]

                h,s,v=colorsys.rgb_to_hsv(r/255.,g/255.,b/255.)
                h=h*360
                l=self._hsv2L(h,s,v)
                LVector[l/6] +=1

        lsum=sum(LVector)
        result = [ v*1.0/lsum for v in LVector]
        print image,result
        return result

    def cluster(self):
        # images=self._loadImages()
        # file=open(self._imageVectorsFile,'w')
        # for oneImage in images:
        #     if not os.path.isdir(oneImage):
        #         lvector=self._getImageColorVector(oneImage)
        #         file.write(oneImage+',')
        #         file.write(','.join(map(str,lvector)))
        #         file.write('\n')
        # file.close()
        km=KMean(self._k)
        km.loadDataFiles([self._imageVectorsFile],0)
        km.normalized()
        km.kCluster()
        imagemembers=km.getMemberClusers()
        for idx,clusterid in enumerate(imagemembers):
            src=km._comment[idx]
            filename=os.path.basename(src)
            dest = os.path.join(os.path.join(self._imageDir,'cluster-{}'.format(clusterid)),filename)
            shutil.copyfile(src,dest)





if __name__=='__main__':
    basedir=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    imagedir=os.path.join(basedir,'images')
    imagecluster=ImagesCluster(imagedir,5)
    imagecluster.cluster()


