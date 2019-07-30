#!/user/bin/env python
# -*- coding:utf-8 -*-
# 创建：2019-07-30
# 更新：2019-03-15
# version：1.0
# @Aze
# 用于计算不同专利申请人的竞争关系，通过计算Cij两个申请人i，j之间的重复专利数，Ci，Cj申请人i，j的专利数，竞争关系 = Cij/（Ci+Cj）。
# 因为不是很熟练，所以未使用模块化的代码，程序使用pandas.Datafram进行相关数据矩阵操作。
# 数据读写都是通过csv文件实现。
# 目前计算512*1602的时间约为1100s（MacBook pro），计算比较缓慢，算法尚需优化。

import csv
import pandas as pd
import numpy as np
from pandas import Series,DataFrame 
Path_read = '/Users/liangze/Desktop/WQ-DATA.csv' ### 原始数据路径，视情况调整
Path_writer = '/Users/liangze/Desktop/WQdata-out.csv'  ###输出结果路径，视情况调整

# 读取原始数据，生成原始数据矩阵fram
csv_file = csv.reader(open(Path_read,'r'))
fram = DataFrame(csv_file)


# 生成申请人与发表专利数量的对应矩阵num_fram，用于记录各申请人的发表专利数，其实可以不用这种方式，之前从原始矩阵中调取即可，之后可以做调整
name_company = fram.iloc[1:,2]
number_patent = fram.iloc[1:,1]
data = [number_patent]
data_array = np.array(data)  #用numpy中array不需要重建索引排序
#data_array = name_company.reset_index(drop=True),number_patent.reset_index(drop=True)  #索引重排序
"""
测试相关数据的大小
m = len(data_array)   ###  2 
n = len(name_company)   ###  512
"""
num_fram = DataFrame(list(data_array),index=['发表专利数'],columns=list(name_company),dtype=int).T
num_fram['发表专利数'] = num_fram['发表专利数'].astype('int')  #将存储数据转化成int类型


# 计算两个申请企业之间的重复专利数量即Cij,生成矩阵Cij_fram
Cij_fram = DataFrame(index=list(name_company),columns=list(name_company),dtype=int)
print(Cij_fram)
sum = 0   #过度数
Cij = 0   #两个申请人i，j之间的重复专利数
Ci = 0    #申请人i的专利数
Cj = 0    #申请人j的专利数
L_nc = len(name_company)  #申请人数量
L_np = len(number_patent)  #专利种类数量
for i in range(L_nc):
	for j in range(L_nc):
		#print(Cij_fram.index[i],type(Cij_fram.index[i]))   测试代码
		#print(Cij_fram.columns[j],type(Cij_fram.columns[j]))
		if Cij_fram.index[i] == Cij_fram.columns[j]:
			Cij_fram.iloc[i,j] = 0  #相同申请人值为0，矩阵对角线为0
		else:
			Cij = 0
			np = 0 
			for np in range(L_np):  #遍历所有专利类别
				if int(fram.iloc[(i+1),(np+3)]) != 0:   #原始表中申请人是从第2行开始，所以+1；专利是从第4列开始的，所以+3
					Ci += int(fram.iloc[(i+1),(np+3)])
					if int(fram.iloc[(j+1),(np+3)]) != 0:    #两个申请人在同一专利数量均不为0是计算两者之和
						Cj +=  int(fram.iloc[(j+1),(np+3)])
						sum = int(fram.iloc[(i+1),(np+3)]) + int(fram.iloc[(j+1),(np+3)])
						Cij += sum
					elif Ci == num_fram.loc[Cij_fram.index[i],'发表专利数']:  #减少遍历次数，如果i已经全部遍历则跳出循环
						break
					elif Cj == num_fram.loc[Cij_fram.columns[j],'发表专利数']:   #减少遍历次数，如果j已经全部遍历则跳出循环
						break
					else :
						continue
				else:
					continue
			Ci = num_fram.loc[Cij_fram.index[i],'发表专利数']   #通过指定方式取值，速度快
			Cj = num_fram.loc[Cij_fram.columns[j],'发表专利数']
			"""
			通过遍历方式取Ci和Cj，速度慢
			nc = 0 
			for nc in range(len(name_company)):   #遍历申请人与所发专利数量的num_fram矩阵，查找申请人i，j发表专利数量Ci，Cj	
				if num_fram.iloc[nc,0] == Cij_fram.index[i]:
					Ci = num_fram.iloc[nc,1]
				if num_fram.iloc[nc,0] == Cij_fram.columns[j]:
				    Cj = num_fram.iloc[nc,1]
			"""
			Cij_fram.iloc[i,j] = float(Cij)/float(Ci + Cj)   #计算矩阵Cij_fram的值
	print(i,'percent: {:.2f}%'.format(((i+1)/512)*100))
print(Cij_fram)	


#计算结果输出到csv文件
Cij_fram.to_csv(Path_writer)

