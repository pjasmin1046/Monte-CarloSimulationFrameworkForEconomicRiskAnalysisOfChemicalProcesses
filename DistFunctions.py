# from scipy import random
import numpy as np
from scipy.stats import uniform, pareto, weibull_min
import statistics
import matplotlib.pyplot as plt
import shutil
import os

variableList = {
    # "FCI" : [12, 14] ,
    "PSS Support Price": ["TD", np.random.triangular(10.2, 11.3, 12.4, 1)],
    "Membrane Lifetime": ["TD", np.random.triangular(1, 3, 5, 1)],
    "Nominal Discount Rate": ["TD", np.random.triangular(0.114, 0.16, 0.176, 1)],
    "CO2Transport": ["TD", np.random.triangular(9, 10, 11, 1)],
    "CO2Tax": ["TD", np.random.triangular(27, 30, 33, 1)],
    "CO2TaxGrowth": ["TD", np.random.triangular(0.054, 0.06, 0.066, 1)],
    "H2SellingPrice": ["TD", np.random.triangular(9, 10, 11, 1)],
    "CombinedTaxes": ["TD", np.random.triangular(0.0, 0.064, 0.095, 1)],
    "MVPlant": ["TD", np.random.triangular(0.135, 0.150, 0.165, 1)],
    "Installation": ["UD", uniform.rvs(size = 1, loc = 0.25 , scale = 0.55 - 0.25)],
    "IC": ["UD", uniform.rvs(size = 1, loc = 0.08 , scale = 0.50 - 0.08)],
    "Piping": ["UD", uniform.rvs(size = 1, loc = 0.1 , scale = 0.8 - 0.1)],
    "Electrical": ["UD", uniform.rvs(size = 1, loc = 0.1 , scale = 0.4 - 0.1)],
    "AUX": ["UD", uniform.rvs(size = 1, loc = 0.1 , scale = 0.7 - 0.1)],
    "Facilities": ["UD", uniform.rvs(size = 1, loc = 0.4 , scale = 1 - 0.4)],
    "Land": ["UD", uniform.rvs(size = 1, loc = 0.04 , scale = 0.08 - 0.04)],
    "Supervision": ["UD", uniform.rvs(size = 1, loc = 0.05 , scale = 0.3 - 0.05)],
    "Legal": ["UD", uniform.rvs(size = 1, loc = 0.01 , scale = 0.03 - 0.01)],
    "Construction": ["UD", uniform.rvs(size = 1, loc = 0.1 , scale = 0.2 - 0.1)],
    "Contingency": ["UD", uniform.rvs(size = 1, loc = 0.05 , scale = 0.15 - 0.05)],
    "Insurance": ["UD", uniform.rvs(size = 1, loc = 0.004 , scale = 0.01 - 0.004)],
    "WC": ["UD", uniform.rvs(size = 1, loc = 0.1 , scale = 0.2 - 0.1)],
    "Financing Interest": ["UD", uniform.rvs(size = 1, loc = 0.06 , scale = 0.1 - 0.06)],
    "Overhead": ["UD", uniform.rvs(size = 1, loc = 0.05 , scale = 0.15 - 0.05)],
    "Patents/Loyalties": ["UD", uniform.rvs(size = 1, loc = 0.0 , scale = 0.06 - 0)],
    "Admin Costs": ["UD", uniform.rvs(size = 1, loc = 0.02 , scale = 0.05 - 0.02)],
    "Marketing": ["UD", uniform.rvs(size = 1, loc = 0.02 , scale = 0.06 - 0.02)],
    "Capacity Factor" : ["TD", np.random.triangular(0.75, 0.8, 0.85, 1)],
    "De-Rating Factor" : ["UD", uniform.rvs(size = 1, loc = 0.05 , scale = 0.05)],
}

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

def MV_Plant_FN():
    return np.random.triangular(0.135, 0.150, 0.165, 1)

def Installation_FN():
    return uniform.rvs(size = 1, loc = 0.25 , scale = 0.55 - 0.25)

def IC_FN():
    return uniform.rvs(size = 1, loc = 0.08 , scale = 0.50 - 0.08)

def Piping_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.8 - 0.1)

def Electrical_FN():
    return uniform.rvs(size = 1, loc = 0.1 , scale = 0.4 - 0.1)

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



def createDist_FN(NPVList, numOfSubranges, saveStatus):
    totalRange = max(NPVList) - min(NPVList)
    numRanges = numOfSubranges
    rangeSize = totalRange / numRanges
    saveStatus = saveStatus
    x_values = []
    # x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    y_values = []

    lowerBound = min(NPVList)
    upperBound = lowerBound + rangeSize
    # print("MIN: ", min(NPVList), "\nMAX: ", max(NPVList), "\nRangeSize", rangeSize, "\nLB: ", lowerBound, "\nUB: ",
    #       upperBound)
    globalCount = 0

    for i in range(1, numRanges + 1):
        count = 0
        x_values.append((upperBound + lowerBound) / 2)
        for j in range(0, len(NPVList)):
            if (NPVList[j] > lowerBound and NPVList[j] < upperBound):
                count += 1
                globalCount += 1
        y_values.append(count)

        lowerBound = upperBound
        upperBound = lowerBound + rangeSize
        # print("LB: ", lowerBound, "\nUB: ", upperBound)

    # print("X: ", len(x_values))
    # print("Y: ", len(y_values))

    # print(globalCount)
    return x_values, y_values
    # plt.plot(x_values, y_values)
    # plt.xlabel("NPV ($)")
    # plt.ylabel("# of NPVs")
    # plt.title("Distribution of NPVs")

    # if(saveStatus == "SAVE"):
    #     plt.savefig("NPV_Dist.pdf")
    #     sourcePath = r"C:\Users\Paul\PycharmProjects\MQP\NPV_Dist.pdf"
    #     destinationDirectory = r"C:\Users\Paul\Desktop\MQP\NPV_Dist_From_Python"
    #     destinationPath = os.path.join(destinationDirectory, os.path.basename(sourcePath))
    #     shutil.move(sourcePath, destinationPath)
    # plt.show()

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

def createCumDist_FN(NPVList, numOfSubranges, saveStatus):
    totalRange = max(NPVList) - min(NPVList)
    numRanges = numOfSubranges
    rangeSize = totalRange / numRanges
    saveStatus = saveStatus
    x_values = []
    # x_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    y_values = []

    lowerBound = min(NPVList)
    upperBound = lowerBound + rangeSize
    # print("MIN: ", min(NPVList), "\nMAX: ", max(NPVList), "\nRangeSize", rangeSize, "\nLB: ", lowerBound, "\nUB: ",
    #       upperBound)
    globalCount = 0

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