# Reduced copy of TestDefs.py, containing only the 100 GtC pulse example, with
# the function call re-cast such that it can be used for carbon cycle calibration

import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ClimDICE as cld

importlib.reload(cld)

#Masses
M1750 = np.array([588., 360., 1720.])   #CDICE carbon cycle equations, equilibrium mass in the three reservoirs, default values
M1850 = M1750/276.*285.                 #CDICE carbon cycle equations, eq. in the three reservoirs, re-scaled from 276 ppm in 1750  to 285 ppm in 1850
M2015 = np.array([851., 460., 1740.])
MPDEQ = M1750/M1750[0]*M2015[0]
T1750 = np.array([0.  , 0.    ]) 
T2015 = np.array([0.85, 0.0068])

#CDICE coefficients
Nt2x  = 3.25         #MMM from G13
Nf2x  = 3.45         #MMM from G13
Nc1   = 0.137        #MMM from G13
Nc2   = Nf2x/Nt2x    #MMM from Gq3
Nc3   = 0.73         #MMM from G13
Nc4   = 0.00689      #MMM from G13

#pulse related stuff
P100  = 100.
gtc2ppmco2 = 0.47  #conversion factor: 100GtC <-> 47ppm CO2 [Ref: Caption of Fig.3 in Dietz et al. (2020)]

def BenchMarkPuls(Nb12 = 0.054 , Nb23 = 0.0082, NME18 = np.array([607., 489., 1281.])):
    #for the original DICE with 5 year time step coefficients are hard-wired, so we set them to 'dummy 1.0' here in the pandas data frame
    MCALI    = NME18/NME18[0]*M2015[0]
    #print('Nb12='+str(Nb12)+'    Nb23='+str(Nb23)+'   MCALI[0]='+str(MCALI[0])+'   MCALI[1]='+str(MCALI[1])+'   MCALI[2]='+str(MCALI[2]))
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label','simu']
    df1_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label']
    runs.append(['new','new',1,    'no' ,'Puls', Nb12,Nb23,MCALI, Nf2x, Nt2x, Nc1, Nc3,  Nc4, P100,  MCALI, T2015,  'solid',6,14,[1.0, 0.0, 0.0],'CDICE'])
    BeMa.append(['Joos13','new',1, 'no' ,'Puls',  1.0, 1.0,M1850,  1.0,  1.0, 1.0, 1.0,  1.0, P100,  M2015, T2015,  'solid',6,10,[0.0, 0.0, 0.0], 'J13, MMM']) #specification for BM
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #J13 PD puls experiment emits Carbon such as to maintina PD CO2 of 389 ppm without puls; so diagnose emissions needed to keep atmospheric CO2 at level of 2015
    for i in range(len(runs)):
        #For calibration, it is sufficient to examine a pulse to pre-industrial conditions in CDICE
        #This although J13 PD puls experiment emits - besides the puls as such - Carbon such as to maintina PD CO2 of 389 ppm without the puls
        #CDICE is not sensitive to the background atmosphere by construction, as long as it is in equilibrium (as such and if maintained via emissions)
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichClimInt'][i])     #old or new formulation of climate (temperature) integration
        simu.SelCCInt(selint=df1['WhichCCInt'][i])         #old or new formulation of carbon cycle integration
        if (df1['WhichCCInt'][i] == 'new'):
            simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))        #CC: carbon mass in reservoirs at equilibrium
            simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
            simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.ModIntCoef(nys=1000)                          #number of time steps
        simu.SelProb(selprob=df1['Problem'][i])        #second pass: select problem 'puls'
        simu.ModProb(M_puls=df1['M_puls'][i])          #modify the puls height
        simu.ModProb(M_ini=df1['M_ini'][i])                #change initial mass in the three reservoirs
        simu.ModProb(T_ini=df1['T_ini'][i])                #change initial temperature in the two EB layers
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    #as J13 does not supply an ocean tempature, use that space in simu.T_of_t[1,:] to store the tempearture evolution if atmospheric carbon mass is kept fixed at 851 GtC
    simu=cld.CCC();                             simu.ModIntCoef(dys=dfb['dys'][0]);       simu.ModIntCoef(nys=1000);
    simu.SelProb(selprob=dfb['Problem'][0]);    simu.ModProb(M_puls=dfb['M_puls'][0]);    simu.BenchMarkJoos()
    BeMa[0].append(simu);     runs.append(BeMa[0]);          df2=pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2

