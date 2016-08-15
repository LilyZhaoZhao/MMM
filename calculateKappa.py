#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

import numpy as np

def metrics(pre1,pre2,classN=2):
    k1=np.zeros([classN,])
    k2=np.zeros([classN,])
    kx=np.zeros([classN,])
    n=np.size(pre1)
    for i in range(n):
        p1=pre1[i]
        p2=pre2[i]
        k1[p1]=k1[p1]+1
        k2[p2]=k2[p2]+1
        if p1==p2:
            kx[p1]= kx[p1]+1

    pe=np.sum(k1*k2)/n/n
    pa=np.sum(kx)/n
    kappa=(pa-pe)/(1-pe)
    return kappa

# 自己写的计算kappa值
def calKappa(p,r,classN = 16):
    cList = [[0]*3 for i in range(classN)] #存储内容为： 预测为该类别的个数，实际为该类别的个数，预测为该类别正确的个数
    n = len(p)
    for i in range(n):
        cList[int(p[i])-1][0] += 1
        cList[int(r[i])-1][1] += 1
        if p[i]==r[i]:
            cList[int(r[i])-1][2] += 1
#    return cList

#def calAccuracy(cList, classN = 16):
    po = 0
    sum1 = 0
    sum2 = 0
    #print '每一类的预测正确的个数，每一类实际的ap个数: '
    rightAp = []
    realAp = []
    for i in range(classN):
        sum1 += cList[i][2]
        sum2 += (cList[i][0] * cList[i][1])
        rightAp.append(cList[i][2])
        realAp.append(cList[i][1]) #每一类的预测正确的个数，每一类实际的ap个数

    fw1.write(str(rightAp[0]))
    for i in range(1, classN):
        fw1.write(','+str(rightAp[i]))
    for i in range(classN):
        fw1.write(','+str(realAp[i]))
    fw1.write('\n')

    po = float(sum1)/n #就是准确率
    pe = float(sum2)/(n**2)
    kappa = float(po - pe)/(1 - pe)
    fw2.write(str(po)+','+str(kappa)+'\n') #准确率，kappa值


def outputFunc(day):
    ss = s+"_03"+str(day)+"_predictCtgy"
    fr = open(ss,'r') #szPoiba_0321_predictCtgy2
    p0 = [] #存储每个权重对的预测值
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    p9 = []
    p10 = []
    r = []
    for l in fr.readlines():
        l = l.strip('\n')
        l = l.split(',')
        if(int(l[12])==0): #对未知类型ap的预测结果的kappa值
#        if(len(l)==16):   #所有ap的预测结果的kappa值
            p0.append(int(l[1]))
            p1.append(int(l[2]))
            p2.append(int(l[3]))
            p3.append(int(l[4]))
            p4.append(int(l[5]))
            p5.append(int(l[6]))
            p6.append(int(l[7]))
            p7.append(int(l[8]))
            p8.append(int(l[9]))
            p9.append(int(l[10]))
            p10.append(int(l[11]))
            r.append(int(l[13]))
    fr.close()

    cl0 = calKappa(p0,r,16)
    cl1 = calKappa(p1,r,16)
    cl2 = calKappa(p2,r,16)
    cl3 = calKappa(p3,r,16)
    cl4 = calKappa(p4,r,16)
    cl5 = calKappa(p5,r,16)
    cl6 = calKappa(p6,r,16)
    cl7 = calKappa(p7,r,16)
    cl8 = calKappa(p8,r,16)
    cl9 = calKappa(p9,r,16)
    cl10 = calKappa(p10,r,16)






if __name__=="__main__":
    s = cmdArgv[1] #szPoiba
    fw1 = open(s+"_numOfRightAndRealEachCtgy16_22",'w') #每一天，每种权值，一行为 每类的正确个数，每类的实际个数
    fw2 = open(s+"_accuracyAndKappa16_22",'w')#每一天，每种权值，一行为 对未知ap的预测准确率，kappa
    for day in range(16,23):
        outputFunc(day)
    fw1.close()
    fw2.close()
