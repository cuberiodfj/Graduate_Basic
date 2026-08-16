import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#中文修复,修复运行时候柱状图和相关性热力图文字乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]   # 黑体

#生成模拟成绩数据集
np.random.seed(3202610548)       #使用3202610548作为随机种子，方便生成的随机成绩数据可以复现
score_main = np.random.randint(50,150,(200,3))   #主科语数英成绩200个数据
score_vice = np.random.randint(20,100,(200,3))   #副科以新高考选科的物化地为例200个数据
score = np.concatenate((score_main,score_vice),axis=1) #用numpy的concatenate函数把主科和副科成绩合并
stu_id = []                       #学号列表
for i in range(0,200):            #学号从3202610001开始计算，取200个
    stu_id.append(i+3202610001)
columns_subject = ["语文","数学","英语","物理","化学","地理"]#列标签为学科名
dataframe_score = pd.DataFrame(score,stu_id,columns_subject) #学科标签，学号标签和成绩数据合并为1个dataframe对象
dataframe_score.to_csv(r"D:\filetest\original_score.csv",index = True,header=True,encoding = 'gbk')   #生成原始成绩数据文件



#手动操作改成绩制造缺失值异常值
###手动操作中。。。。。。。。。



score_df = pd.read_csv(r"D:\filetest\original_score.csv",index_col = 0,encoding = 'gbk')#read_csv方法读取修改过后的成绩
#缺失值处理
print("成绩列表中的数据缺失值个数分别为：")
print(score_df.isnull().sum())         #统计每个学科成绩的缺失值
score_clean = score_df.copy() 
for col in score_clean.columns:
    fill_val = score_clean[col].mean() #计算每个学科的平均成绩
    score_clean[col] = score_clean[col].fillna(fill_val) #用对应学科平均值填充缺失值
#异常值剔除
full_score = {        #用字典存储各科标签与满分的对应关系，用于判断是否存在不合理的成绩
    "语文": 150,
    "数学": 150,
    "英语": 150,
    "物理": 100,
    "化学": 100,
    "地理": 100
}
print("剔除前，学生成绩条数为",len(score_clean))
for sub in score_df.columns:
    max_s = full_score[sub]       
    score_clean = score_clean[(score_clean[sub] > 0) & (score_clean[sub] <= max_s)]#成绩大于各科满分或者是负数的都是异常值，应该剔除
print("剔除后，学生成绩条数为",len(score_clean))
#各科成绩指标
print("各科成绩指标统计：")
score_indicators=score_clean.describe() #用dataframe的describe方法得出成绩指标数据
print((score_indicators.T).astype(float))
#结果可视化
##柱状图
fig, (bar_chart,correlation_heatmap) = plt.subplots(1,2,figsize = (16,7))
score_clean_avg = score_clean.mean()
scores_bar_chart = bar_chart.bar(score_clean_avg.index,score_clean_avg.values)
bar_chart.set_title("某地高考物化地组合考生平均分对比图",fontsize=15)
bar_chart.set_ylabel("平均分",fontsize=13)
#相关性热力图
corr_matrix = score_clean.corr()
sns.heatmap(corr_matrix , annot=True,cmap="coolwarm",ax = correlation_heatmap)
correlation_heatmap.set_title("各科成绩相关性热力图", fontsize=14)
plt.show()