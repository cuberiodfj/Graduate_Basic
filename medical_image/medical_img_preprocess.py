import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#用圆模拟一个CT脑部横切面图
size = [256, 256]
phantom = np.zeros(size, dtype=np.float32)
y, x = np.ogrid[-128:128, -128:128]#建立坐标网格，原点在图像中心
skull = x**2 + y**2 <= 110**2      #第一层模拟头骨（大圆，半径110）
phantom[skull] = 250               #最亮，模拟头骨
brain = x**2 + y**2 <= 95**2       #模拟第二层脑组织（中圆，半径95）
phantom[brain] = 180               #中等亮度，模拟脑灰质
white_matter = x**2 + y**2 <= 65**2 #第三层：白质（小圆，半径65）
phantom[white_matter] = 120         #模拟脑白质
ventricle = x**2 + y**2 <= 25**2   #第四层：脑室（更小的圆，半径25）
phantom[ventricle] = 50            #暗色，模拟脑室
#加噪声，用numpy.random.norma()生成正态分布的噪声数据
noise = np.random.normal(0, 8, size).astype(np.float32)
phantom = phantom + noise           #两个numpy数组相加，弄出加入噪声的CT图
phantom[phantom < 0] = 0
image = sitk.GetImageFromArray(phantom)#那numpy数组phantom转成SimpleITK 图像
#输出未处理qian原始影像参数
print("原始影像参数为")
print("尺寸:", image.GetSize())
print("像素间距:", image.GetSpacing())
print("原点:", image.GetOrigin())
print("像素:", image.GetPixelIDTypeAsString())
imag_np_array = sitk.GetArrayFromImage(image)#把SimpleITK图像转成NumPy数组，用numpy的min和max函数找最大最小值
print("\n归一化前像素值范围")
print("最小值: ",(imag_np_array.min()))
print("最大值: ",(imag_np_array.max()))
print("归一化前的部分像素数据")
print(imag_np_array[0:5, 0:5])              #取第0行到第4行，第0列到第4列的数据
#用MinMax归一化
pixel_min = imag_np_array.min()             #最大像素值
pixel_max = imag_np_array.max()             #最小像素值
imag_np_array_normalized = (imag_np_array - pixel_min) / (pixel_max - pixel_min)
#归一化后的结果
print("\n归一化后像素值范围")
print("最小值 :",(imag_np_array_normalized.min()))
print("最大值 :",(imag_np_array_normalized.max()))
print("归一化后的部分像素数据")
print(imag_np_array_normalized[0:5, 0:5])              #取第0行到第4行，第0列到第4列的数据
normalized = sitk.GetImageFromArray(imag_np_array_normalized)#再把NumPy数组转成SimpleITK图像
normalized.CopyInformation(image)
print("尺寸:", normalized.GetSize())
print("像素间距:", normalized.GetSpacing())
print("原点:", normalized.GetOrigin())
print("像素类型:", normalized.GetPixelIDTypeAsString())
