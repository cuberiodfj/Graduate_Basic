#过滤列表负数值
def filter_negative(list):
    list[:] = [x for x in list if x>=0]  #用切片的方法从函数内部修改列表并影响外部函数结果
    results = [max(list),min(list),sum(list)/len(list)]  
    return results

#冒泡排序
def bubble_sort(list):
    for i in range(0,len(list)):
        j=len(list)-1        
        flag=False       #记录当前的一趟排序有没有发生元素交换
        while j>i:
            if list[j-1]>list[j]:    #前一个元素比后一个元素大，交换
                temp=list[j]
                list[j]=list[j-1]
                list[j-1]=temp
                flag=True
            j=j-1
        if not flag:      #如果当前的一趟排序没有发生交换，说明序列基本有序，冒泡排序提前结束
            break

#主程序
if __name__ == "__main__":
    n = int(input())
    list = []
    print("请输入列表数据：")
    for i in range(0,n):
        temp = int(input())
        list.append(temp)
    print("处理前列表数据为：",list)
    res = filter_negative(list)
    print("处理后列表数据为：",list)
    print(f"最大值为：{res[0]},最小值为{res[1]}平均值为：{res[2]}")
    bubble_sort(list)
    print("过滤后冒泡排序的列表为：",list)
    