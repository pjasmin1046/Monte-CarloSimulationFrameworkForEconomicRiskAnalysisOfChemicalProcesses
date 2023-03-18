from SMRCostNPV import *
from ElectrolysisCostNPV import *
from PyrolysisCostNPV import *
from DistFunctions import *
import statistics
from matplotlib import pyplot as plt
import numpy as np



def diagnostic(NPVList):
    print("\n5th:", np.percentile(NPVList, 5))
    print("95th:", np.percentile(NPVList, 95))
    print("STDEV:", statistics.pstdev(NPVList))
    print("AVGNPV:", to_scientific_notation(statistics.fmean(NPVList)), "\n")

def to_scientific_notation(number):
    a, b = '{:.4E}'.format(number).split('E')
    return '{:.5f}E{:+03d}'.format(float(a), int(b))

elecNPVList = []
pyroNPVList = []
SMRNPVList = []

totalSamples = 10000

for i in range (1, totalSamples + 1):
    if(i == (int)(.25 * (totalSamples + 1))):
        print("25%")
    if (i == (int)(.5 * (totalSamples + 1))):
        print("50%")
    if (i == (int)(.75 * (totalSamples + 1))):
        print("75%")

    elecNPVList.append(findNPVElec())
    SMRNPVList.append(findNPVSMR())
    pyroNPVList.append(findNPVPyro())




print("ELEC: ")
diagnostic(elecNPVList)
print("SMR: ")
diagnostic(SMRNPVList)
print("PYRO: ")
diagnostic(pyroNPVList)


numSubranges = 200

a,b = createCumDist_FN(elecNPVList, numSubranges, "")
c,d = createCumDist_FN(SMRNPVList, numSubranges, "")
e,f = createCumDist_FN(pyroNPVList, numSubranges, "")

plt.plot(a,b, label = "ELEC")
plt.plot(c,d, label = "SMR")
plt.plot(e,f, label = "PYRO")
plt.legend()
plt.xlabel("CNPV ($e10)")
plt.ylabel("Cumulative Frequency")
plt.title("CNPV Cumulative Distribution Model")
plt.show()






# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
#
# y, binEdges = np.histogram(elecNPVList, bins=100)
# z, binEdges = np.histogram(SMRNPVList, bins=100)
# q, binEdges = np.histogram(pyroNPVList, bins=100)
# plt.hist(elecNPVList, bins=100, edgecolor='black')
# plt.hist(SMRNPVList, bins=100, edgecolor='blue')
# plt.hist(pyroNPVList, bins=100, edgecolor='red')
#
# bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
# plt.plot(bincenters, y, '-', c='black')
# plt.plot(bincenters, z, '-', c='blue')
# plt.plot(bincenters, q, '-', c='red')
# plt.show()