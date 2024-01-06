# Simulation of Haber Bosch synthesis with CH4 Pyrolysis as the hydrogen input. CTM is the Carbon Tax Multiplier which
# can be manipulated in the mainSim file to simulate varying intensities of carbon regulation

from DistFunctions import *

# Initializations
FCI = 0
NPVList = []
# Returns one CNPV for 30 year plant simulation, Pyrolysis to ammonia
def findNPVPyro(CTM = 1):
    # Purchased Equipment ($) taken from literature
    NH3ProductionLoop = 3.42e8
    AirSelectionUnit = 4.99e8
    pyrolysisEquipment = 9.24e7
    NH3CatFill = 3.07e5
    purchasedEquipment = NH3CatFill + NH3ProductionLoop + AirSelectionUnit + pyrolysisEquipment


    # Direct Costs
    DC = purchasedEquipment * (
                1 + Installation_FN() + IC_FN() + Piping_FN() +
                Electrical_FN() + AUX_FN() + Facilities_FN() +
                Land_FN())


    # Indirect Costs
    IC = Supervision_FN() + Legal_FN() + Construction_FN() + Contingency_FN()

    # FCI
    FCI = (DC * (1 + Supervision_FN())) / (1 - IC)


    # TCI and Working Capital
    WC = uniform.rvs(size=1, loc=0.1, scale=0.1)
    TCI = FCI / (1 - WC)


    # OP Costs from literature
    opCosts = 8.09e8
    marketValue = FCI * MV_Plant_FN()
    salvage = marketValue - (marketValue * Combined_Taxes_FN())
    carbonTaxYrOne = CTM * (np.random.triangular(27, 30, 33, 1))
    carbonTransport = np.random.triangular(9, 10, 11, 1)
    CO2PerDay = 1141.6 # TONNE/DAY

    # Deprecation (MACRS) from IRS
    depreciationArray = [0.0375, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285, 0.04888, 0.04522, 0.04462, 0.04461,
                         0.04462, 0.04461, 0.04462, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462,
                         0.02231, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    discount = 0.16
    GPV = 0

    # Simulation of 30 year plant lifetime: salvage added in after year 29 and carbon tax incremented after year one
    for i in range(1, 31):
        taxShield = (depreciationArray[i - 1] * Combined_Taxes_FN()) * FCI

        if (i == 1):
            CTax = (carbonTaxYrOne * CO2PerDay * 365)

            CTS = (carbonTransport * CO2PerDay * 365)
            INS = (FCI * Insurance_FN())

            FIC = (TCI * Financing_Interest_FN())

            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + CTS + CTax + INS + FIC) / denominator


            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)


            GPV += CFD

            carbonTaxNew = carbonTaxYrOne * (1 + CO2_Tax_Growth_FN())


        if (i == 30):

            CTax = (carbonTaxNew * CO2PerDay * 365)

            CTS = (carbonTransport * CO2PerDay * 365)
            INS = (FCI * Insurance_FN())

            FIC = (TCI * Financing_Interest_FN())

            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC30 = (opCosts + CTS + CTax + INS + FIC) / denominator
            CF30 = (-TPC30) * (1 - Combined_Taxes_FN()) + taxShield + salvage
            CFD30 = CF30 / ((1 + discount) ** 30)

            GPV += CFD30


        else:
            CTax = (carbonTaxNew * CO2PerDay * 365)

            CTS = (carbonTransport * CO2PerDay * 365)
            INS = (FCI * Insurance_FN())

            FIC = (TCI * Financing_Interest_FN())

            denominator = 1 - ((Admin_Costs_FN() + Marketing_FN()) +
                               Contingency_FN() + 0.05 + Patents_Loyalties_FN() +
                               Overhead_FN())

            TPC = (opCosts + CTS + CTax + INS + FIC) / denominator


            CF = (-TPC) * (1 - Combined_Taxes_FN()) + taxShield
            CFD = CF / ((1 + discount) ** i)


            GPV += CFD

            carbonTaxNew = carbonTaxNew * (1 + CO2_Tax_Growth_FN())

    # NPV calculation
    NPV = GPV - FCI

    # CNPV = -(NPV)
    return float(-NPV)
