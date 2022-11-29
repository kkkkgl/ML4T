#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:21:19 2022

@author: connie
"""
import datetime as dt 
import TheoreticallyOptimalStrategy as tos 
import marketsimcode as ms 
import indicators

def author():     
  return 'kdang49' 


if __name__ == '__main__':
  
    tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)  
    ms.compute_portvals()
    indicators.main()
