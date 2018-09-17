"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as op
from util import get_data, plot_data

def get_sddr(allocs, norm):
    alloc = norm * allocs
    port_val = alloc.sum(axis=1)
    daily_return = port_val.copy()
    daily_return[1:] = (port_val[1:]/port_val[:-1].values)-1
    daily_return = daily_return[1:]
    sddr = daily_return.std()
    return sddr


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), \
    syms=['GOOG','AAPL','GLD','XOM', 'IBM'], gen_plot=True):
    
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    initial_allocs = [(1./len(syms))]*len(syms) # add code here to find the allocations
    #print initial_allocs
    normed = prices/prices.iloc[0]
    
    
    constraints = ({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })
    bounds = ((0.0,1.0),)*prices.shape[1]
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = op.minimize(get_sddr, initial_allocs, args=(normed,), method = "SLSQP", bounds=bounds, constraints=(constraints))
    optimal = allocs.x
    # Get daily portfolio value
     # add code here to compute daily portfolio values
     
    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values
    
    allocated = normed * optimal
    pos_vals = allocated * 1000000
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
    sr = (daily_return.mean()/daily_return.std())*np.sqrt(252)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        port_val = port_val/port_val[0]
        prices_SPY = prices_SPY/prices_SPY[0]
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot()
        plt.show()
        pass

    return optimal, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
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
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
