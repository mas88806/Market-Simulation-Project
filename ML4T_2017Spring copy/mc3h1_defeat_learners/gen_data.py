"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regresstion than random trees
def best4LinReg():
    X = np.random.normal(size = (100, 4)) 
    Y = np.sin(X[:,1])*np.cos(1./(0.0001+X[:,0]**2)) 
    return X, Y

def best4RT():
    X = np.random.normal(size = (50, 2)) 
    Y = 0.8 * X[:,0] + 5.0 * X[:,1] 
    return X, Y

if __name__=="__main__":
    print "they call me Tim."
