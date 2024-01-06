# This file will produce an CNPV analysis using a Monte-Carlo Simulation for a PEM electrolyzer. Fixed hydrogen flow
# of 0.08 kmol/s, 30MW electrolyzer operated at a mean current density of 1.7A/cm2. Electricity prices are sampled from datasets
# by region of the US for a more insightful comparison of the cost profiles by location.

from DistFunctions import *
from ResamplingAlgorithm import *
import pandas as pd
import plotly.graph_objs as go
import csv

# Instantiation of constants and empty lists to store NPVs by US region
NE_NPVList = []
MA_NPVList = []
PC_NPVList = []
Mount_NPVList = []

opHours = 8760 * 0.92 # Accounts for holidays, downtime, maintenance routines etc.
O2Output = 4876 # kg/hr
O2Profit = 22 * 1.05 * (10**6) # $/yr
H2Output = 4448 * 1000 # kg/yr
waterConverter = 15812.5 # converts from $(2016)/kgal to $(2022)/yr assuming 39678 MT/yr usage

# Read in pertinent datasets and prep for dist fitting
utilityPriceDF = pd.read_csv('Average_retail_price_of_electricity_industrial_monthly.csv')

# List of water price data
waterRMPrices = []
with open('Water Cost Data New.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Iterate through each row in the CSV and append it to the list
    for row in csv_reader:
        for e in row:
            price = e.strip()
            waterRMPrices.append(float(price))


# Datasets for prices of electrical utilities and water raw material input
NEelecUtilPrices = utilityPriceDF['New England cents per kilowatthour'].tolist()
MAelecUtilPrices = utilityPriceDF['Middle Atlantic cents per kilowatthour'].tolist()
PCelecUtilPrices = utilityPriceDF['Pacific Contiguous cents per kilowatthour'].tolist()
MountelecUtilPrices = utilityPriceDF['Mountain cents per kilowatthour'].tolist()

# Prints important results to console
def diagnostic(NPVList):
    print("5th:", np.percentile(NPVList, 5))
    print("95th:", np.percentile(NPVList, 95))
    print("STDEV:", statistics.pstdev(NPVList))
    print("AVGNPV:", to_scientific_notation(statistics.fmean(NPVList)), "\n")

# Converts number to SCI notation
def to_scientific_notation(number):
    a, b = '{:.4E}'.format(number).split('E')
    return '{:.5f}E{:+03d}'.format(float(a), int(b))

# Function to return a single NPV value for Hydrogen-From-Electrolysis process, taking in lists of resampled price data
# (from fitted distributions) for each uncertain cost.
def findElectolysisNPV(UtilBestParam , RMBestParameters, debug = False, name = None):
    # Purchased Equipment = Bare Module Cost from literature for Hydrogen Production Equipment (Dollars)
    purchasedEquipment = 30.54 * 1.05 * (10**6)

    # Samples 20 values from the continuously random variable defined by the best fit distribution
    CUtil = GetSampledValue(UtilBestParam, numSamples=20)
    CWater = GetSampledValue(RMBestParameters, numSamples=20)


    # Direct Costs as calculated in Kazantzis framework, pulling continuously random values from DistFunctions file
    DC = purchasedEquipment * (
                1 + Installation_FN() + IC_FN() + Piping_FN() +
                Electrical_FN() + AUX_FN() + Facilities_FN() +
                Land_FN())

    # Indirect Costs as calculated in Kazantzis framework, pulling continuously random values from DistFunctions file
    IC = Supervision_FN() + Legal_FN() + Construction_FN() + Contingency_FN()

    # FCI as calculated in Kazantzis framework
    FCI = (DC * (1 + IC))

    # Calculation of Total Capital Investment including Working Capital
    TCI = FCI / (1 - WC_FN())

    # Calculation of Market and Salvage values of the plant
    marketValue = FCI * MV_Plant_FN()
    salvage = marketValue - (marketValue * Combined_Taxes_FN())

    # Depreciation by year for the 20 year plant lifetime according to IRS MACRS Schedule
    depreciationArray = [0.0375, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285, 0.04888, 0.04522, 0.04462, 0.04461,
                         0.04462, 0.04461, 0.04462, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462,
                         0.02231, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    discount = 0.16
    GPV = 0

    # Lists to hold pertinent results for each year of the simulation
    opCostList = []
    TPCList = []
    CFList = []
    CFDList = []
    elecCostList = []
    waterCostList = []

    # Finds yearly cash flow and TPC correctly resampling distributions where necessary. Salvage value is added back in
    # after year 20
    for i in range(0, 20):
        taxShield = (depreciationArray[i] * Combined_Taxes_FN()) * FCI
        elecCost = (CUtil[i]/100) * opHours * 30 * 1000  # $
        elecCostList.append(elecCost)
        waterCost = CWater[i] * waterConverter
        waterCostList.append(waterCost)


        if(i == 19):
            opCosts = (.280 * FCI) + (2.73 * 0.008 * FCI) + (1.23 * (elecCost + waterCost))
            opCostList.append(opCosts)

            INS = (FCI * Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())
            TPC = (opCosts + INS + FIC) / denominator
            TPCList.append(TPC)

            # REV = (H2_Selling_Price_FN() * H2Output)
            CF = (- TPC ) * (1 - Combined_Taxes_FN()) + taxShield + salvage
            CFD = CF / ((1 + discount) ** (i+1))
            CFList.append(CF)
            CFDList.append(CFD)

            GPV += CFD

        else:
            opCosts = (.280 * FCI) + (2.73 * 0.008 * FCI) + (1.23 * (elecCost + waterCost))
            opCostList.append(opCosts)

            INS = (FCI * Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())
            TPC = (opCosts + INS + FIC) / denominator
            TPCList.append(TPC)

            # REV = (H2_Selling_Price_FN() * H2Output)
            CF = (- TPC ) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** (i+1))
            CFList.append(CF)
            CFDList.append(CFD)

            GPV += CFD

    NPV = GPV - FCI

    # Optional additional print statements for debugging
    if debug:
        print(f'REGION: {name}')
        print(f'TCI: {TCI}')
        print(f'CUTIL: {CUtil}')
        print(f'ELEC: {elecCostList}')
        print(f'WATER: {waterCostList}')
        print(f'OC: {opCostList}')
        print(f'TPC: {TPCList}')
        print(f'CF: {CFList}')
        print(f'CFD: {CFDList}')
        print(f'GPV: {GPV}\n\n')

    return float(-NPV)


# Executes NPV simulation taking in desired number of NPV samples and subranges for graphing
def Execution(totalSamples, subRanges, debug = False):

    # Fits distribution to price data and samples continuously random variable once for each year of plant lifetime returning a list.
    print("NE: ")
    NE_CUtilBestFitParameters = FitProcedure(NEelecUtilPrices, show=False, outputParam=True)
    print("\nMA: ")
    MA_CUtilBestFitParameters = FitProcedure(MAelecUtilPrices, show=False, outputParam=True)
    print("\nPC: ")
    PC_CUtilBestFitParameters = FitProcedure(PCelecUtilPrices, show=False, outputParam=True)
    print("\nMountain: ")
    Mount_CUtilBestFitParameters = FitProcedure(MountelecUtilPrices, show=False, outputParam=True)
    print("\nWater: ")
    CWaterBestFitParameters = FitProcedure(waterRMPrices, show=False, outputParam=True)



    for i in range(0, totalSamples):
        # Prints progress for user validation
        if (i == (int)(.25 * (totalSamples + 1))):
            print("25%")
        if (i == (int)(.5 * (totalSamples + 1))):
            print("50%")
        if (i == (int)(.75 * (totalSamples + 1))):
            print("75%")

        # Appending NPVs by region to correct list
        if debug:
            NE_NPVList.append(findElectolysisNPV(NE_CUtilBestFitParameters, CWaterBestFitParameters, debug = True, name = 'NE'))
            MA_NPVList.append(findElectolysisNPV(MA_CUtilBestFitParameters, CWaterBestFitParameters, debug=True, name = 'MA'))
            PC_NPVList.append(findElectolysisNPV(PC_CUtilBestFitParameters, CWaterBestFitParameters, debug=True, name = 'PC'))
            Mount_NPVList.append(findElectolysisNPV(Mount_CUtilBestFitParameters, CWaterBestFitParameters, debug=True, name = 'Mountain'))
        else:
            NE_NPVList.append(findElectolysisNPV(NE_CUtilBestFitParameters, CWaterBestFitParameters))
            MA_NPVList.append(findElectolysisNPV(MA_CUtilBestFitParameters, CWaterBestFitParameters))
            PC_NPVList.append(findElectolysisNPV(PC_CUtilBestFitParameters, CWaterBestFitParameters))
            Mount_NPVList.append(findElectolysisNPV(Mount_CUtilBestFitParameters, CWaterBestFitParameters))



    # Prints P5, P95, STDEV, AVGNPV to console by region
    print("\nSUMMARY: ")
    print("\nNew England:")
    diagnostic(NE_NPVList)
    print("\nMid-Atlantic:")
    diagnostic(MA_NPVList)
    print("\nPacific Contiguous:")
    diagnostic(PC_NPVList)
    print("\nMountain:")
    diagnostic(Mount_NPVList)


    # Compiles Cumulative Distribution of the NPV list
    numSubranges = subRanges
    a,b = createCumDist_FN(NE_NPVList, int(numSubranges))
    c,d = createCumDist_FN(MA_NPVList, int(numSubranges))
    e,f = createCumDist_FN(PC_NPVList, int(numSubranges))
    g,h = createCumDist_FN(Mount_NPVList, int(numSubranges))


    # Graphing and Data Vis in Plotly
    # Create traces of each CNPV cumulative distribution curve with labels
    NETrace = go.Scatter(
        x=a,  # X-axis data
        y=b,  # Y-axis data
        mode='lines',  # 'lines' mode for a line plot
        name='NE Regional Elec',  # Name of the trace
        line=dict(color='green', width=2)  # Line color and width
    )
    MATrace = go.Scatter(
        x=c,  # X-axis data
        y=d,  # Y-axis data
        mode='lines',  # 'lines' mode for a line plot
        name='MA Regional Elec',  # Name of the trace
        line=dict(color='blue', width=2)  # Line color and width
    )
    PCTrace = go.Scatter(
        x=e,  # X-axis data
        y=f,  # Y-axis data
        mode='lines',  # 'lines' mode for a line plot
        name='PC Regional Elec',  # Name of the trace
        line=dict(color='red', width=2)  # Line color and width
    )
    MountTrace = go.Scatter(
        x=g,  # X-axis data
        y=h,  # Y-axis data
        mode='lines',  # 'lines' mode for a line plot
        name='Mountain Regional Elec',  # Name of the trace
        line=dict(color='black', width=2)  # Line color and width
    )

    # Figure Layout
    layout = go.Layout(
        title='CNPV Cumulative Distribution Model',
        xaxis=dict(title='CNPV ($)'),
        yaxis=dict(title='Cumulative Frequency (%)'),
        barmode='group',
        bargap=0
    )

    # Instantiate and Show Plotly Figure
    fig = go.Figure(
        data=[NETrace, MATrace, PCTrace, MountTrace],
        layout=layout)

    fig.show()

Execution(10000, 200, debug = False)



