#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:44:55 2022

@author: connie
"""
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
import pandas as pd 
import matplotlib.pyplot as plt 
import datetime as dt 

def different_impact_to_learner(symbol,sd,ed,sv) :
    '''
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000 
    '''

    impact_list = [0.0, 0.005, 0.01, 0.1] 
    n = len(impact_list)
    portvals_list = []
    for impact in impact_list:
        sl = StrategyLearner(verbose=False, impact=impact, commission = 0)
        sl.add_evidence(symbol, sd, ed, sv)
        trade = sl.testPolicy(symbol,sd,ed,sv) 
        trade = trade[[symbol]]
        portvals = compute_portvals(trade,sv,commission= 9.95,impact = impact)
        portvals_list.append(portvals)
        
    return portvals_list

def compare_impact(symbol,sd,ed,sv):
    
    portvals_list = different_impact_to_learner(symbol,sd,ed,sv) 
    trade = pd.concat(portvals_list, axis = 1)
    normalized_trade = trade/trade.iloc[0]
    normalized_trade.columns = ['0.0', '0.005','0.01','0.1']
    
    normalized_trade.plot(kind='line')
    plt.legend(loc='upper left')
    plt.grid()
    plt.title('different impact to learner')
    plt.xlabel('date')
    plt.ylabel('cumulative return')
    plt.savefig('experiment2.png')

if __name__ == '__main__':
    compare_impact(symbol = 'JPM', sd = dt.datetime(2008,1,1), ed= dt.datetime(2009,12,31), sv= 100000)