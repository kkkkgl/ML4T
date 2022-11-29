#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 12:47:31 2022

@author: connie
"""
import datetime as dt
from ManualStrategy import ManualStrategy 
from StrategyLearner import StrategyLearner
from experiment1 import insample_compare, outofsample_compare
from experiment2 import compare_impact
from marketsimcode import compute_portvals

def Manual_Benchmark_plot(symbol,sv):
    
    ms = ManualStrategy()
    ms.generate_my_plot(symbol,sv)


def experiment1():
    
    insample_compare(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000,commision=0,impact=0,verbose=False)
    outofsample_compare(symbol='JPM',sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000,commision=0,impact=0,verbose=False)
    
def experiment2():
    
    compare_impact(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    
def manual_trade():
    ms = ManualStrategy()
    trade_insample = ms.testPolicy(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    trade_outsample = ms.testPolicy(symbol='JPM',sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000)
    portvals_in = compute_portvals(trade_insample,100000,commission=0, impact=0) 
    portvals_out = compute_portvals(trade_outsample,100000,commission=0, impact=0) 
    
    return portvals_in,portvals_out

def strategy_learner():
    sl = StrategyLearner(verbose=False, impact=0, commission = 0)
    sl.add_evidence(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    trade_in = sl.testPolicy(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    trade_out = sl.testPolicy(symbol='JPM',sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000)
    portvals_in = compute_portvals(trade_in,100000,commission=0, impact=0) 
    portvals_out = compute_portvals(trade_out,100000,commission=0, impact=0) 
    
    return portvals_in,portvals_out

if __name__ == '__main__':
    
    symbol = 'JPM'
    sv = 100000 
    Manual_Benchmark_plot(symbol,sv)
    experiment1()
    experiment2()
    manual_trade()
    strategy_learner()