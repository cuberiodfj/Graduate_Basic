import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(3202610548)
# 生成模拟的500条医保数据
n = 500
original_data = pd.DataFrame({
    "ID": range(3202610001, n + 3202610001),
    "姓名": [f"患者{i}" for i in range(1, n + 1)],
    "年龄": np.random.randint(1, 100, n),
    "性别": np.random.choice(["男", "女"], n),
    "科室": np.random.choice(["内科", "外科", "心内科", "骨科", "儿科"], n),
    "诊断": np.random.choice(["高血压", "糖尿病", "骨折", "冠心病", "感冒"], n),
    "费用": np.random.uniform(100, 20000, n),
    "报销金额": np.random.uniform(50, 15000, n),
})
original_data["报销金额"] = np.minimum(original_data["报销金额"], original_data["费用"])
print("生成数据：", len(original_data), "条")

# 制造缺失值
dirty_data = original_data.copy()
for col, size in [("年龄", 50), ("性别", 30), ("费用", 40), ("诊断", 20)]:
    idx = np.random.choice(dirty_data.index, size, replace=False)
    dirty_data.loc[idx, col] = np.nan
# 制造异常值
for i in np.random.randint(1,500,15): #for循环再1-499内随机选取15个i，然后循环内部对特定的各个字段进行异常值制造
    dirty_data.loc[i, "年龄"] = 200   
    dirty_data.loc[i+2, "年龄"] = -5
    dirty_data.loc[i+3, "费用"] = -5000
print("\n脏数据统计")
print(dirty_data.isnull().sum())
#数据清洗
clean_data = dirty_data.copy()
##填充缺失值
clean_data["年龄"] = clean_data["年龄"].fillna(clean_data["年龄"].mean())#年龄的缺失值用字体数据的平均值来替换
clean_data["费用"] = clean_data["费用"].fillna(clean_data["费用"].mean())
clean_data["性别"] = clean_data["性别"].fillna(clean_data["性别"].mode()[0])#mode函数寻找数据中的众数，用出现最多的数据填充性别的缺失值
clean_data["诊断"] = clean_data["诊断"].fillna(clean_data["诊断"].mode()[0])
clean_data["报销金额"] = clean_data["报销金额"].fillna(clean_data["报销金额"].median())
##异常删除
clean_data = clean_data[(clean_data["年龄"] >= 0) & (clean_data["年龄"] <= 120)]  #年龄太大或者为负数的去掉
clean_data = clean_data[(clean_data["费用"] >= 0) ]                              #费用三十负数的去掉
print(f"\n清洗前：{len(dirty_data)} 条 → 清洗后：{len(clean_data)} 条")
#数据清理结果
print("清洗后费用统计")
print(clean_data["费用"].describe().to_string())
print("各科室人数")
print(clean_data["科室"].value_counts().to_string())
print("各诊断次数")
print(clean_data["诊断"].value_counts().to_string())
#清理数据可视化
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
axes[0].hist(clean_data["费用"], bins=30, color="steelblue", edgecolor="white")
axes[0].set_title("费用分布")
axes[0].set_xlabel("费用（元）")
axes[0].set_ylabel("人数")
clean_data["科室"].value_counts().plot(kind="bar", color="seagreen", edgecolor="white", ax=axes[1])
axes[1].set_title("各科室就诊人数")
axes[1].tick_params(axis='x', rotation=0)
clean_data["诊断"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=axes[2])
axes[2].set_title("各诊断占比")
axes[2].set_ylabel("")
plt.tight_layout()
plt.savefig("医保数据可视化.png", dpi=150)
plt.show()