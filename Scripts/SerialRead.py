#!/usr/bin/env python
#-*- coding: utf-8 -*-
import serial
import serial.tools.list_ports
import thread
import time
import sys
import numpy as np

'''
SerialPort_list列出所有串口号及其相关信息, 如：
SerialPort_list[0] = [u'COM3', u'Arduino Leonardo (COM3)', 'USB VID:PID=2341:8036 SER=7 LOCATION=1-2.4:x.0']
SerialPort_list[1] = [u'COM9', u'USB-SERIAL CH340 (COM9)', 'USB VID:PID=1A86:7523 SER=6 LOCATION=1-2.3']

SerialPort_list[0]是第一个串口的所有信息
SerialPort_list[0][0]是第一个串口的串口号, 可以传入serial.Serial()用来连接串口
'''
SerialPort_list = serial.tools.list_ports.comports()
wave=''
w = []
#选择串口号
if not SerialPort_list:
    print("Can't find any Serial port!")
    sys.exit("sorry, goodbye!")
else:
    SerialPort = SerialPort_list[0][0] #for example: 'COM3'
    print SerialPort

#打开串口
try:
    ser = serial.Serial(baudrate = 115200, port = SerialPort, timeout = 1)#配置串口并打开
except Exception as e:
    print(e.message)
    sys.exit("sorry, goodbye!")	
else:
    print("Open %s successfully!" % SerialPort)


def SerialReadStr(threadName):
    global flag
    global wave
    while flag:
        Bytes = ser.in_waiting #读取串口缓冲区中字节数
        if Bytes>0:
            data = ser.read(Bytes)#将缓冲区中字节全部读出
            wave = wave + data #字符串拼接



def main():
    global flag
    global wave
    flag = True
    wave = ''

    #串口接收线程，不断读取串口接收缓冲区内数据，直到标志位flag为false，线程结束
    thread.start_new_thread(SerialReadStr, ("thread: SerialReadStr",))
    while True:
        cmd = input("please input cmd: a:start, b:stop, c:quit\n")
        if cmd=='a':            
            ser.flushInput()
            wave = ''
            w = []
            ser.write(b'\xa9')
            print("collecting...")
        if cmd=='b':
            ser.write(b'\xb9')
            w=[ord(i) for i in wave]
            print("finish")
            print("receive %d bytes" %len(w))            
            np.save("wave.npy",w)
            print("data saved to \"./wave.npy\"")
        if cmd=='c':
            print("Quit")
            flag=False
            time.sleep(0.1)
            break
        time.sleep(0.01)

if __name__=="__main__":
    try:
        main()
        ser.close()
        sys.exit("finish task!")
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            sys.exit("finish task!")
