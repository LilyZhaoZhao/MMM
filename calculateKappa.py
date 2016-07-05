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

if __name__=="__main__":

    fr = open(cmdArgv[1],'r') #szPoiba_0321_predictCtgy2
    p = []
    r = []
    for l in fr.readlines():
        l = l.strip('\n')
        l = l.split(' ')
        p.append(int(l[1]))
        r.append(int(l[3]))
    fr.close()
    print metrics(p,r,17)
