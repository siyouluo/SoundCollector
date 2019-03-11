#!/usr/bin/python
# -*- coding: utf-8 -*-

# gui.py

import sys
from PyQt4 import QtGui, QtCore
import time
import numpy as np
#import thread
from threading import Thread
import serial
import serial.tools.list_ports

class SoundCollector(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(SoundCollector, self).__init__()
        self.s = self.SerialConnect()
        self.flag=True
        print(self.s)
        self.wave = ''
        self.w = []
        self.t = Thread(target=self.receive_bytes, args=("thread: receive_bytes", ))
        self.t.start()
        self.initUI()

    def initUI(self):

        button1 = QtGui.QPushButton("Start", self)
        button1.move(30, 50)

        button2 = QtGui.QPushButton("Stop", self)
        button2.move(150, 50)

        button3 = QtGui.QPushButton("Quit", self)
        button3.move(270, 50)


        self.connect(button1, QtCore.SIGNAL('clicked()'), self.button1_process)
        
        self.connect(button2, QtCore.SIGNAL('clicked()'), self.button2_process)

        self.connect(button3, QtCore.SIGNAL('clicked()'), self.button3_process)

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('SoundCollector')
        self.setWindowIcon(QtGui.QIcon('images/littleStar.ico'))
        self.resize(500, 200)
        self.center()

    def center(self):
    	#窗体居中
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def button1_process(self):
    	
        self.statusBar().showMessage('collecting...')
    	self.s.flushInput()
    	self.wave = ''
    	self.w = []
    	self.s.write(b'\xa9')
    	
    	
    def button2_process(self):
        self.s.write(b'\xb9')
        for i in self.wave:
            self.w.append(ord(i))
        self.statusBar().showMessage('finish ')
        print(len(self.w))
        np.save("wave.npy",self.w)
        #print(self.wave)

    def button3_process(self):
    	self.flag=False
    	sys.exit("goodbye!")	


    def receive_bytes(self, threadName):
        while self.flag:
            data = self.s.read(100)# read a '\n' terminated line
            self.wave = self.wave + data
                #self.wave.append(ord(data))
                #print ord(data)

    def SerialConnect(self):
        SerialPort_list = serial.tools.list_ports.comports()
        if not SerialPort_list:
            print("Can't find any Serial port!")
        else:
            SerialPort = SerialPort_list[0][0]
            print SerialPort
        try:
            ser = serial.Serial(baudrate = 115200, port = SerialPort, timeout = 1)
        except Exception as e:
            print(e.message)
            sys.exit("sorry, goodbye!")	
        else:
            print("Open %s successfully!" % SerialPort)
            return ser

#    def buttonClicked(self)
#        sender = self.sender()
#        self.statusBar().showMessage(sender.text() + ' was pressed')

app = QtGui.QApplication(sys.argv)
widget = SoundCollector()
widget.show()
sys.exit(app.exec_())