#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 13:30:03 2019

@author: Ben
"""

'''
    This file is a test for logic of creating orders
'''

from pandas import DataFrame as df
import pandas as pd
import configparser


config = configparser.ConfigParser()
def main():   
        #Declare Variable
    config.read(r'OpenOrders.ini')
    allocated_balance = config.getfloat('settings','balance')
    coinlist = list(config['settings']['coinlist'].split(','))
    maFileName = str
    nm = {}
    daily_check = allocated_balance
    i = 0          
    for coin in coinlist:
        maFileName = str(coin + '_EMA')
        price_df = pd.read_excel(f'MovingAverages/{maFileName}.xlsx')
        price_df.pop("Unnamed: 0")
        nm.update({str(coin):price_df})
        
    
    for int in range(1000):
        
        
        post_nm = dict(nm)
        openOrders = dict(config['openOrders'])
        for a,b in openOrders.items():
            b = list(b.split(','))
            item = (item.strip() for item in b)
            b = list(map(float,b))
            openOrders.update({a:b})
        openOrders_backup = dict(openOrders)
    
        #1: Check open orders                
        lkj = working(allocated_balance,coinlist,openOrders,nm,None)
        orders_toDelete = lkj.checkOpenOrder()
        
        brap = working(allocated_balance,None,nm,orders_toDelete,openOrders_backup).calculateProfit()
        print(brap)
        allocated_balance = brap + allocated_balance
        config['settings']['balance'] = str(allocated_balance)
        with open('OpenOrders.ini','w') as configfile:
            config.write(configfile)
        #2: Sell if requirements are met/update base balance
        for item in orders_toDelete:
            del openOrders_backup[item]
        for item in openOrders_backup:
            del post_nm[item.upper()]
        

        #3: Place Order
        for a,b in openOrders.items():
            openOrders.update({a:str(b).strip('[]')})
        checkOrder = working(allocated_balance,None,openOrders,post_nm,None)
        checkOrder.makeOrder()
        
        print('------')
        for poo,loo in nm.items():
            nm.update({poo:loo.shift()})
            
    print('done')
                   

    #MAIN CLASS TO ANALYSE FILE
class working():
    def __init__(self,money,symbols,orders,dictionary,df1):
        self.order = orders
        self.money = money*0.2
        self.symbols = symbols
        self.dictionary = dictionary
        self.df1 = df1
        self.interval = 979
        

        #TESTING FUNCTIONALITY
    def printing(self):
        symbl = self.dictionary
        print(symbl)
        
        
        #CREATES A TEST-ORDER
    def makeOrder(self):
        orders = self.order
        dic = self.dictionary
        money = self.money
        lust = dict
        for a,b in dic.items():
            lust = b
            if((lust.at[self.interval,'EMA10']) > lust.at[self.interval,'EMA20']):
                aa = lust.at[self.interval,'close']
                ab = [money,aa]
                ab = str(ab).strip('[]')
                orders.update({a:ab})
        config['openOrders'] = orders
        with open('OpenOrders.ini','w') as configfile:
            config.write(configfile)
        return

        
        
        
        #Checks if the open orders have been satisfied prior to placing any new ones
    def checkOpenOrder(self):
        dicl = self.dictionary
        orders = self.order
        to_delete = []
        for t,y in orders.items():
            get_price = dicl[t.upper()]
            if(get_price.at[self.interval,'EMA10'] < (get_price.at[self.interval,'EMA20'])):
                to_delete.append(t)
                
        for item in to_delete:
            del orders[item]
        return to_delete
    
    
    
    
    
    def calculateProfit(self):

        to_delete = self.dictionary
        sell_dataframe = self.order
        money = self.money
        price_df = self.df1
        amc = []
        smr = []
        for item in to_delete:
            amc = sell_dataframe[item.upper()]
            aa = price_df[item][1]
            ab = price_df[item][0]
            ac = amc.at[self.interval,'close']
            pre_cal = ac/aa
            final_sell = (ab * pre_cal)-ab
            smr.append(final_sell)
            print('Position closed:\nInitial investment and invested amount(usdt): ',aa,'/',ab,'\nPosition closed at: ',ac,'\nTotal Profit: ',final_sell)    
        profit2 = sum(smr)

        return(profit2)
        

    
    
 












