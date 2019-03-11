# readme.md

# 业务逻辑
使用pySerial进行串口读写
上位机发送开始录音命令, 上位机清空接收缓冲区(ser.flushInput()),
下位机接收到开始指令(串口接收中断)之后清空AD缓冲区, 打开中断, 在中断服务函数中进行AD转换,
将采集到的数据放入AD缓冲区中. 在主函数中判断AD缓冲区是否为空, 若不为空则将数据通过串口
发送到上位机.  
上位机发送停止录音命令, 上位机将接收缓冲区内数据全部读出, 存文件, 播放.
下位机接收到指令之后, 关闭AD采集的中断, 主函数中将AD缓冲区内数据全部发送到上位机.  

# 音频读取播放
[PyAudio](http://people.csail.mit.edu/hubert/pyaudio/)  
代码复制自: https://people.csail.mit.edu/hubert/pyaudio/docs/#id3
可读取\*.wav文件, 进行播放
运行前需安装pyAudio, 参考: https://people.csail.mit.edu/hubert/pyaudio/
pyAudio文档参考: https://people.csail.mit.edu/hubert/pyaudio/docs/
Plays a wave file.
Usage: python play.py filename.wav

# 串口接收(SerialRead.py)
调用pySerial控制串口, 由PC机向stm32发送开始采集命令(由命令行读入'a', 串口发送 b'\xa9' ),
单片机开始采集AD值, 放入AD缓冲区后再用串口发送给PC机.  
采集完成之后, 用户在命令行输入字符'b', 串口给stm32发送 b'\xb9' , 单片机接收后停止AD采样,
但AD缓冲区中的数据还会继续发送给PC机. PC机则把接收到的数据存储成\*.npy文件.  
这时如果要重新采集, 可以在命令行输入字符'a', 但是后面采集的数据会把前面的覆盖.  
采集完成之后, 命令行输入字符'c', 退出当前程序.  
usage:	
将PC机用USB转ttl模块连接到stm32  
打开cmd窗口, 进入的程序所在路径  
python SerialRead.py  

# GUI开发 
## PyQt4安装:  
下载合适版本的[PyQt4](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)  
将下载的文件放到合适目录下, cmd进入该目录  
pip install PyQt4-4.11.4-cp27-cp27m-win_amd64.whl

新建脚本运行测试, 会弹出一个hello world窗口
```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
from PyQt4.QtGui import *
import sys
a= QApplication(sys.argv)
w= QWidget()
w.resize(320, 240)
w.setWindowTitle("Hello World")
w.show()
sys.exit(a.exec_())
```

## 重构串口接收(gui.py)
这部分程序功能和SerialRead.py一样, 只是用按钮替换命令行字符命令:  
Start -- 'a'  
Stop  -- 'b'  
Quit  -- 'c'  
usage:	
将PC机用USB转ttl模块连接到stm32  
打开cmd窗口, 进入的程序所在路径  
python gui.py  

# Develop Log
2019/3/2:
- [ ] 完成pyAudio播放\*.wav文件的编程(./play.py ./demo.wav)
(\*.wav文件是别的地方复制过来的)

2019/3/11:
- [x] pySerial接收stm32发来的字节并解析成列表, 存储成\*.npy格式(./SerialRead.py)
- [x] 用PyQt4开发简单的图形界面, 实现同样的功能(./gui.py)


# 参考资料
[Welcome to pySerial’s documentation](https://pythonhosted.org/pyserial/)  
[PyQt4教程](http://www.qaulau.com/books/PyQt4_Tutorial/)  
[PyQt4 Reference Guide](http://pyqt.sourceforge.net/Docs/PyQt4/)  
[win10下安装PyQt4](https://blog.csdn.net/u013360881/article/details/80304033)  
[pySerial’s documentation](https://pythonhosted.org/pyserial/)  
