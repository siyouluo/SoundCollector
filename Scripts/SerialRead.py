#!/usr/bin/env python
#-*- coding: utf-8 -*-
import serial
import easygui
import time
ser = serial.Serial()
ser.baudrate = 57600 #设置波特率（这里使用的是stc89c52）
ser.port = 'COM7' #端口是COM3
print(ser)
ser.open()#打开串口
print(ser.is_open)#检验串口是否打开
''' 
    while(1):
        Yes_or_No = easygui.buttonbox("是否良品?", choices = ['Yes','No','退出'])#提供简易UI
        if Yes_or_No=='退出':break
        if Yes_or_No=='Yes':
            demo=b"2"#传入2的ASCII码 这里用b+str强制转换
        else:
            demo=b"1"#传入1的ASCII码 这里用b+str强制转换
     
        ser.write(demo)
    '''  
while True:
    datainput = raw_input("Please input the character:\n")
    n = ser.write(datainput)
    print n
    data = ser.read(1)
    print data

'''
--------------------- 
作者：dgut_guangdian 
来源：CSDN 
原文：https://blog.csdn.net/dgut_guangdian/article/details/78391270 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''