""""""  		  	   		  	  		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
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
GT User ID: tb34 (replace with your User ID)  		  	   		  	  		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  	  		  		  		    	 		 		   		 		  
"""  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  	  		  		  		    	 		 		   		 		  
import os  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd  	
import math	  	   		  	  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
def author(): 
    
  return 'kdang49' # replace tb34 with your Georgia Tech username. 
		  	   		  	  		  		  		    	 		 		   		 		  
def compute_portvals(  		  	   		  	  		  		  		    	 		 		   		 		  
    orders_file,  		  	   		  	  		  		  		    	 		 		   		 		  
    start_val,  		  	   		  	  		  		  		    	 		 		   		 		  
    commission=0,  		  	   		  	  		  		  		    	 		 		   		 		  
    impact=0):  		
    #"./orders/orders.csv" / '/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/marketsim/orders/orders-01.csv' 	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		  	  		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  	
	  	   		  	  		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		  	  		  		  		    	 		 		   		 		  
    :type start_val: int  
		  	   		  	  		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  	  		  		  		    	 		 		   		 		  
    :type commission: float  
		  	   		  	  		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  	  		  		  		    	 		 		   		 		  
    :type impact: float  
		  	   		  	  		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  	  		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		  	  		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  	  		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		  	   		  	  		  		  		    	 		 		   		 		  
    # TODO: Your code here  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    # In the template, instead of computing the value of the portfolio, we just  		  	   		  	  		  		  		    	 		 		   		 		  
    # read in the value of IBM over 6 months  
    ''' 	   		  	  		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2011,1, 10)  		  	   		  	  		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2011, 12, 28)  		  	   		  	  		  		  		    	 		 		   		 		  
    portvals = get_data(["IBM"], pd.date_range(start_date, end_date))  		  	   		  	  		  		  		    	 		 		   		 		  
    portvals = portvals[["IBM"]]  # remove SPY  		  	   		  	  		  		  		    	 		 		   		 		  
    rv = pd.DataFrame(index=portvals.index, data=portvals.values)  	
 	''' 
    '''  		  	  		  		  		    	 		 		   		 		  
    orders_file = '/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/marketsim/orders/orders-12.csv'
    start_val = 1000000
    commission = 0
    impact = 0.005
    '''
    #my code starts from here 
    orders = pd.read_csv(orders_file, index_col = 'Date', parse_dates=True,na_values=['nan'])  
    orders = orders.sort_index(axis = 0)	
    start_date = orders.index[0]
    end_date = orders.index[-1]
    symbols = orders['Symbol'].unique().tolist()
    
    dfs = []
    for symbol in symbols:
        value = get_data([symbol], pd.date_range(start_date, end_date)) 
        value = value[[symbol]]
        dfs.append(value)
    dfs = pd.concat(dfs, join='outer', axis=1)
    merge = pd.merge(orders,dfs,how='outer',left_index=True,right_index=True)
    merge = merge.reset_index()
    '''
    count = 0 
    for symbol in symbols:
        value = get_data([symbol], pd.date_range(start_date, end_date)) 
        value = value[[symbol]] 
        if count == 0:
            merge_symbols = value
        else:
            merge_symbols = pd.merge(merge_symbols,value,how='outer',right_index=True,left_index=True)
        count+=1   
    merge = pd.merge(orders,merge_symbols,how='outer',left_index=True,right_index=True)
	'''
    
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
        
    merge['cash'] = 0.0 
    merge['equity_value'] = 0.0
    merge['port_value'] = 0.0
    merge['market_impact'] = 0.0
    
    #method 1 
    cash = start_val
    prev_cash = cash 
    prev_stock = 0 
    for i, row in merge.iterrows():
        symbol = row['Symbol']
        if symbol in symbols:
            if row['Order']=='BUY':
                merge.at[i,'prev_cash'] = prev_cash
                value_change = row[symbol]*row['Shares']*(1+impact)
                cash = prev_cash - value_change - commission
                merge.at[i,'cash'] = cash
                prev_cash = cash
                
            elif row['Order']=='SELL':
                merge.at[i,'prev_cash'] = prev_cash
                value_change = row[symbol]*row['Shares']*(1-impact)
                cash = prev_cash + value_change - commission
                merge.at[i,'cash'] = cash
                prev_cash = cash        
        else:
            merge.at[i,'prev_cash'] = prev_cash 
            merge.at[i,'cash'] = prev_cash 
        
        equity_val = 0 
        for symbol in symbols: 
            
            if row['Symbol'] == symbol:  
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
                    
                else:
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
                if i==0:
                    merge.at[i,symbol+'_stock'] = 0
                    prev_stock_dict[symbol + '_prev_stock'] = 0 
                else:
                    merge.at[i,symbol+'_stock']  = prev_stock_dict[symbol + '_prev_stock'] 
                    
            #print("rows: ", row[symbol], merge.at[symbol+'_stock'] , row['equity_value'], row['cash'])
            equity_val += row[symbol] * merge.at[i, symbol+'_stock']  
        merge.at[i,'equity_value'] = equity_val 
        merge.at[i,'port_value'] = merge.at[i, 'equity_value'] + merge.at[i, 'cash']
    
    merge = merge.set_index('index')
    portvals = merge['port_value']	 		  
    portvals = portvals[~portvals.index.duplicated(keep='last')]
    	   		  	  		  		  		    	 		 		   		 		  
    return portvals  

    # '''
    #         #method 2 
    # merge['value_change'] = 0.0  
    # for i in symbols:
    #     merge['value_change'] = merge.apply(lambda row: if row['Symbol']==i and row['Order']=='BUY' (-1)*row['Shares']*row[i]*(1+impact) else row['Shares']*row[i]*(1-impact))
    #     merge.where(merge['Symbol'] == i , merge['value_change'].apply((-1)*merge['Shares']*merge[i]*(1+impact) if merge['Order']=='BUY' else merge['Shares']*merge[i]*(1-impact) ))
    # '''
    # '''
    # method 1 prime
    # '''
    # cash = start_val
    # for i, row in merge.iterrows():
    #     symbol = row['Symbol']
    #     prev_cash = cash if i == 0 else merge.at[i-1, 'cash']
    #     if symbol in symbols:
    #         value_change = row[symbol] * row['Shares']* (1 + impact)
    #         if row['Order'] == 'BUY':
    #             row['cash'] = prev_cash - value_change - commission   
    #         else: 
    #             value_change = row[symbol] * row['Shares']* (1 - impact)
    #             row['cash'] = prev_cash + value_change - commission
    #         print("changed cash: ", row['cash'])
    #     else:
    #         row['cash'] = prev_cash
    #         print("unchanged cash: ", row['cash'])
    #     print("now cash: ", merge.at[i, 'cash'])
           

    #     equval = 0 
    #     #update stock 
    #     for symbol in symbols:
    #         prev_stock = 0 if i == 0 else merge.at[i-1, symbol+'_stock']
    #         if row['Symbol'] == symbol:
    #             if row['Order'] == 'BUY':
    #                 row[symbol+'_stock'] = row['Shares'] + prev_stock
    #             else:
    #                 row[symbol+'_stock'] = - row['Shares'] + prev_stock
    #         else:
    #             row[symbol+'_stock'] = prev_stock

    #         #calculate equity values
    #         equval += row[symbol] * row[symbol+'_stock']
            
    #     #update equity values and port values
    #     row['equity_value'] = equval
    #     row['port_value'] = row['equity_value'] + row['cash']
    #     print(row) if row["cash"] != 0 else None
    
    # '''####################################
    # '''
                
    # #calculate cash
    # cash = start_val
    # for i in range(total_rows):         
    #     symbol = merge['Symbol'][i]
    #     prev_cash = cash if i == 0 else merge['cash'][i-1]
    #     if symbol in symbols:
    #         value_change = merge[symbol][i] * merge['Shares'][i]* (1 + impact)        
    #         if merge['Order'][i] == 'BUY':
    #             merge['cash'][i] = prev_cash - value_change - commission     
    #         else: 
    #             value_change = merge[symbol][i] * merge['Shares'][i]* (1 - impact)
    #             merge['cash'][i] = prev_cash + value_change - commission
    #     else:
    #         merge['cash'][i] = prev_cash
           

    #     equval = 0 
    #     #update stock 
    #     for symbol in symbols:
    #         prev_stock = 0 if i == 0 else merge[symbol+'_stock'][i-1]
    #         if merge['Symbol'][i] == symbol:
    #             if merge['Order'][i] == 'BUY':
    #                 merge[symbol+'_stock'][i] = merge['Shares'][i] + prev_stock
    #             else:
    #                 merge[symbol+'_stock'][i] = - merge['Shares'][i] + prev_stock
    #         else:
    #             merge[symbol+'_stock'][i] = prev_stock

    #         #calculate equity values
    #         equval += merge[symbol][i] * merge[symbol+'_stock'][i]
            
    #     #update equity values and port values
    #     merge['equity_value'][i] = equval
    #     merge['port_value'][i] = merge['equity_value'][i] + merge['cash'][i]

         
            
    #merge.to_csv('/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/marketsim/merge.csv')	
    		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
def test_code():  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		  	   		  	  		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		  	   		  	  		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    of = '/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/marketsim/orders/orders-12.csv' #"./orders/orders2.csv"  		  	   		  	  		  		  		    	 		 		   		 		  
    sv = 1000000  		 
    commission=0	   		  	  		  		  		    	 		 		   		 		  
    impact=0.005 		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    # Process orders  		  	   		  	  		  		  		    	 		 		   		 		  
    portvals = compute_portvals(of, sv, commission, impact)  		  	   		  	  		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		  	   		  	  		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  	  		  		  		    	 		 		   		 		  
    else:  		  	   		  	  		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    # Get portfolio stats  		  	   		  	  		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		  	  		  		  		    	 		 		   		 		  
    start_date = portvals.index[0]  		  	   		  	  		  		  		    	 		 		   		 		  
    end_date = portvals.index[-1]
    portvals = portvals[~portvals.index.duplicated(keep='last')]
    cum_ret = portvals.values[-1]/portvals.values[0] -1 
    daily_returns = (portvals / portvals.shift(1)) - 1
    avg_daily_ret = daily_returns.mean()  
    std_daily_ret = daily_returns.std()  
    sr = avg_daily_ret/std_daily_ret*np.sqrt(252)	
    
    '''	    		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		  	  		  		  		    	 		 		   		 		  
        0.2,  		  	   		  	  		  		  		    	 		 		   		 		  
        0.01,  		  	   		  	  		  		  		    	 		 		   		 		  
        0.02,  		  	   		  	  		  		  		    	 		 		   		 		  
        1.5,  		  	   		  	  		  		  		    	 		 		   		 		  
    ]  		  	   		  	  		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		  	  		  		  		    	 		 		   		 		  
        0.2,  		  	   		  	  		  		  		    	 		 		   		 		  
        0.01,  		  	   		  	  		  		  		    	 		 		   		 		  
        0.02,  		  	   		  	  		  		  		    	 		 		   		 		  
        1.5,  		  	   		  	  		  		  		    	 		 		   		 		  
    ]  		  	   		  	  		  		  		    	 		 		   		 		  
  	'''
	  	   		  	  		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		  	   		  	  		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  	  		  		  		    	 		 		   		 		  
    print()  		  	   		  	  		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sr}")  		  	   		  	  		  		  		    	 		 		   		 		  
    #print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  	  		  		  		    	 		 		   		 		  
    print()  		  	   		  	  		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  	  		  		  		    	 		 		   		 		  
    #print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  	  		  		  		    	 		 		   		 		  
    print()  		  	   		  	  		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  	  		  		  		    	 		 		   		 		  
    #print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  	  		  		  		    	 		 		   		 		  
    print()  		  	   		  	  		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  	  		  		  		    	 		 		   		 		  
    #print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  	  		  		  		    	 		 		   		 		  
    print()  		  	   		  	  		 
    print(portvals) 		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  	  		  		  		    	 		 		   		 		  
    test_code()  		  	   		  	  		  		  		    	 		 		   		 		  
