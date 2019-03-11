#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt 
wav = np.load("wave.npy")
plt.plot(wav)
plt.show()