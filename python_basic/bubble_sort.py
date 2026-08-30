##冒泡排序
def bubble_sort(list):
    for i in range(0,len(list)):
        j=len(list)-1        
        flag=False       #记录当前的一趟排序有没有发生元素交换
        while j>i:
            print(j)
            if list[j-1]>list[j]:    #前一个元素比后一个元素大，交换
                temp=list[j]
                list[j]=list[j-1]
                list[j-1]=temp
                flag=True
            j=j-1
        if not flag:      #如果当前的一趟排序没有发生交换，说明序列基本有序，冒泡排序提前结束
            break
if __name__=="__main__":
    print("请输入数据个数，以及具体数据")
    n = int(input())
    list=[]
    for i in range(0,n):
        list.append(float(input()))
    bubble_sort(list)
    print("冒泡排序后的结果为：",list)
