# 导入pandas与numpy工具包。
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 创建特征列表。
# column_names = ['样本编号', '肿块厚度', '细胞大小均一性', '细胞形态均一性', '边际黏连', '单个细胞到校', '裸核', '染色体', '正常核', '有丝分裂', '分类']
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
# 使用pandas.read_csv函数从互联网读取指定数据。
data = pd.read_csv('breast-cancer-wisconsin.data', names = column_names )
# 将?替换为标准缺失值表示。
data = data.replace(to_replace='?', value=np.nan)
# 丢弃带有缺失值的数据（只要有一个维度有缺失）。
data = data.dropna(how='any')
# 输出data的数据量和维度。
data.shape
data.head()

data1 = data[data['Class']==4]#良性肿瘤数据
data2 = data[data['Class']==2]#恶性肿瘤数据

alpha = 0.5
plt.figure(figsize=(10,10))
# 直接通过class分类（聚类）定义不同散点的color
plt.scatter(data1['Clump Thickness'], data1['Uniformity of Cell Size'], color='g', alpha=alpha)#绿色
plt.scatter(data2['Clump Thickness'], data2['Uniformity of Cell Size'], color='r', alpha=alpha)#红色
plt.title('肿瘤细胞可视化')
plt.show()


