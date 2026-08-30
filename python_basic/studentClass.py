#学生类
class Student:
    def __init__(self,name,age):
        self.n=name
        self.a=age
    def introduce(self):
        print("大家好，我叫%s,今年%d岁。"%(self.n,self.a))
if __name__=="__main__":
    print("请输入姓名和年龄:")
    name=input()
    age=int(input())
    s1=Student(name,age)
    s1.introduce()