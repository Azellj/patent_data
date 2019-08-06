#!/user/bin/env python3
# -*- coding:utf-8 -*-
# 创建：2019-07-30
# 更新：2019-08-03
# version：1.2
# @Aze
# 用于计算不同专利申请人的竞争关系，通过计算Cij两个申请人i，j之间的重复专利数，Ci，Cj申请人i，j的专利数，竞争关系 = Cij/（Ci+Cj）。
# 因为不是很熟练，所以未使用模块化的代码，程序使用pandas.Datafram进行相关数据矩阵操作。
# 数据读写都是通过csv文件实现。
# 1.2版本重构了数据结构，以减少遍历复杂度,计算用约75s，远少于之前的2800s

import numpy as np 
import pandas as pd 
import pdb
import csv
from tqdm import tqdm
from pandas import Series,DataFrame


Path_read = '/Users/liangze/Desktop/测试数据.csv'
Path_writer = '/Users/liangze/Desktop/测试数据out.csv'
Path_name_company = '/Users/liangze/Desktop/name_company.csv'  ### 读取申请人顺序

csv_file = csv.reader(open(Path_read,'r'))
Frame = DataFrame(csv_file)
csv_file_name_company = csv.reader(open(Path_name_company,'r'))
name_company_fram = DataFrame(csv_file_name_company)

Dict_company = {}  #用于储存原始数据的字典
name_company = name_company_fram[0]  #申请人名称
name_patent = Frame.iloc[0,2:]   #专利种类

# 生成一个以申请人名称和专利种类为索引的数据矩阵Data_Frame
newF = np.array(Frame.iloc[1:,2:]).astype('int')
Data_Frame = DataFrame(newF,index=list(name_company),columns=list(name_patent))
Data_Frame['col_sum'] = Data_Frame.apply(lambda x: x.sum(), axis=1)  # 增加一列申请人专利总数

# 通过Data_Frame转化成“申请人 = {'专利名称'：数量}”的形式
Data = Series(index=list(name_company))  #字典列表,用有索引的列表存储申请人专利情况
for x in tqdm(list(name_company)):   #tqdm用于显示程序处理进度
	Dict_company = {}
	for y in list(Data_Frame.columns): #因为增加了一列“col_sum”，所以不能用name_patent遍历
		if int(Data_Frame.loc[x,y]) !=0:
			Dict_company[y] = Data_Frame.loc[x,y]
			Data[x] = Dict_company


# 定义结果矩阵Cij_fram，用于存储数据处理结果，横纵坐标均为申请人名称
Cij_fram = DataFrame(index=list(name_company),columns=list(name_company),dtype='float')

# 计算过程
for i in tqdm(name_company):  
	for j in set(name_company): 
		Cij = 0
		if i == j:
			Cij_fram.loc[i,j] =0
		else:
			for name_i, num_i in Data[i].items():
				if name_i == 'col_sum':
					Ci = num_i
				for name_j, num_j in Data[j].items():
					if name_j == 'col_sum':
						Cj = num_j
					elif name_i == name_j:
						Cij +=(num_i + num_j)
		Cij_fram.loc[i,j] = float(Cij)/float(Ci + Cj)
Cij_fram.to_csv(Path_writer,encoding="utf_8_sig")







