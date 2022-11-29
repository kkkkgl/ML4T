'''
ShuHo Chou: schou33
'''
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import util as ut
import BagLearner as bl
import DTLearner as dt
import numpy as np
from indicators import exponential_moving_average, simple_moving_average, bollinger_band
from marketsimcode import marketsim
import StrategyLearner as sl
import ManualStrategy as ms
import random

def author():
    return 'schou33'

if __name__ == '__main__':
    symbol = 'JPM'
    # sd = datetime.datetime(2010, 1, 1)
    # ed = datetime.datetime(2011, 12, 31)
    sd = datetime.datetime(2008, 1, 1)
    ed = datetime.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    prices_all = ut.get_data([symbol], dates)  # automatically adds SPY


    prices = ut.get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    benchmark_trades = prices_all[[symbol,]].copy(deep=True)  # only portfolio symbols
    benchmark_trades.values[:, :] = 0
    benchmark_trades.values[0, :] = 1000
    vals_bench = marketsim(benchmark_trades, prices)

    learner = sl.StrategyLearner(verbose = False, impact = 0) # constructor
    learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = 100000) # training phase
    df_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000) # testing phase
    vals_ml = marketsim(df_trades, prices, impact = 0)

    manual_trades = ms.testPolicy(symbol=symbol, sd=sd, ed=ed)
    vals_manual = marketsim(manual_trades, prices, impact = 0, commission = 0)

    # portvals = portvals / portvals.ix[0]
    vals_bench = vals_bench / vals_bench.ix[0]
    vals_ml = vals_ml / vals_ml.ix[0]
    vals_manual = vals_manual / vals_manual.ix[0]

    benchmark, = plt.plot(vals_bench, 'b', label = 'Benchmark')
    mystrategy, = plt.plot(vals_manual, 'k', label = 'Manual Strategy')
    mlstrategy, = plt.plot(vals_ml, 'r', label = 'ML strategy')

    plt.legend(handles=[benchmark, mystrategy, mlstrategy], loc=2)
    plt.show()
