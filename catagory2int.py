#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv

#将poi数据中的catagory用数字代替
def catagory2int(s1):
    with open(s1,'r') as f: # data/bupt/apnum/buptpoi16_22 or szPoi_0316
        datas = f.readlines()
    fw = open(s1+'_intCatagory','w')# data/bupt/apnum/buptpoi16_22_intCatagory or szPoi_0316_intCatagory

    catagoryDict = {"房产小区":1,"购物":2,"医疗保健":3,"教育学校":4,"酒店宾馆":5,"公司企业":6,"旅游景点":7,"娱乐休闲":8,"汽车":9,"基础设施":10,"文化场馆":11,"机构团体":12,"生活服务":13,"美食":14,"运动健身":15,"银行金融":16}
    for line in datas:
        line = line.strip('\n')
        data = line.split('|')
        if(len(data)==7):
            ctgy = data[6]
            ctgy = ctgy.split(';')
            catagory = catagoryDict[ctgy[0]]
            fw.write(line+'|'+str(catagory)+'\n')
    fw.close()
    f.close()

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

    #catagory2int(cmdArgv[1])

    sortByLonLat(cmdArgv[1],cmdArgv[2])
