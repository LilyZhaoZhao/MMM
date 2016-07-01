#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

from numpy import *

#欧几里得距离
def euclideanDistance(vector1,vector2):
    d=0;
    for a,b in zip(vector1,vector2):
        d+=(float(a)-float(b))**2
    return d**0.5


#得到两两ap之间的经纬度距离（欧几里得距离）相似度矩阵
def getDistanceMatrix(macLonlat):

    macDistance = {}

    macList = macLonlat.keys() #表示dict中所有的mac，按顺序存储

    length = len(macList)
    for i in range(length):
        mac = macList[i]
        v1 = macLonlat[mac]
        distanceList = []
        for j in range(length):
            v2 = macLonlat[macList[j]]
            distanceList.append(euclideanDistance(v1, v2))
        macDistance[mac] = distanceList

    return macDistance




if __name__=="__main__":
    fr1 = open(cmdArgv[1],'r')#buptpoi16_22_intCatagory_block_trainset
    fr2 = open(cmdArgv[2],'r')#buptpoi16_22_intCatagory_block_testset

    macLonlat = {}
    macCtgyTrue = {}
    macCtgyPredict = {}

    for data in fr1.readlines():
        data = data.strip('\n')
        data = data.split('|')
        mac = data[1]
        lon = data[2]
        lat = data[3]
        catagory = data[7]
        macLonlat[mac] = (lon,lat)
        macCtgyTrue[mac] = catagory
        macCtgyPredict[mac] = catagory

    fr1.close()

    for data in fr2.readlines():
        data = data.strip('\n')
        data = data.split('|')
        mac = data[1]
        lon = data[2]
        lat = data[3]
        catagory = data[7]
        macLonlat[mac] = (lon,lat)
        macCtgyTrue[mac] = catagory
        macCtgyPredict[mac] = 0 #测试集的catagory设为0，表示未知
    fr2.close()

    macDistance = getDistanceMatrix(macLonlat)b   # 需要改进：只需要计算未知poi与所有poi之间的距离，减少计算量；??????????????????????????????

    fw = open(cmdArgv[3], 'w') #buptpoi16_22_intCatagory_distanceMatrix
    for mac in macDistance.keys():
        fw.write(mac)
        for d in macDistance[mac]:
            fw.write(','+str(d))
        fw.write(','+str(macCtgyPredict[mac])+','+str(macCtgyTrue[mac])+'\n')  #输出格式：mac,[macDistance],用于预测的mac类别值，真实的mac类别值
    fw.close()
