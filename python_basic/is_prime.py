"""
函数的参数n是要判断的数。
count用于计数，判断从2到n-1之内是否存在一个数可以被n整除，如果存在一个count就加1。
"""
def is_prime(n):
    count=0
    for i in range(2,n):     #从2开始遍历到n-1寻找可以被n整除的数
        if n%i==0:           #取余为0，说明2到n-1内存在可以被n整除的数
            count=count+1    #计数器加一
    if count:                #count不为零时，n不是素数返回值为Flase
        return False
    else:                    #count为零，n是素数，返回值为True
        return True
if __name__=="__main__":
    print("请输入要判断的数：")
    num = int(input())
    if is_prime(num):
        print(num,"是素数")
    else:
        print(num,"不是素数")