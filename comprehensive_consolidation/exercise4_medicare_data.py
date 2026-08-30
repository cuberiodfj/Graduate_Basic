"""
习题 4医保大数据综合复习题（周四）
题目 生成 250 条医保模拟数据：年龄、就诊费用、就诊次数；
1.填充费用字段缺失值；
2.剔除费用 > 80000 的异常记录；
3.筛选 65 岁以上老年患者；
4.统计老年患者平均就诊费用与平均就诊次数；
5.画出老年患者报销费用直方图。
"""
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt

np.random.seed(3202610548)
df_medicare_data = pd.DataFrame({
                                 "user_id":range(1,251),
                                 "age":np.random.normal(52,22,250).astype(int),
                                 "med_coast":np.random.gamma(shape=2.5, scale=600, size=250),
                                 "med_number":np.random.randint(0,15,250)
})
print("模拟的医保数据为：\n",df_medicare_data)
#随机制造异常值和缺失值
outlier = 0.05
mask_out = np.random.choice([True,False] , size = 250,p=(outlier , 1-outlier))
df_medicare_data.loc[mask_out , "age"] = pd.NA     #缺少值
df_medicare_data.loc[mask_out,"med_coast"] = 80001 #异常值
print("模拟的存在缺失值的医保数据个数为：\n",df_medicare_data["age"].isna().sum())
print("模拟的存在异常值的医保数据个数为：\n",(df_medicare_data["med_coast"]>80000).sum())
#填充缺失值
df_medicare_data.loc[df_medicare_data["age"].isna(),"age"] = df_medicare_data["age"].mean()
#剔除异常值
print("剔除异常值前数据条数为",len(df_medicare_data))
df_medicare_data = df_medicare_data.loc[df_medicare_data["med_coast"]<80000]
print("剔除异常值后数据条数为",len(df_medicare_data))
#筛选65以上老年患者
old = df_medicare_data.loc[df_medicare_data["age"]>65]
print(old)
print("老年患者的平均就诊费用为",old["med_coast"].mean())
print("老年患者的平均就诊次数为",int(old["med_number"].mean()))
old["reimburse_cost"] = old["med_coast"]*np.random.uniform(0.5,0.8,len(old))
#绘制直方图
####设置中文
plt.rcParams["font.sans-serif"] = ["SimHei"]   #黑体，Windows
plt.rcParams["axes.unicode_minus"] = False     #解决负号显示成方块
plt.figure(figsize=(6,4))
plt.hist(old["reimburse_cost"],bins = 15,color = "skyblue",edgecolor = "black")
plt.title("老年患者报销费用直方图")
plt.xlabel("报销费用")
plt.ylabel("患者人数")
plt.show()