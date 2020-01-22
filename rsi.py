#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 18:00:56 2019

@author: Ben
"""
import pandas.DataFrame as df

class necessaryInfo():
    def __init__(self, coin):
        symb = coin
        
        candles = client.get_klines(symbol=symb, interval=client.KLINE_INTERVAL_1DAY)
        first_df = df(candles)
        
        
        
        
        
        
 def getCurrentTime():
        milli_sec = int(round(int(t.time) * 1000))
        toDays = int(round(milli_sec-(200*86400000)))
        return toDays
    
    
