# Simulation of Haber Bosch synthesis with Electrolysis as the hydrogen input. CTM is the Carbon Tax Multiplier which
# can be manipulated in the mainSim file to simulate varying intensities of carbon regulation

from DistFunctions import *

# Initializations
FCI = 0
NPVList = []

# Returns one CNPV for 30 year plant simulation, PEM Elec to ammonia
def findNPVElec(CTM = 1):
    # Purchased Equipment ($) from literature
    NH3ProductionLoop = 3.42e8
    AirSelectionUnit = 4.99e8
    electrolysisEquipment = 1.12e9
    NH3CatFill = 3.07e5
    purchasedEquipment = NH3CatFill + NH3ProductionLoop + AirSelectionUnit + electrolysisEquipment


    # Direct cost
    DC = purchasedEquipment * (
                1 + Installation_FN() + IC_FN() + Piping_FN() +
                Electrical_FN() + AUX_FN() + Facilities_FN() +
                Land_FN())

    # Indirect cost
    IC = Supervision_FN() + Legal_FN() + Construction_FN() + Contingency_FN()

    # FCI
    FCI = (DC * (1 + Supervision_FN())) / (1 - IC)


    # TCI & Working Capital
    WC = uniform.rvs(size=1, loc=0.1, scale=0.1)
    TCI = FCI / (1 - WC)

    # Op costs from literature
    opCosts = 3.9e9
    marketValue = FCI * MV_Plant_FN()
    salvage = marketValue - (marketValue * Combined_Taxes_FN())
    # Depreciation schedule (MACRS) from IRS
    depreciationArray = [0.0375, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285, 0.04888, 0.04522, 0.04462, 0.04461,
                         0.04462, 0.04461, 0.04462, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462,
                         0.02231, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    discount = 0.16
    GPV = 0

    # Simulation of 30 year plant lifetime: salvage added in after year 29 and carbon tax incremented after year one
    for i in range(1, 31):

        taxShield = (depreciationArray[i-1] * Combined_Taxes_FN()) * FCI

        if (i == 1):
            INS = (FCI * Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + INS + FIC) / denominator

            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)

            GPV += CFD

        if (i == 30):
            INS = (FCI * Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC30 = (opCosts + INS + FIC) / denominator
            CF30 = (-TPC30) * (1 - Combined_Taxes_FN()) + taxShield + salvage
            CFD30 = CF30 / ((1 + discount) ** 30)

            GPV += CFD30

        else:
            INS = (FCI * Insurance_FN())
            FIC = (TCI * Financing_Interest_FN())
            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + INS + FIC) / denominator

            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)

            GPV += CFD
    # NPV calculation
    NPV = GPV - FCI

    # CNPV = -(NPV)
    return float(-NPV)

