# Some test definitions, test themselves plus plotting
# Tests are the four calibration / evaluation tests suggested in the CDICE paper:
# 1) 100 GtC pulse to present atmosphere -> calibration of carbon cycle
# 2) 4xCO2 to pre-industrial atmosphere -> calibration of climate / temperature equations
# 3) 1pct CO2 -> transient climate response
# 4) CMIP5, based on concentrations and emissions, respectively -> gold standard test
#
# Coefficients for the climate / temperature equations are taken from Geoffrey et al. (2013),
# the multi-model-mean (MMM) as well as HadGem (high ECS) and GISS (low ECS), because functional
# form of equations is identical in DICE and Geoffrey at al. (2013)
#
# Coefficients for the carbon cylce (CC) are obtained from Pratyuksh, using Joos et al. (2013)
# parameterized data and a maximum norm over the first 100 years after the puls
#
# to use:
# import TestDefs
#
import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ClimDICE as cld

importlib.reload(cld)


#====================================================================================
#some short hands
#====================================================================================
#original DICE coefficients
Dt2x  = 3.1          #DICE climate equations, bug-fixed, default value of constant t2xco2 for 1 yr time step, as set in SetClimInt
Df2x  = 3.6813       #DICE climate equations, bug-fixed, default value of constant fco22x for 1 yr time step, as set in SetClimInt
Dc1   = 0.1005       #DICE climate equations, bug-fixed, default value of constant c1 for 1 yr time step, as set in SetClimInt
Dc2   = Df2x/Dt2x    #DICE climate equations, bug-fixed, default value of constant c2 for 1 yr time step, as set in SetClimInt
Dc3   = 0.088/0.1005 #DICE climate equations, bug-fixed, default value of constant c3 for 1 yr time step, as set in SetClimInt
Dc4   = 0.025/5.     #DICE climate equations, bug-fixed, default value of constant c4 for 1 yr time step, as set in SetClimInt
Db12  = 0.12/5.      #DICE carbon cycle equations, transfer coefficient from atmosphere to upper ocean, default value
Db23  = 0.007/5.     #DICE carbon cycle equations, transfer coefficient from upper ocean to deep ocean, default value
M1750 = np.array([588., 360., 1720.])   #DICE carbon cycle equations, equilibrium mass in the three reservoirs, default values
M1850 = M1750/276.*285.                 #DICE carbon cycle equations, eq. in the three reservoirs, re-scaled from DICE 276 ppm in 1750  to CMIP5 285 ppm in 1850
M2015 = np.array([851., 460., 1740.])
MPDEQ = M1750/M1750[0]*M2015[0]
T1750 = np.array([0.  , 0.    ]) 
T2015 = np.array([0.85, 0.0068])

#new DICE coefficients
Nt2x  = 3.25         #MMM from G13
Nf2x  = 3.45         #MMM from G13
Nc1   = 0.137        #MMM from G13
Nc2   = Nf2x/Nt2x    #MMM from Gq3
Nc3   = 0.73         #MMM from G13
Nc4   = 0.00689      #MMM from G13

Nb12  = 0.054        #fitted to J13 MMM, maximum norm, from Prat
Nb23  = 0.0082       #fitted to J13 MMM, maximum norm, from Prat

NME18 = np.array([607., 489., 1281.])  #J13 MMM, new PI equilibrium masses in 1850
NMIMM = np.array([851., 628., 1323.])  #MMM new initial mass in year 2015, from Prat

NMEME = np.array([607., 305.,  865.])  #J13 MESMO PI equilibrium masses in 1850
NMIME = np.array([851., 404.,  893.])  #MESMO new initial mass in year 2015, from Prat

NMELO = np.array([607., 600., 1385.])  #J13 LOVECLIM PI equilibrium masses in 1850
NMILO = np.array([851., 770., 1444.])  #LOVECLIM new initial mass in year 2015, from Prat

NME17 = NME18/285.*276.                #J13 MMM, new PI equilibrium masses, scaled to 1750

#test example related stuff
P100  = 100.
P5000 = 5000.
gtc2ppmco2 = 0.47  #conversion factor: 100GtC <-> 47ppm CO2 [Ref: Caption of Fig.3 in Dietz et al. (2020)]

#plotting stuff
fsl       = 8 #default font size for legends
coco_simo = [0.8, 0.8, 0.8]  #default colors for CMIP single models



#====================================================================================
#function definitions
#====================================================================================

#------------------------------------------------------------------------------------
#1) Benchmark test:
#   A) BenchMarkPuls():                           Joos et al. (2013) [J13] Benchmark
#   B) BenchMarkPulsMod():                        Modify DICE to better match Joos et al. (2013) [J13] Benchmark
#   C) BenchMark4xCO2():                          Geoffrey et al. (2013) [G13] Benchmark
#   D) BenchMark4xCO2Mod():                       Modified DICE to better match Geoffrey et al. (2013) [G13] Benchmark
#   E) BenchMarkTDEmiOrConc(CMIP='RCP45_EMI'):    CMIP benchmarks: CMIP5, one percent CO2, historical + rcp26 | rcp45 | rcp60 | rcp85
#   F) BenchMarkTDEmiOrConcMod(CMIP='RCP45_EMI'): Modified DICE to better match CMIP5 Benchmarks
#   G) Dietz et al. (2020) [D20]
#------------------------------------------------------------------------------------

# A) Puls test with Joos et al. 2013 bench mark
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMarkPuls():
    #for the original DICE with 5 year time step coefficients are hard-wired, so we set them to 'dummy 1.0' here in the pandas data frame
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label','simu']
    df1_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label']
    runs.append(['old','old',5,'emi_pyr','Puls',  1.0, 1.0,M1850,  1.0,  1.0, 1.0, 1.0,  1.0, P100,  M2015, T2015, 'dashed',2,25,[0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,NME18, Nf2x, Nt2x, Nc1, Nc3,  Nc4, P100,  NMIMM, T2015,  'solid',6,14,[1.0, 0.0, 0.0],'CDICE'])
    runs.append(['new','new',1, 'no'    ,'Puls', Nb12,Nb23,NME18, Nf2x, Nt2x, Nc1, Nc3,  Nc4,P5000,  NME18, T2015, 'dotted',3,20,[0.9, 0.7, 0.0],'CDICE, 5000 GtC in 1850'])
    runs.append(['new','new',1,'emi_pyr','Puls', 0.059,0.008 ,NMEME,Nf2x,Nt2x,Nc1, Nc3,  Nc4, P100,  NMIME, T2015, 'dotted',2,14,[1.0, 0.0, 0.0],'CDICE-MESMO'])
    runs.append(['new','new',1,'emi_pyr','Puls', 0.067,0.0095,NMELO,Nf2x,Nt2x,Nc1, Nc3,  Nc4, P100,  NMILO, T2015,'dashdot',2,14,[1.0, 0.0, 0.0],'CDICE-LOVECLIM'])
    #runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,NME18, Nf2x, Nt2x, Nc1, Nc3,  Nc4, P100,  M2015, T2015,  'solid',6, 8,[1.0, 0.0, 0.0],'CDICE'])
    BeMa.append(['Joos13','new',1, 'no' ,'Puls',  1.0, 1.0,M1850,  1.0,  1.0, 1.0, 1.0,  1.0, P100,  M2015, T2015,  'solid',6,10,[0.0, 0.0, 0.0], 'J13, MMM']) #specification for BM
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #J13 PD puls experiment emits Carbon such as to maintina PD CO2 of 389 ppm without puls; so diagnose emissions needed to keep atmospheric CO2 at level of 2015
    for i in range(len(runs)):
        #J13 PD puls experiment emits - besides the puls as such - Carbon such as to maintina PD CO2 of 389 ppm without the puls
        #thus we need to integrate twice:
        #first pass (jpass=0) to diagnose emissions needed to keep atmospheric CO2 at level of 2015
        #second pass (japss=1) to diagnose evolution of puls on top of '2015 background plus emissions from first pass to maintain 2015 background'
        for jpass in range(2):
            simu = cld.CCC()
            simu.SelClimInt(selint=df1['WhichClimInt'][i])     #old or new formulation of climate (temperature) integration
            simu.SelCCInt(selint=df1['WhichCCInt'][i])         #old or new formulation of carbon cycle integration
            if (df1['WhichCCInt'][i] == 'new'):
                simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))        #CC: carbon mass in reservoirs at equilibrium
                simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
                simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
            simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
            simu.ModIntCoef(nys=1000)                          #number of time steps
            #first pass: no pulse, just determine emissions to maintain atmospheric CO2 concentration of initial year
            if (jpass == 0):
                simu.SelProb(selprob='DM4MConst')              #fist pass: select problem 'DM4MConst', determine delta mass for mass to be constant
            #second pass: actual test, puls on top of emissions that maintain atmospheric CO2 concentration of initial year
            if (jpass == 1):
                simu.SelProb(selprob=df1['Problem'][i])        #second pass: select problem 'puls'
                simu.ModProb(M_puls=df1['M_puls'][i])          #modify the puls height
                if (df1['ModCarbEmi'][i] == 'emi_pyr'): simu.ModCarbEmi(emi_pyr=Emi_389ppm)  #add emissions to maintain 2015 CO2 concentration in absence of puls
            simu.ModProb(M_ini=df1['M_ini'][i])                #change initial mass in the three reservoirs
            simu.ModProb(T_ini=df1['T_ini'][i])                #change initial temperature in the two EB layers
            simu.TimeIntDICE()                                 #run the simulation
            #first pass: keep diagnosed emissions needed to fix the atmospheric mass of carbon at 851 GtC and associated temperature change (J13 plots difference to this change)
            if (jpass == 0):
                Emi_389ppm     = simu.GtC_Emi                  #diagnosed emissions needed to fix the atmospheric mass of carbon at 851 GtC
                Tatm_389ppm    = np.empty(simu.ndts)           
                Tatm_389ppm[:] = simu.T_of_t[0,:]              #temperature change associated with fixed carbon load of 851 GtC of the atmosphere
            #second pass: J13 plots deviation of temperature due to puls from temperature evolution when keeping carbon load fixed at 851 GtC
            if (jpass == 1):
                 if (df1['ModCarbEmi'][i] == 'emi_pyr'): simu.T_of_t[0,:] = simu.T_of_t[0,:]+simu.T_ini[0]-Tatm_389ppm[:]
                 
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    #as J13 does not supply an ocean tempature, use that space in simu.T_of_t[1,:] to store the tempearture evolution if atmospheric carbon mass is kept fixed at 851 GtC
    simu=cld.CCC();                             simu.ModIntCoef(dys=dfb['dys'][0]);       simu.ModIntCoef(nys=1000);
    simu.SelProb(selprob=dfb['Problem'][0]);    simu.ModProb(M_puls=dfb['M_puls'][0]);    simu.BenchMarkJoos()
    BeMa[0].append(simu);     runs.append(BeMa[0]);          df2=pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2



# B) Puls test with Joos et al. 2013 bench mark, but with modify DICE CC parameter values (notably b12 and M_eq) such as to better match J13
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMarkPulsMod():
    #coefficients of temperature equation of DICE and comparison with G13
    #c1 = 1/D2G13_C        D2G13_C     \in [4.7     | 7.3     | 8.6       ]   ---> c1     \in [0.116   | 0.137   | 0.213]    [min | MMM | max]
    #c3 = D2G13_gamma      D2G13_gamma \in [0.50    | 0.73    | 1.16      ]   ---> c3     \in [0.50    | 0.73    | 1.16 ]
    #                      D2G13_CO    \in [53.     | 106.    | 127. (317)]
    #c4 = c3/D2G13_C0      c3/D2G13_CO \in [0.00205 | 0.00689 | 0.0128    ]   ---> c4     \in [0.00205 | 0.00689 | 0.0128]
    #t2xco2 = 0.5*t4xco2   t4xco2      \in [4.1     | 6.5     | 8.5 (9.1) ]   ---> t2xco2 \in [2.05    | 3.25    | 4.25 (4.55)]
    #fco22x = 0.5*fco2x4   fco2x4      \in [5.1     | 6.9     | 8.5       ]   ---> t2xco2 \in [2.55    | 3.45    | 4.25 ]
    #coefficients of carbon cycle equation of DICE and comparison with G13
    #b12 = 0.12/5.  = 0.024
    #b23 = 0.007/5. = 0.0014
    #M1750 = np.array([588., 360., 1720.])
    #NME18 = np.array([607.,489.,1281.])    #J13 MMM, new PI equilibrium masses in 1850
    runs    =[]  #list of DICE runs for this figure / test
    BeMa    =[]  #list of BenchMarks for this figure / test
    df2_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label','simu']
    df1_keys=['WhichClimInt','WhichCCInt','dys','ModCarbEmi','Problem','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','M_puls','M_ini','T_ini','ls','lw','zo','rgb','label']
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12*3.,Nb23,NME18         ,Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015, 'dashed', 2,20,[0.0, 1.0, 1.0], 'b12*3'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12/3.,Nb23,NME18         ,Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015, 'dashed', 2,20,[0.0, 0.6, 0.6], 'b12/3'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23*3.,NME18         ,Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015, 'dotted', 2,20,[1.0, 0.0, 1.0], 'b23*3'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23/3.,NME18         ,Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015, 'dotted', 2,20,[0.6, 0.0, 0.6], 'b23/3'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,[607.,589.,1281.],Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015,'dashdot', 2,20,[0.0, 1.0, 0.0],'MUO+100'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,[607.,289.,1281.],Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015,'dashdot', 2,20,[0.0, 0.5, 0.0],'MUO-200'])
    runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,NME18            ,Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4,P100,NMIMM,T2015,  'solid', 6, 8,[1.0, 0.0, 0.0],'CDICE'])
    #runs.append(['new','new',1,'emi_pyr','Puls', Nb12,Nb23,np.array([607.,489./3.,1281.]),Nf2x,Nt2x,Nc1,Nc3,Nc4,P100,NMIMM,T2015,  'solid', 6, 8,[0.0, 0.0, 1.0],'CDICEMOD'])
    #runs.append(['new','new',1,'emi_pyr','Puls', Nb12/3.,Nb23,np.array([607.,489./3.,1281.]),Nf2x,Nt2x,Nc1,Nc3,Nc4,P100,NMIMM,T2015,  'solid', 6, 8,[0.0, 0.0, 1.0],'CDICEMOD'])
    #runs.append(['new','new',1,'emi_pyr','Puls', Nb12*3.,Nb23*3.,NME18      ,Nf2x,Nt2x,Nc1,Nc3,Nc4,P100,NMIMM,T2015,  'solid', 6, 8,[0.0, 0.0, 1.0],'CDICEMOD'])
    #runs.append(['new','new',1,'emi_pyr','Puls', Db12*2.5,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689,P100,M2015,T2015,'dashed',4,[1.0,0.0,1.0],'b12*3,b23*3,MUO=600,BEST'])
    BeMa.append(['Joos13','new',1, 'no' ,'Puls',0.024, 0.0014,M1850         ,Df2x,    Dt2x,   Dc1,   Dc3,   Dc4,P100,M2015,T2015,   'solid', 6, 6,[0.0, 0.0, 0.0], 'J13, MMM']) 
   
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        #J13 PD puls experiment emits - besides the puls as such - Carbon such as to maintina PD CO2 of 389 ppm without the puls
        #thus we need to integrate twice:
        #first pass (jpass=0) to diagnose emissions needed to keep atmospheric CO2 at level of 2015
        #second pass (japss=1) to diagnose evolution of puls on top of '2015 background plus emissions from first pass to maintain 2015 background'
        for jpass in range(2):
            simu = cld.CCC()
            simu.SelClimInt(selint=df1['WhichClimInt'][i])        #old or new formulation of climate (temperature) integration
            simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))        #CC: carbon mass in reservoirs at equilibrium
            simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
            simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
            simu.ModIntCoef(dys=df1['dys'][i])                    #time step 
            simu.ModIntCoef(nys=1000)                             #number of time steps
            #first pass: no pulse, just determine emissions to maintain atmospheric CO2 concentration of initial year
            if (jpass == 0):
                simu.SelProb(selprob='DM4MConst')              #fist pass: select problem 'DM4MConst', determine delta mass for mass to be constant
            #second pass: actual test, puls on top of emissions that maintain atmospheric CO2 concentration of initial year
            if (jpass == 1):
                simu.SelProb(selprob=df1['Problem'][i])        #second pass: select problem 'puls'
                simu.ModProb(M_puls=df1['M_puls'][i])          #modify the puls height
                if (df1['ModCarbEmi'][i] == 'emi_pyr'): simu.ModCarbEmi(emi_pyr=Emi_389ppm)  #add emissions to maintain 2015 CO2 concentration in absence of puls
            simu.ModProb(M_ini=df1['M_ini'][i])                #change initial mass in the three reservoirs
            simu.ModProb(T_ini=df1['T_ini'][i])                #change initial temperature in the two EB layers
            simu.TimeIntDICE()                                 #run the simulation
            #first pass: keep diagnosed emissions needed to fix the atmospheric mass of carbon at 851 GtC and associated temperature change (J13 plots difference to this change)
            if (jpass == 0):
                Emi_389ppm     = simu.GtC_Emi                  #diagnosed emissions needed to fix the atmospheric mass of carbon at 851 GtC
                Tatm_389ppm    = np.empty(simu.ndts)           
                Tatm_389ppm[:] = simu.T_of_t[0,:]              #temperature change associated with fixed carbon load of 851 GtC of the atmosphere
            #second pass: J13 plots deviation of temperature due to puls from temperature evolution when keeping carbon load fixed at 851 GtC
            if (jpass == 1):
                 if (df1['ModCarbEmi'][i] == 'emi_pyr'): simu.T_of_t[0,:] = simu.T_of_t[0,:]+simu.T_ini[0]-Tatm_389ppm[:]
                 
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    #as J13 does not supply an ocean tempature, use that space in simu.T_of_t[1,:] to store the tempearture evolution if atmospheric carbon mass is kept fixed at 851 GtC
    simu=cld.CCC();                             simu.ModIntCoef(dys=dfb['dys'][0]);       simu.ModIntCoef(nys=1000);
    simu.SelProb(selprob=dfb['Problem'][0]);    simu.ModProb(M_puls=dfb['M_puls'][0]);    simu.BenchMarkJoos()
    BeMa[0].append(simu);     runs.append(BeMa[0]);          df2=pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2


# C) 4xCO2 test with Geoffrey et al. 2013 bench mark
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMark4xCO2():
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    #df2_keys =  ['WhichClimInt','dys','Problem','M_eq',   'ls','lw','zo',           'rgb',    'label', 'simu'] #df key with simus
    #df1_keys =  ['WhichClimInt','dys','Problem','M_eq',   'ls','lw','zo',           'rgb',    'label']         #df keys without simus
    #runs.append([         'new',   1.,  'XxCO2', M1850, 'solid',   5, 10, [1.0, 0.0, 0.0], 'DICE, bug-fixed, 1yr step'])
    #runs.append([         'new',   5.,  'XxCO2', M1850, 'solid',   2, 10, [0.7, 0.3, 1.0], 'DICE, bug-fixed, 5yr step'])
    #runs.append([         'old',   1.,  'XxCO2', M1850,'dashed',   2, 10, [0.0, 0.0, 1.0], 'DICE, original, 1yr step'])
    #runs.append([         'old',   5.,  'XxCO2', M1850, 'solid',   2, 10, [0.0, 0.0, 1.0], 'DICE, original, 5yr step']) #specify DICE runs, one per line
    #BeMa.append([  'Geoffrey13',   1.,  'XxCO2', M1850, 'solid',   5, 10, [0.0, 0.0, 0.0], 'G13, MMM']) #specification for benchmark
    df2_keys =  ['WhichClimInt','dys','Problem','M_eq','fco22x','t2xco2',  'c1',  'c3',   'c4',    'ls','lw','zo', 'rgb','label','simu'] #df key with simus
    df1_keys =  ['WhichClimInt','dys','Problem','M_eq','fco22x','t2xco2',  'c1',  'c3',   'c4',    'ls','lw','zo', 'rgb','label']        #df key w/o simus
    runs.append([         'old',   5.,  'XxCO2', M1850,    Df2x,    Dt2x,   Dc1,   Dc3,    Dc4,'dashed',   2, 8, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
    #runs.append([         'new',   1.,  'XxCO2', M1850,    Df2x,    Dt2x,   Dc1,   Dc3,    Dc4, 'solid',   2, 8, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4, 'solid',   2,10, [1.0, 0.0, 0.0], 'CDICE']) #bug-fixed, G13 MMM coefs
    runs.append([         'new',   1.,  'XxCO2', M1850,    2.95,    4.55, 0.154,  0.55,0.00671, 'solid',   2,10, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    3.65,    2.15, 0.213,  1.16,0.00921, 'solid',   2,10, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R'])
    BeMa.append([  'Geoffrey13',   1.,  'XxCO2', M1850,    Df2x,    Dt2x,   Dc1,   Dc3,    Dc4, 'solid',   6, 6, [0.0, 0.0, 0.0], 'G13, MMM']) #BM specs.
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichClimInt'][i])     #old or new formulation of climate (temperature) integration
        if (df1['WhichClimInt'][i]=='new'): simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #clim. eq. coeff.
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.ModIntCoef(nys=1000)                          #number of years of integration
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    simu = cld.CCC();         simu.ModIntCoef(dys=dfb['dys'][0]);  simu.ModIntCoef(nys=1000);     simu.SelProb(selprob=df1['Problem'][0]);      simu.BenchMarkGeoffrey()
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2



# D) Modified DICE, to better match 4xCO2 test with Geoffrey et al. 2013 bench mark
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMark4xCO2Mod():
    #illustrate sensitivity of temperature / climate to individual parameters in the bug-fixed temperature equations
    #c1 = 1/D2G13_C        D2G13_C     \in [4.7     | 7.3     | 8.6       ]   ---> c1     \in [0.116   | 0.137   | 0.213]    [min | MMM | max]
    #c3 = D2G13_gamma      D2G13_gamma \in [0.50    | 0.73    | 1.16      ]   ---> c3     \in [0.50    | 0.73    | 1.16 ]
    #                      D2G13_CO    \in [53.     | 106.    | 127. (317)]
    #c4 = c3/D2G13_C0      c3/D2G13_CO \in [0.00205 | 0.00689 | 0.0128    ]   ---> c4     \in [0.00205 | 0.00689 | 0.0128]
    #t2xco2 = 0.5*t4xco2   t4xco2      \in [4.1     | 6.5     | 8.5 (9.1) ]   ---> t2xco2 \in [2.05    | 3.25    | 4.25 (4.55)]
    #fco22x = 0.5*fco2x4   fco2x4      \in [5.1     | 6.9     | 8.5       ]   ---> t2xco2 \in [2.55    | 3.45    | 4.25 ]
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys =  ['WhichClimInt','dys','Problem','M_eq','fco22x','t2xco2',  'c1',  'c3',   'c4',    'ls','lw','zo', 'rgb','label','simu'] #df key with simus
    df1_keys =  ['WhichClimInt','dys','Problem','M_eq','fco22x','t2xco2',  'c1',  'c3',   'c4',    'ls','lw','zo', 'rgb','label']        #df key w/o simus
    ####Modification based on G13 extreme cases
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4, 'solid',   2,  8, [1.0, 0.0, 0.0], 'CDICE']) #G13 MMM coefs.
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    2.05,   Nc1,   Nc3,    Nc4,'dashdot',  2, 10, [0.6, 0.0, 0.6], 't2xco2=2.05'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    4.25,   Nc1,   Nc3,    Nc4,'dashdot',  2, 10, [1.0, 0.2, 1.0], 't2xco2=4.25'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x, 0.116,   Nc3,    Nc4,'dashed',   2, 10, [0.8, 0.4, 0.0], 'c1=0.116'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x, 0.213,   Nc3,    Nc4,'dashed',   2, 10, [1.0, 0.7, 0.0], 'c1=0.213'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,  0.50,    Nc4, 'solid',   2, 10, [0.0, 0.5, 0.0], 'c3=0.50'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,  1.16,    Nc4, 'solid',   2, 10, [0.0, 1.0, 0.0], 'c3=1.16'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,0.00205,'dotted',   2, 10, [0.3, 0.8, 0.8], 'c4=0.00205'])
    ##runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,0.01280,'dotted',   2, 10, [0.5, 1.0, 1.0], 'c4=0.01280'])
    ####Modification based on multiples of coefficients
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4, 'solid',   2,  8, [1.0, 0.0, 0.0], 'CDICE']) #G13 MMM coefs.
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    1.0,    Nc1,   Nc3,    Nc4,'dashdot',  2, 10, [0.6, 0.0, 0.6], 't2xco2=1.0'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    6.0,    Nc1,   Nc3,    Nc4,'dashdot',  2, 10, [1.0, 0.2, 1.0], 't2xco2=6.0'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x, Nc1/3.,  Nc3,    Nc4,'dashed',   2, 10, [0.8, 0.4, 0.0], 'c1/3'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x, Nc1*3.,  Nc3,    Nc4,'dashed',   2, 10, [1.0, 0.7, 0.0], 'c1*3'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1, Nc3/3.,   Nc4, 'solid',   2, 10, [0.0, 0.5, 0.0], 'c3/3'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1, Nc3*3.,   Nc4, 'solid',   2, 10, [0.0, 1.0, 0.0], 'c3*3'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3, Nc4/3.,'dotted',   2, 10, [0.3, 0.8, 0.8], 'c4/3'])
    runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3, Nc4*3.,'dotted',   2, 10, [0.5, 1.0, 1.0], 'c4*3'])
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4, 'solid',   2,  8, [1.0, 0.0, 0.0], 'CDICE']) #G13 MMM coefs.
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    2.5,   Nc1,   Nc3,    Nc4, 'solid',   2,  8, [0.0, 1.0, 0.0], 'CDICE ECS25']) #G13 MMM coefs.
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    4.5,   Nc1,   Nc3,    Nc4, 'solid',   2,  8, [1.0, 0.0, 1.0], 'CDICE ECS45']) #G13 MMM coefs.
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    Nf2x,    4.55,   Nc1,   Nc3,    Nc4, 'dashed',   2,  8, [0.0, 0.0, 1.0], 'CDICE ECS455']) #G13 MMM coefs.
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    2.95,    4.55, 0.154,  0.55,0.00671, 'solid',   2,10, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    2.95,    4.55, 0.154,  0.55,0.00671,'dashed',   5, 10, [1.0, 0.4, 0.0], 'DICE, HadGEM2-ES'])
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    3.65,    2.15, 0.213,  1.16,0.00921,'dashed',   5, 10, [1.0, 0.8, 0.0], 'DICE, GISS-E2-R'])
    ###runs.append([         'new',   1.,  'XxCO2', M1850,    3.10,    2.05, 0.116,  0.65,0.00205,'dashed',   5, 10, [0.8, 0.4, 0.0], 'DICE, INM-CM4'])
    BeMa.append([  'Geoffrey13',   1.,  'XxCO2', M1850,    Nf2x,    Nt2x,   Nc1,   Nc3,    Nc4, 'solid',   6,  6, [0.0, 0.0, 0.0], 'G13, MMM']) #BM specs.
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichClimInt'][i])     #old or new formulation of climate (temperature) integration
        simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.ModIntCoef(nys=1000)                          #number of years of integration
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    simu = cld.CCC();         simu.ModIntCoef(dys=dfb['dys'][0]);  simu.ModIntCoef(nys=1000);     simu.SelProb(selprob=df1['Problem'][0]);      simu.BenchMarkGeoffrey()
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2




# E) CMIP benchmarks: CMIP5, one percent CO2, historical + rcp26 | rcp45 | rcp60 | rcp85
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMarkTDEmiOrConc(CMIP='RCP45_EMI'):
    #CMIP : any of
    #       C5HIST_EMI, RCP26_EMI, RCP45_EMI, RCP60_EMI, RCP85_EMI,
    #       C5PICT_CONC, C5HIST_CONC, RCP26_CONC, RCP45_CONC, RCP60_CONC, RCP85_CONC,
    #       1pctCO2
    #based on CMIP key word, what basic sort of problem (prb) is wanted?
    if (CMIP in ["C5HIST_EMI", "RCP26_EMI", "RCP45_EMI", "RCP60_EMI", "RCP85_EMI"]):                     prb="TD_emiCO2"
    if (CMIP in ["C5PICT_CONC", "C5HIST_CONC", "RCP26_CONC", "RCP45_CONC", "RCP60_CONC", "RCP85_CONC"]): prb="TD_ppmCO2"
    if (CMIP in ["1pctCO2"]):                                                                            prb="1pctCO2"
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label','simu'] #df keys w simus
    df1_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label'] #df keys w/o simus
    if (prb=="TD_emiCO2"):
        #runs.append([ 'old',1,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 20, [0.9, 0.7, 0.0], 'DICE, orig, 1yr'])
        #runs.append([ 'new',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 15, [0.0, 0.0, 1.0], 'DICE, bug fixed, 5yr'])
        #runs.append([ 'old',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 24, [1.0, 0.7, 0.0], 'DICE-2016, 5yr, Fex=0.3*FCO2'])
        #runs.append([ 'new',1,prb,CMIP,'DICE',0.0,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'dotted',  2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF, Fex=0.3*FCO2'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'dotted',  2, 20, [1.0, 0.0, 0.0], 'CDICE, Fex=0'])
        runs.append([ 'old',5,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 25, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   5, 20, [1.0, 0.0, 0.0], 'CDICE'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,Nf2x, 4.5, Nc1, Nc3,    Nc4, 'dotted',   3, 20, [1.0, 1.0, 0.0], 'CDICE ECS45'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,Nf2x, 2.5, Nc1, Nc3,    Nc4, 'dashed',   3, 20, [1.0, 1.0, 0.0], 'CDICE ECS25'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,np.array([607.,489./3.,1281.]),Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   5, 20, [0.0, 0.0, 1.0], 'CDICEMOD'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12/3.,Nb23,np.array([607.,489./3.,1281.]),Nf2x, Nt2x, Nc1/3., Nc3,    Nc4, 'solid',   5, 20, [0.0, 0.0, 1.0], 'CDICEMOD'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12*3.,Nb23*3.,NME18,Nf2x, Nt2x, Nc1*3., Nc3,    Nc4, 'solid',   5, 20, [0.0, 0.0, 1.0], 'CDICEMOD'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12/3.,Nb23,NME18,Nf2x, Nt2x, Nc1/3., Nc3,    Nc4, 'solid',   5, 20, [0.0, 0.0, 1.0], 'CDICEMOD'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12*3.,Nb23,NME18,Nf2x, Nt2x, Nc1*3., Nc3,    Nc4, 'solid',   5, 20, [0.0, 0.0, 1.0], 'CDICEMOD'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,2.95,4.55,0.154,0.55,0.00671, 'solid',   3, 12, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,3.65,2.15,0.213,1.16,0.00921, 'solid',   3, 12, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.059,0.008, NMEME,Nf2x, Nt2x, Nc1, Nc3, Nc4, 'dotted',  2, 20, [1.0, 0.0, 0.0], 'CDICE-MESMO'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.067,0.0095,NMELO,Nf2x, Nt2x, Nc1, Nc3, Nc4,'dashdot',  2, 20, [1.0, 0.0, 0.0], 'CDICE-LOVECLIM'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.059,0.008, NMEME,2.95,4.55,0.154,0.55,0.00671, 'dotted',   2, 12, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES-MESMO'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.067,0.0095,NMELO,2.95,4.55,0.154,0.55,0.00671,'dashdot',   2, 12, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES-LOVECLIM'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.059,0.008, NMEME,3.65,2.15,0.213,1.16,0.00921, 'dotted',   2, 12, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R-MESMO'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,0.067,0.0095,NMELO,3.65,2.15,0.213,1.16,0.00921,'dashdot',   2, 12, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R-LOVECLIMG'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,3.10,2.05,0.116,0.65,0.00205, 'solid',   2, 10, [0.0, 0.5, 0.0], 'CDICE-INM-CM4'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.
        ###for getting T_INI, 220404
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.11,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   5, 20, [1.0, 0.0, 0.0], 'CDICE'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',-0.12,Nb12,Nb23,NME18,2.95,4.55,0.154,0.55,0.00671, 'solid',   3, 12, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
        ###runs.append([ 'new',1,prb,CMIP,'Fac',0.57,Nb12,Nb23,NME18,3.65,2.15,0.213,1.16,0.00921, 'solid',   3, 12, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R'])
    if (prb=="TD_ppmCO2"):
        #runs.append([ 'old',1,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 20, [0.9, 0.7, 0.0], 'DICE, orig, 1yr'])
        #runs.append([ 'new',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 15, [0.0, 0.0, 1.0], 'DICE, bug fixed, 5yr'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE, bug fixed'])
        #runs.append([ 'old',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 24, [1.0, 0.7, 0.0], 'DICE-2016, 5yr, Fex=0.3*FCO2'])
        runs.append([ 'old',5,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 25, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
        #runs.append([ 'new',1,prb,CMIP,'DICE',0.0,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'dotted',  2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF, Fex=0.3*FCO2'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'dotted',  2, 20, [0.9, 0.4, 0.0], 'CDICE, Fex=0'])
        #runs.append([ 'new',1,prb,CMIP,'DICE',0.0,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'dashed', 2, 20, [0.9, 0.4, 0.0], 'CDICE, Fex=DICE'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,2.95,4.55,0.154,0.55,0.00671, 'solid',   2, 10, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,3.65,2.15,0.213,1.16,0.00921, 'solid',   2, 10, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Nb12,Nb23,NME18,3.10,2.05,0.116,0.65,0.00205, 'solid',   2, 10, [0.0, 0.5, 0.0], 'CDICE-INM-CM4'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.
    if (prb=="1pctCO2"):
        runs.append([ 'old',5,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 25, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18               ,Nf2x,   Nt2x,   Nc1,   Nc3,   Nc4, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18               ,2.95,4.55,0.154,0.55,0.00671, 'solid',   2, 10, [0.0, 0.8, 0.8], 'CDICE-HadGEM2-ES'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18               ,3.65,2.15,0.213,1.16,0.00921, 'solid',   2, 10, [0.0, 0.8, 0.0], 'CDICE-GISS-E2-R'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18               ,3.10,2.05,0.116,0.65,0.00205, 'solid',   2, 10, [0.0, 0.5, 0.0], 'CDICE-INM-CM4'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.

    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)

    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichDICEInt'][i])     #old or new formulation of climate (temperature) integration
        simu.SelCCInt(selint=df1['WhichDICEInt'][i])       #old or new formulation of carbon cycle integration
        #simu.ModIntCoef(nys=1000)                         #number of time steps
        if (df1['WhichDICEInt'][i]=='new'): 
            simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
            simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
        #print('i='+str(i)+'...c3='+str(simu.c3))
        simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))     #CC: carbon mass in reservoirs at equilibrium
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(M_ini=df1['M_eq'][i],FVar=df1['FVar'][i],FVarFac=df1['FVarFac'][i])   #change initial mass in the three reservoirs
        EorC = 'C'
        if (df1['Problem'][i]=='TD_emiCO2'): EorC = 'E'
        if np.any( (df1['Problem'][i]=='TD_emiCO2') or (df1['Problem'][i]=='TD_ppmCO2') ): simu.ModCarbEmi(emi_con_ext=df1['DataTag'][i],EorC=EorC)
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    print('BenchMarkTDEmiOrConc: prb is '+str(dfb['Problem'][0]))
    simu = cld.CCC();         simu.BenchMarkCMIP(prb=dfb['Problem'][0],CMIP=dfb['DataTag'][0])
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    #def BenchMarkCMIP(self,prb="TD_emiCO2",CMIP="RCP45_EMI",TalkTalk=1):

    return df2







# E-MIP) CMIP benchmarks: CMIP5, one percent CO2, historical + rcp26 | rcp45 | rcp60 | rcp85
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMarkTDEmiOrConcMIP(CMIP='RCP45_EMI'):
    #CMIP : any of
    #       C5HIST_EMI, RCP26_EMI, RCP45_EMI, RCP60_EMI, RCP85_EMI,
    #       C5PICT_CONC, C5HIST_CONC, RCP26_CONC, RCP45_CONC, RCP60_CONC, RCP85_CONC,
    #       1pctCO2
    #based on CMIP key word, what basic sort of problem (prb) is wanted?
    if (CMIP in ["C5HIST_EMI", "RCP26_EMI", "RCP45_EMI", "RCP60_EMI", "RCP85_EMI"]):                     prb="TD_emiCO2"
    if (CMIP in ["C5PICT_CONC", "C5HIST_CONC", "RCP26_CONC", "RCP45_CONC", "RCP60_CONC", "RCP85_CONC"]): prb="TD_ppmCO2"
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label','simu'] #df keys w simus
    df1_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label'] #df keys w/o simus
    if (prb=="TD_emiCO2"):
        #runs.append([ 'old',1,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 20, [0.9, 0.7, 0.0], 'DICE, orig, 1yr'])
        #runs.append([ 'new',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 15, [0.0, 0.0, 1.0], 'DICE, bug fixed, 5yr'])
        #runs.append([ 'old',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 24, [1.0, 0.7, 0.0], 'DICE-2016, 5yr, Fex=0.3*FCO2'])
        runs.append([ 'old',5,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 25, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
        runs.append([ 'new',1,prb,CMIP,'DICE',0.0,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'dotted',  2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF, Fex=0.3*FCO2'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.0,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'dotted',  2, 20, [1.0, 0.0, 0.0], 'CDICE, Fex=0'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,2.95,4.55,0.154,0.55,0.00671, 'solid',   2, 10, [0.0, 1.0, 1.0], 'CDICE-HadGEM2-ES'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,3.65,2.15,0.213,1.16,0.00921, 'solid',   2, 10, [0.0, 1.0, 0.0], 'CDICE-GISS-E2-R'])
        #runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,3.10,2.05,0.116,0.65,0.00205, 'solid',   2, 10, [0.0, 0.5, 0.0], 'CDICE-INM-CM4'])
        BeMa.append(['CMIP',1,prb,CMIP,'MIP',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.
    if (prb=="TD_ppmCO2"):
        #runs.append([ 'old',1,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 20, [0.9, 0.7, 0.0], 'DICE, orig, 1yr'])
        #runs.append([ 'new',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 15, [0.0, 0.0, 1.0], 'DICE, bug fixed, 5yr'])
        #runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE, bug fixed'])
        #runs.append([ 'old',5,prb,CMIP,'Fac',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 24, [1.0, 0.7, 0.0], 'DICE-2016, 5yr, Fex=0.3*FCO2'])
        runs.append([ 'old',5,prb,CMIP,'DICE',0.3,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4,'dashed',   2, 25, [0.0, 0.0, 1.0], 'DICE-2016, 5yr step'])
        runs.append([ 'new',1,prb,CMIP,'DICE',0.0,Db12,  Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'dotted',  2, 15, [0.7, 0.3, 1.0], 'DICE-2016-BF, Fex=0.3*FCO2'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.0,Nb12,Nb23,NME18,Nf2x, Nt2x, Nc1, Nc3,    Nc4, 'dotted',  2, 20, [1.0, 0.0, 0.0], 'CDICE, Fex=0'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,2.95,4.55,0.154,0.55,0.00671, 'solid',   2, 10, [0.0, 1.0, 1.0], 'CDICE-HadGEM2-ES'])
        runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,3.65,2.15,0.213,1.16,0.00921, 'solid',   2, 10, [0.0, 1.0, 0.0], 'CDICE-GISS-E2-R'])
        #runs.append([ 'new',1,prb,CMIP,'MIP',0.3,Nb12,Nb23,NME18,3.10,2.05,0.116,0.65,0.00205, 'solid',   2, 10, [0.0, 0.5, 0.0], 'CDICE-INM-CM4'])
        BeMa.append(['CMIP',1,prb,CMIP,'MIP',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.

    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)

    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichDICEInt'][i])     #old or new formulation of climate (temperature) integration
        simu.SelCCInt(selint=df1['WhichDICEInt'][i])       #old or new formulation of carbon cycle integration
        #simu.ModIntCoef(nys=1000)                         #number of time steps
        if (df1['WhichDICEInt'][i]=='new'): 
            simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
            simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
        #print('i='+str(i)+'...c3='+str(simu.c3))
        simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))     #CC: carbon mass in reservoirs at equilibrium
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(M_ini=df1['M_eq'][i],FVar=df1['FVar'][i],FVarFac=df1['FVarFac'][i])   #change initial mass in the three reservoirs
        EorC = 'C'
        if (df1['Problem'][i]=='TD_emiCO2'): EorC = 'E'
        if np.any( (df1['Problem'][i]=='TD_emiCO2') or (df1['Problem'][i]=='TD_ppmCO2') ): simu.ModCarbEmi(emi_con_ext=df1['DataTag'][i],EorC=EorC)
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    print('BenchMarkTDEmiOrConc: prb is '+str(dfb['Problem'][0]))
    simu = cld.CCC();         simu.BenchMarkCMIP(prb=dfb['Problem'][0],CMIP=dfb['DataTag'][0])
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    #def BenchMarkCMIP(self,prb="TD_emiCO2",CMIP="RCP45_EMI",TalkTalk=1):

    return df2



# F) CMIP benchmarks illustrating role of non-co2 forcing: CMIP5,  historical + rcp26 | rcp45 | rcp60 | rcp85
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def BenchMarkFextCMIP(CMIP='RCP45_EMI'):
    #CMIP : any of
    #       C5HIST_EMI, RCP26_EMI, RCP45_EMI, RCP60_EMI, RCP85_EMI,
    #       C5PICT_CONC, C5HIST_CONC, RCP26_CONC, RCP45_CONC, RCP60_CONC, RCP85_CONC,
    #       1pctCO2
    #based on CMIP key word, what basic sort of problem (prb) is wanted?
    if (CMIP in ["C5HIST_EMI", "RCP26_EMI", "RCP45_EMI", "RCP60_EMI", "RCP85_EMI"]):                     prb="TD_emiCO2"
    if (CMIP in ["C5PICT_CONC", "C5HIST_CONC", "RCP26_CONC", "RCP45_CONC", "RCP60_CONC", "RCP85_CONC"]): prb="TD_ppmCO2"
    if (CMIP in ["1pctCO2"]):                                                                            prb="1pctCO2"
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label','simu'] #df keys w simus
    df1_keys =  ['WhichDICEInt','dys','Problem','DataTag','FVar','FVarFac','b12','b23','M_eq','fco22x','t2xco2','c1','c3','c4','ls','lw','zo','rgb','label'] #df keys w/o simus
    if (prb=="TD_emiCO2"):
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',   2, 20, [0.5, 0.0, 0.5], 'CDICE, fex=0'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.35,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',  2, 20, [1.0, 0.0, 1.0], 'CDICE, fex=0.35'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.26,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',  2, 20, [1.0, 0.8, 0.0], 'CDICE, fex=0.26'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.
    if (prb=="TD_ppmCO2"):
        runs.append([ 'new',1,prb,CMIP,'Fac',0.3,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',   2, 20, [0.5, 0.0, 0.5], 'CDICE, fex=0'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.35,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',  2, 20, [1.0, 0.0, 1.0], 'CDICE, fex=0.35'])
        runs.append([ 'new',1,prb,CMIP,'Fac',0.26,Db12*3.0,Db23*3.0,[607.,600.,1772.],3.45,3.25,0.137,0.73,0.00689, 'solid',  2, 20, [1.0, 0.8, 0.0], 'CDICE, fex=0.26'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.
    if (prb=="1pctCO2"):
        runs.append([ 'new',1,prb,CMIP,'Fac',0.0,Nb12,Nb23,NME18               ,Nf2x,   Nt2x,   Nc1,   Nc3,   Nc4, 'solid',   4, 20, [1.0, 0.0, 0.0], 'CDICE'])
        BeMa.append(['CMIP',1,prb,CMIP,'Fac',0.0,Db12,   Db23,M1850            ,Df2x,   Dt2x,   Dc1,   Dc3,   Dc4, 'solid',   5, 10, [0.0, 0.0, 0.0], 'CMIP: '+CMIP]) #BM specs.

    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)

    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichDICEInt'][i])     #old or new formulation of climate (temperature) integration
        simu.SelCCInt(selint=df1['WhichDICEInt'][i])       #old or new formulation of carbon cycle integration
        #simu.ModIntCoef(nys=1000)                         #number of time steps
        if (df1['WhichDICEInt'][i]=='new'): 
            simu.ModIntCoef(b12=df1['b12'][i],b23=df1['b23'][i])  #CC: transfer coefficient atmosphere to upper ocean
            simu.ModIntCoef(fco22x=df1['fco22x'][i],t2xco2=df1['t2xco2'][i],c1=df1['c1'][i],c3=df1['c3'][i],c4=df1['c4'][i])   #climate equation coefficients
        #print('i='+str(i)+'...c3='+str(simu.c3))
        simu.ModIntCoef(M_eq=np.array(df1['M_eq'][i]))     #CC: carbon mass in reservoirs at equilibrium
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(M_ini=df1['M_eq'][i],FVar=df1['FVar'][i],FVarFac=df1['FVarFac'][i])   #change initial mass in the three reservoirs
        EorC = 'C'
        if (df1['Problem'][i]=='TD_emiCO2'): EorC = 'E'
        if np.any( (df1['Problem'][i]=='TD_emiCO2') or (df1['Problem'][i]=='TD_ppmCO2') ): simu.ModCarbEmi(emi_con_ext=df1['DataTag'][i],EorC=EorC)
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    print('BenchMarkTDEmiOrConc: prb is '+str(dfb['Problem'][0]))
    simu = cld.CCC();         simu.BenchMarkCMIP(prb=dfb['Problem'][0],CMIP=dfb['DataTag'][0])
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    #def BenchMarkCMIP(self,prb="TD_emiCO2",CMIP="RCP45_EMI",TalkTalk=1):

    return df2





# G) Dietz et al. 2020: 100GtC puls test into PD atmosphere (with Joos et al. 2013 bench mark)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def Dietz20Puls():
    runs     =  []  #list of DICE runs for this figure / test
    BeMa     =  []  #list of BenchMarks for this figure / test
    df2_keys =  ['WhichClimInt','dys','Problem','M_eq','M_puls','M_ini','T_ini',   'ls','lw',           'rgb',    'label', 'simu'] #df keys with simus
    df1_keys =  ['WhichClimInt','dys','Problem','M_eq','M_puls','M_ini','T_ini',   'ls','lw',           'rgb',    'label']         #df keys without simus
    runs.append([         'old',    5,   'Puls', M1850,    P100,  M1850, T1750, 'solid',   4, [0.0, 0.0, 1.0], 'old, 5yr, M1850, T1750']) #specify DICE runs
    runs.append([         'old',    5,   'Puls', M1850,    P100,  M2015, T1750, 'solid',   2, [0.0, 1.0, 0.0], 'old, 5yr, M2015, T1750']) #specify DICE runs
    runs.append([         'old',    5,   'Puls', M1850,    P100,  M1850, T2015, 'dashed',   2, [1.0, 0.0, 0.0], 'old, 5yr, M1850, T2015']) #specify DICE runs
    runs.append([         'old',    5,   'Puls', M1850,    P100,  M2015, T2015, 'dotted',   2, [0.0, 0.0, 0.0], 'old, 5yr, M2015, T2015']) #specify DICE runs
    BeMa.append([      'Joos13',    1,   'Puls', M1850,    P100,  M2015, T2015, 'solid',   1, [1.0, 1.0, 0.0],'Joos et al. 2013']) #specification for benchmark
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);     dfb=pd.DataFrame.from_records(BeMa, columns=df1_keys)
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.SelClimInt(selint=df1['WhichClimInt'][i])     #old or new formulation of climate (temperature) integration
        simu.ModIntCoef(dys=df1['dys'][i])                    #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(M_ini=df1['M_ini'][i])                #change initial mass in the three reservoirs
        simu.ModProb(T_ini=df1['T_ini'][i])                #change initial temperature in the two EB layers
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    #compute bench mark (Joos et al. 2013, 100 GtC puls), add result to bench mark list, wrap up everything in one data frame (all DICE results & bench mark)
    simu = cld.CCC();         simu.ModIntCoef(dys=dfb['dys'][0]);     simu.BenchMarkJoos()
    BeMa[0].append(simu);     runs.append(BeMa[0]);                df2 = pd.DataFrame.from_records(runs, columns=df2_keys)

    return df2




#------------------------------------------------------------------------------------
#2) Sensitivity and Scaling Tests:
#   A) TempScalXxCO2    : Scaling of temperature response to XxCO2, time evolution and equilibrium temperature
#   B) TempSensTiniPD   : Sensitivity to T_ini when letting PD equilibrate
#   C) TempSensECSPD    : Sensitivity to ECS when letting PD equilibrate
#   D) TempSensECS4xCO2 : Sensitivity to ECS when letting 4xCO2 on PI equilibrate
#   Z) ArbitTest        : For fooling around
#------------------------------------------------------------------------------------

# A) XxCO2 scaling of DICE response
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def TempScalXxCO2():
    runs     =  []  #list of DICE runs for this figure / test
    df2_keys =  ['WhichClimInt','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x',    'ls','lw',           'rgb',    'label', 'simu'] #df key with simus
    df1_keys =  ['WhichClimInt','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x',    'ls','lw',           'rgb',    'label']         #df keys w/o simus
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        0.0 , 'solid',   4, [0.0, 0.0, 0.0], '0.0  x F(2xCO2)']) #specify DICE runs
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        0.25, 'solid',   4, [0.0, 0.0, 0.6], '0.25 x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        0.5 , 'solid',   4, [0.0, 0.0, 1.0], '0.5  x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        0.75, 'solid',   4, [0.6, 0.0, 0.6], '0.75 x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        1.0 , 'solid',   4, [1.0, 0.0, 1.0], '1.0  x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        2.0 , 'solid',   4, [1.0, 0.6, 0.0], '2.0  x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        3.0 , 'solid',   4, [1.0, 0.0, 0.0], '3.0  x F(2xCO2)'])
    runs.append([         'new',    1, 5000,  'XxCO2', M1850,  M1850,  T2015,        4.0 , 'solid',   4, [0.6, 0.0, 0.0], '4.0  x F(2xCO2)'])

    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.ModIntCoef(nys=df1['nys'][i])                 #time step 
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(X_x_fco22x=df1['X_x_fco22x'][i])      #adjust forcing
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    
    return df2


# B) T_ini sensitivity, PD to equilibrium, DICE response
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def TempSensTiniPD():
    runs     =  []  #list of DICE runs for this figure / test
    df2_keys =  ['WhichClimInt','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x',    'ls','lw',           'rgb',    'label', 'simu'] #df key with simus
    df1_keys =  ['WhichClimInt','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x',    'ls','lw',           'rgb',    'label']         #df keys w/o simus
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,          T2015,0.0 , 'solid',   4, [0.0, 0.0, 0.0], '0.85 / 0.0068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[0.85,   0.68 ],0.0 , 'solid',   4, [0.0, 0.5, 0.0], '0.85 / 0.68']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[0.85,  0.068 ],0.0 , 'solid',   4, [0.0, 1.0, 0.0], '0.85 / 0.068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[0.85, 0.00068],0.0 , 'solid',   4, [0.0, 0.0, 1.0], '0.85 / 0.00068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[1.85,  0.0068],0.0 , 'solid',   4, [1.0, 0.0, 0.0], '1.85 / 0.0068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[0.45,  0.0068],0.0 , 'solid',   4, [1.0, 0.7, 0.0], '0.45 / 0.0068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[2.85,  0.0068],0.0 , 'solid',   4, [0.5, 0.0, 0.5], '2.85 / 0.0068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[2.85,   0.068],0.0 , 'solid',   4, [0.6, 0.0, 0.0], '2.85 / 0.068']) #specify DICE runs
    runs.append([         'new',    1,  500,  'XxCO2', M1850,  M1850,[2.85,    0.68],0.0 , 'solid',   4, [1.0, 0.0, 1.0], '2.85 / 0.68']) #specify DICE runs
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.ModIntCoef(nys=df1['nys'][i])                 #time step 
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        simu.ModProb(X_x_fco22x=df1['X_x_fco22x'][i])      #adjust forcing
        simu.ModProb(T_ini=np.array(df1['T_ini'][i]))      #adjust forcing
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    
    return df2


# C) ECS sensitivity, PD to equilibrium, DICE response
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def TempSensECSPD():
    return



# D) ECS sensitivity, 4xCO2 on PI to equilibrium, DICE response
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def TempSensECS4xCO2():
    return


# Z) ArbitTest, for fooling around
#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
def ArbitTest():
    runs     =  []  #list of DICE runs for this figure / test
    df2_keys =  ['WhichClimInt','IntCC','IntClim','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x','b12','b23',    'ls','lw',           'rgb',    'label', 'simu'] #w simus
    df1_keys =  ['WhichClimInt','IntCC','IntClim','dys','nys','Problem','M_eq','M_ini','T_ini','X_x_fco22x','b12','b23',    'ls','lw',           'rgb',    'label']   #w/o simus
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  360., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [1.0, 0.0, 0.0], 'UO 360'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  380., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [1.0, 0.8, 0.0], 'UO 380'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  400., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [0.8, 0.5, 0.0], 'UO 400'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  420., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [0.0, 1.0, 0.0], 'UO 420'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  440., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [0.0, 1.0, 1.0], 'UO 440'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  460., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [0.0, 0.0, 1.0], 'UO 460'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  480., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [0.5, 0.0, 0.5], 'UO 480'])
    runs.append(['new', 'true',   'true',    1,  500,   'Puls', [ 607.,  500., 1772.],  [ 607.,  360., 1772.], T2015, 0.0 ,0.12/5.,0.007/5., 'solid',   4, [1.0, 0.0, 1.0], 'UO 500'])
    
    #cast list of desired runs into pandas dataframe, for better transparancy of 'who is who' and 'what is what'
    df1=pd.DataFrame.from_records(runs, columns=df1_keys);
    #loop through all desired DICE runs, compute results, add results to existing list
    for i in range(len(runs)):
        simu = cld.CCC()
        simu.ModIntCoef(nys=df1['nys'][i])                 #time step 
        simu.ModIntCoef(dys=df1['dys'][i])                 #time step 
        simu.ModIntCoef(TalkTalk=0,b12=df1['b12'][i])                 #time step 
        simu.ModIntCoef(b23=df1['b23'][i])                 #time step 
        simu.ModIntCoef(M_eq=df1['M_eq'][i])                 #time step 
        simu.SelProb(selprob=df1['Problem'][i])            #make sure we solve the correct problem
        #simu.ModProb(X_x_fco22x=df1['X_x_fco22x'][i])      #adjust forcing
        simu.ModProb(T_ini=np.array(df1['T_ini'][i]))      #adjust initial temperature
        simu.ModProb(M_ini=np.array(df1['M_ini'][i]))      #adjust initial carbon mass
        #simu.ModProb(M_puls=np.array([100.0, 0.0, 0.0]))      #carbon puls
        #simu.ModCarbEmi(fix_GtC_per_year=np.array([0.2, 0.0, 0.0]))  #carbon emission per year to each reservoire
        simu.TimeIntDICE()                                 #run the simulation
        runs[i].append(simu)                               #add simulation result to appropriate run from list of runs
    df2 = pd.DataFrame.from_records(runs, columns=df2_keys)
    
    return df2






#def BenchMarkTDEmiOrConc(self,CMIP='RCP45_EMI'):
    
#------------------------------------------------------------------------------------
#3) plotting functions for the above tests
#   A) PlotDCO2PPM      : Default CO2 Plot: change in CO2 concentration in ppm, wrt to M_ini 
#   B) PlotDTempK       : Default Temperature Plot: change in temperature in K, wrt to T_ini 
#   C) PlotDForcWm2     : Default Forcing Plot: change in forcing in W/m2, wrt to F_of_t[t=0] 
#   D) PlotAbsCO2PPM    : Default CO2 Plot: absolute CO2 concentration in ppm
#   E) PlotAbsTempC     : Default Temperature Plot: absolute temperature in degree Celsius, assuming a global mean temperature of  13.75 degree Celsius in year 1900
#   F) PlotAbsForcWm2   : Default Forcing Plot: absolute forcing in W/m2
#   G) PlotPulsMassFrac : J13 BM, 100GtC Puls to PD, plot FRACTION OF PULS MASS remaining in atmosphere -> comparison with D20 (J13 data overplotted)
#   H) PlotPulsMassPPM  : J13 BM, 100GtC Puls to PD, plot PPM OF PULS MASS remaining in atmosphere -> comparison with J13 (J13 data overplotted)
#   I) PlotPulsTemp     : J13 BM, 100GtC Puls to PD, plot temperature evolution of atmosphere -> comparison with J13 (J13 data overplotted)
#   J) Plot4xCO2Temp    : G13 BM, 4xCO2 to PI, plot temperature evolution of atmosphere -> comparison with G13 (G13 data overplotted)
#   K) PlotTDMassPPM    : CMIP BM, any of historical | rcp | 1pctco2 -> comparison with CMIP output
#   L) PlotTDTemp       : CMIP BM, any of historical | rcp | 1pctco2 -> comparison with CMIP output
#   M) PlotResMassGtC   : CMIP hist+RCPs, plot mass in different reservoires
#   N) PlotEmiCMIPGtC   : CMIP hist+RCPs, plot carbon emissions
#   O) PlotConcCMIPppm  : CMIP hist+RCPs, plot CO2 concentrations
#   P) PlotForcWm2CMIP  : CMIP hist+RCPs, plot forcing
#   Q)
#
#

#------------------------------------------------------------------------------------

# A) Default CO2 Plot: change in CO2 concentration in ppm, wrt to M_ini 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotDCO2PPM(df2, axis_range=[0.,200.,-50.,50.], grid_yn='on', xstr='years', ystr='CO2 concentration change [ppm]', fout='PlotDCO2PPM.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        yplt = (sisi.M_of_t[0,:] - sisi.M_ini[0])*gtc2ppmco2
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# B) Default Temperature Plot: change in temperature in K, wrt to T_ini 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotDTempK(df2, axis_range=[0.,200.,-10.,10.], grid_yn='on', xstr='years', ystr='change in temperature [K] wrt T(t=0)', fout='PlotDTempK.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        yplt = (sisi.T_of_t[0,:] - sisi.T_ini[0])
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# C) Default Forcing Plot: change in forcing in W/m2, wrt to inital state (e.g. before carbon puls is applied)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotDForcWm2(df2, axis_range=[0.,200.,-1.,1.], grid_yn='on', xstr='years', ystr='change in radiative forcing [W/m2]', fout='PlotDForcWm2.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        #yplt = sisi.F_of_t[:] - sisi.F_of_t[0]
        yplt = sisi.F_of_t[:] - sisi.F_ini
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# D) Default CO2 Plot: absolute CO2 concentration in ppm
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotAbsCO2PPM(df2, axis_range=[0.,200.,-50.,50.], grid_yn='on', xstr='years', ystr='absolute CO2 concentration [ppm]', fout='PlotCO2PPM.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        yplt = sisi.M_of_t[0,:]*gtc2ppmco2
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# E) Default Temperature Plot: absolute temperature in degree Celsius, assuming a global mean temperature of  13.75 degree Celsius in year 1900
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotAbsTempC(df2, axis_range=[0.,200.,-10.,10.], grid_yn='on', xstr='years', ystr='temperature [deg C], 13.75 C in 1900', fout='PlotTempC.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        yplt = sisi.T_of_t[0,:] + 13.75
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# F) Default Forcing Plot: absolute forcing in W/m2
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotAbsForcWm2(df2, axis_range=[0.,200.,-5.,5.], grid_yn='on', xstr='years', ystr='radiative forcing [W/m2]', fout='PlotForcWm2.png'):
    plt.figure()
    nsimu=len(df2['simu'])
    for i in range(nsimu):
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        yplt = sisi.F_of_t[:]
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la)
    plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# G) 100GtC Puls benchmark, Joos et al. 2013: plot FRACTION OF PULS MASS remaining in atmosphere
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotPulsMassFrac(df2, axis_range=[0.,200.,0.,1.], grid_yn='on', xstr='years', ystr='fraction of GtC puls',\
                     fout='PlotPulsMassFrac.png', joos_yn='no', joos_indi='yes', joos_indi2='yes', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes', skip_simu=[]):
    plt.figure()
    nsimu = len(df2['simu'])-1                    #default: omit J13
    nati  = df2['simu'][nsimu].nati               #still get J13, nati = number of individual models with atmos.carb.mass
    natm  = df2['simu'][nsimu].natm               #still get J13, natm = number of multi-model-means (i.e. one...) with atmos.carb.mass
    natb  = df2['simu'][nsimu].natb               #still get J13, natb = number of Bern3D-LPJ special curves (four) with atmos.carb.mass (PD & PI, w & w/o clim. feedback)
    nirfa = df2['simu'][nsimu].nirfa              #still get J13: nirfa = nati+natm+natb = 16+1+4 = 21
    if (joos_yn == 'yes'): nsimu=len(df2['simu']) #add curve for J13
    for i in range(nsimu):
        if (i in skip_simu): continue
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    zo = df2['zo'][i];    la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0]
        i2na = np.where(xplt>100)
        if np.any((i<nsimu-1) or (joos_yn == 'no')):
            yplt = (sisi.M_of_t[0,:] - sisi.M_ini[0]) / sisi.M_puls
            plt.plot(xplt, yplt, color=coco, linestyle=ls, linewidth=lw, zorder=zo, label=la)
        if ((joos_yn == 'yes') and (i==nsimu-1)):
            #J13: multi-model-mean
            for j in range(nati,nati+natm):
                yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0]) / sisi.M_puls
                plt.plot(xplt, yplt, color=coco, linestyle=ls, linewidth=lw, zorder=zo, label=la)
            if (joos_indi == 'yes'): 
                #J13: individual models
                for j in range(0,nati):
                    yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0]) / sisi.M_puls
                    if (j==15): continue               #skip model TOTEM
                    if (j<3): yplt[xplt>100.]=np.nan   #first three models are full ESMs and have data only for up to about 100 years
                    if (j==0): plt.plot(xplt, yplt, color=coco_simo, linestyle='solid', linewidth=1, zorder=5, label='J13 single models')
                    if (j >0): plt.plot(xplt, yplt, color=coco_simo, linestyle='solid', linewidth=1, zorder=5)
                #J13: Bern3D-LPJ special curves
                if (joos_indi2 == 'yes'):
                    for j in range(nati+natm,nati+natm+natb):
                        idbs = nati+natm
                        if (j == idbs+0): coco=[0.3, 0.3, 0.3]; ls='dotted'; lw=2; la='J13, PI wcf';
                        if (j == idbs+1): coco=[0.7, 0.7, 0.7]; ls='dotted'; lw=2; la='J13, PI w/ocf';
                        if (j == idbs+2): coco=[0.3, 0.3, 0.3]; ls='dashed'; lw=2; la='J13, PD wcf';
                        if (j == idbs+3): coco=[0.7, 0.7, 0.7]; ls='dashed'; lw=2; la='J13, PD w/ocf';
                        yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0]) / sisi.M_puls
                        plt.plot(xplt, yplt, color=coco, linestyle=ls, linewidth=lw, zorder=15, label=la)

    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    #if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp, loc='upper right');
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')
    #plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# H) 100GtC Puls benchmark, Joos et al. 2013: plot PPM OF PULS MASS remaining in atmosphere
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotPulsMassPPM(df2, axis_range=[0.,200.,0.,50.], grid_yn='on', xstr='years', ystr='CO2 concentration change [ppm]',\
                    fout='PlotPulsMassPPM.png', joos_yn='no', joos_indi='yes', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes', skip_simu=[]):
    plt.figure()
    nsimu = len(df2['simu'])-1                    #default: omit J13
    nati  = df2['simu'][nsimu].nati               #still get J13, nati = number of individual models with atmos.carb.mass
    natm  = df2['simu'][nsimu].natm               #still get J13, natm = number of multi-model-means (i.e. one...) with atmos.carb.mass
    natb  = df2['simu'][nsimu].natb               #still get J13, natb = number of Bern3D-LPJ special curves (four) with atmos.carb.mass (PD & PI, w & w/o clim. feedback)
    nirfa = df2['simu'][nsimu].nirfa              #still get J13: nirfa = nati+natm+natb = 16+1+4 = 21
    if (joos_yn == 'yes'): nsimu=len(df2['simu']) #add curve for J13
    for i in range(nsimu):
        if (i in skip_simu): continue
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];     la = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        if np.any((i<nsimu-1) or (joos_yn == 'no')):
            yplt = (sisi.M_of_t[0,:] - sisi.M_ini[0])*gtc2ppmco2
            plt.plot(xplt, yplt, color=coco, linestyle=ls, zorder=zo, linewidth=lw, label=la)
        if ((joos_yn == 'yes') and (i==nsimu-1)):
            #J13: multi-model-mean
            for j in range(nati,nati+natm):
                yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0])*gtc2ppmco2
                plt.plot(xplt, yplt, color=coco, linestyle=ls, zorder=zo, linewidth=lw, label=la)
            if (joos_indi == 'yes'): 
                #J13: individual models
                for j in range(0,nati):
                    yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0])*gtc2ppmco2
                    if (j==0): plt.plot(xplt, yplt, color=coco_simo, linestyle='solid', linewidth=1, zorder=5, label='J13 single models')
                    if (j >0): plt.plot(xplt, yplt, color=coco_simo, linestyle='solid', linewidth=1, zorder=5)
                #J13: Bern3D-LPJ special curves
                for j in range(nati+natm,nati+natm+natb):
                    idbs = nati+natm
                    if (j == idbs+0): coco=[0.3, 0.3, 0.3]; ls='dotted'; lw=2; la='J13, PI wcf';
                    if (j == idbs+1): coco=[0.7, 0.7, 0.7]; ls='dotted'; lw=2; la='J13, PI w/ocf';
                    if (j == idbs+2): coco=[0.3, 0.3, 0.3]; ls='dashed'; lw=2; la='J13, PD wcf';
                    if (j == idbs+3): coco=[0.7, 0.7, 0.7]; ls='dashed'; lw=2; la='J13, PD w/ocf';
                    yplt = (sisi.M_of_t[0,:,j] - sisi.M_ini[0])*gtc2ppmco2
                    plt.plot(xplt, yplt, color=coco, linestyle=ls, zorder=10, linewidth=lw, label=la)

    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp, loc='upper right');
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')
    #plt.legend(); plt.xlabel(xstr); plt.ylabel(ystr); plt.axis(axis_range); plt.grid(grid_yn); plt.show(block=False); plt.savefig(fout,format='png')


# I) 100GtC Puls benchmark, Joos et al. 2013: plot temperature evolution of atmosphere
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotPulsTemp(df2, axis_range=[0.,200.,-1.,1.], grid_yn='on', xstr='years', ystr='temperature change [K]',\
                 fout='PlotPulsTemp.png', joos_yn='no', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes', skip_simu=[]):
    plt.figure()
    nsimu=len(df2['simu'])-1                         #omit curve for Joos et al. 2013 
    if (joos_yn == 'yes'): nsimu=len(df2['simu'])    #add curve for Joos et al. 2013 (default)
    for i in range(nsimu):
        if (i in skip_simu): continue
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls   = df2['ls'][i];    lw   = df2['lw'][i];    zo = df2['zo'][i];   la   = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        if (len(sisi.T_of_t.shape)>1):  yplt = sisi.T_of_t[0,:] - sisi.T_ini[0]  #DICE has 2D temperature array
        if (len(sisi.T_of_t.shape)==1): yplt = sisi.T_of_t[:]   - sisi.T_ini[0]  #Joos et al 2013 so far has 1D temperature array
        plt.plot(xplt,yplt,color=coco,linestyle=ls, zorder=zo, linewidth=lw, label=la)
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')


# J) 4xCO2 benchmark, Geoffrey et al. 2013: plot temperature evolution of atmosphere
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def Plot4xCO2Temp(df2,axis_range=[0.,200.,0.,10.],grid_yn='on',xstr='years',ystr='temperature change [K]',\
                  fout='Plot4xCO2Temp.png',geoff_yn='yes',geoff_indi='yes',fst=18,fsa=18,fsl=14,lsp=0.1,leg='yes',skip_simu=[]):
    plt.figure()
    nsimu=len(df2['simu'])-1                          #omit curve for Geoffrey et al. 2013 
    if (geoff_yn == 'yes'): nsimu=len(df2['simu'])    #add curve for Geoffrey et al. 2013 (default)
    for i in range(nsimu):
        if (i in skip_simu): continue
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
        xplt = sisi.n_year - sisi.n_year[0] 
        if (len(sisi.T_of_t.shape)==2): yplt = sisi.T_of_t[0,:] - sisi.T_ini[0]  #DICE has 2D temperature array
        #Geoffrey et al 2013: returns 3D temperature array [atmos./ocean, time, model]; multi-model-mean (MMM) is last entry
        if (len(sisi.T_of_t.shape)==3):
            nT    = sisi.T_of_t.shape[2]
            yplt  = sisi.T_of_t[0,:,nT-1] - sisi.T_ini[0]  #CMIP5 multi-model mean from Geoffrey et al. (2013) is last entry 
        plt.plot(xplt,yplt,color=coco,linestyle=ls, zorder=zo, linewidth=lw,label=la)
        #add single models from Geoffrey et al 2013 to plot
        if (geoff_indi == 'yes'):
            if (len(sisi.T_of_t.shape)==3):
                nT    = sisi.T_of_t.shape[2]
                for j in range(nT-1):
                    yplt  = sisi.T_of_t[0,:,j] - sisi.T_ini[0]  #individual CMIP5 models from Geoffrey et al. (2013)
                    if (j==0): plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', zorder=1, linewidth=1, label='G13 single models')
                    if (j>0):  plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', zorder=1, linewidth=1)
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn);
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')



#   K) PlotTDMassPPM    : CMIP BM, any of historical | rcp | 1pctco2 -> comparison with CMIP output
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotTDMassPPM(df2, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='CO2 concentration [ppm]',\
                  fout='PlotTDMassPPM.png', cmip_yn='yes', cmip_indi='yes', pm5pct='no',fst=18,fsa=18,fsl=14,lsp=0.1,leg='yes',skip_simu=[]):
    plt.figure()
    nsimu=len(df2['simu'])-1                         #omit curve for CMIP
    if (cmip_yn == 'yes'): nsimu=len(df2['simu'])    #add curve for CMIIP (default)
    for i in range(nsimu):
        if (i in skip_simu): continue
        dyrf = 1. if (df2['Problem'][i]=="1pctCO2") else 0.     #for 1pctCO2 we need to shift the time axis by its initial value
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
        xplt = sisi.n_year - dyrf*sisi.n_year[0]
        if (sisi.M_of_t.shape[0]==3): yplt = sisi.M_of_t[0,:]*gtc2ppmco2  #DICE has 2D mass array M_of_t[reservoir,time]
        #CMIP: returns 2D mass array M_of_t[time, model]; multi-model-mean (MMM) is last model entry
        if (sisi.M_of_t.shape[0]>3):
            nT    = sisi.M_of_t.shape[1]-1
            xplt  = sisi.n_year[:,nT] - dyrf*sisi.n_year[0,nT]
            yplt  = sisi.M_of_t[:,nT]*gtc2ppmco2  #multi-model mean from CMIP is last entry
            la    = 'CMIP, MMM'
            if (pm5pct=='yes'):
                plt.plot(xplt,yplt*1.05,color=coco,linestyle='dotted', linewidth=1, zorder=50)
                plt.plot(xplt,yplt*0.95,color=coco,linestyle='dotted', linewidth=1, zorder=50)
                plt.plot(xplt,yplt*1.20,color=coco,linestyle='dotted', linewidth=1, zorder=50)
                plt.plot(xplt,yplt*0.80,color=coco,linestyle='dotted', linewidth=1, zorder=50)
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la, zorder=zo)
        #add single models from CMIP
        if (cmip_indi=='yes'):
            if (sisi.M_of_t.shape[0]>3):
                nT    = sisi.M_of_t.shape[1]-1
                for j in range(nT):
                    xplt  = sisi.n_year[:,j] - dyrf*sisi.n_year[0,j]
                    yplt  = sisi.M_of_t[:,j]*gtc2ppmco2  #individual CMIP5 models
                    if (j==0): plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', linewidth=1, zorder=5, label='CMIP single models')
                    if (j>0):  plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', linewidth=1, zorder=5)
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')

#   L) PlotTDTemp       : CMIP BM, any of historical | rcp | 1pctco2 -> comparison with CMIP output
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotTDTemp(df2, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='temperature change [K]',\
               fout='PlotTDTemp.png', cmip_yn='yes', cmip_indi='yes', avyr=20,pad=1.08,fst=18,fsa=18,fsl=14,lsp=0.1,leg='yes', skip_simu=[]):
    plt.figure()
    nsimu=len(df2['simu'])-1                         #omit curve for CMIP
    if (cmip_yn == 'yes'): nsimu=len(df2['simu'])    #add curve for CMIIP (default)
    for i in range(nsimu):
        if (i in skip_simu): continue
        dyrf = 1. if (df2['Problem'][i]=="1pctCO2") else 0.     #for 1pctCO2 we need to shift the time axis by its initial value
        sisi = df2['simu'][i]
        coco = df2['rgb'][i];    ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
        avyrs = int(float(avyr)/sisi.dys)
        xplt = sisi.n_year - dyrf*sisi.n_year[0]
        if (sisi.T_of_t.shape[0]==2): yplt = sisi.T_of_t[0,:] - np.mean(sisi.T_of_t[0,0:avyrs])  #DICE has 2D temperature array T_of_t[layer,time]
        #CMIP: returns 2D temperature array T_of_t[time, model]; multi-model-mean (MMM) is last model entry
        if (sisi.T_of_t.shape[0]>2):
            nT    = sisi.T_of_t.shape[1]-1
            xplt  = sisi.n_year[:,nT] - dyrf*sisi.n_year[0,nT]
            yplt  = sisi.T_of_t[:,nT] - np.mean(sisi.T_of_t[0:avyrs,nT])  #multi-model mean from CMIP is last entry
            la    = 'CMIP, MMM'
        plt.plot(xplt,yplt,color=coco,linestyle=ls, linewidth=lw,label=la, zorder=zo)
        #print('i, yplt='+str(i)+'...'+str(yplt[0])+'...'+str(yplt[20]))
        #add single models from CMIP
        if (cmip_indi=='yes'):
            if (sisi.T_of_t.shape[0]>2):
                nT    = sisi.T_of_t.shape[1]-1
                for j in range(nT):
                    xplt  = sisi.n_year[:,j] - dyrf*sisi.n_year[0,j]
                    yplt  = sisi.T_of_t[:,j] - np.mean(sisi.T_of_t[0:avyrs,j])  #individual CMIP5 models 
                    if (j==0): plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', linewidth=1, zorder=5, label='CMIP single models')
                    if (j>0):  plt.plot(xplt,yplt,color=coco_simo,linestyle='solid', linewidth=1, zorder=5)
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(pad=pad); plt.show(block=False); plt.savefig(fout,format='png')

#   M) PlotResMassGtC  : CMIP hist+RCPs, plot mass in different reservoires
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotResMassGtC(df_26, df_45, df_60, df_85, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='Mass [GtC]',\
                  fout='PlotResMassGtC.png', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes',skip_simu=[]):
    plt.figure()
    for j in range(4):
        #if (j==2): continue #do not want df_60
        if (j==0): df2=df_26; coco=[0.0, 0.0, 1.0]; lala='RCP26'
        if (j==1): df2=df_45; coco=[0.2, 0.8, 0.2]; lala='RCP45'
        if (j==2): df2=df_60; coco=[1.0, 0.7, 0.0]; lala='RCP60'
        if (j==3): df2=df_85; coco=[1.0, 0.0, 0.0]; lala='RCP85'
        nsimu=len(df2['simu'])-1                         #omit curve for CMIP
        for i in range(nsimu):
            if (i in skip_simu): continue
            sisi = df2['simu'][i]
            #coco = df2['rgb'][i];
            #ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
            lw=2; zo=10; la=''
            xplt = sisi.n_year
            if (sisi.M_of_t.shape[0]==3):
                yplt0 = sisi.M_of_t[0,:]
                yplt1 = sisi.M_of_t[1,:]
                yplt2 = sisi.M_of_t[2,:]#-1000.
            plt.plot(xplt,yplt0,color=coco,linestyle='solid', linewidth=lw,label=lala, zorder=zo)
            plt.plot(xplt,yplt1,color=coco,linestyle='dashed', linewidth=lw,label=la, zorder=zo)
            plt.plot(xplt,yplt2,color=coco,linestyle='dotted', linewidth=lw,label=la, zorder=zo)
            #print('i,j='+str(i)+'...'+str(j))
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')


#   N) PlotEmiCMIPGtC  : CMIP hist+RCPs, plot carbon emissions
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotEmiCMIPGtC(df_26, df_45, df_60, df_85, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='CO2 Emissions [GtC / year]',\
                  fout='PlotEmiCMPIGtC.png', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes',skip_simu=[]):
    plt.figure()
    for j in range(4):
        #if (j==2): continue #do not want df_60
        if (j==0): df2=df_26; coco=[0.0, 0.0, 1.0]; lala='RCP26'
        if (j==1): df2=df_45; coco=[0.2, 0.8, 0.2]; lala='RCP45'
        if (j==2): df2=df_60; coco=[1.0, 0.7, 0.0]; lala='RCP60'
        if (j==3): df2=df_85; coco=[1.0, 0.0, 0.0]; lala='RCP85'
        nsimu=len(df2['simu'])-1                         #omit curve for CMIP
        for i in range(nsimu):
            if (i in skip_simu): continue
            sisi = df2['simu'][i]
            #coco = df2['rgb'][i];
            #ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
            lw=2; zo=10; la=''
            xplt = sisi.n_year
            yplt = sisi.GtC_Emi[:]
            plt.plot(xplt,yplt,color=coco,linestyle='solid', linewidth=lw,label=lala, zorder=zo)
            #print('i,j='+str(i)+'...'+str(j))
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')


#   O) PlotConcCMIPppm  : CMIP hist+RCPs, plot CO2 concentrations
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotConcCMIPppm(df_26, df_45, df_60, df_85, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='CO2 Concentration [ppm]',\
                  fout='PlotConcCMPIppm.png', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes',skip_simu=[]):
    plt.figure()
    for j in range(4):
        #if (j==2): continue #do not want df_60
        if (j==0): df2=df_26; coco=[0.0, 0.0, 1.0]; lala='RCP26'
        if (j==1): df2=df_45; coco=[0.2, 0.8, 0.2]; lala='RCP45'
        if (j==2): df2=df_60; coco=[1.0, 0.7, 0.0]; lala='RCP60'
        if (j==3): df2=df_85; coco=[1.0, 0.0, 0.0]; lala='RCP85'
        nsimu=len(df2['simu'])-1                         #omit curve for CMIP
        for i in range(nsimu):
            if (i in skip_simu): continue
            sisi = df2['simu'][i]
            #coco = df2['rgb'][i];
            #ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
            lw=2; zo=10; la=''
            xplt = sisi.n_year
            yplt = sisi.M_of_t[0,:]*gtc2ppmco2
            plt.plot(xplt,yplt,color=coco,linestyle='solid', linewidth=lw,label=lala, zorder=zo)
            #print('i,j='+str(i)+'...'+str(j))
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')


#   P) PlotForcWm2CMIP  : CMIP hist+RCPs, plot forcing
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def PlotForcWm2CMIP(df_26, df_45, df_60, df_85, axis_range=[0.,200.,0.,10.], grid_yn='on', xstr='years', ystr='Forcing [W / m2]',\
                    fout='PlotForcWm2CMPI.png', fst=18, fsa=18, fsl=14, lsp=0.1, leg='yes',skip_simu=[]):
    plt.figure()
    for j in range(4):
        #if (j==2): continue #do not want df_60
        if (j==0): df2=df_26; coco=[0.0, 0.0, 1.0]; lala='RCP26'
        if (j==1): df2=df_45; coco=[0.2, 0.8, 0.2]; lala='RCP45'
        if (j==2): df2=df_60; coco=[1.0, 0.7, 0.0]; lala='RCP60'
        if (j==3): df2=df_85; coco=[1.0, 0.0, 0.0]; lala='RCP85'
        nsimu=len(df2['simu'])-1                         #omit curve for CMIP
        for i in range(nsimu):
            if (i in skip_simu): continue
            sisi = df2['simu'][i]
            #coco = df2['rgb'][i];
            #ls = df2['ls'][i];    lw = df2['lw'][i];    zo = df2['zo'][i];   la = df2['label'][i]
            lw=2; zo=10; la=''
            xplt  = sisi.n_year
            yplt1 = sisi.F_of_t[:]
            yplt2 = sisi.FCO2_of_t[:]
            yplt3 = sisi.FVar_of_t[:]
            plt.plot(xplt,yplt1,color=coco,linestyle='solid', linewidth=lw,label=lala, zorder=zo)
            plt.plot(xplt,yplt2,color=coco,linestyle='dashed', linewidth=lw,label='', zorder=zo)
            plt.plot(xplt,yplt3,color=coco,linestyle='dotted', linewidth=lw,label='', zorder=zo)
            #print('i,j='+str(i)+'...'+str(j))
    if (leg == 'yes'): plt.legend(fontsize=fsl, labelspacing=lsp);
    plt.xlabel(xstr, fontsize=fsa); plt.ylabel(ystr, fontsize=fsa); plt.axis(axis_range); plt.grid(grid_yn); 
    plt.tick_params(axis='x', labelsize=fst);   plt.tick_params(axis='y', labelsize=fst)
    plt.tight_layout(); plt.show(block=False); plt.savefig(fout,format='png')

