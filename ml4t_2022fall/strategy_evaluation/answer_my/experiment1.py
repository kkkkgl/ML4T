""""""  		  	   		  	  		  		  		    	 		 		   		 		  
"""  		  	   		  	  		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  	  		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  	  		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  	  		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  	  		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  		  		  		    	 		 		   		 		  
or edited.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  	  		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  	  		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  	  		  		  		    	 		 		   		 		  
GT User ID: kdang49		  	   		  	  		  		  		    	 		 		   		 		  
GT ID: 903825229 		  	   		  	  		  		  		    	 		 		   		 		  
"""  		

from ManualStrategy import ManualStrategy
import datetime as dt 
from marketsimcode import compute_portvals
from StrategyLearner import StrategyLearner
import matplotlib.pyplot as plt
from util import get_data
import pandas as pd 

def author():
    return'kdang49'

def ManualResult(symbol,sd,ed,sv,commission,impact):
    
    '''
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    
    '''
    ms = ManualStrategy() 
    trade = ms.testPolicy(symbol,sd,ed,sv)
    portvals = compute_portvals(trade,sv,commission,impact)
    
    return portvals 

def Learner(sd, ed, sv, symbol = 'JPM',verbose=False, impact=0.005, commission=9.95, insample=False):
    
    '''
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    '''
    
    sl = StrategyLearner(verbose=verbose, impact=impact, commission = commission)
    if insample == True:
        sl.add_evidence(symbol, sd, ed, sv)
        trade = sl.testPolicy(symbol, sd, ed, sv)
    else:
        trade = sl.testPolicy(symbol, sd, ed, sv)
    portvals = compute_portvals(trade,sv,commission, impact) 
    
    return portvals 

def insample_compare(symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000,commision=0,impact=0,verbose=False):
    
    benchmark = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
    benchmark = benchmark[[symbol]]*1000
    
    manual = ManualResult(symbol,sd,ed,sv,commission=0,impact=0) 
    learner = Learner(sd,ed,sv,symbol = 'JPM', verbose=False, impact=0.0, commission=0.0, insample=True)
    
    normalized_manual = manual/manual.iloc[0]
    normalized_learner = learner/learner.iloc[0]
    normalized_benchmark = benchmark/benchmark.iloc[0]
    
    plt.figure(figsize = (12,8))
    plt.plot(normalized_manual,label='Manual',color='green')
    plt.plot(normalized_learner,label='QLearner', color = 'red')
    plt.plot(normalized_benchmark, label ='Benchmark', color ='blue')
    plt.grid()
    plt.title('In sample Comparision')
    plt.xlabel('date')
    plt.ylabel('cumulative return')
    plt.legend() 
    plt.savefig('experiment1-insample.png')
    
def outofsample_compare(symbol='JPM',sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000,commision=0.005,impact=9.95,verbose=False):
    
    benchmark = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
    benchmark = benchmark[[symbol]]*1000
    
    manual = ManualResult(symbol,sd,ed,sv,commission=0,impact=0) 
    learner = Learner(sd,ed,sv,symbol = 'JPM', verbose=False, impact=0.0, commission=0.0, insample=False)
    
    normalized_manual = manual/manual.iloc[0]
    normalized_learner = learner/learner.iloc[0]
    normalized_benchmark = benchmark/benchmark.iloc[0]
    
    plt.figure(figsize = (12,8))
    plt.plot(normalized_manual,label='Manual',color='green')
    plt.plot(normalized_learner,label='QLearner', color = 'red')
    plt.plot(normalized_benchmark, label ='Benchmark', color ='blue')
    plt.grid()
    plt.title('Out of sample Comparision')
    plt.xlabel('date')
    plt.ylabel('cumulative return')
    plt.legend() 
    plt.savefig('experiment1-outsample.png')

if __name__ == '__main__':
    insample_compare() 
    outofsample_compare() 