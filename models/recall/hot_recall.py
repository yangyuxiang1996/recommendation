#!/usr/bin/env python
# coding=utf-8
'''
Author: Yuxiang Yang
Date: 2021-08-17 21:10:11
LastEditors: Yuxiang Yang
LastEditTime: 2021-08-17 21:43:09
FilePath: /recommendation/models/recall/hot_recall.py
Description: 
基于热度的召回
'''
import matplotlib.pyplot as plt
import math


def decay_function(alpha=0.01, init=10000, deltaT=100):
    data = []
    for t in range(deltaT):
        if len(data) == 0:
            temp = init / math.pow(t+1, alpha)  # math.exp(-alpha * math.log(t+1))
        else:
            temp = data[-1] / math.pow(t+1, alpha)  
        data.append(temp)

    plt.plot([t for t in range(deltaT)], data, label='alpha={}'.format(alpha))
        

init = 10000
deltaT = 60
plt.figure(figsize=(20, 8))
decay_function(0.05, init, deltaT)

plt.xticks([t for t in range(deltaT)])
plt.grid()
plt.legend()
plt.show()
    
    



