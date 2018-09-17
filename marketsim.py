"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    start_date = dt.datetime(2011,1,1)
    end_date = dt.datetime(2012,1,1)
    
    dates = pd.date_range(start_date, end_date)
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    min_date = orders.index.min()
    max_date = orders.index.max()
    symbols = orders["Symbol"]
    #x = len(symbols.index)
    syms = symbols.unique()
    prices = get_data(syms, pd.date_range(min_date, max_date), addSPY = False, colname='Adj Close')
    prices = prices.dropna()
    prices["Cash"] = pd.Series(1.0, index = prices.index)
    trades = prices.copy()
    trades[0:] = 0
    #print prices
    """for x in range(len(orders.index)):
        for date in dates:
            if (orders["Date"][x]) == date.date():
                print "dog"
                if orders["Order"][x] is "BUY":
                    trades[orders["Symbol"][x]] += orders["Shares"][x]
                else:
                    trades[orders["Symbol"][x]] -= orders["Shares"][x]"""
    for x in range(0,len(orders)):
        time = orders.iloc[x].name
        time = time.date()
        time = time.strftime('%Y%m%d')
        print time
        symb = orders.iloc[x]['Symbol']
        orderType = orders.iloc[x]['Order']
        shares = orders.iloc[x]['Shares']

        price = prices.loc[time][symb]
        
        if orderType == 'BUY':
         trades.at[time,symb] = shares
         temp = trades.loc[time]['Cash']
         trades.at[time,'Cash'] = temp + (price * -1.005 * shares) - 9.95
        else:
         trades.at[time,symb] = -.995*(shares)
         temp = trades.loc[time]['Cash'] 
         trades.at[time,'Cash'] = temp + (price * shares) - 9.95

    print trades
    holdings = trades.copy()
    holdings[0:] = 0
    holdings.iloc[0]['Cash'] = start_val
    cash_col = len(syms)
    
    for r in range(0,len(syms)):
        holdings.iat[0,r] = trades.iloc[0,r]
    holdings.iloc[0,cash_col] = holdings.iloc[0,cash_col] + trades.iloc[0,cash_col]
    
    
    for x in range(1,len(prices.index)):
        for y in range(0,len(syms)+1):
            holdings.iloc[x,y] = trades.iloc[x,y] + holdings.iloc[x-1,y]
            
    print holdings        
    values = prices.multiply(holdings)
    print values
    portvals = values.sum(axis=1)
    print portvals
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0,0,0,0]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0,0,0,0]
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    syms = ["SPY"]
    dates = pd.date_range(start_date, end_date)
    
    prices_SPY = get_data(syms, dates)  # only SPY, for comparison later
    normed = prices_SPY/prices_SPY.iloc[0]
    allocated = normed * 0.2
    pos_vals = allocated * sv
    port_val = pos_vals.sum(axis=1)
    port_val = port_val.apply(lambda x: x/port_val[0])
    
    daily_return = port_val.copy()
    daily_return[1:] = (port_val[1:]/port_val[:-1].values)-1
    daily_return = daily_return[1:]
    
    cum_ret_SPY = (port_val.iloc[-1]/port_val.iloc[0])-1
    avg_daily_ret_SPY = daily_return.mean()
    std_daily_ret_SPY = daily_return.std()
    sharpe_ratio_SPY = (daily_return.mean()/daily_return.std())*np.sqrt(252)
    
    
    
    cum_ret = (portvals.iloc[-1]/portvals.iloc[0])-1
    avg_daily_ret = portvals.mean()
    std_daily_ret = portvals.std()
    sharpe_ratio = (portvals.mean()/portvals.std())*np.sqrt(252)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
