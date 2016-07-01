#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

from numpy import *

#欧几里得距离：值越小表示距离越近
def euclideanDistance(vector1,vector2):
    d = (float(vector1[0])-float(vector2[0]))**2 + (float(vector1[1])-float(vector2[1]))**2
    return d**0.5

#余弦距离[-1,1]: 值越大表示越相似
def cos(vector1,vector2):
    dot_product = 0.0
    normA = 0
    normB = 0
    for i in range(len(vector1)):
        dot_product += int(vector1[i]) * int(vector2[i])
        normA += int(vector1[i])**2
        normB += int(vector2[i])**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return float(dot_product) / ((normA*normB)**0.5)

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


def getUtilizationMatrix():

    fr = open("apnum0316",'r')
    macUtilization = {}

    for data in fr.readlines():
        data = data.strip('\n')
        data = data.split(',')
        mac = data[0]
        utilizationList = []
        for i in range(1,len(data)):
            utilizationList.append(data[i])
        macUtilization[mac] = utilizationList

    macDistance ={} #存储每个ap之间的余弦相似度
    macList = macUtilization.keys() #表示dict中所有的mac，按顺序存储

    length = len(macList)
    for i in range(length):
        mac = macList[i]
        v1 = macUtilization[mac]
        distanceList = []
        for j in range(length):
            v2 = macUtilization[macList[j]]
            distanceList.append(cos(v1, v2)) #这里用余弦相似度
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

    macDistance = getDistanceMatrix(macLonlat)   # 需要改进：只需要计算未知poi与所有poi之间的距离，减少计算量；??????????????????????????????

    fw = open(cmdArgv[3], 'w') #buptpoi16_22_intCatagory_distanceMatrix
    for mac in macDistance.keys():
        fw.write(mac)
        for d in macDistance[mac]:
            fw.write(','+str(d))
        fw.write(','+str(macCtgyPredict[mac])+','+str(macCtgyTrue[mac])+'\n')  #输出格式：mac,[macDistance],用于预测的mac类别值，真实的mac类别值
    fw.close()

    macCosine = getUtilizationMatrix()

    fw2 = open("buptpoi16_cosineMatrix", 'w') #buptpoi16_cosineMatrix
    for mac in macDistance.keys():
        fw2.write(mac)
        for d in macDistance[mac]:
            fw2.write(','+str(d))
        fw2.write(','+str(macCtgyPredict[mac])+','+str(macCtgyTrue[mac])+'\n')  #输出格式：mac,[macCosine],用于预测的mac类别值，真实的mac类别值
    fw2.close()
