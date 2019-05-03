#!/usr/bin/python
# -*- coding: utf-8 -*-
# http://qixinbo.info/2017/12/04/pyqt4-widgets/
# gui.py

import sys
import thread
import time
import wave
import winsound
import os
import numpy as np
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
import pyqtgraph as pg
import Ui_demo
import serial
import serial.tools.list_ports
class CustomComboBox(QtGui.QComboBox):
    """docstring for CustomComboBox
    重载下拉列表，每次点击时搜索串口号，将其添加到列表中
    继承自QtGui.QComboBox
    参考自：
    https://blog.csdn.net/MaggieTian77/article/details/79205192
    """
    popupAboutToBeShown = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)
    def showPopup(self):
        '''
        点击弹出列表时执行以下操作：
        清空下拉列表内容
        搜索串口号
        将串口号添加到下拉列表
        如果没有串口，弹框提示“找不到”
        '''
        self.clear()
        SerialPort_list = serial.tools.list_ports.comports()
        if not SerialPort_list:
            msg = QtGui.QMessageBox().question(self, 'msg', "Can't find any Serial port", QtGui.QMessageBox.Ok)
        else:
            for port in SerialPort_list:
                self.addItem(port.device)
                #print(p.description) #返回设备名字
                #print(p.location) #返回设备在计算机上的位置
        QtGui.QComboBox.showPopup(self)#执行QtGui.QComboBox定义的操作

class MyThread(QThread):
    '''
    重载线程类，继承自QThread
    pyqt线程间通信,自定义信号，发出该信号时触发相应的槽，执行对应函数
    参考自：
    http://www.voidcn.com/article/p-risthuvv-bdr.html
    '''
    signalOut = QtCore.pyqtSignal(list)

    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)

        self.identity = None #线程名
        self.flag = True    #定义标志变量，方便从外部退出线程

    def setIdentity(self,text,serialObject):
        self.identity = text
        self.ser=serialObject    #将串口类传入线程，执行串口读取
        #print self.identity

    def run(self):
        '''
        线程开启后自动运行该函数, 直到flag标志为false, 函数自动退出，线程结束
        '''
        while self.flag:
            if self.ser.isOpen():
                try:
                    Bytes = self.ser.in_waiting #读取串口缓冲区中字节数
                    if Bytes>0:
                        data = self.ser.read(Bytes)#将缓冲区中字节全部读出                        
                        data = np.fromstring(data, np.uint8)
                        self.signalOut.emit(list(data))
                        #print(len(data))
                        #data是str类型, 但被槽函数接收之后变成了QString类型
                except Exception as e:
                    pass
                    #print e

class MainWindow(QtGui.QMainWindow, Ui_demo.Ui_Dialog):
    '''
    窗体类, 继承自QtGui.QMainWindow
    '''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.flag=True
        self.s = serial.Serial()#新建一个串口Object
        self.s.timeout = 1#1s未读取到串口数据则超时退出
        self.s.baudrate=115200
        self.wave = np.array([])#存储所有串口接收到的字符
        self.wav_file_name = ".tempwav.wav"
        self.PlayFlag = True
        self.framerate = 8000#采样频率
        self.setupUi(self)
 
        self.p = self.WavegraphicsView.addPlot()
        self.p.setYRange(-5, 260, padding=0) 
        self.p.showGrid(x=True, y=True, alpha=0.5) 
        self.curve = self.p.plot()

        self.updateUi()
        self.PlayButton.setEnabled(False)
        self.t = MyThread()
        self.t.setIdentity("Serial Read Thread", self.s)
        self.t.signalOut.connect(self.addtoText)
        self.t.start()
        thread.start_new_thread(self.DrawWave, ("thread: DrawWave", ))
        self.statusBar().showMessage('Ready!')
    def updateUi(self):
    	self.BaudratecomboBox.setCurrentIndex(self.BaudratecomboBox.findText("115200"))
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.setWindowTitle('SoundCollector')
        self.setWindowIcon(QtGui.QIcon('./images/littleStar.ico'))
        #self.SerialPortcomboBox = CustomComboBox(self)
        self.connect(self.StartButton, QtCore.SIGNAL('clicked()'), self.StartButton_process)        
        self.connect(self.StopButton, QtCore.SIGNAL('clicked()'), self.StopButton_process)
        self.connect(self.PlayButton, QtCore.SIGNAL('clicked()'), self.PlayButton_process)
        self.connect(self.OnOffButton, QtCore.SIGNAL('clicked()'), self.OnOffButton_process)  
        self.connect(self.DisInWaveradioButton, QtCore.SIGNAL('clicked()'), self.DisInWaveradioButton_process)
        self.connect(self.DisInValueradioButton, QtCore.SIGNAL('clicked()'), self.DisInValueradioButton_process)        
        self.connect(self.ClearReceiveBufpushButton, QtCore.SIGNAL('clicked()'), self.ClearReceiveBufpushbutton_process)        
        self.connect(self.ClearTransmitBufpushButton, QtCore.SIGNAL('clicked()'), self.ClearTransmitBufpushButton_process)        
        self.connect(self.BaudratecomboBox, QtCore.SIGNAL('activated(QString)'),self.BaudratecomboBox_Activated)
        self.connect(self.SerialPortcomboBox, QtCore.SIGNAL('activated(QString)'),self.SerialPortcomboBox_Activated)
        self.connect(self.DatabitscomboBox, QtCore.SIGNAL('activated(QString)'),self.DatabitscomboBox_Activated)
        self.connect(self.StopbitscomboBox, QtCore.SIGNAL('activated(QString)'),self.StopbitscomboBox_Activated)
        self.connect(self.ParitybitcomboBox, QtCore.SIGNAL('activated(QString)'),self.ParitybitcomboBox_Activated)

    def StartButton_process(self):
    	try:
            if self.s.isOpen():
                self.statusBar().showMessage('collecting...')
                self.s.flushInput()
                self.PlayFlag=True
                self.PlayButton.setEnabled(False)
                self.curve.setPos(0, 0)
                self.wave = np.array([])
                self.s.write(b'\xa9')
            else:
                QtGui.QMessageBox().question(self, 'msg', "The serial port has not been opened yet", QtGui.QMessageBox.Ok) 
        except Exception as e:
            print e
    def StopButton_process(self):
        try:
            if self.s.isOpen():
                self.s.write(b'\xb9')  
                self.statusBar().showMessage("Receive %d bytes"% len(self.wave))
                self.PlayButton.setEnabled(True)
                np.save("wave.npy",self.wave)
                wave_data = (self.wave.astype(np.short)-125)*600
                f = wave.open(self.wav_file_name, "wb")
                # 配置声道数、量化位数和取样频率
                f.setnchannels(1)
                f.setsampwidth(2)#byte
                f.setframerate(self.framerate)
                # 将wav_data转换为二进制数据写入文件
                f.writeframes(wave_data.tostring())
                f.close()
            else:
                QtGui.QMessageBox().question(self, 'msg', "The serial port has not been opened yet", QtGui.QMessageBox.Ok) 

        except Exception as e:
            print e
    def PlayButton_process(self):
        try:
            self.PlayFlag=False
            self.curve.setPos(0, 0)
            self.curve.setData(self.wave)
            winsound.PlaySound(self.wav_file_name, winsound.SND_ASYNC)
        except Exception as e:
            print e
    def OnOffButton_process(self):
        text = self.sender().text()
        try:
            if self.sender().text() == 'Close':
                if self.s.isOpen():                 
                    self.s.close()
                    self.OnOffButton.setText('Open')
                    self.SerialPortcomboBox.setEnabled(True)
                    self.BaudratecomboBox.setEnabled(True)
                    self.DatabitscomboBox.setEnabled(True)
                    self.StopbitscomboBox.setEnabled(True)
                    self.ParitybitcomboBox.setEnabled(True)
                    self.statusBar().showMessage("%s %s successfully!" % (text, self.s.port))
            else:
                if not self.s.isOpen():
                    self.s.open()
                    self.OnOffButton.setText('Close')
                    self.SerialPortcomboBox.setEnabled(False)
                    self.BaudratecomboBox.setEnabled(False)
                    self.DatabitscomboBox.setEnabled(False)
                    self.StopbitscomboBox.setEnabled(False)
                    self.ParitybitcomboBox.setEnabled(False)
                    self.statusBar().showMessage("%s %s successfully!" % (text, self.s.port))
        except Exception as e:
            QtGui.QMessageBox().question(self, 'msg', "fail to open/close port", QtGui.QMessageBox.Ok)
            print e
    def DisInWaveradioButton_process(self):
        self.stackedWidget.setCurrentWidget (self.page_2)
    def DisInValueradioButton_process(self):
        self.stackedWidget.setCurrentWidget (self.page)
    def ClearReceiveBufpushbutton_process(self):
        self.ReceiveBuftextBrowser.clear()
    def ClearTransmitBufpushButton_process(self):
        self.TransmittextEdit.clear()
    def BaudratecomboBox_Activated(self, text):
        self.s.baudrate=int(text)
        self.statusBar().showMessage("Baudrate : %s "% self.s.baudrate)
    def SerialPortcomboBox_Activated(self, text):
        self.s.port = str(text)
        self.statusBar().showMessage("Serial Port : %s "% self.s.port)
    def DatabitscomboBox_Activated(self, text):
        self.s.bytesize = int(text)
        self.statusBar().showMessage("Bytesize : %s "% self.s.bytesize)
    def StopbitscomboBox_Activated(self, text):
        if text=='1':
            self.s.stopbits = serial.STOPBITS_ONE
        elif text=='1.5':
            self.s.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        elif text=='2':
            self.s.stopbits = serial.STOPBITS_TWO
        self.statusBar().showMessage("Stopbits : %s "% self.s.stopbits)
    def ParitybitcomboBox_Activated(self, text):
        if text=="None":
            self.s.parity=serial.PARITY_NONE
        elif text=="Odd":
            self.s.parity=serial.PARITY_ODD
        elif text=="Even":
            self.s.parity=serial.PARITY_EVEN
        elif text=="Mark":
            self.s.parity=serial.PARITY_MARK
        elif text=="Space":
            self.s.parity=serial.PARITY_SPACE
        self.statusBar().showMessage("Parity : %s "% self.s.parity)
    def DrawWave(self, threadname):
        while self.flag:        
            if self.s.isOpen() and self.DisInWaveradioButton.isChecked() and self.PlayFlag:
                try:
                    if len(self.wave)>10000:
                        self.curve.setData(self.wave[-10000:-1])
                        self.curve.setPos(len(self.wave)-10000, 0)
                    else:
                        self.curve.setData(self.wave)
                except Exception as e:
                    print e
            time.sleep(0.1)
    def addtoText(self, data):
        #print(data)
        self.wave = np.hstack([self.wave, data])
        if self.DisInValueradioButton.isChecked():
            if self.ReceiveDisInHEXradioButton.isChecked():          
                self.ReceiveBuftextBrowser.append(str(data)[1:-1])
                self.statusBar().showMessage('Display in Decimal!')
            else:
                try:
                    self.ReceiveQTextEdit.append(''.join(chr(i) for i in data))
                except Exception as e:
                    self.statusBar().showMessage('encoded wrong!')
                else:
                    self.statusBar().showMessage('Display in Character!')
    def closeEvent(self, event):
        '''
        关闭窗口时先将线程的flag标志改成false
        使线程终止
        '''
        self.t.flag=False
        self.flag=False
        time.sleep(0.1)
        sys.exit("goodbye!")

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())