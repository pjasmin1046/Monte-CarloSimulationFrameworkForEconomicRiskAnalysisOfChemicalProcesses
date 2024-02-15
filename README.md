# MainSim_V2
    MainSim file should be used to conduct probabalistic cost analyses of ammonia production plants 
    with SMR, Electrolysis, or Pyrolysis hydrogen input technologies. totalSamples, numsubranges parameters
    can be changed to reflect different simulation lengths and the granularity of the graphical output. 
    Carbon Tax Multiplier (CTM) can be maniuplated to simulate various intensities of carbon regulation.

    MainSim file imports all other necessary files contained within the repo.
    
# BSMS_Elec
    BSMS_Elec file is a self contained sim file conducting a probabalistic cost analysis of a PEM 
    Electrolyzer with variable electricity and utility cost data gridated by geographical area of the US 
    for a regional comparison of cost profiles. The execution function takes in the desired number of simulation 
    runs and granularity of graphical output. 

    BSMS_Elec imports all necessary files contained within the repo.

# ResamplingAlgorithm
    This file is used to fit Probability Density Functions (PDFs) of common distributions to datasets (mainly price data)
    to create continuously random variables from which to sample during a Monte Carlo simulation. Normal, Pareto, Wiebull,
    Triangular, Gamma, and Uniform distributions are fitted and the user has the option of manual selection, or automatic
    selection of the best fit PDF. 

# DistFunctions_V2
    This file holds functions to return sampled values from disributions modeling the uncertainty of cost parameters in 
    the plant simulation models. This file is imported into each simulation file and pertinent sampler functions are 
    called at each iteration of the discounted cash flow models to ensure accurate resampling of distributions occurs.

    Distributions for uncertain cost parameters are taken from various literature sources. The framework used to evaluate
    plant costs can be found at https://www.sciencedirect.com/science/article/abs/pii/S0098135417300200?via%3Dihub.
