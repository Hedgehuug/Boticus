#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 12:31:26 2019

@author: Ben
"""

import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import datetime as dt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

charting_list = ['volume','close_time','asset_volume','trade_number','taker_buy_base','taker_buy_quote']

print ("*** PROGRAM STARTED ***")

price_df = pd.read_excel(r'BTCprice.xlsx')
chart_df = price_df


for column in charting_list:
    chart_df.pop(column)

chart_df['date'] = chart_df['date'].map(mdates.date2num)
chart_df = chart_df.iloc[-80::]

def chartboi():
    ax = plt.subplot()
    candlestick_ohlc(ax, chart_df.values, width=3, colorup='g', colordown='r')
    ax.xaxis_date()
    ax.grid(True)
    plt.show()
    plt.savefig('Chartboi.png')

chartboi()





