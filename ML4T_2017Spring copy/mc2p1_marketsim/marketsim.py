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
        symb = orders.iloc[x]['Symbol']
        orderType = orders.iloc[x]['Order']
        shares = orders.iloc[x]['Shares']

        price = prices.loc[time][symb]

        if orderType == 'BUY':
    		trades.at[time,symb] = shares
    		trades.at[time,'Cash'] = (price * -1 * shares)
        else:
    		trades.at[time,symb] = -1.0*(shares)
    		trades.at[time,'Cash'] = price * shares

    #print trades
    holdings = trades.copy()
    holdings[0:] = 0
    holdings.iloc[0]['Cash'] = start_val
    
    for x in len(prices.index):
        for y in len(syms):
            holdings[x][y]
        
    print holdings[9][8]
    portvals = prices
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

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
