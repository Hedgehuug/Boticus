#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 16:00:24 2019

@author: Ben
"""

import pandas as pd
from pandas import DataFrame as df
import BitcoinChart
import matplotlib.dates as mdates
import configparser


config = configparser.ConfigParser()
config.read(r'OpenOrders.ini')
coinlist = list(config['settings']['coinlist'].split(','))
necessaryInfo = BitcoinChart.necessaryInfo
allTheCharts = BitcoinChart.allTheCharts
swapData = BitcoinChart.swapData
columnList = ['date','open','high','low','close']



    #RETRIEVES AND SAVES DATA FROM BINANCE
for s in coinlist:
    btcboi = necessaryInfo(s)
    fileName = str(s + '_Graph')
    print(fileName + '\n processing...')
    date_df = btcboi.first_df()
    date_df.to_excel(f'KleinsData/{fileName}.xlsx')
    print(fileName + ' has finished saving \n ------------------------')


    
print("Now calculating EMA")


    #CALCULATES Exponential Moving Average(EMA) for strategy
for a in coinlist:
    fileName = str(a + '_Graph')
    chartName = str(a + '_Chart')
    maName = str(a+'_EMA')
    price_df = pd.read_excel(f'KleinsData/{fileName}.xlsx')
    swappingData = swapData(price_df,None,None)
    t_df = swappingData.dfMa()
    t_df = t_df.iloc[::-1]
    t_df.to_excel(f'MovingAverages/{maName}.xlsx')
    disChart = allTheCharts(None,None, price_df)
    candle_df = disChart.prepareCandle()
    maChart = allTheCharts(t_df,chartName, candle_df)    
    print(fileName + ' has finished importing\n--------------------------\nNow saving chart')
    maChart.chartMA()
    #if(t_df.loc[499:'MA10':] < t_df.loc[499:'MA15']):
        
 
