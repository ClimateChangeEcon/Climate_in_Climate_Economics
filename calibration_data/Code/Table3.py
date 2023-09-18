# Script determines reservoir masses for year 2015 and any year where M_AT = 400 ppm and prints them to screen
#
# Uses: TestDefs.py, ClimDICE.py
#
# Input: none
# Output: reservoir masses for Table 3 in the paper
#
# Note that reservoir masses depend only on the carbon cycle, not on the temperature part of CDICE
#
# To run: exec(open("./Table3.py").read())

import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ClimDICE as cld
import TestDefs as td

importlib.reload(cld)
importlib.reload(td)

F_RCP85E  = 'yes'   #CMIP5, RCP26 from emi.; Figs: temp. / CO2 conc.

#CMIP5, historical plus RCP26 from carbon emissions
if (F_RCP85E == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP85_EMI')

ibe = 1
ien = len(df2['label'])-2
for i in range(ibe,ien+1):
#for i in range(1,5):
    df2['label'][i]
    sisi = df2['simu'][i]
    j = np.argmin(np.abs(sisi.M_of_t[0,:]-400./0.47))  #get array index where atmospheric mass is closest to 400 ppm CO2
    k = 165                                            #array index of year 2000
    print("i = " + str(i) + " ... " + str(df2['label'][i]))
    print("  Year 2015:    M = " + str(sisi.M_of_t[:,k]) + "    T = " + str(sisi.T_of_t[:,k]) + "    year = " + str(sisi.n_year[k]))
    print("    400 ppm:    M = " + str(sisi.M_of_t[:,j]) + "    T = " + str(sisi.T_of_t[:,j]) + "    year = " + str(sisi.n_year[j]))

