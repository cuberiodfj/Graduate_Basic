if __name__=="__main__":
    print("请输入学生姓名以及成绩：")
    student = input()
    list=[]
    for i in range(0,3):
        list.append(input())
    course1=float(list[0])
    course2=float(list[1])
    course3=float(list[2])
    sum=course1+course2+course3
    print("学生"+student+"的平均成绩为:",f"{sum/3:.2f}")