# Code to estimate optimal parameters for Carbon Cycle (CC)
# Calibration test case is 100 GtC pulse of Joos et al. (2013)
# Calibration / pulse can be run on equilibrium conditions, as CDICE by construction
# is not sensitive to background conditions (pre-industrial, present-day etc.)
# Calibration minimizes maximum norm over NMY years of data
#
# Uses: TestCalibCC.py, ClimDICE.py
# 
# Input: User defined input below in code, consisting of
#        model - one of MMM, MESMO, LOVECLIM
#        pre-defined search range - one of COARSE or FINE
#        number of years over which to take maximum norm
#
# Output: best fit values, as search progresses, to command prompt plus final, illustrating figures
#
# To run: exec(open("./Table1.py").read())

import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy
import ClimDICE as cld
import TestCalibCC as td

importlib.reload(cld)
importlib.reload(td)

#user defined input starts here
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

M2C = 'DEMO'     #what model to calibrate? 'MMM', 'MESMO', or 'LOVECLIM'? 'DEMO'-> fast demonstration of code
COF = 'COARSE'  #coarse or fine search range? 'COARSE' or 'FINE'? (pre-defined, see below)
NMY = 250       #maximum norm over how many years? At most 1000

ShowAllTries = 'yes'  #in final plots, show gray lines for each try?


# Below come the pre-defined search ranges for CC parameters [b12, b23, muo, mlo] for models MMM, MESMO, LOVECLIM
# For demonstration purposes, and to reduce the run time, two sets of parameter search ranges per model are prescribed:
#  - a COARSE search range, chosen such that the best fit values in Table 1 are one point in this search space
#  - a FINE, NEAR OPTIMUM search range, exploring the vicinity of the best fit values in Table 1 / the COARSE search range
# For demonstration purposes, a really small search range is also given, which you may uncomment (and set M2C to 'none')
# For a true search, the parameter ranges are large and the step size for searchin fine.

if (M2C == 'DEMO'):
    # SMALL CODE DEMONSTRATION SEARCH RANGE for model MMM - to use, uncomment and set above M2C='none'
    #------------------------------------------------------------------------
    n2f = 16 #MMM - the model from J13 we want to fit, number given by implementation of J13 in ClimDICE.py        [MMM -> n2f=16, MESMO -> n2f=10, LOVECLIM -> n2f=9]
    Tb12 = np.arange(0.053, 0.055, 0.001)
    Tb23 = np.arange(0.0081, 0.0083, 0.0001)
    Tmuo = np.arange(488., 490., 1.)
    Tmlo = np.arange(1280., 1282., 1.)

if (M2C == 'MMM'):
    n2f = 16 #MMM - the model from J13 we want to fit, number given by implementation of J13 in ClimDICE.py
    if (COF == 'COARSE'):
        # COARSE SEARCH RANGE for model MMM
        Tb12 = np.arange(0.034, 0.095, 0.005)
        Tb23 = np.arange(0.0052, 0.0112, 0.0005)
        Tmuo = np.arange(289., 690., 50.)
        Tmlo = np.arange(1081., 1482., 50.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.05399999999999999   b23=0.008200000000000002   muo=489.0   mlo=1281.0   dist=0.021039764318253495    idi=20

    if (COF == 'FINE'):
        # FINE, NEAR OPTIMUM SEARCH RANGE for model MMM
        Tb12 = np.arange(0.050, 0.059, 0.001)
        Tb23 = np.arange(0.0078, 0.0087, 0.0001)
        Tmuo = np.arange(444., 535., 5.)
        Tmlo = np.arange(1236., 1327., 5.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.054000000000000006   b23=0.008599999999999995   muo=484.0   mlo=1236.0   dist=0.019837612839701257    idi=20

if (M2C == 'MESMO'):
    n2f = 10 #MESMO - the model from J13 we want to fit, number given by implementation of J13 in ClimDICE.py
    if (COF == 'COARSE'):
        # COARSE SEARCH RANGE for model MESMO
        Tb12 = np.arange(0.039, 0.090, 0.005)
        Tb23 = np.arange(0.003, 0.0102, 0.0005)
        Tmuo = np.arange(205., 606., 50.)
        Tmlo = np.arange(665., 1066., 50.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.05899999999999999   b23=0.008   muo=305.0   mlo=915.0   dist=0.027641126137730287    idi=2

    if (COF == 'FINE'):
        # FINE, NEAR OPTIMUM SEARCH RANGE for model MESMO
        Tb12 = np.arange(0.055, 0.064, 0.001)
        Tb23 = np.arange(0.0076, 0.0085, 0.0001)
        Tmuo = np.arange(260., 351., 5.)
        Tmlo = np.arange(870., 961., 5.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.060000000000000005   b23=0.008500000000000002   muo=300.0   mlo=880.0   dist=0.02700142654535853    idi=61

if (M2C == 'LOVECLIM'):
    n2f =  9 #LOVECLIM - the model from J13 we want to fit, number given by implementation of J13 in ClimDICE.py
    if (COF == 'COARSE'):
        # COARSE SERCH RANGE for model LOVECLIM
        Tb12 = np.arange(0.037, 0.088, 0.005)
        Tb23 = np.arange(0.0065, 0.0126, 0.0005)
        Tmuo = np.arange(450.,  751., 50.)
        Tmlo = np.arange(1185., 1486., 50.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.061999999999999986   b23=0.008499999999999997   muo=650.0   mlo=1185.0   dist=0.03630465851778697    idi=2

    if (COF == 'FINE'):
        # FINE, NEAR OPTIMUM SEARCH RANGE for model LOVECLIM
        Tb12 = np.arange(0.058, 0.067, 0.001)
        Tb23 = np.arange(0.0081, 0.0091, 0.0001)
        Tmuo = np.arange(605.,  696., 5.)
        Tmlo = np.arange(1140., 1231., 5.)
        # above parameter range over NMY=250 yields BEST OF ALL IS: b12=0.063   b23=0.009099999999999994   muo=640.0   mlo=1200.0   dist=0.0325078407853277    idi=61 

#user defined input ends here, no more changes below this line
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#100GtC puls to PD atmosphere benchmark from  Joos et al. (2013)
#def BenchMarkPuls(Nb12 = 0.054 , Nb23 = 0.0082, NME18 = np.array([607., 489., 1281.])):
dist = 1.e20
b12_best = 0.
b23_best = 0.
muo_best = 0.
mlo_best = 0.
f1=plt.figure(1)
f2=plt.figure(2)
f3=plt.figure(3)

for i12 in range(len(Tb12)):
    #print('i12 = '+str(i12))
    for i23 in range(len(Tb23)):
        #print('i23 = '+str(i23))
        for iuo in range(len(Tmuo)):
            for ilo in range(len(Tmlo)):
                df2 = td.BenchMarkPuls(Nb12 = Tb12[i12], Nb23 = Tb23[i23], NME18 = np.array([607., Tmuo[iuo], Tmlo[ilo]]))
                sisi0  = df2['simu'][0]
                sisi1  = df2['simu'][1]
                tmp0   = (sisi0.M_of_t[0,:] - sisi0.M_ini[0]) / sisi0.M_puls
                tmp1   = (sisi1.M_of_t[0,:,n2f] - sisi1.M_ini[0]) / sisi1.M_puls
                tmp    = np.abs(tmp1[0:NMY] - tmp0[0:NMY])
                dist01 = np.max(tmp)
                idi01  = np.argmax(tmp)
                if (ShowAllTries=='yes'):
                    plt.figure(1); plt.plot(tmp0[0:21],color=[0.6,0.6,0.6],linewidth=1);
                    plt.figure(2); plt.plot(tmp0[0:201],color=[0.6,0.6,0.6],linewidth=1);
                    plt.figure(3); plt.plot(tmp0[0:1000],color=[0.6,0.6,0.6],linewidth=1);
                if (dist01<dist):
                    b12_best = Tb12[i12]
                    b23_best = Tb23[i23]
                    muo_best = Tmuo[iuo]
                    mlo_best = Tmlo[ilo]
                    sis_best = copy.deepcopy(sisi0)
                    dis_best = copy.deepcopy(dist)
                    idi_best = copy.deepcopy(idi01)
                    dist     = copy.deepcopy(dist01)
                    print('BEST: b12='+str(b12_best)+'   b23='+str(b23_best)+'   muo='+str(muo_best)+'   mlo='+str(mlo_best)+'   dist='+str(dis_best))

print('BEST OF ALL IS: b12='+str(b12_best)+'   b23='+str(b23_best)+'   muo='+str(muo_best)+'   mlo='+str(mlo_best)+'   dist='+str(dis_best)+'    idi='+str(idi_best))
tmp0   = (sis_best.M_of_t[0,:] - sis_best.M_ini[0]) / sisi0.M_puls
tmp1   = (sisi1.M_of_t[0,:,n2f] - sisi1.M_ini[0]) / sisi1.M_puls
plt.figure(1); plt.plot(tmp1[0:21],'k',linewidth=3);     plt.plot(tmp0[0:21],'r',linewidth=3);     plt.tight_layout(); plt.grid("on"); plt.show(block=False)
plt.savefig('PulseCalibration_20.png')
plt.figure(2); plt.plot(tmp1[0:201],'k',linewidth=3);    plt.plot(tmp0[0:201],'r',linewidth=3);    plt.tight_layout(); plt.grid("on"); plt.show(block=False)
plt.savefig('PulseCalibration_200.png')
plt.figure(3); plt.plot(tmp1[0:1000],'k',linewidth=3);   plt.plot(tmp0[0:1000],'r',linewidth=3);   plt.tight_layout(); plt.grid("on"); plt.show(block=False)
plt.savefig('PulseCalibration_1000.png')


                
