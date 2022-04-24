# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:02:15 2022

@author: pc
"""

import heartpy as hp
import matplotlib.pyplot as plt

sample_rate = 400

data = hp.get_data('h1_filter_Output_mono.csv')

plt.figure(figsize=(12,4))
plt.plot(data)
plt.show()

#run analysis
wd, m = hp.process(data, sample_rate)

#visualise in plot of custom size
plt.figure(figsize=(12,4))
hp.plotter(wd, m)

#display computed measures
for measure in m.keys():
        print('%s: %f' %(measure, m[measure]))
        