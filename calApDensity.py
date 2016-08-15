#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

def getApYesNo(i, s):
    ss = s+"_03"+str(i)+"_predictCtgy" #szPoiba_0316_predictCtgy
    fr = open(ss,'r')
    yesOrNo = 0

    for l in fr.readlines():
        l = l.strip('\n')
        l = l.split(',')
        numOfAp = l[14]
        numOfKnownAp = l[15]
        if int(l[12])==0:
            if l[11]==l[13]:
                yesOrNo = 1
            else:
                yesOrNo = 0
            densityList.append((yesOrNo,numOfAp,numOfKnownAp))
    fr.close()

if __name__=="__main__":

    s = cmdArgv[1] #szPoiba
    densityList = []
    for i in range(16,23):
        getApYesNo(i, s)

    numOfApList = []
    for t in densityList:
        numOfApList.append(int(t[1]))
    size = max(numOfApList)/20 + 1
    allApList = [0]*size
    rightApList = [0]*size
    for t in densityList:
        index = int(t[1])/20
        allApList[index] += 1
        if int(t[0])==1:
            rightApList[index] += 1

    fw = open(s+"_apDensity16_22",'w')
    for i in range(size):
        if allApList[i] == 0:     #注意，如果该区间内没有ap，则令准确率为整数0
            fw.write(str(i*20)+',0\n')  #按20为间隔，划分邻域ap个数的区间，则准确率就是：在这个区间内，预测正确的ap个数占比
        else:
            fw.write(str(i*20)+','+str(float(rightApList[i])/allApList[i])+'\n')

#    for m in densityList:
#        fw.write(str(m[0])+','+str(m[1])+','+str(m[2])+'\n')
    fw.close()
