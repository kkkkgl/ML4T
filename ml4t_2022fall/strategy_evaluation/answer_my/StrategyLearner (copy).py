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

  		  	   		  	  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import random  		  	   		  	  		  		  		    	 		 		   		 		  	  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  	  		  		  		    	 		 		   		 		  
import util as ut  		
from indicators import sma, momentum,bollinger_bands
from util import get_data, plot_data  
import QLearner as ql
import matplotlib.pyplot as plt 

class StrategyLearner(object):  
    
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  	  		  		  		    	 		 		   		 		    	   		  	  		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  	  		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  	  		  		  		    	 		 		   		 		  
        self.commission = commission 
        self.lookback = 10 
        self.symbol = 'JPM'
        self.learner = ql.QLearner(num_states = 125,
                                  num_actions = 3,
                                  alpha = 0.2,
                                  gamma = 0.9,
                                  rar = 0.9,
                                  radr = 0.99,
                                  dyna = 100)
    
    def compute_my_indicators(self,sd,ed,symbol):
        prices = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
        _sma, sma_ratio = sma(prices,self.lookback)
        bbands = bollinger_bands(prices,_sma,self.lookback)
        mtm = momentum(prices,self.lookback)
        spy = prices['SPY']
        
        indicators = (sma_ratio,bbands,mtm)
        return indicators 
    
    def discretizer_sma_ratio(self,indicators):
        """Discretizes the sma indicators"""
        '''
        Typical range for sma: -0.5 to 0.5
        Five conditions:
        1. x < -0.5
        2. -0.5 <= x <= 0.0
        3. 0.0 < x <= 0.5
        4. x > 0.5
        5. x == NaN
        '''
        discretized = indicators[0].copy()
        sma = indicators[0].copy()
        discretized = sma.copy()
        discretized.values[sma < -0.5] = 0
        discretized.values[(sma >= -0.5) & (sma <= 0.0)] = 1
        discretized.values[(sma > 0.0) & (sma <= 0.5)] = 2
        discretized.values[sma > 0.5] = 3
        discretized.values[sma.isnull()] = 4
        '''total conditions'''
        n = 4 

        return discretized.astype('int32'), n
    
    def discretizer_bollinger_bands(self, indicators):
        """Discretizes the Bollinger Bands indicators"""
        '''
        Typical range: -1.0 to 1.0
        Five conditions:
        1. x < -1.0
        2. -1.- <= x <= 0.0
        3. 0.0 < x <= 1.0
        4. x > 1.0
        5. x == NaN
        '''
        discretized = indicators[1].copy()
        bbands = indicators[1].copy()
        discretized.values[bbands < -1.0] = 0
        discretized.values[(bbands >= -1.0) & (bbands <= 0.0)] = 1
        discretized.values[(bbands > 0.0) & (bbands <= 1.0)] = 2
        discretized.values[bbands > 1.0] = 3
        discretized.values[bbands.isnull()] = 4
        '''total conditions'''
        n = 4 

        return discretized.astype('int32'),n

    
    def discretizer_momentum(self, indicators):
        """Discretizes the Momentum indicator"""
        '''
        Typical range for momentum: -0.5 to 0.5
        Five conditions:
        1. x < -0.5
        2. -0.5 <= x <= 0.0
        3. 0.0 < x <= 0.5
        4. x > 0.5
        5. x == NaN
        '''
        discretized = indicators[2].copy()
        mtm = indicators[2].copy()
        discretized = mtm.copy()
        discretized.values[mtm < -0.5] = 0
        discretized.values[(mtm >= -0.5) & (mtm <= 0.0)] = 1
        discretized.values[(mtm > 0.0) & (mtm <= 0.5)] = 2
        discretized.values[mtm > 0.5] = 3
        discretized.values[mtm.isnull()] = 4
        '''total conditions''' 
        n = 4
        
        return discretized.astype('int32'),n 
    
    
    def trading_states(self,indicators):
        '''discretize my indicators'''
        discretized_sma, sma_ratio_n = self.discretizer_sma_ratio(indicators)
        discretized_bb, bbands_n = self.discretizer_bollinger_bands(indicators)
        discretized_mtm, mtm_n = self.discretizer_momentum(indicators)
        
        discretized_sma = discretized_sma.rename(columns={self.symbol:'sma_ratio'})
        discretized_bb = discretized_bb.rename(columns={self.symbol:'bbands'})
        discretized_mtm = discretized_mtm.rename(columns={self.symbol:'mtm'})
        df = [discretized_sma,discretized_bb,discretized_mtm]
        df = pd.concat(df,axis = 1)
        
        discretized_sma = df[['sma_ratio']]
        discretized_bb = df[['bbands']]
        discretized_mtm = df[['mtm']]
        discretized_data = df[['sma_ratio','bbands','mtm']]
        
        for i in range(discretized_data.shape[0]):
            discretized_data['state'] = discretized_data['sma_ratio']*(5**2) + discretized_data['bbands']*(5**1) + discretized_data['mtm']
            
        ''' in total there are 125 trading states'''
        all_conditions = [sma_ratio_n, bbands_n, mtm_n]
        return discretized_sma,discretized_bb,discretized_mtm,discretized_data
    
    
    def compute_current_state(self,indicators,i):
        discretized_sma,discretized_bb,discretized_mtm,discretized_data = self.trading_states(indicators)
        state_number = discretized_data['state'][i]
        return state_number
        
    
    #create a Qlearner and train it for trading 
    def add_evidence(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		  	  		  		  		    	 		 		   		 		  
    ):
        
        '''	  
        symbol="JPM"	  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1) 		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 12, 31)	  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000
        
        '''
        indicators = self.compute_my_indicators(sd,ed,symbol)
        discretized_sma,discretized_bb,discretized_mtm,discretized_data = self.trading_states(indicators)
        
        '''set my adj close data and an empty trade dataframe'''
        data = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
        prices = data[[symbol]].ffill().bfill()
        spy = data[['SPY']]
        data_trades = spy.rename(columns={'SPY':symbol}).astype({symbol:'int32'})
        data_trades[:] = 0
        data_trades['cash'] = 0
        data_trades['equity'] = 0
        data_trades['total_val'] = 0 
        dates = data.index
        
        '''train Q learner'''
        position=0; prev_position = 0 
        cash =sv ; prev_cash = sv  
        
        for i in range(1, len(dates)):
            yesterday = dates[i-1]
            today = dates[i]
            
            s_prime = self.compute_current_state(indicators,i)
            r = (position * prices.loc[today].loc[symbol] + cash ) - (prev_position * prices.loc[yesterday].loc[symbol] + prev_cash) 
            
            ''' 
            Three actions in total:
            0: short 
            1: cash/hold 
            2: long 
            '''
            next_action = self.learner.query(s_prime,r)
            if next_action == 0:
                trade = -1000 -position 
            elif next_action == 1:
                trade = -position 
            else:
                trade = 1000 - position 
            
            prev_position = position 
            position += trade 
            data_trades.loc[today].loc[symbol] = trade 
            if trade > 0 :
                 impact = self.impact 
            else:
                impact = -self.impact    
            prev_cash = cash 
            cash += -prices.loc[today].loc[symbol]*(1+impact)*trade 
            data_trades.at[today,'cash'] = cash 
            data_trades.at[today,'equity'] = position * prices.loc[today].loc[symbol]
            data_trades.at[today,'total_val'] = data_trades.loc[today].loc['cash'] + data_trades.loc[today].loc['equity']
            
            
            
    #use the existing policy and test it against new data  		  	   		  	  		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		  	  		  		  		    	 		 		   		 		  
    ):  
        indicators = self.compute_my_indicators(sd,ed,symbol)
        discretized_sma,discretized_bb,discretized_mtm,discretized_data = self.trading_states(indicators)
        
        '''set my adj close data and an empty trade dataframe'''
        data = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
        prices = data[[symbol]].ffill().bfill()
        spy = data[['SPY']]
        data_trades = spy.rename(columns={'SPY':symbol}).astype({symbol:'int32'})
        data_trades[:] = 0
        data_trades['cash'] = 0
        data_trades['equity'] = 0
        data_trades['total_val'] = 0 
        dates = data.index
        
        position = 0 
        cash = sv
        
        for i in range(1,len(dates)):
            yesterday = dates[i-1]
            today = dates[i]
            s_prime = self.compute_current_state(indicators,i)
            next_action = self.learner.querysetstate(s_prime)
            if next_action == 0:
                trade = -1000 -position 
            elif next_action == 1:
                trade = -position 
            else:
                trade = 1000 - position 
                
            position += trade 
            data_trades.at[today,symbol] = trade
            if trade > 0 :
                impact = self.impact 
            else:
                impact = -self.impact 
                
            cash += -prices.loc[today].loc[symbol]*(1+impact)*trade 
            data_trades.at[today,'cash'] = cash 
            data_trades.at[today,'equity'] = position * prices.loc[today].loc[symbol]
            data_trades.at[today,'total_val'] = data_trades.loc[today].loc['cash'] + data_trades.loc[today].loc['equity']
            
        return data_trades
    
if __name__ == '__main__'  :
    self = StrategyLearner() 
    
    #Train Q learner 
    self.add_evidence(
        symbol="JPM",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000) 
    
    #Backtest with new data using trained Q Learner
    data_trades, prices = self.testPolicy(		  	   		  	  		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000)
    
    #Plot the result 
    port_value = data_trades['total_val']
    port_value.plot() 
    plt.grid() 
    plt.title('Test Result')
    plt.ylabel('portfolio value', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    
    
    
