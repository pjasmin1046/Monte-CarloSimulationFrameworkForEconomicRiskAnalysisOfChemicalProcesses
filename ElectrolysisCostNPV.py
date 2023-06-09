# from scipy import random
# import numpy as np
# from scipy.stats import uniform, pareto, weibull_min
# import statistics
from DistFunctions import *
import matplotlib.pyplot as plt

FCI = 0
totalSamples = 10000
NPVList = []
def findNPVElec():
    # Purchased Equipment ($)
    NH3ProductionLoop = 3.42e8
    AirSelectionUnit = 4.99e8
    electrolysisEquipment = 1.12e9
    NH3CatFill = 3.07e5

    NH3CatalystRecurring = 8.13e5


    purchasedEquipment = NH3CatFill + NH3ProductionLoop + AirSelectionUnit + electrolysisEquipment
    # print(totalCatalystFill)
    # print(totalCatalystRecurring)
    # print("PE: ", purchasedEquipment)

    # DC
    DC = purchasedEquipment * (
                1 + Installation_FN() + IC_FN() + Piping_FN() +
                Electrical_FN() + AUX_FN() + Facilities_FN() +
                Land_FN())

    # print (DC)

    # IC
    IC = Supervision_FN() + Legal_FN() + Construction_FN() + Contingency_FN()

    # FCI
    FCI = (DC * (1 + Supervision_FN())) / (1 - (Legal_FN() + Construction_FN() + Contingency_FN()))
    # print("FCI: ", FCI)

    # TCI
    WC = uniform.rvs(size=1, loc=0.1, scale=0.1)
    TCI = FCI / (1 - WC)
    # print("TCI: " , TCI)

    # OP Costs
    H2PerDay = 685
    ammoniaPerDay = 3850.0107
    # # metric tons per day
    #
    # annualH2OCost = 4.92e6
    # # $/year
    #
    #
    # fuelCosts = (historicalCoalPrice / 1.12) * coalPerDay * 365
    # # $/year
    #
    # print("FUEL: ", fuelCosts)
    # # membraneLifetime = membrane / (np.random.triangular(1, 3, 5, 1))
    # # op = fuel + [operating + maintainence + admin + property] + [maintainence material + membrane replacement]
    #
    # fixedOM = fuelCosts + 2.25 * (.008 * (FCI)) + (.02 * FCI)
    # print("FixedOM: ", fixedOM)
    # variableOM = .02 * FCI + totalCatalystRecurring + annualH2OCost
    # print("VariableOM: ", variableOM)
    opCosts = 3.9e9

    # 30 YEAR SUMMATION
    NPV = 0
    marketValue = FCI * MV_Plant_FN()
    # print("MV: ", marketValue)
    salvage = marketValue - (marketValue * Combined_Taxes_FN())
    # print("SV: ", salvage)
    carbonTaxYrOne = np.random.triangular(27, 30, 33, 1)
    carbonTransport = np.random.triangular(9, 10, 11, 1)
    # print(carbonTaxYrZero)
    CO2perCoal = 2.86
    # mass/mass
    depreciation = 1 / 30
    depreciationArray = [0.0375, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285, 0.04888, 0.04522, 0.04462, 0.04461,
                         0.04462, 0.04461, 0.04462, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462,
                         0.02231, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # taxShield = (depreciation * Combined_Taxes_FN()) * FCI
    # print("TaxShield: ", taxShield)
    # revenue = H2_Selling_Price_FN() * Capacity_Factor_FN() * H2PerDay * (1 - De_Rating_Factor_FN()) * 365 * 1000
    # revenue = ammoniaSellingPrice * Capacity_Factor_FN() * ammoniaPerDay * (1 - De_Rating_Factor_FN()) * 365
    # print("R", revenue)
    discount = 0.16
    GPV = 0
    TPC30 = 0

    # GPV for years 1-29
    for i in range(1, 31):
        # taxGrowth = CO2_Tax_Growth_FN()
        # INSVAR = uniform.rvs(size=1, loc=0.004, scale=0.01 - 0.004)
        taxShield = (depreciationArray[i-1] * Combined_Taxes_FN()) * FCI

        if (i == 1):
            # CTax = (carbonTaxYrOne * CO2perCoal * coalPerDay * 365)
            # print("year 1", carbonTaxYrOne)
            # HDC = (H2PerDay * 3 * 1000 * 365)
            ADC = (ammoniaPerDay * 3 * 1000 * 365)
            # CTS = (carbonTransport * coalPerDay * CO2perCoal * 365)
            INS = (FCI * Insurance_FN())
            # print("INS (", i ,"): ", INS)
            FIC = (TCI * Financing_Interest_FN())
            # print("FIC (", i, "): ", FIC)
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + INS + FIC) / denominator
            # print("TPC (", i, "): ", TPC)

            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)
            # print("CF(D) (", i, "): ", CFD, "\n")

            GPV += CFD

            # carbonTaxNew = carbonTaxYrOne * (1 + taxGrowth)
            # print("after 1", carbonTaxNew)

        if (i == 30):
            # print(i, carbonTaxNew)
            # CTax = (carbonTaxNew * CO2perCoal * coalPerDay * 365)
            # HDC = (H2PerDay * 3 * 1000 * 365)
            ADC = (ammoniaPerDay * 3 * 1000 * 365)
            # CTS = (carbonTransport * coalPerDay * CO2perCoal * 365)
            INS = (FCI * Insurance_FN())
            # print("INS (30): ", INS)
            FIC = (TCI * Financing_Interest_FN())
            # print("FIC (30): ", FIC)
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC30 = (opCosts + INS + FIC) / denominator
            break

        else:
            # CTax = (carbonTaxNew * CO2perCoal * coalPerDay * 365)
            # print("year " , i, carbonTaxNew)
            # HDC = (H2PerDay * 3 * 1000 * 365)
            ADC = (ammoniaPerDay * 3 * 1000 * 365)
            # CTS = (carbonTransport * coalPerDay * CO2perCoal * 365)
            INS = (FCI * Insurance_FN())
            # print("INS (", i, "): ", INS)
            # print(Insurance_FN())
            # INS = FCI * insurance
            # print("INS", i, INSVAR)
            # print(Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            # print("FIC (", i, "): ", FIC)
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + INS + FIC) / denominator
            # print("TPC (", i, "): ", TPC)

            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)
            # print("CF(D) (", i, "): ", CFD, "\n")

            GPV += CFD
            # print(i, CFD, GPV)
            # carbonTaxNew = carbonTaxNew * (1 + taxGrowth)
            # print("after ", i, carbonTaxNew)

    # print(TPC30)

    # TPC30 discounted with salvage
    CF30 = (-TPC30) * (1 - Combined_Taxes_FN()) + taxShield + salvage
    CFD30 = CF30 / ((1 + discount) ** 30)
    # print("CF(D) 30: ", CFD30)

    GPV += CFD30
    # print("GPV: ", GPV)
    NPV = GPV - FCI
    # print("CALCULATED", NPV)
    # NPVList.append(float(-NPV))
    # print(float(-NPV))
    return float(-NPV)
    # print("GPV", GPV)
    # print("FCI", FCI)
    # print("NPV", NPV)
#
# for i in range (1,11):
#     findNPVElec()
#     print("NPV", NPVList[i-1], "\n")
#
#
# print("\n5th", np.percentile(NPVList, 5))
# print("95th", np.percentile(NPVList, 95))
# print("STDEV", statistics.pstdev(NPVList))

# createDist_FN(NPVList, 100, "")































# totalRange = max(NPVList) - min(NPVList)
# numRanges = 100
# rangeSize = totalRange/numRanges
# x_values = []
# # x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
# y_values = []
#
# lowerBound = min(NPVList)
# upperBound = lowerBound + rangeSize
# print("MIN: ", min(NPVList), "\nMAX: ", max(NPVList), "\nRangeSize", rangeSize, "\nLB: ", lowerBound, "\nUB: ", upperBound)
# globalCount = 0
# # for k in range(1, numRanges ):
# #     x_values.append(k)
# # print("X: ", x_values)
#
# for i in range(1, numRanges + 1):
#     count = 0
#     x_values.append ((upperBound + lowerBound) / 2)
#     for j in range(0, len(NPVList)):
#         if (NPVList[j] > lowerBound and NPVList[j] < upperBound):
#             count += 1
#             globalCount += 1
#     y_values.append(count)
#
#     lowerBound = upperBound
#     upperBound = lowerBound + rangeSize
#     print("LB: ", lowerBound, "\nUB: ", upperBound)
#
#
#
# print("X: ", len(x_values))
# print("Y: ", len(y_values))
#
# print (globalCount)
# plt.plot(x_values, y_values)
# plt.xlabel("NPV ($)")
# plt.ylabel("# of NPVs")
# plt.title("Distribution of NPVs")
#
# plt.show()
