#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

def getNumNeighbor(i, s):
    ss = s+"_03"+str(i)+"_predictCtgy" #szPoiba_0316_predictCtgy
    fr = open(ss,'r')
    yesOrNo = 0

    for l in fr.readlines():
        l = l.strip('\n')
        l = l.split(',')
        numOfAp = l[14]
        ctgy = int(l[13])
        ctgyNumNeighbor[ctgy-1].append(numOfAp)
    fr.close()

if __name__=="__main__":

    s = cmdArgv[1] #szPoiba
    ctgyNumNeighbor = [[] for i in range(16)]
    for i in range(16,23):
        getNumNeighbor(i, s)

    fw = open(s+"_ctgyNumOfNeighbor16_22",'w')
    for i in range(16):
        ctgyNumNeighbor[i] = set(ctgyNumNeighbor[i])
        fw.write(str(i+1))
        for j in ctgyNumNeighbor[i]:
            fw.write(','+str(j))
        fw.write('\n')
    fw.close()
