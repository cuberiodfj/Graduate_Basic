"""
习题 2-数据分析综合题（周二）
题目 自动生成一份包含「姓名、年龄、收入」共 60 行的数据集；
1.检测缺失值，用均值填充数值字段；
2.剔除收入大于 200000 的异常样本；
3.按年龄段分组：青年 (18-35)、中年 (36-59)、老年 (≥60)；
4.统计每组平均收入；
5.绘制各组平均收入柱状图。
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 设置中文
plt.rcParams["font.sans-serif"] = ["SimHei"]   #黑体，Windows
plt.rcParams["axes.unicode_minus"] = False     #解决负号显示成方块
np.random.seed(3202610548)
#生成模拟数据集
df_wage = pd.DataFrame({
    "name":range(3202610001,3202610001+60),
    "age":np.random.randint(18,63,60),
    "wage":(np.random.normal(7000,3000,60)).astype(int)
})
df_wage.loc[df_wage["wage"]<0,"wage"] = 3000    #随机模拟的数据有概率出现负数，让负数值工资统一为3000
print(df_wage)
#随机制造缺失值和异常值（*）
outlier = 0.05 #缺失值和异常值占数据集0.05
mask_out = np.random.choice([True,False],size = 60,p=[outlier,1-outlier]) 
df_wage.loc[mask_out,"wage"] = 999999    #工资部分异常值
df_wage.loc[mask_out,"age" ] = pd.NA
print("存在缺失值和异常值的模拟数据集：")
print(df_wage)
#检测缺失值，用均值填充
df_wage.loc[df_wage["age"].isna() , "age"] = int(df_wage["age"].mean()) 
df_wage["age"] = (df_wage["age"]).astype(int)  #随机制造缺失值时，其他行数据被强制转换为float型数据
df_wage = df_wage.loc[df_wage["wage"] <= 200000]
print("缺失值和异常值处理之后的模拟数据集：")
print(df_wage)
#统计与画图
young = df_wage[df_wage["age"]<=35]
middle_aged = df_wage[(df_wage["age"]>35) & (df_wage["age"]<60)]
old = df_wage[df_wage["age"]>=60]
wage_avg = [young["wage"].mean(),middle_aged["wage"].mean(),old["wage"].mean()]
group = ["青年","中年","老年"]
plt.figure(figsize=(6,4))
plt.bar(group , wage_avg , color = ["green" , "red" , "blue"])
plt.title("各组平均收入统计柱状图")
plt.xlabel("年龄组别")
plt.ylabel("各分组类别平均收入")
plt.show()
