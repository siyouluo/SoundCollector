#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
本文件复制自: https://people.csail.mit.edu/hubert/pyaudio/docs/#id3
可读取*.wav文件, 进行播放
运行前需安装pyAudio, 参考: https://people.csail.mit.edu/hubert/pyaudio/
pyAudio文档参考: https://people.csail.mit.edu/hubert/pyaudio/docs/
Plays a wave file.
Usage: python play.py filename.wav
'''
import pyaudio
import wave
import sys

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()