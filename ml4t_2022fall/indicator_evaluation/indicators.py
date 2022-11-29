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

def main(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
    
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