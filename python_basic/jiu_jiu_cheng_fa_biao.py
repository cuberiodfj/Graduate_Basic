#九九乘法表
if __name__=="__main__":
    for i in range(1,10):
        if i==1:                          #1*1的式子单独处理
            print(i,"*",i,"=",f"{(i*i):2d}")      #有的式子结果两位数有的是一位数，用f-string字符串统一宽度为2位
        else:
            for j in range(1,i+1):
                print(j,"*",i,"=",f"{(j*i):2d}"," ",end=" ")
            print(" ")