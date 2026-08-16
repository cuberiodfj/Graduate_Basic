#求最值与平均值
def cal_max_min_avg(list):
    my_max=max(list)
    my_min=min(list)
    my_avg=sum(list)/len(list)
    results = [my_max,my_min,my_avg]
    return results
if __name__=="__main__":
    print("请输入数据个数以及具体的数据：")
    number = int(input())
    data_list = []
    for i in range(0,number):
        n = float(input())
        data_list.append(n)
    results = cal_max_min_avg(data_list)
    myMax = results[0]
    myMin = results[1]
    myAvg = results[2]
    print(f"输入数据中最大值为：{myMax},最小值为:{myMin},平均值为:,{myAvg}")
