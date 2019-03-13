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
flag2=True
#选择串口号
if not SerialPort_list:
    print("Can't find any Serial port!")
else:
    SerialPort = SerialPort_list[0][0]
    print SerialPort

#打开串口
try:
    ser = serial.Serial(baudrate = 115200, port = SerialPort, timeout = 1)
except Exception as e:
    print(e.message)
    sys.exit("sorry, goodbye!")	
else:
    print("Open %s successfully!" % SerialPort)

def KeyDetect(threadName):
    global wave
    while True:
        cmd = input("please input cmd: a:start, b:stop, c:quit\n")
        if cmd=='a':
            print("collecting...")
            ser.flushInput()
    	    wave = ''
    	    w = []
            ser.write(b'\xa9')
        if cmd=='b':
            for i in wave:
                w.append(ord(i))
            print("finish")
            print(len(w))
            np.save("wave.npy",w)
            ser.write(b'\xb9')
        if cmd=='c':
            print("Quit")
            global flag
            global flag2
            flag=False
            flag2=False
        time.sleep(0.01)
        print(threadName)

def SerialReadStr(threadName):
    global flag
    global wave
    while flag:
        data = ser.read(100)# read a '\n' terminated line
        wave = wave + data



def main():
    global flag
    global wave
    flag = True
    wave = ''
    thread.start_new_thread(KeyDetect, ("thread: KeyDetect", ))
    thread.start_new_thread(SerialReadStr, ("thread: SerialReadStr",))
    while flag2:
    	pass
    #data = ser.read(10000)## read up to 10000 bytes or as much is in the buffer
    
		

if __name__=="__main__":
    try:
        main()
        ser.close()
        sys.exit("finish task!")
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            sys.exit("finish task!")
