import pandas as pd

from util import get_data, plot_data

def compute_portvals(orders_file, start_val = 100000, commission=9.95, impact=0.005):
    """Returns a single column df with porfolio values from the beginning to the end of the order file. 
       This marketsim function has been modified to only accept a single column df with buy/sell stated as pos/neg, and the symbol has the feature"""
        
    dates = orders_file.index
    symbol = orders_file.columns[0]
    
    # prices data is the Adj close price per trading day
    prices_data = get_data([symbol], pd.date_range(dates[0],dates[-1]))
     # SPY is kept to distinguish trading days, removed if not in the portfolio, get_data adds it automatically
    if symbol != 'SPY':
        prices_data = prices_data.drop('SPY', axis=1)
        
    # df_prices is price data with the cash feature
    df_prices = pd.DataFrame(prices_data)
    df_prices['cash'] = 1
    
    # df_trades represents number of shares held and cash avalable only on order dates
    df_trades = orders_file.copy()
    
    # df_holdings represents df_trades, but on days inbetween traded days
    df_holdings = df_trades.copy()    
        
    for i in orders_file.index:
        if orders_file.at[i,symbol] != 0: # prevents transaction costs on non-trading days
            total_cost = orders_file.loc[i, symbol] * df_prices.loc[i, symbol] # to clean up the code
            df_trades.loc[i, 'cash'] = -total_cost - abs(commission + total_cost * impact) 
    df_trades.fillna(0, inplace=True)
    
    df_holdings.loc[dates[0],'cash'] = start_val + df_trades.loc[dates[0],'cash']
    df_holdings.iloc[0, :-1] = df_trades.iloc[0, :-1]
    
    for i in range(1, df_holdings.shape[0]):
        df_holdings.iloc[i, :] = df_trades.iloc[i, :] + df_holdings.iloc[i-1, :]
        
#    # df_value is the dollar value of the shares at each date
    df_value = df_holdings.multiply(df_prices)
    
    df_portval = df_value.sum(axis=1)
    return(df_portval)
    
def author():
    return('kdang49')