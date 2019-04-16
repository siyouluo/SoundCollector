#readme.md
更新Ui_demo.py后需要在from PyQt4 import QtCore, QtGui后面加上
```python
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
```
并将SerialPortcomboBox的QtGui.QComboBox改为CustomComboBox
```python
self.SerialPortcomboBox = CustomComboBox(self.layoutWidget1)
```
并将第141行左右的声明改为(括号内为空)
```python
self.WavegraphicsView = GraphicsWindow()
```