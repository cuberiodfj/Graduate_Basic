"""
习题 3医学影像巩固题周三
题目 生成二维测试影像；完成：
1.获取影像 numpy 数组
2.像素归一化到 [0-1]
3.将大于 0.5 的像素置为 1    其余置 0    简单二值分割 
4.打印原始数组形状、二值图像素总和。
"""
import numpy as np

np.random.seed(3202610548)
med_img = np.random.uniform(-1000,2000,(256,256)).astype(int)
print("生成的二维测试影像为：\n",med_img)
min = med_img.min()
max = med_img.max()
med_img_norm = (med_img-min)/(max-min)
print("归一化后的影像numpy数组为：\n",med_img_norm)
mde_img_final = np.where(med_img_norm>0.5 , 1 , 0)
print("就行简单的二值分割之后：\n",mde_img_final)
print("原始数组形状为：",med_img.shape)
print("二值图像像素总和为：",mde_img_final.sum())