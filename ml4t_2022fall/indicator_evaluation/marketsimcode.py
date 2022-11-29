#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:23:21 2022

@author: connie
"""

import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import os  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  	
import math	  	   		  	  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  
import matplotlib.pyplot as plt
import TheoreticallyOptimalStrategy as tos

def author(): 
    
  return 'kdang49' 

def compute_portvals(  		
  	   		  	  		  		  		    	 		 		   		 		   		  	   		  	  		  		  		    	 		 		   		 		  
    start_val = 100000,  		  	   		  	  		  		  		    	 		 		   		 		  
    commission = 0,  		  	   		  	  		  		  		    	 		 		   		 		  
    impact = 0,
    trades = tos.testPolicy(),
    symbols = ['JPM']):  	
    
    
    '''  		  	  		  		  		    	 		 		   		 		  
    trades = tos.testPolicy()
    start_val = 100000
    commission = 0
    impact = 0
    symbols = ['JPM']
    '''
    
    
    orders = trades.sort_index(axis = 0)
    start_date = orders.index[0]
    end_date = orders.index[-1]
    
    dfs = []
    for symbol in symbols:
        value = get_data([symbol], pd.date_range(start_date, end_date)) 
        value = value[[symbol]]
        dfs.append(value)
    dfs = pd.concat(dfs, join='outer', axis=1)
    merge = pd.merge(orders,dfs,how='outer',left_index=True,right_index=True)
    merge = merge.reset_index()
    
    total_rows = merge.shape[0]
    cash = start_val
    
    stock_list = []
    for i in symbols:
        stock = i + '_stock'
        stock_list.append(stock)
    
    
    prev_stock_list = [] 
    for i in symbols:
        stock = i + '_prev_stock'
        prev_stock_list.append(stock)

    prev_stock_dict = dict(zip(prev_stock_list, [None]*len(prev_stock_list)))
        
    #set each stock initial share number as 0 
    for i in stock_list:
        merge[i] = 0
        
    
    merge['Order'] = merge['Trade'].apply(lambda x: 'SELL' if x<0 else( 'BUY' if x>0 else 'HOLD'))    
    merge['Shares'] = merge['Trade'].apply(lambda x: abs(x))  
    merge['cash'] = 0.0
    merge['equity_value'] = 0.0
    merge['port_value'] = 0.0
    merge['market_impact'] = 0.0
    merge['Symbol'] = 'JPM'
    

    #method 1 
    cash = start_val
    prev_cash = cash 
    prev_stock = 0 
    
    for i, row in merge.iterrows():
        
        merge.at[i,'prev_cash'] = prev_cash
        
        if row['Order']=='BUY':
            
            value_change = row[symbol]*row['Shares']*(1+impact)
            cash = prev_cash - value_change - commission
            merge.at[i,'cash'] = cash
            
        elif row['Order']=='SELL':
            merge.at[i,'prev_cash'] = prev_cash
            value_change = row[symbol]*row['Shares']*(1-impact)
            cash = prev_cash + value_change - commission
            merge.at[i,'cash'] = cash
            
        else:
            value_change = 0 
            cash = prev_cash + value_change 
            merge.at[i,'cash'] = cash 
            
        prev_cash = cash 

        
        equity_val = 0
        
        for symbol in symbols:
             
            if row['Order'] == 'BUY':
                if i == 0:
                    prev_stock_dict[symbol + '_prev_stock'] = 0 
                    stock = row['Shares'] 
                    merge.at[i,symbol+'_stock'] = stock
                    prev_stock_dict[symbol + '_prev_stock'] = stock
                else:
                    
                    prev_stock = prev_stock_dict[symbol + '_prev_stock'] 
                    stock = row['Shares'] + prev_stock
                    merge.at[i,symbol+'_stock'] = stock 
                    prev_stock_dict[symbol + '_prev_stock'] = stock
                
            elif row['Order'] == 'SELL':
                if i ==0:
                    prev_stock_dict[symbol + '_prev_stock'] = 0 
                    stock = - row['Shares']
                    merge.at[i,symbol+'_stock'] = stock
                    prev_stock_dict[symbol + '_prev_stock'] = stock
                else:
                    prev_stock = prev_stock_dict[symbol + '_prev_stock'] 
                    stock = - row['Shares'] + prev_stock
                    merge.at[i,symbol+'_stock'] = stock 
                    prev_stock_dict[symbol + '_prev_stock'] = stock
            
            else:
                if i ==0:
                    prev_stock_dict[symbol + '_prev_stock'] = 0 
                    stock = - row['Shares']
                    merge.at[i,symbol+'_stock'] = stock
                    prev_stock_dict[symbol + '_prev_stock'] = stock
                else:
                    prev_stock = prev_stock_dict[symbol + '_prev_stock'] 
                    stock = prev_stock
                    merge.at[i,symbol+'_stock'] = stock 
                    prev_stock_dict[symbol + '_prev_stock'] = stock
            
                    
            
            #print("rows: ", row[symbol], merge.at[symbol+'_stock'] , row['equity_value'], row['cash'])
            equity_val += row[symbol] * merge.at[i, symbol+'_stock']              
        merge.at[i,'equity_value'] = equity_val 
        merge.at[i,'port_value'] = merge.at[i, 'equity_value'] + merge.at[i, 'cash']
        
    merge['benchmark_equity'] = merge['JPM']*1000
    merge['benchmark_cash'] = 100000 - merge['JPM'][0]*1000
    merge['benchmark'] = merge['JPM']*1000 + 100000 - merge['JPM'][0]*1000
    merge = merge.set_index('index')
    #normalized data and plot data and the benchmark 
   
    normalized_merge = merge[['benchmark','port_value']]
    normalized_merge[['benchmark','port_value']] = normalized_merge[['benchmark','port_value']]/normalized_merge.iloc[0,:]
    normalized_merge.plot(color=['m','r'])
    plt.grid() 
    plt.title('Compare tos and benchmark')
    plt.ylabel('Normalized tos & benchmark', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('tos_benchmark.png')
    
    start_date = merge.index[0]  		  	   		  	  		  		  		    	 		 		   		 		  
    end_date = merge.index[-1]
    cum_ret = merge['port_value'].values[-1]/merge['port_value'].values[0] -1 
    cum_ret_benchmark = merge['benchmark'].values[-1]/merge['benchmark'].values[0] -1 
    daily_returns = (merge['port_value'] / merge['port_value'].shift(1)) - 1
    daily_returns_benchmark = (merge['benchmark'] / merge['benchmark'].shift(1)) - 1
    avg_daily_ret = daily_returns.mean() 
    avg_daily_ret_benchmark = daily_returns_benchmark.mean()
    std_daily_ret = daily_returns.std()  
    std_daily_ret_benchmark = daily_returns_benchmark.std()
    #sr = avg_daily_ret/std_daily_ret*np.sqrt(252)	
    
    
    portvals = merge['port_value']	 		  
    portvals = portvals[~portvals.index.duplicated(keep='last')]
    #merge.to_csv('/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/indicator_evaluation/data.csv')
 		  	  		  		  		    	 		 		   		 		  
    return portvals  
    
    
    
    
    
    
   
    