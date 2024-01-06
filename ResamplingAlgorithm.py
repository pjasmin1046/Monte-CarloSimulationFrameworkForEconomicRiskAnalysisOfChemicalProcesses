# The following was developed to replicate distribution fitting abilities from @Risk in a Pythonic environment. It is
# primarily for the purposes of fitting distributions to historical price data and creating continuously random variables
# from which prices are sampled throughout a Monte-Carlo simulation. This algorithm attempts fitting of Normal, Pareto, Weibull,
# Gamma, Uniform, and Triangular distributions to input data and returns fit parameters, least squares residual, and
# graphical output of the fitting process. Options are built in to autoselect the best fitting distribution, or prompt
# the user to manually select the desired distribution. Functionality for sampling multiple values from the resulting
# continuously random variables at once is available to simulate an extended plant lifetime without recurring function calls.


import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import math
import plotly.graph_objs as go
from scipy.stats import gamma
import random

# Stores fitting results for all 6 distributions such that residuals and fit parameters can be compared manually
# if necessary
allFitParameters = {}


# DATA MODIFICATION FUNCTIONS:
# Returns the indeces in which the mode of the dataset occurs for triangular distribution fit options.
def getModes(inputData):
    modeIndeces = []
    theBigGuy = max(inputData)
    for i in range(len(inputData)):
        if inputData[i] == theBigGuy:
            modeIndeces.append(i)
    return modeIndeces

# Returns the x coordinates of bin centers for the purposes of graphing a histogram of input data.
def binstoxdata(bins):
    xdata = []
    for i in range(len(bins) - 1):
        xdata.append((bins[i] + bins[i + 1]) / 2)
    return xdata

# Returns list of input data scaled to start at 1. This makes fitting Pareto distributions easier
def ScaleData(inputYData):
    sum = np.sum(inputYData)
    resList = []
    for i in range(0, len(inputYData)):
        resList.append(inputYData[i]/sum)
    return resList


# FITTING FUNCTIONS
# The following functions are to fit the 6 distributions mentioned above to the input dataset. They are all structured
# identically and will be explained here.

# 1. Input data is made into a histogram.

# 2. Generalized versions of the Probability Density Function for the fitted distribution are created.

# 3. For Normal and Triangular (where the fit parameters have a physical/statistical meaning from the data) best fit
# results are calculated directly. Otherwise, fit parameters are optimized to the scaled input data histogram and
# a least squares residual is calculated. All fit results are appended to the AllFitParameters dictionary.

# 4. X,Y data synthesized and returned for plotting purposes.

def TriangularFitFunction(inputData, binArgs):
    hist, bin_edges = np.histogram(inputData, bins = binArgs, density=True)
    xdata = np.asarray(binstoxdata(bin_edges))
    ydata = np.asarray(hist)

    mode = max(ydata)
    xMin = min(inputData)
    xMax = max(inputData)

    modeIndeces = getModes(ydata)

    def leftTriFit(x, xMode):
        y = (mode / (xMode - xMin)) * (x - xMin)
        return y

    def rightTriFit(x, xMode):
        y = (mode / (xMode - xMax)) * (x - xMax)
        return y


    # SS_RES and evaluate fns for each occurance of mode
    ss_res_summary = []

    for e in modeIndeces:
        ss_res = 0
        for i in range(e):
            ss_res += (leftTriFit(xdata[i], xdata[e]) - ydata[i]) ** 2
        for i in range(e, len(xdata)):
            ss_res += (rightTriFit(xdata[i], xdata[e]) - ydata[i]) ** 2
        ss_res_summary.append(ss_res)


    bestFitIndex = ss_res_summary.index(min(ss_res_summary))
    bestMode = modeIndeces[bestFitIndex]
    bestModeX = xdata[bestMode]

    plotXRange = np.linspace(min(inputData),max(inputData))
    leftList = []
    rightList = []

    for e in plotXRange:
        if(e<bestModeX):
            leftList.append(leftTriFit(e, bestModeX))
        elif(e>bestModeX):
            rightList.append(rightTriFit(e, bestModeX))

    triFitData = leftList + rightList

    allFitParameters['Triangular'] = [min(ss_res_summary), [min(inputData), bestModeX, max(inputData)]]

    return plotXRange, triFitData


def ParetoFitFunction(inputData, binArgs):
    hist, bin_edges = np.histogram(inputData, bins = binArgs, density= True)
    xdata = np.asarray(binstoxdata(bin_edges))
    ydata = np.asarray(hist)

    # print("BEFORE PARETO")
    # print(f'MINXDATA: {min(inputData)}')
    def Pareto(x, alpha):
        y = (alpha * (min(inputData)**alpha)/(x ** (alpha+1)))
        return y
    # print("AFTER PARETO")
    parameters, covariance = sp.optimize.curve_fit(Pareto, xdata, ydata)
    fit_A = parameters[0]

    fit_y = Pareto(xdata, fit_A)
    residuals = ydata - fit_y
    ss_res = np.sum(residuals ** 2)
    allFitParameters['Pareto'] = [ss_res, list(parameters), ['Alpha']]

    paretoFitData = []
    plotXRange_linspace = np.linspace(min(xdata), max(inputData), 200)

    for e in plotXRange_linspace:
        paretoFitData.append(Pareto(e, fit_A))



    return xdata, paretoFitData


def WiebullFitFunction(inputData, binArgs):
    hist, bin_edges = np.histogram(inputData,bins = binArgs, density=True)
    xdata = np.asarray(binstoxdata(bin_edges))
    ydata = np.asarray(hist)
    def WiebullVariate(x, alpha, beta):
        y = ((beta/alpha)*(x/alpha)**(beta-1))*(np.exp(-(x/alpha)**beta))
        return y

    parameters, covariance = sp.optimize.curve_fit(WiebullVariate, xdata, ydata)
    fitAlpha = parameters[0]
    fitBeta = parameters[1]
    fit_y = WiebullVariate(xdata, fitAlpha, fitBeta)
    residuals = ydata - fit_y
    ss_res = np.sum(residuals ** 2)

    allFitParameters['Weibull'] = [ss_res, list(parameters), ['Alpha', 'Beta']]

    wiebullFitData = []
    plotXRange = np.linspace(min(inputData), max(inputData))
    for e in plotXRange:
        wiebullFitData.append(WiebullVariate(e, fitAlpha, fitBeta))

    return plotXRange, wiebullFitData


def NormalFitFunction(inputData, binArgs):
    mean = np.mean(inputData)
    stdev = np.std(inputData)

    hist, bin_edges = np.histogram(inputData, bins = binArgs, density=True)
    xdata = np.asarray(binstoxdata(bin_edges))
    # ydataTemp = ScaleData(hist)
    ydata = np.asarray(hist)

    def Normal(x):
        # print(f'MEAN IN FN: {mean}, STDEV IN FN: {stdev}')
        y = (1 / (stdev * (2 * np.pi) ** .5)) * np.exp(-.5 * ((x - mean) / stdev) ** 2)
        return y

    fitY = Normal(xdata)
    residuals = ydata - fitY
    ss_res = np.sum(residuals ** 2)
    allFitParameters['Normal'] = [ss_res, [mean, stdev], ['Mean', 'STDEV']]

    normalFitData = []
    plotXRange = np.linspace(min(inputData), max(inputData))
    for e in plotXRange:
        normalFitData.append(Normal(e))

    return plotXRange, normalFitData


def GammaVariateFitFunction(inputData, binArgs):
    hist, bin_edges = np.histogram(inputData, bins = binArgs, density=True)
    xdata = np.asarray(binstoxdata(bin_edges))
    ydata = np.asarray(hist)

    def gammaVariate(x, alpha, beta):
        return gamma.pdf(x, alpha, scale=beta)

    parameters, covariance = sp.optimize.curve_fit(gammaVariate, xdata, ydata)
    fitAlpha = parameters[0]
    fitBeta = parameters[1]
    fit_y = gammaVariate(xdata, fitAlpha, fitBeta)
    residuals = ydata - fit_y
    ss_res = np.sum(residuals ** 2)
    allFitParameters['GammaVariate'] = [ss_res, list(parameters), ['Alpha', 'Beta']]

    gammaFitData = []
    plotXRange = np.linspace(min(inputData), max(inputData))
    for e in plotXRange:
        gammaFitData.append(gammaVariate(e, fitAlpha, fitBeta))

    return plotXRange, gammaFitData


def UniformFitFunction(inputData, binArgs):
    hist, bin_edges = np.histogram(inputData, bins = binArgs, density = True)
    xdata = np.asarray(binstoxdata(bin_edges))
    ydata = np.asarray(hist)
    def Uniform(x, a):
        y = a*x**0
        return y
    parameters, covariance = sp.optimize.curve_fit(Uniform, xdata, ydata)
    fit_A = parameters[0]
    fit_y = Uniform(xdata, fit_A)
    residuals = ydata - fit_y
    ss_res = np.sum(residuals ** 2)
    parameters = list(parameters)
    parameters.append(min(inputData))
    parameters.append(max(inputData))
    allFitParameters['Uniform'] = [ss_res, list(parameters), ['a', 'Min', 'Max']]

    uniformFitData = []
    plotXRange = np.linspace(min(inputData), max(inputData))
    for e in plotXRange:
        uniformFitData.append(Uniform(e, fit_A))

    return plotXRange, uniformFitData


# The following take in best fit parameters of respective distributions and return a sampled value from the
# corresponding continuously random variable.
def NormalContinuousSampler(parameters):
    y = random.gauss(parameters[0], parameters[1])
    return y

def ParetoContinuousSampler(parameters):
    y = random.paretovariate(parameters[0])
    return y

def WiebullContinuousSampler(parameters):
    y = random.weibullvariate(parameters[0], parameters[1])
    return y

def UniformContinuousSampler(parameters):
    y = random.uniform(parameters[1], parameters[2])
    return y

def TriangularContinuousSampler(parameters):
    y = random.triangular(parameters[0], parameters[1], parameters[2])
    return y

def GammaVariateContinuousSampler(parameters):
    y = random.gammavariate(parameters[0], parameters[1])
    return y


# Takes in [bestFitFunctionName, [fitParam], min(dataset)], and returns the desired number of randomly sampled
# values form the best fit distribution PDF's
def GetSampledValue(bestfitInfo, numSamples = 1):
    result = []

    # Maps bestFitFunctionName from the input list to the correct sampler function defined above.
    functionMapping = {
        "Normal": NormalContinuousSampler,
        "Pareto": ParetoContinuousSampler,
        "Weibull": WiebullContinuousSampler,
        "Uniform": UniformContinuousSampler,
        "GammaVariate": GammaVariateContinuousSampler,
        "Triangular": TriangularContinuousSampler,
    }

    # Synthesizes list of desired number of sampled values
    for i in range(numSamples):
        if bestfitInfo[0] in functionMapping:
            result.append(functionMapping[bestfitInfo[0]](bestfitInfo[1][1]))
    result = np.asarray(result)

    # Re-scales the data to its original magnitude by adding the min(dataset) - 1
    return result + (bestfitInfo[-1] - 1)


# Takes in an input dataset and returns a list in the following format: [bestFitFunctionName, [fitParam], min(dataset)]
def FitProcedure(inputData, show = True, autoSelect = True, outputParam = True, numBins = 10):
    # [functionName, [param], min(dataset)]
    bestFitParameters = []

    # Scale the input data
    scaledInputData = []
    for e in inputData:
        scaledInputData.append(e - min(inputData) + 1)

    # BinArgs establishes the range of x values for which bins of the histogram will be spread over.
    binArgs = np.linspace(min(scaledInputData), max(scaledInputData), numBins)

    # Calling functions to fit distributions to scaled data
    paretoXdata, paretoFit = ParetoFitFunction(scaledInputData, binArgs)
    wiebullXdata, wiebullFitData = WiebullFitFunction(scaledInputData, binArgs)
    normalXdata, normalFitData = NormalFitFunction(scaledInputData, binArgs)
    gammaXData, gammaFitData = GammaVariateFitFunction(scaledInputData, binArgs)
    triXData, triFitData = TriangularFitFunction(scaledInputData, binArgs)
    uniformXData, uniformFitData = UniformFitFunction(scaledInputData, binArgs)

    # Creates histogram of scaled input data for graphing purposes
    counts, bins = np.histogram(scaledInputData, bins=binArgs, density=True)
    bins = binstoxdata(bins)

    # The following are code blocks associated with this functions optional arguments. 'Show' will output Plotly graphs
    # depicting the fitted distributions for visual comparison. 'AutoSelect' = True will ensure the function
    # automatically chooses the fitted distribution with lowest residual to model the input data. 'AutoSelect' = False
    # will probe the user to manually make that decision. 'outputParam' prints best fit parameters and the selected
    # distribution to console.

    if autoSelect:
        minKey = min(allFitParameters, key=lambda key: allFitParameters[key][0])
        bestFitParameters.append(minKey)
        bestFitParameters.append(allFitParameters.get(minKey))

    if not autoSelect:
        validFunctions = ["Normal", "GammaVariate", "Triangular", "Uniform", "Weibull", "Pareto"]

        while True:
            functionType = input(f'Enter the function to use as best fit from the following list: {validFunctions}')
            if functionType in validFunctions:
                bestFitParameters.append(functionType)
                bestFitParameters.append(allFitParameters.get(functionType))
            break

    if show:
        barTrace = go.Bar(
            x=bins,  # X-axis labels (categories)
            y=counts,  # Y-axis values (height of bars)
            marker=dict(color='#99CCFF'),  # Optional: Customize the color of bars
            name='Histogram'
        )

        uniformTrace = go.Scatter(
            x=uniformXData,  # X-axis labels (categories)
            y=uniformFitData,  # Y-axis values (height of bars)
            marker=dict(color='orange'),  # Optional: Customize the color of bars
            name='Uniform Fit'
        )

        paretoTrace = go.Scatter(
            x=paretoXdata,  # X-axis data
            y=paretoFit,  # Y-axis data
            mode='lines',  # 'lines' mode for a line plot
            name='Pareto Fit',  # Name of the trace
            line=dict(color='blue', width=2)  # Line color and width
        )

        GVTrace = go.Scatter(
            x=gammaXData,  # X-axis data
            y=gammaFitData,  # Y-axis data
            mode='lines',  # 'lines' mode for a line plot
            name='Gamma Fit',  # Name of the trace
            line=dict(color='black', width=2)  # Line color and width
        )

        TriTrace = go.Scatter(
            x=triXData,  # X-axis data
            y=triFitData,  # Y-axis data
            mode='lines',  # 'lines' mode for a line plot
            name='Tri Fit',  # Name of the trace
            line=dict(color='gray', width=2),  # Line color and width

        )

        wiebullTrace = go.Scatter(
            x=wiebullXdata,  # X-axis data
            y=wiebullFitData,  # Y-axis data
            mode='lines',  # 'lines' mode for a line plot
            name='Wiebull Fit',  # Name of the trace
            line=dict(color='red', width=2)  # Line color and width
        )

        normalTrace = go.Scatter(
            x=normalXdata,  # X-axis data
            y=normalFitData,  # Y-axis data
            mode='lines',  # 'lines' mode for a line plot
            name='Normal Fit',  # Name of the trace
            line=dict(color='green', width=2)  # Line color and width
        )

        layout = go.Layout(
            title='Distribution Fit Functions',
            xaxis=dict(title='Scaled Price Data ($)'),
            yaxis=dict(title='Cumulative Frequency (%)'),
            barmode='group',
            bargap=0
        )

        fig = go.Figure(
            data=[barTrace, wiebullTrace, paretoTrace, normalTrace, GVTrace, TriTrace, uniformTrace],
            layout=layout)

        fig.show()

    if outputParam:
        print(f'All Fit Parameters: {allFitParameters}')
        print(f'BestFitParameters: {bestFitParameters}\n')


    bestFitParameters.append(min(inputData))
    return bestFitParameters





