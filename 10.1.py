# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 12:36:48 2020

@author: Administrator
"""

import numpy as np
import pandas as pd
#读取Excel数据，统一先按照字符串读入，之后转换
file='./朝阳医院2018年销售数据.xlsx'
xls = pd.ExcelFile(file, dtype='object')
salesDf = xls.parse('Sheet1',dtype='object')
#打印出前5行，以确保数据运行正常
salesDf.head()
salesDf.shape
salesDf.dtypes
colNameDict = {'购药时间':'销售时间'}
salesDf.rename(columns = colNameDict,inplace=True)
salesDf.head()
salesDf=salesDf.dropna(subset=['销售时间','社保卡号'],how='any')
print('删除缺失后大小',salesDf.shape)
#字符串转换为数值（浮点型）
salesDf['销售数量'] = salesDf['销售数量'].astype('float')
salesDf['应收金额'] = salesDf['应收金额'].astype('float')
salesDf['实收金额'] = salesDf['实收金额'].astype('float')
def splitSaletime(timeColSer):
    timeList=[]
    for value in timeColSer:
        #例如2018-01-01 星期五，分割后为：2018-01-01
        dateStr=value.split(' ')[0]
        timeList.append(dateStr)
    
    #将列表转行为一维数据Series类型
    timeSer=pd.Series(timeList)
    return timeSer
timeSer=salesDf.loc[:,'销售时间']
dateSer=splitSaletime(timeSer)
salesDf.loc[:,'销售时间']=dateSer

'''
数据类型转换:字符串转换为日期
'''
#errors='coerce' 如果原始数据不符合日期的格式，转换后的值为空值NaT
#format 是你原始数据中日期的格式
salesDf.loc[:,'销售时间']=pd.to_datetime(salesDf.loc[:,'销售时间'],
                                    format='%Y-%m-%d', 
                                    errors='coerce')

salesDf.dtypes
'''
转换日期过程中不符合日期格式的数值会被转换为空值，
这里删除列（销售时间，社保卡号）中为空的行
'''
salesDf=salesDf.dropna(subset=['销售时间','社保卡号'],how='any')
'''
by：按那几列排序
ascending=True 表示降序排列，
ascending=False表示升序排列
'''
#按销售日期进行升序排列
salesDf=salesDf.sort_values(by='销售时间',ascending=True)

#重命名行名（index）：排序后的列索引值是之前的行号，需要修改成从0到N按顺序的索引值
salesDf=salesDf.reset_index(drop=True)
salesDf.head()
salesDf.describe()
#删除异常值：通过条件判断筛选出数据
#查询条件
querySer=salesDf.loc[:,'销售数量']>0
#应用查询条件
print('删除异常值前：',salesDf.shape)
salesDf=salesDf.loc[querySer,:]
print('删除异常值后：',salesDf.shape)
'''
总消费次数：同一天内，同一个人发生的所有消费算作一次消费
#根据列名（销售时间，社区卡号），如果这两个列值同时相同，只保留1条，将重复的数据删除
'''

kpi1_Df=salesDf.drop_duplicates(subset=['销售时间', '社保卡号'])

#总消费次数：有多少行
totalI=kpi1_Df.shape[0]

print('总消费次数=',totalI)


#月份数,运算符"//"表示取整除，返回商的整数部分
startTime=kpi1_Df.loc[0,'销售时间']
endTime=kpi1_Df.loc[totalI-1,'销售时间']
daysI=(endTime-startTime).days
monthsI=daysI//30
remain = daysI - 30 * monthsI
if(remain > 0):
    monthsI = monthsI + 1
print('月份数：',monthsI)


#业务指标1：月均消费次数=总消费次数 / 月份数
kpi1_I=totalI // monthsI
print('业务指标1：月均消费次数=',kpi1_I)
totalMoneyF=salesDf.loc[:,'实收金额'].sum()
#月均消费金额
monthMoneyF=totalMoneyF / monthsI
print('业务指标2：月均消费金额=',monthMoneyF)
'''
totalMoneyF：总消费金额
totalI：总消费次数
'''
pct=totalMoneyF / totalI
print('客单价：',pct)