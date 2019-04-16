# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
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
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(731, 593)
        self.StartButton = QtGui.QPushButton(Dialog)
        self.StartButton.setGeometry(QtCore.QRect(20, 60, 93, 28))
        self.StartButton.setObjectName(_fromUtf8("StartButton"))
        self.StopButton = QtGui.QPushButton(Dialog)
        self.StopButton.setGeometry(QtCore.QRect(140, 60, 93, 28))
        self.StopButton.setObjectName(_fromUtf8("StopButton"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 100, 211, 61))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.DisInWaveradioButton = QtGui.QRadioButton(self.groupBox)
        self.DisInWaveradioButton.setGeometry(QtCore.QRect(10, 30, 115, 19))
        self.DisInWaveradioButton.setChecked(True)
        self.DisInWaveradioButton.setObjectName(_fromUtf8("DisInWaveradioButton"))
        self.DisInValueradioButton = QtGui.QRadioButton(self.groupBox)
        self.DisInValueradioButton.setGeometry(QtCore.QRect(90, 30, 115, 19))
        self.DisInValueradioButton.setObjectName(_fromUtf8("DisInValueradioButton"))
        self.DTRcheckBox = QtGui.QCheckBox(Dialog)
        self.DTRcheckBox.setGeometry(QtCore.QRect(150, 530, 51, 19))
        self.DTRcheckBox.setObjectName(_fromUtf8("DTRcheckBox"))
        self.RTScheckBox = QtGui.QCheckBox(Dialog)
        self.RTScheckBox.setGeometry(QtCore.QRect(40, 530, 51, 19))
        self.RTScheckBox.setObjectName(_fromUtf8("RTScheckBox"))
        self.TransmittextEdit = QtGui.QTextEdit(Dialog)
        self.TransmittextEdit.setGeometry(QtCore.QRect(260, 430, 451, 81))
        self.TransmittextEdit.setObjectName(_fromUtf8("TransmittextEdit"))
        self.ClearReceiveBufpushButton = QtGui.QPushButton(Dialog)
        self.ClearReceiveBufpushButton.setGeometry(QtCore.QRect(290, 380, 93, 28))
        self.ClearReceiveBufpushButton.setObjectName(_fromUtf8("ClearReceiveBufpushButton"))
        self.SaveReceiveBufpushButton = QtGui.QPushButton(Dialog)
        self.SaveReceiveBufpushButton.setGeometry(QtCore.QRect(420, 380, 93, 28))
        self.SaveReceiveBufpushButton.setObjectName(_fromUtf8("SaveReceiveBufpushButton"))
        self.ClearTransmitBufpushButton = QtGui.QPushButton(Dialog)
        self.ClearTransmitBufpushButton.setGeometry(QtCore.QRect(290, 520, 93, 28))
        self.ClearTransmitBufpushButton.setObjectName(_fromUtf8("ClearTransmitBufpushButton"))
        self.SendTransmitBufpushButton = QtGui.QPushButton(Dialog)
        self.SendTransmitBufpushButton.setGeometry(QtCore.QRect(420, 520, 93, 28))
        self.SendTransmitBufpushButton.setObjectName(_fromUtf8("SendTransmitBufpushButton"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(530, 380, 161, 31))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.ReceiveDisInHEXradioButton = QtGui.QRadioButton(self.groupBox_2)
        self.ReceiveDisInHEXradioButton.setGeometry(QtCore.QRect(20, 10, 51, 19))
        self.ReceiveDisInHEXradioButton.setChecked(False)
        self.ReceiveDisInHEXradioButton.setObjectName(_fromUtf8("ReceiveDisInHEXradioButton"))
        self.ReceiveDisInCHARradioButton = QtGui.QRadioButton(self.groupBox_2)
        self.ReceiveDisInCHARradioButton.setGeometry(QtCore.QRect(100, 10, 61, 19))
        self.ReceiveDisInCHARradioButton.setChecked(True)
        self.ReceiveDisInCHARradioButton.setObjectName(_fromUtf8("ReceiveDisInCHARradioButton"))
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(540, 520, 161, 31))
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.TransmitDisInHEXradioButtonradioButton = QtGui.QRadioButton(self.groupBox_3)
        self.TransmitDisInHEXradioButtonradioButton.setGeometry(QtCore.QRect(20, 10, 51, 19))
        self.TransmitDisInHEXradioButtonradioButton.setObjectName(_fromUtf8("TransmitDisInHEXradioButtonradioButton"))
        self.TransmitDisInCHARradioButtonradioButton = QtGui.QRadioButton(self.groupBox_3)
        self.TransmitDisInCHARradioButtonradioButton.setGeometry(QtCore.QRect(100, 10, 61, 19))
        self.TransmitDisInCHARradioButtonradioButton.setChecked(True)
        self.TransmitDisInCHARradioButtonradioButton.setObjectName(_fromUtf8("TransmitDisInCHARradioButtonradioButton"))
        self.stackedWidget = QtGui.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(260, 20, 451, 361))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.ReceiveBuftextBrowser = QtGui.QTextBrowser(self.page)
        self.ReceiveBuftextBrowser.setGeometry(QtCore.QRect(0, 20, 451, 331))
        self.ReceiveBuftextBrowser.setObjectName(_fromUtf8("ReceiveBuftextBrowser"))
        self.ReceiveZoneLabel = QtGui.QLabel(self.page)
        self.ReceiveZoneLabel.setGeometry(QtCore.QRect(0, 0, 81, 16))
        self.ReceiveZoneLabel.setObjectName(_fromUtf8("ReceiveZoneLabel"))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.widget = QtGui.QWidget(self.page_2)
        self.widget.setGeometry(QtCore.QRect(0, 0, 451, 351))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.WavegraphicsView = GraphicsWindow()
        self.WavegraphicsView.setObjectName(_fromUtf8("WavegraphicsView"))
        self.verticalLayout_3.addWidget(self.WavegraphicsView)
        self.stackedWidget.addWidget(self.page_2)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(21, 201, 71, 301))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.OnOfflabel = QtGui.QLabel(self.layoutWidget)
        self.OnOfflabel.setObjectName(_fromUtf8("OnOfflabel"))
        self.verticalLayout.addWidget(self.OnOfflabel)
        self.SerialPortlabel = QtGui.QLabel(self.layoutWidget)
        self.SerialPortlabel.setObjectName(_fromUtf8("SerialPortlabel"))
        self.verticalLayout.addWidget(self.SerialPortlabel)
        self.Baudratelabel = QtGui.QLabel(self.layoutWidget)
        self.Baudratelabel.setObjectName(_fromUtf8("Baudratelabel"))
        self.verticalLayout.addWidget(self.Baudratelabel)
        self.Databitslabel = QtGui.QLabel(self.layoutWidget)
        self.Databitslabel.setObjectName(_fromUtf8("Databitslabel"))
        self.verticalLayout.addWidget(self.Databitslabel)
        self.Stopbitslabel = QtGui.QLabel(self.layoutWidget)
        self.Stopbitslabel.setObjectName(_fromUtf8("Stopbitslabel"))
        self.verticalLayout.addWidget(self.Stopbitslabel)
        self.Paritybitlabel = QtGui.QLabel(self.layoutWidget)
        self.Paritybitlabel.setObjectName(_fromUtf8("Paritybitlabel"))
        self.verticalLayout.addWidget(self.Paritybitlabel)
        self.TransmitzoneLabel = QtGui.QLabel(Dialog)
        self.TransmitzoneLabel.setGeometry(QtCore.QRect(260, 410, 72, 15))
        self.TransmitzoneLabel.setObjectName(_fromUtf8("TransmitzoneLabel"))
        self.widget1 = QtGui.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(100, 180, 121, 331))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.gridLayout = QtGui.QGridLayout(self.widget1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.BaudratecomboBox = QtGui.QComboBox(self.widget1)
        self.BaudratecomboBox.setObjectName(_fromUtf8("BaudratecomboBox"))
        self.BaudratecomboBox.addItem(_fromUtf8(""))
        self.BaudratecomboBox.addItem(_fromUtf8(""))
        self.BaudratecomboBox.addItem(_fromUtf8(""))
        self.BaudratecomboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.BaudratecomboBox, 2, 0, 1, 1)
        self.DatabitscomboBox = QtGui.QComboBox(self.widget1)
        self.DatabitscomboBox.setObjectName(_fromUtf8("DatabitscomboBox"))
        self.DatabitscomboBox.addItem(_fromUtf8(""))
        self.DatabitscomboBox.addItem(_fromUtf8(""))
        self.DatabitscomboBox.addItem(_fromUtf8(""))
        self.DatabitscomboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.DatabitscomboBox, 3, 0, 1, 1)
        self.ParitybitcomboBox = QtGui.QComboBox(self.widget1)
        self.ParitybitcomboBox.setObjectName(_fromUtf8("ParitybitcomboBox"))
        self.ParitybitcomboBox.addItem(_fromUtf8(""))
        self.ParitybitcomboBox.addItem(_fromUtf8(""))
        self.ParitybitcomboBox.addItem(_fromUtf8(""))
        self.ParitybitcomboBox.addItem(_fromUtf8(""))
        self.ParitybitcomboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.ParitybitcomboBox, 5, 0, 1, 1)
        self.OnOffButton = QtGui.QPushButton(self.widget1)
        self.OnOffButton.setObjectName(_fromUtf8("OnOffButton"))
        self.gridLayout.addWidget(self.OnOffButton, 0, 0, 1, 1)
        self.SerialPortcomboBox = CustomComboBox(self.widget1)
        self.SerialPortcomboBox.setObjectName(_fromUtf8("SerialPortcomboBox"))
        self.gridLayout.addWidget(self.SerialPortcomboBox, 1, 0, 1, 1)
        self.StopbitscomboBox = QtGui.QComboBox(self.widget1)
        self.StopbitscomboBox.setObjectName(_fromUtf8("StopbitscomboBox"))
        self.StopbitscomboBox.addItem(_fromUtf8(""))
        self.StopbitscomboBox.addItem(_fromUtf8(""))
        self.StopbitscomboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.StopbitscomboBox, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.StartButton.setText(_translate("Dialog", "Start", None))
        self.StopButton.setText(_translate("Dialog", "Stop", None))
        self.groupBox.setTitle(_translate("Dialog", "数据显示方式", None))
        self.DisInWaveradioButton.setText(_translate("Dialog", "wave", None))
        self.DisInValueradioButton.setText(_translate("Dialog", "value", None))
        self.DTRcheckBox.setText(_translate("Dialog", "DTR", None))
        self.RTScheckBox.setText(_translate("Dialog", "RTS", None))
        self.ClearReceiveBufpushButton.setText(_translate("Dialog", "清除", None))
        self.SaveReceiveBufpushButton.setText(_translate("Dialog", "保存", None))
        self.ClearTransmitBufpushButton.setText(_translate("Dialog", "清除", None))
        self.SendTransmitBufpushButton.setText(_translate("Dialog", "发送", None))
        self.ReceiveDisInHEXradioButton.setText(_translate("Dialog", "HEX", None))
        self.ReceiveDisInCHARradioButton.setText(_translate("Dialog", "CHAR", None))
        self.TransmitDisInHEXradioButtonradioButton.setText(_translate("Dialog", "HEX", None))
        self.TransmitDisInCHARradioButtonradioButton.setText(_translate("Dialog", "CHAR", None))
        self.ReceiveZoneLabel.setText(_translate("Dialog", "接收数据值", None))
        self.label.setText(_translate("Dialog", "接收数据波形", None))
        self.OnOfflabel.setText(_translate("Dialog", "开/关", None))
        self.SerialPortlabel.setText(_translate("Dialog", "串口号", None))
        self.Baudratelabel.setText(_translate("Dialog", "波特率", None))
        self.Databitslabel.setText(_translate("Dialog", "数据位", None))
        self.Stopbitslabel.setText(_translate("Dialog", "停止位", None))
        self.Paritybitlabel.setText(_translate("Dialog", "校验位", None))
        self.TransmitzoneLabel.setText(_translate("Dialog", "发送区", None))
        self.BaudratecomboBox.setItemText(0, _translate("Dialog", "115200", None))
        self.BaudratecomboBox.setItemText(1, _translate("Dialog", "57600", None))
        self.BaudratecomboBox.setItemText(2, _translate("Dialog", "19200", None))
        self.BaudratecomboBox.setItemText(3, _translate("Dialog", "9600", None))
        self.DatabitscomboBox.setItemText(0, _translate("Dialog", "8", None))
        self.DatabitscomboBox.setItemText(1, _translate("Dialog", "7", None))
        self.DatabitscomboBox.setItemText(2, _translate("Dialog", "6", None))
        self.DatabitscomboBox.setItemText(3, _translate("Dialog", "5", None))
        self.ParitybitcomboBox.setItemText(0, _translate("Dialog", "None", None))
        self.ParitybitcomboBox.setItemText(1, _translate("Dialog", "Even", None))
        self.ParitybitcomboBox.setItemText(2, _translate("Dialog", "Odd", None))
        self.ParitybitcomboBox.setItemText(3, _translate("Dialog", "Mark", None))
        self.ParitybitcomboBox.setItemText(4, _translate("Dialog", "Space", None))
        self.OnOffButton.setText(_translate("Dialog", "Open", None))
        self.StopbitscomboBox.setItemText(0, _translate("Dialog", "1", None))
        self.StopbitscomboBox.setItemText(1, _translate("Dialog", "1.5", None))
        self.StopbitscomboBox.setItemText(2, _translate("Dialog", "2", None))

from pyqtgraph import GraphicsWindow
