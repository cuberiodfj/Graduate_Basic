#文件打开、读取、信息统计以及异常处理
if __name__=="__main__":
    ##文件读取与信息统计
    try:
        file =open(r"D:\filetest\aaa.txt",mode='r',encoding='utf-8')
    except:
        print("文件打开失败")
    else:
        count_line=0
        count_str_num=0
        while True:
            line=file.readline()
            print(line)
            if not line:
                break
            count_line=count_line+1
            if line[len(line)-1]=="\n":
                count_str_num=count_str_num+(len(line)-1)
            else:
                count_str_num=count_str_num+len(line)
        print("该文件一共有",count_line,"行",count_str_num,"个字符")
    try:
        file.close()
    except:
        print("文件关闭失败")
    ##文件写入
    file2 =open(r"D:\filetest\bbb.txt",mode='w',encoding='utf-8')
    print("请输入要写进文件的内容：")
    str = input()
    file2.write(str)
    file2.close()


    
    