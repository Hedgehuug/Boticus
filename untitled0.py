#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:32:26 2019

@author: Ben
"""

#!/usr/bin/python3
import matplotlib
matplotlib.use('Agg') # Bypass the need to install Tkinter GUI framework
 
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

data_x_testing = np.arange(start = 0, stop = 25, step = 1, dtype='int')
data_y_testing = np.random.random(25)*6

peak_indexes_testing = signal.argrelextrema(data_y_testing,np.greater)
peak_indexes_testing = peak_indexes_testing[0]

valley_indexes_testing = signal.argrelextrema(data_y_testing, np.less) 
valley_indexes_testing = valley_indexes_testing[0]

(fig,ax) = plt.subplots()
ax.plot(data_x_testing,data_y_testing)

peak_x_t = peak_indexes_testing
peak_y_t = data_y_testing[peak_indexes_testing]

plt.scatter(peak_x_t,peak_y_t,color='orange',alpha=.5,label='Peaks')
ax.plot(peak_x_t,peak_y_t,linestyle='dashed',color='green')

low_x_t = valley_indexes_testing
low_y_t = data_y_testing[valley_indexes_testing]

plt.scatter(low_x_t,low_y_t,color='orange',alpha=.5,Label='Lows')
ax.plot(low_x_t,low_y_t,linestyle='dashed',color='red')

def main():
    # Generate random data.
    data_x = np.arange(start = 0, stop = 25, step = 1, dtype='int')
    data_y = np.random.random(25)*6
     
    # Find peaks(max).
    peak_indexes = signal.argrelextrema(data_y, np.greater)
    peak_indexes = peak_indexes[0]
     
    # Find valleys(min).
    valley_indexes = signal.argrelextrema(data_y, np.less)
    valley_indexes = valley_indexes[0]
     
    # Plot main graph.
    (fig, ax) = plt.subplots()
    ax.plot(data_x, data_y)
     
    # Plot peaks.
    peak_x = peak_indexes
    peak_y = data_y[peak_indexes]
    ax.plot(peak_x, peak_y, marker='o', linestyle='dashed', color='green', label="Peaks")
     
    # Plot valleys.
    valley_x = valley_indexes
    valley_y = data_y[valley_indexes]
    ax.plot(valley_x, valley_y, marker='o', linestyle='dashed', color='red', label="Valleys")
     
     
    # Save graph to file.
    plt.title('Find peaks and valleys using argrelextrema()')
    plt.legend(loc='best')
    plt.savefig('argrelextrema.png')
    
