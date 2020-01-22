#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:56:06 2019

@author: Ben
"""

import time as t
import sys
b = t.time

milli_sec = int(round(t.time() * 1000))
toDays = int(round(milli_sec-(200*86400000)))



def getCurrentTime(self):
    milli_sec = int(round(int(t.time) * 1000))
    toDays = int(round(milli_sec-(200*86400000)))
    return toDays


