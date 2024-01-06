# This file contains all the functions to return sampled values from continuously random distrubtions modeling uncertain parameters.
# Distributions were taken from Prof. Kazantzis' literature.

import numpy as np
from scipy.stats import uniform, pareto, weibull_min


def PSS_Support_Price_FN():
    return np.random.triangular(10.2, 11.3, 12.4, 1)

def Membrane_Lifetime_FN():
    return np.random.triangular(1, 3, 5, 1)

def H2_Selling_Price_FN():
    return np.random.triangular(9, 10, 11, 1)

def Nominal_Discount_Rate_FN():
    return np.random.triangular(0.114, 0.16, 0.176, 1)

def CO2_Transport_FN():
    return np.random.triangular(9, 10, 11, 1)

def CO2_Tax_FN():
    return np.random.triangular(27, 30, 33, 1)

def CO2_Tax_Growth_FN():
    return np.random.triangular(0.054, 0.06, 0.066, 1)

def Combined_Taxes_FN():
    return np.random.triangular(0.0, 0.064, 0.095, 1)

# Market Value
def MV_Plant_FN():
    return np.random.triangular(0.135, 0.150, 0.165, 1)

def Installation_FN():
    return uniform.rvs(size = 1, loc = 0.25 , scale = 0.55 - 0.25)

# Instrumentation & COntrols
def IC_FN():
    return uniform.rvs(size = 1, loc = 0.08 , scale = 0.50 - 0.08)

def Piping_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.8 - 0.1)

def Electrical_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.4 - 0.1)

# Auxiliary Facilities
def AUX_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.7 - 0.1)

def Facilities_FN():
    return uniform.rvs(size = 1, loc = 0.4 , scale = 1 - 0.4)

def Land_FN():
    return uniform.rvs(size = 1, loc = 0.04 , scale = 0.08 - 0.04)

def Supervision_FN():
    return uniform.rvs(size = 1, loc = 0.05 , scale = 0.3 - 0.05)

def Legal_FN():
    return uniform.rvs(size = 1, loc = 0.01 , scale = 0.03 - 0.01)

def Construction_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.2 - 0.1)

def Contingency_FN():
    return uniform.rvs(size = 1, loc = 0.05 , scale = 0.15 - 0.05)

def Insurance_FN():
    return uniform.rvs(size = 1, loc = 0.004 , scale = 0.01 - 0.004)

# Working Capital
def WC_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.2 - 0.1)

def Financing_Interest_FN():
    return uniform.rvs(size = 1, loc = 0.06 , scale = 0.1 - 0.06)

def Overhead_FN():
    return uniform.rvs(size = 1, loc = 0.05 , scale = 0.15 - 0.05)

def Patents_Loyalties_FN():
    return uniform.rvs(size = 1, loc = 0.0 , scale = 0.06 - 0)

def Admin_Costs_FN():
    return uniform.rvs(size = 1, loc = 0.02 , scale = 0.05 - 0.02)

def Marketing_FN():
    return uniform.rvs(size = 1, loc = 0.02 , scale = 0.06 - 0.02)

def Capacity_Factor_FN():
    return np.random.triangular(0.75, 0.8, 0.85, 1)

def De_Rating_Factor_FN():
    return uniform.rvs(size = 1, loc = 0.05 , scale = 0.05)


# Creates cumulative distribution from the lists of NPVs which result from the simulations and returns x&y data values for graphing purposes.
def createCumDist_FN(NPVList, numOfSubranges):
    totalRange = max(NPVList) - min(NPVList)
    numRanges = numOfSubranges
    rangeSize = totalRange / numRanges

    x_values = []
    y_values = []

    lowerBound = min(NPVList)
    upperBound = lowerBound + rangeSize

    globalCount = 0

    # Determines # of entries in each "Bin" created
    for i in range(1, numRanges + 1):
        count = 0
        x_values.append((upperBound + lowerBound) / 2)
        for j in range(0, len(NPVList)):
            if (NPVList[j] < upperBound):
                count += 1
                globalCount += 1
        y_values.append(count/10000)

        lowerBound = upperBound
        upperBound = lowerBound + rangeSize

    return x_values, y_values