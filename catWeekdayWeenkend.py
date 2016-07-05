#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

#将poi数据中的catagory用数字代替
def catTwoDays(s1, s2):
    with open(s1,'r') as f1: # szPoiba_0316_intCatagory
        datas1 = f1.readlines()
    with open(s2,'r') as f2: # szPoiba_0321_intCatagory
        datas2 = f2.readlines()
    fw = open(s1+s2+'_intCatagory','w')# szPoiba_0316szPoiba_0321_intCatagory

    macList = []
    for line in datas1:
        line = line.strip('\n')
        data = line.split('|')
        if(len(data)==8):
            mac = data[2]
            macList.append(mac)
    for line in datas2:
        line = line.strip('\n')
        data = line.split('|')
        if(len(data)==8):
            ap = data[2]
            if ap in macList:
                fw.write(line+'\n')
    fw.close()
    f1.close()
    f2.close()

#对数据按经纬度排序：先按照第2列（longitude）排序，在按照第3列（latitude）排序
def sortByLonLat(s1,s2):
    with open(s1,'r') as f: # data/bupt/apnum/buptpoi16_22_intCatagory
        datas = f.readlines()
    fw = open(s2,'w')# data/bupt/apnum/buptpoi16_22_intCatagory_sorted

    sortList = []
    for line in datas:
        sortList.append(line)

    sortList.sort(key=lambda x:(x.split('|')[2], x.split('|')[3]))

    for l in sortList:
        fw.write(l)

    fw.close()
    f.close()


if __name__=="__main__":

    catagory2int(cmdArgv[1])

    #sortByLonLat(cmdArgv[1],cmdArgv[2])
