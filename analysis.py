"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

#def compute_daily_return(df):
    #daily_returns = df.copy()
    #daily_returns.iloc[1:] = (df.iloc[1:]/df.iloc[:-1].values)-1
    #daily_returns.iloc[0,:] = 0
    #return daily_returns

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values
    normed = prices/prices.iloc[0]
    allocated = normed * allocs
    pos_vals = allocated * sv
    port_val = pos_vals.sum(axis=1)
    port_val = port_val.apply(lambda x: x/port_val[0])
    
    daily_return = port_val.copy()
    daily_return[1:] = (port_val[1:]/port_val[:-1].values)-1
    daily_return = daily_return[1:]

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0,0,0,0] # add code here to compute stats
    cr = (port_val.iloc[-1]/port_val.iloc[0])-1
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = (daily_return.mean()/daily_return.std())*np.sqrt(sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        port_val = port_val/port_val[0]
        prices_SPY = prices_SPY/prices_SPY[0]
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot()
        plt.show()

    # Add code here to properly compute end value
    ev = sv

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
    
    

if __name__ == "__main__":
    test_code()

#Step 1
#Start with prices data frame
#Step 2
#Normalize data with the first rows
#norm=prices/prices[0]
#Step 3
#multiply norm byt allocations
#alloced = normed * alloc
#Step 5
#portval = alloced * start_val
