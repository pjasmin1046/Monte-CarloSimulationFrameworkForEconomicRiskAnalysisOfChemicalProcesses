# This file should be run to conduct probabilistic simulations of the ammonia plants. CTM can be manipulated to
# simulate varying intensities of carbon regulation
from SMRCostNPV_V2 import *
from ElecCostNPV_V2 import *
from PyrolysisCostNPV_V2 import *
from DistFunctions_V2 import *
import statistics
from matplotlib import pyplot as plt
import numpy as np

# SIMULATION PARAMETERS
totalSamples = 10000
numSubranges = 200

#Carbon Tax Multiplier
CTM = 1

# Prints pertinent statistical results to console
def Display(NPVList):
    print("\n5th:", np.percentile(NPVList, 5))
    print("95th:", np.percentile(NPVList, 95))
    print("STDEV:", statistics.pstdev(NPVList))
    print("AVGNPV:", to_scientific_notation(statistics.fmean(NPVList)), "\n")

def to_scientific_notation(number):
    a, b = '{:.4E}'.format(number).split('E')
    return '{:.5f}E{:+03d}'.format(float(a), int(b))

# NPV lists to hold simulated results
elecNPVList = []
pyroNPVList = []
SMRNPVList = []

# Simulation
for i in range (1, totalSamples + 1):
    # Prints progress to console
    if(i == (int)(.25 * (totalSamples + 1))):
        print("25%")
    if (i == (int)(.5 * (totalSamples + 1))):
        print("50%")
    if (i == (int)(.75 * (totalSamples + 1))):
        print("75%")

    elecNPVList.append(findNPVElec(CTM))
    SMRNPVList.append(findNPVSMR(CTM))
    pyroNPVList.append(findNPVPyro(CTM))



# Display results
print("ELEC: ")
Display(elecNPVList)
print("SMR: ")
Display(SMRNPVList)
print("PYRO: ")
Display(pyroNPVList)



# Create correctly formatted data to graph
a,b = createCumDist_FN(elecNPVList, numSubranges)
c,d = createCumDist_FN(SMRNPVList, numSubranges)
e,f = createCumDist_FN(pyroNPVList, numSubranges)

# Graphing procedure
plt.plot(a,b, label = "ELEC")
plt.plot(c,d, label = "SMR")
plt.plot(e,f, label = "PYRO")
plt.legend()
plt.xlabel("CNPV ($)")
plt.ylabel("Cumulative Frequency")
plt.title("CNPV Cumulative Distribution Model")
plt.show()






