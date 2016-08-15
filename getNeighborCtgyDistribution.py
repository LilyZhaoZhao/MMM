#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

#from numpy import *

minDistance = 0.044 #ap间的距离在这个范围内(经纬度都相差0.001)时，列为邻居
ctgyNum = 16 #其中未知ap的类别为0
kValue = 3 #取前k个最相似的ap，k值取单数，因为是多数投票

#欧几里得距离：值越小表示距离越近
def euclideanDistance(vector1,vector2):
    d = 0
    d = (float(vector1[0])-float(vector2[0]))**2 + (float(vector1[1])-float(vector2[1]))**2
    return d**0.5

#余弦距离[-1,1]: 值越大表示越相似
def cos(vector1,vector2):
    dot_product = 0.0
    normA = 0
    normB = 0
    for i in range(len(vector1)):
        dot_product += float(vector1[i]) * float(vector2[i])
        normA += float(vector1[i])**2
        normB += float(vector2[i])**2
    if normA == 0.0 or normB==0.0:
        return None
    else:
        return float(dot_product) / ((normA*normB)**0.5)

#得到两两ap之间的经纬度距离（欧几里得距离）相似度矩阵
def getDistanceMatrix():

    macDistance = {}
    macList = []
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




#得到在一定距离范围内的ap，返回每个ap的邻域内的类别分布
def nearestDistance(macDistance):
    macCtgyDistribution = {}
    for k,v in macDistance.items():
        mac = k
        distanceDict = v
        nearestMac = []
        for mac2,d in distanceDict.items():
            if d < minDistance:
                nearestMac.append(mac2)
        ctgy = [0]*ctgyNum
        numOfKnownAp = 0 #统计邻域内已知类型的ap个数
        for m in nearestMac:
            catagory = int(macCtgyTest[m])
#            catagory = int(macCtgyTrue[m]) #????????????????没有传入这个变量啊？？？

            if catagory > 0: #注意！！！！！！！！！！！！！！！！！！！这里要舍去类别为0的ap，不然会以为0也是一个类别
                ctgy[catagory-1] += 1
                numOfKnownAp += 1
        for i in range(len(ctgy)):
            ctgy[i] = float(ctgy[i])/len(nearestMac) #求每种类别在该mac的邻域内所占的比例
#        macCtgyDistribution[mac] = ctgy

#在新的macCtgyDistribution中加入了邻域内ap的个数，用于计算ap density；
#则macCtgyDistribution的结构为： dict[ap]=([类别分布向量],#邻域内所有的ap,#已知类型的ap)
        macCtgyDistribution[mac] = (ctgy, len(nearestMac), numOfKnownAp)
    return macCtgyDistribution

#输入一个ap矩阵（可能是类别分布矩阵，也可能是使用模式矩阵），返回与该ap最相似的前k个ap的类别占比
def getDistribution(macCtgyDistribution):
    distribution = {}
    for m1 in macCtgyTest:
        macCosineList = []
        v1 = macCtgyDistribution[m1]
        for m2 in macCtgyTest:
            v2 = macCtgyDistribution[m2]
            macCosineList.append((m2,cos(v1,v2)))
        macCosineList.sort(reverse=True, key=lambda x:x[1])  # 逆序排列！！！！！

        ctgy = [0]*ctgyNum
        for i in range(kValue): #取前k个余弦值最大的ap
            mac = macCosineList[i][0]
            catagory = int(macCtgyTest[mac])
#            catagory = int(macCtgyTrue[mac])

            if catagory > 0:# 注意！！！！！！！！！！！！！！！！！！！这里要舍去类别为0的ap，不然会以为0也是一个类别
                ctgy[catagory-1] += 1
        for i in range(len(ctgy)):
            ctgy[i] = float(ctgy[i])/kValue #求前k=10个ap的类别所占的比例
        distribution[m1] = ctgy
    return distribution





if __name__=="__main__":

    # cmdArgv[1] = szPoiba_0316
    s1 = cmdArgv[1]
    fr1 = open(s1+'_intCatagory_block_trainset','r')#buptpoi16_22_intCatagory_block_trainset
    fr2 = open(s1+'_intCatagory_block_testset','r')#buptpoi16_22_intCatagory_block_testset

    macLonlat = {}
    macCtgyTrue = {}
    macCtgyTest = {}

    for data in fr1.readlines():
        data = data.strip('\n')
        data = data.split('|')
        mac = data[1]
        lon = data[2]
        lat = data[3]
        catagory = data[7]
        macLonlat[mac] = (lon,lat)
        macCtgyTrue[mac] = catagory
        macCtgyTest[mac] = catagory

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
        macCtgyTest[mac] = 0 #测试集的catagory设为0，表示未知
    fr2.close()



    macDistance1 = getDistanceMatrix()   # 需要改进：只需要计算未知poi与所有poi之间的距离，减少计算量；??????????????????????????????

    macCtgyDistribution1 = nearestDistance(macDistance1)

    macCtgyDistribution1_new = {} #存储每个ap对应的邻域的类型占比分布
    numOfApNeighbor = {} #存储每个ap的邻域数目
    numOfApNeighborKnown = {} #存储每个ap的邻域中已知类型的ap数目
    for m,v in macCtgyDistribution1.items():
        numOfApNeighbor[m] = v[1]
        numOfApNeighborKnown[m] = v[2]
        macCtgyDistribution1_new[m] = v[0]

#    distribution1 = getDistribution(macCtgyDistribution1)


    ctgyDict = {}
    for i in range(1,ctgyNum+1):
        ctgyDict[i] = [[0]*ctgyNum, 0]
    for m,v in macCtgyDistribution1_new.items():
        c = int(macCtgyTrue[m])
        for i in range(ctgyNum):
            ctgyDict[c][0][i] += v[i]
        ctgyDict[c][1] += 1

    for c,v in ctgyDict.items():
        count = float(v[1])
        if count == 0:
            break
        else:
            for i in range(ctgyNum):
                v[0][i] /= count

    fw2 = open(s1+'_ctgyNeighborCtgyDistribution3','w') # buptpoi23_predictCtgy or szPoiba_0316_predictCtgy
    for c,v in ctgyDict.items():
        fw2.write(str(c))
        for i in range(ctgyNum):
            fw2.write(',' +str(v[0][i])) #输出格式： mac, 预测的类别，用于预测的mac类别值，真实的mac类别值
        fw2.write('\n')
    fw2.close()






'''

    fr = open(s1+'_Utilization','r') # szPoiba_0316_Utilization
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

#    distribution2 = getDistribution(macUtilization)

    macPattern = {}# 连接邻域模式和使用模式的向量，即连接了macCtgyDistribution1_new ＋ macUtilization
    for m,v in macCtgyDistribution1_new.items():
        macPattern[m] = v+macUtilization[m]

    distribution_new = getDistribution(macPattern) #所以只需要求一个综合分布即可

#    theta1 = 0.4
#    theta2 = 0.6
    predictCtgy = {} #存储最终预测的每个ap的类别
#    for m,v1 in distribution1.items():
#        v2 = distribution2[m]
#        v = [0]*ctgyNum
#        for i in range(len(v)):
#            v[i] = theta1*v1[i] + theta2*v2[i]
#        c = v.index(max(v)) + 1 #所属的类别＝ 概率最大的那个值的下标
#        predictCtgy[m] = c

    for m,v in distribution_new.items():
        c = v.index(max(v)) + 1 #所属的类别＝ 概率最大的那个值的下标
        predictCtgy[m] = c
#    for m,c in predictCtgy.items():
#        print m, c, macCtgyTest[m], macCtgyTrue[m]

    fw1 = open(s1+'_predictCtgy','w') # buptpoi23_predictCtgy or szPoiba_0316_predictCtgy
    for m,c in predictCtgy.items():
        fw1.write(m +',' +str(c)+','+str(macCtgyTest[m])+','+str(macCtgyTrue[m])+','+str(numOfApNeighbor[m])+','+str(numOfApNeighborKnown[m]) +'\n') #输出格式： mac, 预测的类别，用于预测的mac类别值，真实的mac类别值
    fw1.close()
'''
