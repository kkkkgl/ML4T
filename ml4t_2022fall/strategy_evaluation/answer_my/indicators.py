#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:23:42 2022

@author: connie
"""

'''
SMA
BB
Momentum 
Stochastic Indicator
CCI 
'''


import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import os  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  	
import math	  	   		  	  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def author():     
  return 'kdang49' 

def _get_data(symbol,dates,column):
    data = get_data(symbol,dates,colname = column)
    data.fillna(method='ffill',inplace = True)
    data.fillna(method='bfill',inplace = True)
    return data 

def sma(prices,lookback):
    sma = prices.rolling(window=lookback,center=False).mean()
    ratio = prices/sma-1 
    std_ratio = (ratio - ratio.mean())/ratio.std()
    return sma,std_ratio
    
def momentum(prices, lookback):
    indicator = prices/prices.shift(lookback)-1 
    std_indicator = (indicator - indicator.mean())/indicator.std()
    return std_indicator

def bollinger_bands(prices, _sma,lookback):
    std =prices.rolling(window=lookback,min_periods=lookback).std()
    _indicator = (prices-_sma)/(2*std)
    _std_indicator = (_indicator - _indicator.mean())/_indicator.std()
    return _std_indicator

def save_my_indicators(indicators,names):
    for index,indicator in enumerate(indicators):
        indicator.to_csv("{}.csv".format(names[index]))
    
def main(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
    
    lookback = 10 
    dates = pd.date_range(sd,ed)
    prices = _get_data([symbol],dates,'Adj Close')
    highs = _get_data([symbol],dates,'High')
    lows = _get_data([symbol],dates,'Low')
    volumes = _get_data([symbol],dates,'Volume')
    
    dates = prices.index 
    
    #create and save my indicators
    _sma,ratio = sma(prices,lookback)
    _momentum = momentum(prices,lookback)
    _bbands = bollinger_bands(prices,_sma,lookback)
    save_my_indicators((ratio,_momentum,_bbands),['sma','momentum','bollingerbands'])
    
    
    value = get_data([symbol], pd.date_range(sd, ed)) 
    JPM = pd.DataFrame(value['JPM'])
    
    #simple moving average 
    lookback_period = 20
    JPM_normalized = (JPM-JPM.mean())/JPM.std()
    JPM_normalized['SMA'] = JPM_normalized['JPM'].rolling(window=lookback_period, center=False).mean() #min_periods=1
    
    JPM_normalized.plot()
    plt.grid()
    plt.title('SMA Indicator', fontsize=10)
    plt.ylabel('normalized price & sma indicator', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('sma_indicator')
    

    #Bolliger Bond 
    bb = pd.DataFrame(value['JPM'])    
    bb['JPM'] = (bb['JPM']-bb['JPM'].mean())/bb['JPM'].std()
    bb['rolling_std'] = bb['JPM'].rolling(lookback_period).std()
    bb['rolling_mean'] = bb['JPM'].rolling(lookback_period).mean() 
    bb['UPPER'] = bb['rolling_mean'] + 2*bb['rolling_std']
    bb['LOWER'] = bb['rolling_mean'] - 2*bb['rolling_std']
    bb = bb[['UPPER','LOWER','JPM','rolling_mean']]
    bb.plot()
    plt.grid() 
    plt.title('Bollinger Bond Indicator')
    plt.ylabel('normalized price & bollinger bond indicator', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('bollinger_bond_indicator')
    
    
    #Momentum 
    mom = pd.DataFrame(value['JPM'])
    mom['shift'] = mom['JPM'].shift(lookback_period)
    mom['momentum'] = mom['JPM']/mom['shift'] - 1
    mom_normalized = mom[['JPM','momentum']]
    mom_normalized = (mom_normalized - mom_normalized.mean())/mom_normalized.std()
    mom_normalized.plot()
    plt.grid() 
    plt.title('Momentum Indicator')
    plt.ylabel('Normalized price & Momentum indicator', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('Momentum_indicator')
    
    
    #Commodity channel index 
    cci = pd.DataFrame(value['JPM']) 
    cci['rolling_mean'] = cci['JPM'].rolling(lookback_period).mean() 
    cci['mean_deviation'] = abs(cci['JPM']-cci['rolling_mean']).rolling(lookback_period).mean()
    cci['cci'] = (cci['JPM'] - cci['rolling_mean'])/cci['mean_deviation']*100
    cci['JPM'] = (cci['JPM']-cci['JPM'].mean())/cci['JPM'].std()
    cci_new = cci[['cci']]
    cci_new.plot()
    plt.grid() 
    plt.title('Commodity channel index Indicator')
    plt.ylabel('Normalized price & CCI indicator', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('cci_indicator')
    
    #Stochastic Oscillator 
    stos = pd.DataFrame(value['JPM']) 
    stos['rolling_min'] = stos['JPM'].rolling(14).min() 
    stos['rolling_max'] = stos['JPM'].rolling(14).max()
    stos['stos'] = (stos['JPM'] - stos['rolling_min'])/(stos['rolling_max']-stos['rolling_min'])*100
    stos['JPM'] = (stos['JPM']-stos['JPM'].mean())/stos['JPM'].std()
    stos_new = stos[['JPM','stos']]
    stos_new.plot()
    plt.grid() 
    plt.title('Stochastic Oscillator index Indicator')
    plt.ylabel('Normalized price & Stochastic Oscillator indicator', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    plt.savefig('Stochastic_Oscillator_indicator')


    
    
if __name__ == '__main__':
    
    run = main()