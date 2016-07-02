#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

from numpy import *

minDistance = 0.0014 #ap间的距离在这个范围内时，列为邻居
ctgyNum = 16 #其中未知ap的类别为0
kValue = 10 #取前k个最相似的ap

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
        distanceDict = {}
        for j in range(length):
            mac2 = macList[j]
            v2 = macLonlat[mac2]
            distanceDict[mac2] = euclideanDistance(v1, v2)
        macDistance[mac] = distanceDict
    return macDistance


def getUtilizationMatrix(macUtilization):

    macDistance ={} #存储每个ap之间的余弦相似度
    macList = macUtilization.keys() #表示dict中所有的mac，按顺序存储

    length = len(macList)
    for i in range(length):
        mac = macList[i]
        v1 = macUtilization[mac]
        distanceDict = {}
        for j in range(length):
            mac2 = macList[j]
            v2 = macUtilization[mac2]
            distanceDict[mac2] = cos(v1, v2) # 这里用余弦相似度
        macDistance[mac] = distanceDict
    return macDistance



#得到在一定距离范围内的ap，返回每个ap的邻域内的类别分布
def nearestDistance(macDistance,macCtgyPredict):
    macCtgyDistribution = {}
    for k,v in macDistance.items():
        mac = k
        distanceDict = v
        nearestMac = []
        for mac2,d in distanceDict.items():
            if d < minDistance:
                nearestMac.append(mac2)
        ctgy = [0]*ctgyNum
        for m in nearestMac:
            catagory = int(macCtgyPredict[m])
#            catagory = int(macCtgyTrue[m])

            if catagory > 0: #注意！！！！！！！！！！！！！！！！！！！这里要舍去类别为0的ap，不然会以为0也是一个类别
                ctgy[catagory-1] += 1
        for i in range(len(ctgy)):
            ctgy[i] = float(ctgy[i])/len(nearestMac) #求每种类别在该mac的邻域内所占的比例
        macCtgyDistribution[mac] = ctgy
    return macCtgyDistribution

#输入一个ap矩阵（可能是类别分布矩阵，也可能是使用模式矩阵），返回与该ap最相似的前k个ap的类别占比
def getDistribution(macCtgyDistribution, macCtgyPredict):

    distribution = {}
    for m1 in macCtgyPredict:
        macCosineList = []
        v1 = macCtgyDistribution[m1]
        for m2 in macCtgyPredict:
            v2 = macCtgyDistribution[m2]
            macCosineList.append((m2,cos(v1,v2)))
        macCosineList.sort(key=lambda x:x[1])

        ctgy = [0]*ctgyNum
        for i in range(kValue): #取前10个余弦值最大的ap
            mac = macCosineList[i][0]
            catagory = int(macCtgyPredict[mac])
#            catagory = int(macCtgyTrue[mac])

            if catagory > 0:# 注意！！！！！！！！！！！！！！！！！！！这里要舍去类别为0的ap，不然会以为0也是一个类别
                ctgy[catagory-1] += 1
        for i in range(len(ctgy)):
            ctgy[i] = float(ctgy[i])/kValue #求前k=10个ap的类别所占的比例
        distribution[m1] = ctgy
    return distribution





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

    macCtgyDistribution = nearestDistance(macDistance, macCtgyPredict)
    distribution1 = getDistribution(macCtgyDistribution, macCtgyPredict)

#    fw = open(cmdArgv[3], 'w') #buptpoi16_22_intCatagory_distanceMatrix
#    macList = macDistance.keys()

#    for mac in macList:
#        fw.write(mac)
#        for mac2 in macList:
#            d = macDistance[mac][mac2]
#            fw.write(','+str(d))
#        fw.write(','+str(macCtgyPredict[mac])+','+str(macCtgyTrue[mac])+'\n')  #输出格式：mac,[macDistance],用于预测的mac类别值，真实的mac类别值
#    fw.close()


    fr = open("0323",'r')
    macUtilization = {}

    for data in fr.readlines():
        data = data.strip('\n')
        data = data.split(',')
        mac = data[0]
        utilizationList = []
        for i in range(1,len(data)):
            utilizationList.append(data[i])
        macUtilization[mac] = utilizationList
    fr.close()

    distribution2 = getDistribution(macUtilization, macCtgyPredict)

    theta1 = 0.1
    theta2 = 0.9
    predictCtgy = {} #存储最终预测的每个ap的类别
    for m,v1 in distribution1.items():
        v2 = distribution2[m]
        v = [0]*ctgyNum
        for i in range(len(v)):
            v[i] = theta1*v1[i] + theta2*v2[i]
        c = v.index(max(v)) + 1 #所属的类别＝ 概率最大的那个值的下标
        predictCtgy[m] = c

    fw1 = open('buptpoi23_predictCtgy','w')
    for m,c in predictCtgy.items():
        fw1.write(m +',' +str(c)+','+str(macCtgyPredict[m])+','+str(macCtgyTrue[m]) +'\n') #输出格式： mac, 预测的类别，用于预测的mac类别值，真实的mac类别值
    fw1.close()

#    macCosine = getUtilizationMatrix(macUtilization)

#    fw2 = open("buptpoi16_cosineMatrix", 'w') #buptpoi16_cosineMatrix
#    macList2 = macCosine.keys()

#    for mac in macList2:
#        fw2.write(mac)
#        for mac2 in macList2:
#            d = macCosine[mac][mac2]
#            fw2.write(','+str(d))
#        fw2.write(','+str(macCtgyPredict[mac])+','+str(macCtgyTrue[mac])+'\n')  #输出格式：mac,[macDistance],用于预测的mac类别值，真实的mac类别值
#    fw2.close()
