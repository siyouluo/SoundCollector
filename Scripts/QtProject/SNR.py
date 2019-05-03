#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np
noise = np.load("noise.npy")
signal = np.load("signal.npy")

average_noise = np.mean(noise)
average_signal = np.mean(signal)

noise_AC = noise - average_noise
signal_AC = signal - average_signal

P_noise = np.sum(noise_AC*noise_AC)/len(noise_AC)
P_signal = np.sum(signal_AC*signal_AC)/len(signal_AC)
SNR = 10*np.log10(P_signal/P_noise)
print(u"信噪比 %f dB"%SNR)