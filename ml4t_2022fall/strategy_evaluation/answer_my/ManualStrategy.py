#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 10:40:59 2022

@author: connie
"""

import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import random  		  	   		  	  		  		  		    	 		 		   		 		  	  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  	  		  		  		    	 		 		   		 		  
import util as ut  		
from indicators import sma, momentum,bollinger_bands
from util import get_data, plot_data  
import QLearner as ql
import matplotlib.pyplot as plt 
from marketsimcode import compute_portvals

class ManualStrategy():
    
    def __init__(self,):
        self.lookback = 10 
        pass 
    
    def author(self,):
        return 'kdang49'

    def testPolicy(self, symbol, sd, ed, sv):
        
        '''
        symbol = 'JPM'
        sd = dt.datetime(2008,1,1)
        ed = dt.datetime(2009,12,31)
        '''
        
        #### get symbol data ####
        data = get_data([symbol],pd.date_range(sd,ed))
        normalized_data = data/data.iloc[0] 
        df = data[['SPY']]
        df = df.rename(columns={'SPY': symbol})
        df[:] = 0
        dates = df.index
        
        
        #### get indicators ####
        _sma, sma_ratio = sma(data,self.lookback)
        _mtm = momentum(data,self.lookback)
        _bbands = bollinger_bands (data,_sma,self.lookback)
        _sma_ratio =  sma_ratio[symbol]
        _mtm = _mtm[symbol]
        _bbands = _bbands[symbol]
        
        
        #### my trading actions #### 
        #### set position #### 
        position = 0 
        #### mark long short for each indicator #### 
        _sma_ratio_ls = 0 
        _mtm_ls = 0 
        _bbands_ls = 0 
        for i in range(df.shape[0]):
            today = dates[i]
            ##### update _sma_ratio_ls ####
            if _sma_ratio.loc[today] > 0.5:
                _sma_ratio_ls = -1 
            elif _sma_ratio.loc[today] < -0.5:
                _sma_ratio_ls = 1
            else:
                _sma_ratio_ls = 0 
            #### update _mtm_ls #### 
            if _mtm.loc[today] > 0.5:
                _mtm_ls = -1 
            elif _mtm.loc[today] < -0.5:
                _mtm_ls = -1 
            else:
                _mtm_ls = 0 
            #### update _bbands_ls ####
            if _bbands.loc[today] > 1:
                _bbands_ls = -1 
            elif _bbands.loc[today] < -1:
                _bbands_ls = 1
            else:
                _bbands_ls = 0 
            #### maunally combine the ls to give signals #### 
            '''
            long_signal = 1
            short_signal = 2
            hold_signal = 0 
            '''
            ls_sum = _sma_ratio_ls + _mtm_ls + _bbands_ls
            if ls_sum >= 2:
                #long#
                signal = 1                    
            elif ls_sum <= -2.5:
                #short#
                signal = 2 
            else:
                signal = 0 
            df.loc[today].loc[symbol] = signal
        trade = self.signal_to_trade([symbol],df)
        trade = trade.rename(columns={'Trade': symbol})
        '''
        portvals = compute_portvals(trade,
                                    100000,  		  	   		  	  		  		  		    	 		 		   		 		  
                                    0,  		  	   		  	  		  		  		    	 		 		   		 		  
                                    0,
                                    )
            '''
        return trade
        
            
    def signal_to_trade(self, symbol, df):
        
        '''symbol = ['JPM']'''
        position = 0 
        symbol = symbol[0]
        dates = df.index
        df['Position'] = 0 
        df['Trade'] = 0 
        
        for i in range(df.shape[0]):
            today = dates[i]
            if df.at[today,symbol] == 1:
                if position == - 1000:
                    trade = 2000
                elif position < 1000:
                    trade =  1000
                else:
                    trade = 0 
            elif df.at[today,symbol] == 2:
                if position == 1000:
                    trade = - 2000
                elif position > (-1) * 1000:
                    trade = -1 * 1000
                else:
                    trade = 0 
            else:
                trade = 0 
            position += trade 
            df.at[today,'Position'] = position
            df.at[today,'Trade'] = trade
        df.to_csv('df.csv')
        trade = df[['Trade']]
        return trade
    
    def benchmark(self,symbol,sd,ed):
        '''
        symbol = 'JPM'
        sd = dt.datetime(2008,1,1)
        ed = dt.datetime(2009,12,31)
        sv = 100000

        '''
        data = get_data([symbol],pd.date_range(sd,ed))
        sym_data = data[[symbol]]
        sym_data['benchmark'] = 1000*sym_data[symbol]
        benchmark = sym_data[['benchmark']]
        return benchmark 
    
    def performance_metrics(self,symbol,sd,ed,sv):
        '''
        
        '''
        trade = self.testPolicy(symbol, sd, ed, sv)
        portvals = compute_portvals(trade,sv,commission=9.95,impact=0.005)
        portvals = portvals/portvals.iloc[0]
        benchmark = get_data([symbol],pd.date_range(sd,ed))
        benchmark = benchmark[symbol]
        benchmark = benchmark/benchmark.iloc[0]
        
        # cumulative return 
        cr_ben = benchmark[-1] / benchmark[0] - 1
        cr_the = portvals[-1] / portvals[0] - 1
    
        # adily return in percentage
        dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
        dr_the = (portvals / portvals.shift(1) - 1).iloc[1:]
    
        # [Stdev of daily returns]
        sddr_ben = dr_ben.std()
        sddr_the = dr_the.std()
    
        # [Mean of daily returns]
        adr_ben = dr_ben.mean()
        adr_the = dr_the.mean()

        print("")
        print("[ManualStrategy]")
        print("Cumulative return: " + str(cr_the))
        print("Stdev of daily returns: " + str(sddr_the))
        print("Mean of daily returns: " + str(adr_the))
        print("")
        print("[Benchmark]")
        print("Cumulative return: " + str(cr_ben))
        print("Stdev of daily returns: " + str(sddr_ben))
        print("Mean of daily returns: " + str(adr_ben))
        print("")
        
        
    def generate_my_plot(self, symbol, sv) :
        
        
        in_sd = dt.datetime(2008,1,1)
        in_ed = dt.datetime(2009,12,31) 
        
        out_sd = dt.datetime(2010,1,1)
        out_ed = dt.datetime(2011,12,31)
        
        short_in = [] 
        long_in = [] 
        short_out = []
        long_out = []
        
        benchmark = get_data([symbol],pd.date_range(in_sd,in_ed),'Adj Close')
        benchmark = benchmark[[symbol]]*1000
        trade_in = self.testPolicy(symbol, in_sd, in_ed, sv)
        dates_in = trade_in.index 
        for i in range(len(trade_in)):
            date = dates_in[i]
            if trade_in.at[date,symbol] < 0:
                short_in.append(date)
            elif trade_in.at[date,symbol] > 0:
                long_in.append(date)
            else:
                pass 
        portvals_in = compute_portvals(trade_in, start_val = sv, commission=9.95, impact=0.005)
        normalized_benchmark_in = benchmark/benchmark.iloc[0]
        normalized_portvals_in = portvals_in/portvals_in.iloc[0]
        plt.figure(figsize = (12,8))
        plt.plot(normalized_portvals_in,label='Manual',color='red')
        plt.plot(normalized_benchmark_in, label ='Benchmark', color ='purple')
        plt.grid()
        plt.title('In sample Manual & Benchmark')
        plt.xlabel('date')
        plt.ylabel('cumulative return')
        for date in short_in:
            plt.axvline(date, color ='black')
        for date in long_in:
            plt.axvline(date, color = 'blue')
        plt.legend() 
        plt.savefig('Manual&Benchmark-insample.png')
        
        
        benchmark = get_data([symbol],pd.date_range(out_sd,out_ed),'Adj Close')
        benchmark = benchmark[[symbol]]*1000
        trade_out = self.testPolicy(symbol, out_sd, out_ed, sv)
        dates_out = trade_out.index 
        for i in range(len(trade_out)):
            date = dates_out[i]
            if trade_out.at[date,symbol] < 0:
                short_out.append(date)
            elif trade_out.at[date,symbol] > 0:
                long_out.append(date)
            else:
                pass 
        trade_out = self.testPolicy(symbol, out_sd, out_ed, sv)
        portvals_out = compute_portvals(trade_out, start_val = sv, commission=9.95, impact=0.005)
        normalized_benchmark_out = benchmark/benchmark.iloc[0]
        normalized_portvals_out = portvals_out/portvals_out.iloc[0]
        plt.figure(figsize = (12,8))
        plt.plot(normalized_portvals_out,label='Manual',color='red')
        plt.plot(normalized_benchmark_out, label ='Benchmark', color ='purple')
        plt.grid()
        plt.title('Out of sample Manual & Benchmark')
        plt.xlabel('date')
        plt.ylabel('cumulative return')
        for date in short_out:
            plt.axvline(date, color ='black')
        for date in long_out:
            plt.axvline(date, color = 'blue')
        plt.legend() 
        plt.savefig('Manual&Benchmark-outsample.png')
        
        
        
        pass 

if __name__ == '__main__':
    
    self = ManualStrategy()
    trade =  self.testPolicy('JPM',
                                  dt.datetime(2008,1,1),
                                  dt.datetime(2009,12,31),
                                  100000)    
    
    self.performance_metrics('JPM',
                                  dt.datetime(2008,1,1),
                                  dt.datetime(2009,12,31),
                                  100000) 
    
    self.generate_my_plot('JPM', 100000)
    trade.to_csv('trade.csv')
    
    
        
        
        
        
        
        
        