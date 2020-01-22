#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:18:46 2019

@author: Ben
"""


from BinanceKeys import BinanceKey1

import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
from pandas import DataFrame as df
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime as dt
from binance.client import Client
from binance.enums import *
import numpy as np
from scipy.signal import argrelextrema
import configparser
from scipy import signal

config = configparser.ConfigParser()
api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
client = Client(api_key,api_secret)
charting_list = ['volume','close_time','asset_volume','trade_number','taker_buy_base','taker_buy_quote']
r = int
config.read(r'OpenOrders.ini')
coinlist = list(config['settings']['coinlist'].split(','))


    #CLASS TO RETRIEVE DATA FROM BINANCE AND SAVE IT AS AN EXCEL FILE
class necessaryInfo():
    def __init__(self, coin):
        symb = coin
        
        candles = client.get_klines(symbol=symb, interval=client.KLINE_INTERVAL_4HOUR)
        self.currentPrice = client.get_ticker(symbol=symb)
        self.candles_data_frame = df(candles)
        self.candles_data_frame_date = self.candles_data_frame[0]
        
        #ORGANISE AND STRIP FETCHED DATA FOR RELEVANT INFORMATION
    def first_df(self):
        candles = self.candles_data_frame_date  
        candles_full = self.candles_data_frame
        candles_full.pop(0)
        candles_full.pop(11)
        final_date = []
        for time in candles.unique():
            readable = dt.fromtimestamp(int(time/1000))
            final_date.append(readable)
            
        date_df = df(final_date, columns = ['date'])
        final_df = date_df.join(candles_full)
        final_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'asset_volume', 'trade_number', 'taker_buy_base', 'taker_buy_quote']
        for column in charting_list:
            final_df.pop(column)
        return final_df
    
    
    def current_price(self):
        currentTicker = self.currentPrice
        currentPrice = currentTicker['lastPrice']
        print(currentPrice)
        return(currentPrice)
        
        
        

    #CLASS FOR ORGANISING THE DATAFRAME TO BE USED FOR DATA ANALYSIS BY THE BOT
class swapData():
    def __init__(self,df1,df2,df3):
        self.df1 = df1
        self.df2 = df2
        self.df3 = df3
        
        
        #CHANGE AND LABEL DATAFRAMES FOR FURTHER READING
    def dfMa(self):
        df1 = self.df1
        #df1.pop('Unnamed: 0')
        df1 = df1.iloc[-100::]
        p_df = df1['close']
        d_df = df(df1['date'])
        #ma_p_df = df(p_df.rolling(window=10).mean())
        ma_p_df = df(p_df.ewm(span=10,min_periods=10,adjust=False).mean())
        #ma_20_p = df(p_df.rolling(window=20).mean())
        ma_20_p = df(p_df.ewm(span=20,min_periods=20,adjust=False).mean())
        ma_p_df.columns = ['EMA10']
        ma_20_p.columns = ['EMA20']
        ma_p_df['EMA10'] = ma_p_df['EMA10'].fillna(0)
        ma_20_p['EMA20'] = ma_20_p['EMA20'].fillna(0)
        f_df = d_df.join(ma_p_df['EMA10'])
        t_df = f_df.join(ma_20_p['EMA20'])
        t_df = t_df.join(p_df)
        t_df['date'] = t_df['date'].map(mdates.date2num)
        t_df['date'] = t_df['date'] - 2
        t_df = t_df.iloc[-80::]
        return t_df
        
        



    #CLASS FOR CHARTING CANDLES AND INDICATORS
class allTheCharts():
    def __init__(self, dataFrame, name, ogFrame):
        self.frame = dataFrame
        self.ax = plt.subplot(title=name)
        self.name = name
        self.ogFrame = ogFrame
        

        #DEFINES ALL VARIABLES, PRINTS AND SAVES EMA CHART
    def chartMA(self):
        ax = self.ax
        frame = self.frame
        name = self.name
        ogFrame = self.ogFrame
        candlestick_ohlc(ax, ogFrame.values, width=0.09, colorup='g', colordown='r',)
        frame.plot(kind='line',x='date',y='EMA10',ax=ax)
        frame.plot(kind='line',x='date',y='EMA20',color='purple',ax=ax)
        plt.savefig(f'Charts/{name}.png')
        plt.show()
        return
    
    
        #CREATE AND MATCH CANDLESTICK CHART TO MATCH WITH INDICATORS
    def prepareCandle(self):
        ogFrame = self.ogFrame
        ogFrame = ogFrame.iloc[-80::]
        ogFrame['date'] = ogFrame['date'].map(mdates.date2num)
        ogFrame['date'] = ogFrame['date'] - 2
        candle_df = df(ogFrame)
        return candle_df
 
    



class MACD_MinMax():
    def __init__(self,dataframe):
        self.dataframe = dataframe
        
        
    def get_min_max(self):
        data_frame = self.dataFrame
        data_x = data_frame['date']
        data_x = data_x.map(mdates.date2num)
        data_y = data_frame['close']
        
        
        peak_indexes = signal.argrelextrema(data_y.values,np.greater)
        peak_indexes = peak_indexes[0]
        
        low_indexes = signal.argrelextrema(data_y.values,np.less)
        low_indexes = low_indexes[0]
        
        date_df = df(data_x,columns=['date','index'])
        date_df['index'] = date_df.index
    
        
        readable_peak = np.array(peak_indexes).tolist()
        readable_low = np.array(low_indexes).tolist()
        
        charting_peak = []
        charting_low = []
        
        for x in readable_peak:
            for i in date_df['index']:
                if(x==i):
                    charting_peak.append(date_df['date'][x])
                    
        for x in readable_low:
            for i in date_df['index']:
                if(x==i):
                    charting_low.append(date_df['date'][x])
                               
        data_y_list = []
        
        for y in data_y:
            data_y_list.append(float(y))
             
        peak_x = charting_peak
        peak_y = []
        for a in readable_peak:
            peak_y.append(data_y_list[a])
        
        
        
        low_x = charting_low
        low_y = []
        for a in readable_low:
            low_y.append(data_y_list[a])
    
    
        (fig,ax) = plt.subplots()
        #candlestick_ohlc(ax, df(data_frame.values), width=0.09, colorup='g', colordown='r')
        ax.plot(data_x,data_y_list,color='blue')
        plt.scatter(peak_x,peak_y,color='orange',alpha=.5,label='Peaks')
        plt.scatter(low_x,low_y,color='green',alpha=.5,label='Lows')
        plt.show()
        figName = 'Low-High'
        plt.savefig(f'Charts/{figName}.png',dpi=300)
        
    def macd(self):
        
    
    
'''
for coin in coinlist:   
    first_df = necessaryInfo(coin).first_df()
    #test_minMaxFrame = get_min_max(swapData(first_df,None,None).dfMa())
    minMax = get_min_max(first_df)        
'''

        
        
        

    