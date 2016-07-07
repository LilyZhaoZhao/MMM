#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
cmdArgv = sys.argv


#功能描述： 首先对poi经纬度进行格子划分，取100m*100m的范围为一个格子，并且编号；
#          然后在每个格子中按照比例选取一定数量的ap，作为测试集；其余的用作训练集；
#          最后输出的文件格式：poi原始数据|catagory编号|block编号

datas = open(sys.argv[1],'r').readlines() #buptpoi16_22_intCatagory or szPoi_0316_intCatagory
output1 = open(sys.argv[1]+'_block_testset', 'w') #输出的poi作为未知类别的ap，用于验证
output2 = open(sys.argv[1]+'_block_trainset', 'w') #输出的poi作为已知类别的ap

res = {}
id  = {}
count = 0

for line in datas:
    data = line
    data = data.strip('\n').split('|')
    try:
        lon = float(data[2])
        lat  = float(data[3])
    except ValueError:
        for i in range(len(data)-1):
            try:
                lon = float(data[i])
                lat  = float(data[i+1])
                break
            except ValueError:
                pass
    lon = int(lon*1000) # 取经纬度的小数点后第3位数，也即距离为100m，那么格子的大小就是100m*100m
    lat  = int(lat *1000)

    if (lon, lat) in res:
       res[(lon,lat)] += [line]
    else:
       count += 1
       res[(lon,lat)] = [line]
       id[(lon,lat)] = count

#for item in res:
#    print >> output, item[0],item[1],len(res[item]),id[item] #得出格子的经纬度区间，每个格子内的ap数量，格子的编号
    #poi = res[item]
    #for line in poi:
    #    print >> output, line.strip('\n')


samplingRatio = 0.5 #采样比例，即留出30%作为测试集

for item in res:
    numOfApInItem = len(res[item])
    if(numOfApInItem > 0): #如果该格子内有ap，则按比例采样
#        numOfSampling = int(samplingRatio * numOfApInItem)+1
        numOfSampling = int(samplingRatio * numOfApInItem)

        poi = res[item]
        #print numOfSampling, numOfApInItem
        for i in range(numOfSampling):
            print >> output1, poi[i].strip('\n')+'|'+str(id[item])
        for j in range(numOfSampling, numOfApInItem):
            print >> output2, poi[j].strip('\n')+'|'+str(id[item])
output1.close()
output2.close()
