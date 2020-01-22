#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 15:21:21 2019

@author: Ben
"""

#U1 = current balance
u1 = float(865)
u1_working = u1

#Target Balance
uN = float

#weekly target
r = 1.05

#Periods
n = 52

#Formula = un = u1*(r^(n-1))

for a in range(n-1):
    u1_working = u1_working+20
    u1_working *= 1.05
    print('Currently at week ' + str(a+1) + '\ncurrent balance: ' + str(u1_working)+'\n')
    
print(u1_working)