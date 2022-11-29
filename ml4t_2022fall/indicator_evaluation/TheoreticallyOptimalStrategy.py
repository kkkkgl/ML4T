#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:22:04 2022

@author: connie
"""
import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import os  	
import pandas as pd 	  	   		  	  		  		  		    	 		 		   		 		  
pd.set_option('display.max_columns', None)		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		    		  	   		  	  		  		  		    	 		 		   		 		   	
import math	  	   		  	  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  	

def author(): 
  return 'kdang49' 

def testPolicy(symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009,12,31), sv = 100000) :    
    data = get_data([symbol],  pd.date_range(sd, ed)) 
    data['next_JPM'] = data['JPM'].shift(-1) 
    data['position'] = 0 
    position = 0 
    for index,row in data.iterrows():
        if row['next_JPM'] > row['JPM']: 
            if position == 1000:             
                data.at[index,'signal'] = 'hold'  
                data.at[index,'Trade'] = 0                
            elif position == -1000:
                data.at[index,'signal'] = 'buy'
                data.at[index,'Trade'] = 2000
                position += 2000                
            else:
                data.at[index,'signal'] = 'buy'
                data.at[index,'Trade'] = 1000
                position += 1000
        elif row['next_JPM'] < row['JPM']:
            if position == -1000:
                data.at[index,'signal'] = 'hold'     
                data.at[index,'Trade'] = 0 
            elif position == 1000:
                data.at[index,'signal'] = 'sell'
                data.at[index,'Trade'] = -2000
                position -= 2000                
            else:
                data.at[index,'signal'] = 'sell'
                data.at[index,'Trade'] = -1000
                position-=1000
        else:
            data.at[index,'signal'] = 'hold'
            data.at[index,'Trade'] = 0
        data.at[index,'position'] = position
    
    trades = pd.DataFrame(data['Trade'])
    return trades
    #data.to_csv('/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/indicator_evaluation/data.csv')
