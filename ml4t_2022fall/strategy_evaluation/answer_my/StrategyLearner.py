 		  	   		  	  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		   		  	   		  	  		  		  		    	 		 		   		 		  	  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  	  		  		  		    	 		 		   		 		  
import util as ut  		
from indicators import sma, momentum,bollinger_bands
from util import get_data, plot_data  
import QLearner as ql
import matplotlib.pyplot as plt 
import random 

class StrategyLearner(object):  
    
    def __init__(self,verbose=False, impact=0.005, commission=9.95):  		  	   		  	  		  		  		    	 		 		   		 		    	   		  	  		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  	  		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  	  		  		  		    	 		 		   		 		  
        self.commission = commission 
        self.lookback = 10 
        self.learner = ql.QLearner(num_states = 125,
                                  num_actions = 3,
                                  alpha = 0.2,
                                  gamma = 0.9,
                                  rar = 0.9,
                                  radr = 0.99,
                                  dyna = 100)
        
    def author(self,):
        return'kdang49'
    
    '''
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    
    '''
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
    
    
    def trading_states(self,symbol,indicators):
        '''discretize my indicators'''
        discretized_sma, sma_ratio_n = self.discretizer_sma_ratio(indicators)
        discretized_bb, bbands_n = self.discretizer_bollinger_bands(indicators)
        discretized_mtm, mtm_n = self.discretizer_momentum(indicators)
        
        discretized_sma = discretized_sma.rename(columns={symbol:'sma_ratio'})
        discretized_bb = discretized_bb.rename(columns={symbol:'bbands'})
        discretized_mtm = discretized_mtm.rename(columns={symbol:'mtm'})
        #df = [discretized_sma,discretized_bb,discretized_mtm]
        #df = pd.concat(df,axis = 1)
        
        discretized_sma = discretized_sma[['sma_ratio']]
        discretized_bb = discretized_bb[['bbands']]
        discretized_mtm = discretized_mtm[['mtm']]
        #discretized_data = df[['sma_ratio','bbands','mtm']]
        state = [] 
        for i in range(discretized_sma.shape[0]):
            state_i = discretized_sma.iloc[i][0]*(25) + discretized_bb.iloc[i][0]*(5) + discretized_mtm.iloc[i][0]
            state.append(state_i)
        ''' in total there are 125 trading states'''
        return state
    
    '''
    def compute_current_state(self,symbol,indicators,):
        discretized_sma,discretized_bb,discretized_mtm,discretized_data = self.trading_states(symbol,indicators)
        state = discretized_data['state']
        return state
    '''  
    
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
        
        '''set my adj close data and an empty trade dataframe'''
        data = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
        prices = data[[symbol]].ffill().bfill()
        spy = data[['SPY']]
        data_trades = spy.rename(columns={'SPY':symbol}).astype({symbol:'int32'})
        data_trades[:] = 0
        #data_trades['cash'] = 0
        #data_trades['equity'] = 0
        #data_trades['total_val'] = 0 
        dates = data.index
        
        '''train Q learner'''
        position=0; prev_position = 0 
        cash =sv ; prev_cash = sv  
        state = self.trading_states(symbol,indicators)
        
        for i in range(1, len(dates)):#len(dates)
            
            yesterday = dates[i-1]
            today = dates[i]
            
            s_prime = state[i]
            r = (position * prices.at[today,symbol] + cash ) - (prev_position * prices.at[yesterday,symbol] + prev_cash) 
            
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
            data_trades.at[today,symbol] = trade 
            impact = self.impact if trade > 0 else -self.impact
            prev_cash = cash 
            cash += -prices.at[today,symbol]*(1+impact)*trade 
            #data_trades.at[today,'cash'] = cash 
            #data_trades.at[today,'equity'] = position * prices.loc[today].loc[symbol]
            #data_trades.at[today,'total_val'] = data_trades.loc[today].loc['cash'] + data_trades.loc[today].loc['equity']
            
            
            
    #use the existing policy and test it against new data  		  	   		  	  		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        symbol="UNH",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		  	  		  		  		    	 		 		   		 		  
    ):  
        indicators = self.compute_my_indicators(sd,ed,symbol)
        
        '''set my adj close data and an empty trade dataframe'''
        data = get_data([symbol],pd.date_range(sd,ed),'Adj Close')
        prices = data[[symbol]].ffill().bfill()
        spy = data[['SPY']]
        data_trades = spy.rename(columns={'SPY':symbol}).astype({symbol:'int32'})
        data_trades[:] = 0
        #data_trades['cash'] = 0
        #data_trades['equity'] = 0
        #data_trades['total_val'] = 0 
        dates = data.index
        state = self.trading_states(symbol,indicators)
        position = 0 
        cash = sv
        
        for i in range(1,len(dates)):
            yesterday = dates[i-1]
            today = dates[i]
            s_prime = state[i]
            next_action = self.learner.querysetstate(s_prime)
            if next_action == 0:
                trade = -1000 -position 
            elif next_action == 1:
                trade = -position 
            else:
                trade = 1000 - position 
                
            position += trade 
            data_trades.at[today,symbol] = trade
            #impact = self.impact if trade > 0 else -self.impact
            #cash += -prices.loc[today].loc[symbol]*(1+impact)*trade 
            #data_trades.at[today,'cash'] = cash 
            #data_trades.at[today,'equity'] = position * prices.loc[today].loc[symbol]
            #data_trades.at[today,'total_val'] = data_trades.loc[today].loc['cash'] + data_trades.loc[today].loc['equity']
            
        return data_trades
    
if __name__ == '__main__'  :
    self = StrategyLearner() 
    
    #Train Q learner 
    self.add_evidence(
        symbol="UNH",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000) 
    
    #Backtest with new data using trained Q Learner
    data_trades = self.testPolicy(		  	   		  	  		  		  		    	 		 		   		 		  
        symbol="UNH",  		  	   		  	  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		  	  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		  	  		  		  		    	 		 		   		 		  
        sv=10000)
    
    #Plot the result 
    '''
    port_value = data_trades['total_val']
    port_value.plot() 
    plt.grid() 
    plt.title('Test Result')
    plt.ylabel('portfolio value', fontsize=10)
    plt.xlabel('dates', fontsize=10)
    '''
    
    
    
