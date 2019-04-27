# readme.md  

使用QtDesinger开发GUI程序：  
1. 在QtDesinger中拖拽控件完成界面布局,并修改命名和属性  
2. pyuic4 -o Ui_demo.py demo.ui从ui文件生成界面代码  
3. 新建python文件, 导入Ui_demo.py, 在已有的界面上实现需求  

一般情况下,不要试图修改Ui_demo.py文件, 因为每次运行pyuic4之后, 手动所做的修改都会被覆盖.  
但是对于本项目,我不得不这么做,所以每次更新Ui_demo.py后需要作以下修改:  
在from PyQt4 import QtCore, QtGui后面加上  
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
self.SerialPortcomboBox = CustomComboBox(self.layoutWidget2)
```
并将第141行左右的声明改为(括号内为空)
```python
self.WavegraphicsView = GraphicsWindow()
```