# Python module (python3) to play with the climate part (temperature / climate plus carbon cycle) of DICE
#
# Basic idea is that the module is used from within TestDefs.py, where different climate specific tests are defined.
# Basic idea is, further, that the tests within TestDefs.py are accessed from Figs4Paper.py
# This 'front end' bundles tests in a manner that is useful for climate scientists to judge the performance of DICE (climate part)
#
# Note that this is all 'work in progress', a 'playground'.
# So there is definitely room for improvement.
# And although I try to document within the code, there may be inconsistencies or stuff that does not work properly.
#
#
# The module contains:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#    def __init__(self,TalkTalk=0):
#    def SelClimInt(self,selint='new',TalkTalk=0):                               ---> select integrator for the climate part of DICE (two coupled ODEs)
#    def SelCCInt(self,selint='new'):                                            ---> select integrator for the carbon cycle (CC) part of DICE (3x3 matrix)
#    def SelProb(self,selprob='Equilibrate',TalkTalk=0):                         ---> select what problem to set up
#    def ModProb(self,TalkTalk=0,**kwargs):                                      ---> modify the test problem
#    def ModCarbEmi(self,TalkTalk=0,**kwargs):                                   ---> modify carbon emissions
#    def ModIntCoef(self,TalkTalk=0, **kwargs):                                  ---> modify intetration coefficients
#    def ReMapTdEmiConc(self, EorC='N', TalkTalk=0, **kwargs):                   ---> re-map (time) time dependent emissions / concentrations
#    def TimeIntDICE(self,TalkTalk=1):                                           ---> integrator of DICE (climate / temperature and carbon cycle)
#    def LoadEmiAndConcData(self,Path2Files='../EmiAndConcData',TalkTalk=0):      ---> load emission and concentration data
#    def LoadTempData(self,Path2Dirs='../DataFromCMIP',TalkTalk=0):               ---> load temperature data, for benchmarking
#    def BenchMarkCMIP(self,prb="TD_emiCO2",CMIP="RCP45_EMI",TalkTalk=1):        ---> benchmark against CMIP5 data
#    def BenchMarkGeoffrey(self,TalkTalk=1):                                     ---> benchmark climate part of DICE against Geoffrey et al. (2013)
#    def BenchMarkJoos(self,TalkTalk=1):                                         ---> benchmark carbon cycle part of DICE against Joos et al. (2013)
#
#
# To use this module stand alone (caution, this could be a bit outdated!):
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  python3
#  import ClimDICE as cld
#  Temp = cld.Temperature()       #instantiate class Temperature, DICE temperature model
#  Temp.ProbSetUp()               #problem set up: start year & its initial temperature change of upper / lower layer wrt. 1850    [default: year 1850]
#  Temp.NewDICE()                 #compute temperature evolution using our new, adapted, bug-free (?) formulation of DICE2016 with arbitraty timestep
#
#  CC = cld.CarbonCycle()         #instantiate class CarbonCylce, DICE carbon cycle model
#  CC.ProbSetUp()                 #problem set up: start year & mass in atmos. / upper ocean / lower ocean in equilibrium(1750) & in start year [default: start-year 2015]
#  CC.TimeIntDICE()                   #compute carbon cycle evolution using our new, adapted, bug-free (?) formulation of DICE2016 with arbitraty timestep
#
#  import matplotlib.pyplot as plt
#  import importlib
#  importlib.reload(cld)
#  CC = cld.CarbonCycle()
#  CC.TimeIntDICE()
#  plt.plot(CC.n_year,(CC.M_of_t[0,:]-CC.M_ini[0])*CC.gtc2ppmco2)
#  plt.show(block=False)
#  plt.close("all")
#
#  to debug
#  del RawData
#  import importlib
#  importlib.reload(StruFu)
#  or
#  importlib.reload(sf)
#  if before you used
#  import StruFu as sf
#
#  Some more on calling...
#  import StruFu as sf
#  RawData = sf.RawDataCF("/home/folini/projects/acc_strufu/","vels")
#  RawData.Load(TalkTalk=0)
#  SelDat = sf.SelectData()             #instantiate class SelectData
#  SSData = SelDat.SubSample(RawData)   #use SubSample out of the SelectData class
#
#-----------------------------------------------------------------------------------
#
"""Climate Model Part of DICE"""
import numpy as np
import pandas as pd
import netCDF4 as nc
import glob
import copy
import re
import os
#import matplotlib.pyplot as plt


#=====================================================================================================================
class CCC:

    """Climate-Carbon-Cycle from DICE, original & corrected, plus benchmark tests"""

    #class attributes - each instance of the class has access to this same attribute
    #-------------------------------------------------------------------------------
    gtc2ppmco2      = 0.47  #conversion factor: 100GtC <-> 47ppm CO2 [Ref: Caption of Fig.3 in Dietz et al. (2020)]
    M_eq_DICE       = np.array([588., 360., 1720.])     #GtC in 3 reservoirs [atmos., upper & lower ocean] at equilibrium, year 1750 (numbers from gms-code)
    M_eq_DICE_1850  = M_eq_DICE/276.*285.               #GtC in 3 reservoirs [atmos., upper & lower ocean] at equilibrium, rescaled to atmosphere ppm in year 1850
    M_ini_DICE      = np.array([851., 460., 1740.])     #GtC in three reservoirs [atmos., upper ocean, lower ocean] in start year (2015)
    T_ini_DICE      = np.array([0.85, 0.0068])          #temperature change in start year (2015) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
    ppmCO2_eq       = M_eq_DICE[0]*gtc2ppmco2           #CO2 conc. of equilibrium carbon mass in atmos. in 1750; used to calculate forcing if atmos. conc. is prescribed
    ppmCO2_eq_1850  = M_eq_DICE_1850[0]*gtc2ppmco2      #CO2 conc. of equilibrium carbon mass in atmos. in 1850; used to calculate forcing if atmos. conc. is prescribed
    fex0_DICE       = 0.5                               #exogenous radiative forcing in DICE2016, hard wired to fex0+1/85*min(year-2015,1)*(fex1-fex0) for year >=2015
    fex1_DICE       = 1.0

    #init method or constructor
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def __init__(self,TalkTalk=0):

        """Initialize to: 100 GtC puls in 2015, corrected DICE2016 time integration, 5 yr timestep, 500 yr integration"""
        
        if (TalkTalk==1): print('init class ClimDICE')

        #Initialize class with default problem:
        #Let initial conditions (M_ini, T_ini) start to equilibrate over 100 years with time step of 1 year
        
        #time stepping & integration time
        self.dys       = 1.                                           #time step in years 
        self.nys       = 500.                                         #total integration time in years, end year minus start year
        self.ndts      = int(self.nys/self.dys)+1                     #number of time steps dys to cover total integration time, including start and end year
        #climate equation coefficients (including ECS / t2xco2 & fco22x): temperature of atmosphere / upper ocean & lower ocean; corrected DICE2016 values
        CCC.SelClimInt(self,selint='new')
        #carbon-cycle equation: transfer matrix between the three reservoirs: as in DICE2016 [tacitly assumes dys=5 year time step]
        CCC.SelCCInt(self,selint='new')
        #what problem to solve: 'Equilibrate' | 'Puls' | 'XxCO2' | '1pctCO2' | 'TD_ppmCO2' | 'TD_emiCO2' (use ModProb to further fine tune these default problems)
        CCC.SelProb(self,selprob='Equilibrate')
        #make sure for integrators and problem setup to be in sync with time step and years of integration
        CCC.ModIntCoef(self,dys=self.dys,nys=self.nys) 
        #CCC.LoadEmiAndConcData(self)                         #load emission and concentration data files !!!CALL HERE IN __init__ ONLY FOR TESTING PURPOSES!!!

        return


    #selection of climate integrator coefficients
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def SelClimInt(self,selint='new',TalkTalk=0):

        """Select Old (wrong) or New (corrected) Climate Integration"""

        #corrected DICE2016 values (and correspondingly corrected equations in the integrator itself)
        if (selint == 'new'):
            if (TalkTalk==1): print('new climate integrator selected: time step factored out, DICE coefficients appropriately corrected')
            self.WhichClimInt = 'new'                      #remember choice, old or new climate integrator
            self.fco22x       = 3.6813                     #Forcings of equilibrium CO2 doubling (Wm-2)
            self.t2xco2       = 3.1                        #Equilibrium Climate Sensitivity (equilibrium warming in Kelvin per doubling CO2)
            self.c1           = 0.1005                     #Climate eq. coef. for upper level, c1=1/C, C = eff. heat capacity of upper layer in G13   [c1] = [1/C] = m2*K/W/yr
            self.c2           = self.fco22x/self.t2xco2    #lambda parameter [lambda]=W/m2/K
            self.c3           = 0.088/self.c1              #Transfer coef. upper to lower stratum, c3 = gamma in G13                                  [c3] = [gamma] = W/m2/K
            self.c4           = 0.025/5.                   #Transfer coef. for lower level, c4=gamma/C0, C0 = eff. heat capac. of lower layer in G13  [c4] = [gamma/C0] = 1/yr
            self.D2G13_C      = 1./self.c1                 #translation of DICE coefficients to G13 coefficients: c1      -> C      [yr*W/m2/K]
            self.D2G13_gamma  = self.c3                    #translation of DICE coefficients to G13 coefficients: c3      -> gamma  [W/m2/K]
            self.D2G13_C0     = self.c3/self.c4            #translation of DICE coefficients to G13 coefficients: c3 & c4 -> C0     [yr*W/m2/K]

        #original DICE2016 values (and corresponding equations in the integrator itself)
        if (selint == 'old'):
            if (TalkTalk==1): print('old climate integrator selected: 5 yr time step hard wired (partially wrongly!) into coefficients')
            self.WhichClimInt = 'old'                      #remember choice, old or new climate integrator
            self.fco22x       = 3.6813                     #Forcings of equilibrium CO2 doubling (Wm-2)    /3.6813/
            self.t2xco2       = 3.1                        #Equilibrium temp impact (oC per doubling CO2)  / 3.1  /
            self.c1           = 0.1005                     #Climate equation coefficient for upper level   /0.1005/
            self.c2           = self.fco22x/self.t2xco2    #lambda parameter                               /1.1875/
            self.c3           = 0.088                      #Transfer coefficient upper to lower stratum    /0.088 /
            self.c4           = 0.025                      #Transfer coefficient for lower level           /0.025 /
            self.D2G13_C      = 1./self.c1                 #translation of DICE coefficients to G13 coefficients: c1      -> C
            self.D2G13_gamma  = self.c3                    #translation of DICE coefficients to G13 coefficients: c3      -> gamma
            self.D2G13_C0     = self.c3/self.c4            #translation of DICE coefficients to G13 coefficients: c3 & c4 -> C0
                                                           #translation of DICE coefficients to G13 coefficients: fco22x and t2xco2, thus lambda = fco22x/t2xco2 are the same
            
        return


    #selection of carbon-cycle transfer-matrix coefficients
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def SelCCInt(self,selint='new'):

        """Select Carbon Cycle transfer matrix [old: original DICE2016; new: time step issue fixed"""

        if (selint == 'old'):
            self.WhichCCInt = 'old'                           #remember choice
            self.M_eq = copy.deepcopy(CCC.M_eq_DICE)          #GtC in 3 reservoirs [atmos., upper & lower ocean] at equilibrium, year 1750 (numbers from gms-code)
            self.b12  = 0.12                                  #transfer coefficient from atmosphere to upper ocean; DICE value of 0.12 is for 5 year time step
            self.b23  = 0.007                                 #transfer coefficient from upper ocean to deep ocean; DICE value of 0.007 is for 5 year time step
            self.b11  = 1. - self.b12                         #mass conservation: what goes from atmosphere to upper ocean must leave atmosphere
            self.b21  = self.b12*self.M_eq[0]/self.M_eq[1]    #in equilibrium, must have M_atmos*'Atmos-to-UprOce' = M_UprOce*'UprOce-to-Atmos'
            self.b22  = 1. - self.b21 - self.b23              #mass conservation, what goes from upper ocean to either atmos. or lower ocean must leave upper ocean
            self.b32  = self.b23*self.M_eq[1]/self.M_eq[2]    #in equilibrium, must have M_UprOce*'UprOce-to-LwrOce' = M_LwrOce*'LwrOce-to-UprOce'
            self.b33  = 1. - self.b32                         #mass conservation: what goes from lower ocean to upper ocean must leave lower ocean
            self.b31  = 0.                                    #no direct transfer from lower ocean to atmosphere
            self.b13  = 0.                                    #no direct transfer from atmosphere to lower ocean
            self.A    = np.empty(3*3).reshape(3,3)            #carbon-cycle transfer matrix between three reservoirs [atmos., upper ocean, lower ocean]
            self.A[0,0]=self.b11;     self.A[0,1]=self.b21;     self.A[0,2]=self.b31
            self.A[1,0]=self.b12;     self.A[1,1]=self.b22;     self.A[1,2]=self.b32
            self.A[2,0]=self.b13;     self.A[2,1]=self.b23;     self.A[2,2]=self.b33
            #self.A         = np.array([[0.88,    0.196,    0.0],
            #                           [0.12,    0.797,    0.001465],
            #                           [0.0,     0.007,    0.998535]])

        if (selint == 'new'):
            self.WhichCCInt = 'new'                           #remember choice
            self.M_eq = copy.deepcopy(CCC.M_eq_DICE_1850)          #GtC in 3 reservoirs [atmos., upper & lower ocean] at equilibrium, year 1750 (numbers from gms-code)
            self.b12  = 0.12/5.*self.dys                      #transfer coefficient from atmosphere to upper ocean; DICE value of 0.12 is for 5 year time step
            self.b23  = 0.007/5.*self.dys                     #transfer coefficient from upper ocean to deep ocean; DICE value of 0.007 is for 5 year time step
            self.b11  = 1. - self.b12                         #mass conservation: what goes from atmosphere to upper ocean must leave atmosphere
            self.b21  = self.b12*self.M_eq[0]/self.M_eq[1]    #in equilibrium, must have M_atmos*'Atmos-to-UprOce' = M_UprOce*'UprOce-to-Atmos'
            self.b22  = 1. - self.b21 - self.b23              #mass conservation, what goes from upper ocean to either atmos. or lower ocean must leave upper ocean
            self.b32  = self.b23*self.M_eq[1]/self.M_eq[2]    #in equilibrium, must have M_UprOce*'UprOce-to-LwrOce' = M_LwrOce*'LwrOce-to-UprOce'
            self.b33  = 1. - self.b32                         #mass conservation: what goes from lower ocean to upper ocean must leave lower ocean
            self.b31  = 0.                                    #no direct transfer from lower ocean to atmosphere
            self.b13  = 0.                                    #no direct transfer from atmosphere to lower ocean
            self.A    = np.empty(3*3).reshape(3,3)            #carbon-cycle transfer matrix between three reservoirs [atmos., upper ocean, lower ocean]
            self.A[0,0]=self.b11;     self.A[0,1]=self.b21;     self.A[0,2]=self.b31
            self.A[1,0]=self.b12;     self.A[1,1]=self.b22;     self.A[1,2]=self.b32
            self.A[2,0]=self.b13;     self.A[2,1]=self.b23;     self.A[2,2]=self.b33
            #self.A         = np.array([[0.88,    0.196,    0.0],
            #                           [0.12,    0.797,    0.001465],
            #                           [0.0,     0.007,    0.998535]])

            
        return
    

    #selection of default problem
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def SelProb(self,selprob='Equilibrate',TalkTalk=0):

        """Select Basic Problem (use ModProb to further fine tune)"""

        #Let initial conditions M_ini & T_ini equilibrate; testing how equilibrium is reached and probably the most simple problem possible
        if (selprob == 'Equilibrate'):
            if (TalkTalk==1): print('Problem Selected: Let Equilibrate')
            self.WhichSelProb = 'Equilibrate'                          #remember choice
            #problem set up
            self.beg_yr     = 2015                              #year when integration begins
            self.end_yr     = self.beg_yr + self.nys            #year when integration ends
            self.M_ini      = copy.deepcopy(CCC.M_ini_DICE)     #GtC in three reservoirs [atmos., upper ocean, lower ocean] in start year (2015)
            self.T_ini      = copy.deepcopy(CCC.T_ini_DICE)     #temperature change in start year (2015) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                #100 GtC carbon puls to atmosphere in start year (2015)
            self.X_x_fco22x = 0.                                #constant forcing, X times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)   #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)   #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            #flags indicating what to integrat, what forcing
            self.IntCC      = 'true'     #integrate carbon-cycle ['true' | 'false']
            self.IntClim    = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2       = 'CC'       #CO2 Forcing based on carbon-cycle / associated change of carbon in atmosphere ['CC' | 'ppmCO2' | 'Xx2CO2']
            self.FVar       = 'None'     #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac    = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'

        #100 GtC puls into the atmosphere in 2015; M_ini and T_ini from DICE / gams-code; for testing 'carbon-cycle only' or 'climate-carbon-cycle'
        if (selprob == 'Puls'):
            if (TalkTalk==1): print('Problem Selected: Carbon Puls')
            self.WhichSelProb = 'Puls'                          #remember choice
            #problem set up
            self.beg_yr     = 2015                              #year when integration begins
            self.end_yr     = self.beg_yr + self.nys            #year when integration ends
            self.M_ini      = copy.deepcopy(CCC.M_ini_DICE)     #GtC in three reservoirs [atmos., upper ocean, lower ocean] in start year (2015)
            self.T_ini      = copy.deepcopy(CCC.T_ini_DICE)     #temperature change in start year (2015) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 100.                              #100 GtC carbon puls to atmosphere in start year (2015)
            self.X_x_fco22x = 0.                                #constant forcing, X times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)   #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)   #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            #flags indicating what to integrat, what forcing
            self.IntCC      = 'true'     #integrate carbon-cycle ['true' | 'false']
            self.IntClim    = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2       = 'CC'       #CO2 Forcing based on carbon-cycle / associated change of carbon in atmosphere ['CC' | 'ppmCO2' | 'Xx2CO2']
            self.FVar       = 'None'     #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac    = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'

        #Instantaneous quadroupling of CO2 wrt pre-industrial values; for testing 'climate part only'
        if (selprob == 'XxCO2'):
            if (TalkTalk==1): print('Problem Selected: 4xcO2')
            self.WhichSelProb = 'XxCO2'                          #remember choice
            #problem set up
            self.beg_yr     = 1850                               #year when integration begins
            self.end_yr     = self.beg_yr + self.nys             #year when integration ends
            self.M_ini      = np.array([0., 0., 0.])             #GtC in three reservoirs in start year (1850)
            self.T_ini      = np.array([0., 0.])                 #temperature change in start year (1850) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                 #no carbon puls to atmosphere in start year
            self.X_x_fco22x = 2.                                 #constant forcing, 2 times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)    #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)    #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                 #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            #flags indicating what to integrat, what forcing
            self.IntCC      = 'false'    #integrate carbon-cycle ['true' | 'false']
            self.IntClim    = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2       = 'Xx2CO2'   #CO2 Forcing as multiple of 'forcing from doubling pre-industrial CO2' ['CC' | 'ppmCO2' | 'Xx2CO2'] 
            self.FVar       = 'None'     #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac    = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'

        #CO2 concentration increasing at 1% per year for 140 years wrt pre-industrial values !!!!!!!!!! YET TO BE DONE !!!!!!!!!!
        if (selprob == '1pctCO2'):
            if (TalkTalk==1): print('Problem Selected: 1pctCO2')
            self.WhichSelProb = '1pctCO2'                        #remember choice
            #problem set up
            self.beg_yr     = 1850                               #year when integration begins
            self.end_yr     = self.beg_yr + self.nys             #year when integration ends
            self.M_ini      = copy.deepcopy(CCC.M_eq_DICE_1850)  #GtC in three reservoirs in start year (1850)
            self.T_ini      = np.array([0., 0.])                 #temperature change in start year (1850) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                 #no carbon puls to atmosphere in start year
            self.X_x_fco22x = 2.                                 #constant forcing, 2 times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)    #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.ppmCO2[0]  = copy.deepcopy(CCC.ppmCO2_eq_1850)       #CO2 concentration in 1850, equilibrium CO2 concentration from M_eq of DICE
            for i in range(1,self.ndts): self.ppmCO2[i]=self.ppmCO2[i-1]*np.power(1.01,self.dys)  #one percent increase of CO2 concentration each year
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)    #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                 #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            #flags indicating what to integrat, what forcing
            self.IntCC     = 'false'    #integrate carbon-cycle ['true' | 'false']
            self.IntClim   = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2      = 'ppmCO2'   #CO2 Forcing based on carbon-cycle / associated change of carbon in atmosphere ['CC' | 'ppmCO2' | 'Xx2CO2']
            self.FVar      = 'None'     #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac   = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'

        #pre-scribed, time-dependent CO2 concentrations in ppm !!!!!!!!!! YET TO BE DONE !!!!!!!!!!
        if (selprob == 'TD_ppmCO2'):
            if (TalkTalk==1): print('Problem Selected: Prescribed Time Dependent ppm CO2')
            self.WhichSelProb = 'TD_ppmCO2'                      #remember choice
            #problem set up
            self.beg_yr     = 1850                               #year when integration begins
            self.end_yr     = self.beg_yr + self.nys             #year when integration ends
            self.M_ini      = np.array([0., 0., 0.])             #GtC in three reservoirs in start year (1850)
            self.T_ini      = np.array([0., 0.])                 #temperature change in start year (1850) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                 #no carbon puls to atmosphere in start year
            self.X_x_fco22x = 0.                                 #constant forcing, 2 times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)    #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)    #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                 #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            CCC.LoadEmiAndConcData(self)                         #load emission and concentration data files
            self.ppmCO2     = CCC.ReMapTdEmiConc(self, EorC='C', in_val='RCP85_CONC',TalkTalk=2)
            #flags indicating what to integrat, what forcing
            self.IntCC   = 'false'    #integrate carbon-cycle ['true' | 'false']
            self.IntClim = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2    = 'ppmCO2'   #CO2 Forcing from prescribed CO2 concentration ['CC' | 'ppmCO2' | 'Xx2CO2'] 
            self.FVar    = 'Fac'      #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'

        #pre-scribed, time-dependent CO2 emissions in GtC !!!!!!!!!! YET TO BE DONE !!!!!!!!!!
        if (selprob == 'TD_emiCO2'):
            if (TalkTalk==1): print('Problem Selected: Prescribed Time Dependent GtCO2 emission')
            self.WhichSelProb = 'TD_emiCO2'                      #remember choice
            #problem set up
            CCC.LoadEmiAndConcData(self)                         #load emission and concentration data files
            self.beg_yr    = 1850                                #year when integration begins
            self.end_yr    = self.beg_yr + self.nys              #year when integration ends
            self.M_ini     = copy.deepcopy(CCC.M_eq_DICE_1850)   #GtC in three reservoirs in start year (1850)
            self.T_ini     = np.array([0., 0.])                  #temperature change in start year (1850) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                 #no carbon puls to atmosphere in start year
            self.X_x_fco22x = 0.                                 #constant forcing, 2 times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)    #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)    #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                 #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            CCC.LoadEmiAndConcData(self)                         #load emission and concentration data files
            self.GtC_Emi    = CCC.ReMapTdEmiConc(self, EorC='E', in_val='RCP85_EMI',TalkTalk=2)
            #flags indicating what to integrat, what forcing
            self.IntCC     = 'true'     #integrate carbon-cycle ['true' | 'false']
            self.IntClim   = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2      = 'CC'       #CO2 Forcing based on carbon-cycle / associated change of carbon in atmosphere ['CC' | 'ppmCO2' | 'Xx2CO2']
            self.FVar      = 'Fac'      #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac   = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'
            
        #diagnose carbon emission per time step, such as to keep M_ini[0] = constant; for testing
        if (selprob == 'DM4MConst'):
            if (TalkTalk==1): print('Problem Selected: Determine Annual Carbon Emission To Keep Atmospheric Carbon Constant')
            self.WhichSelProb = 'DM4MConst'                     #remember choice
            #problem set up
            self.beg_yr     = 2015                              #year when integration begins
            self.end_yr     = self.beg_yr + self.nys            #year when integration ends
            self.M_ini      = copy.deepcopy(CCC.M_ini_DICE)     #GtC in three reservoirs [atmos., upper ocean, lower ocean] in start year (2015)
            self.T_ini      = copy.deepcopy(CCC.T_ini_DICE)     #temperature change in start year (2015) wrt 1900 in two EB layers [atmos. & upper oce., lower oce.]
            self.M_puls     = 0.                                #no carbon puls to atmosphere in start year
            self.X_x_fco22x = 0.                                #constant forcing, X times that of fco22x (doubling of co2; fco22x is a coefficient in the solver)
            self.ppmCO2     = np.zeros(self.ndts,dtype=float)   #pre-scribed atmos. CO2 concentration [ppm], in each time step
            self.GtC_Emi    = np.zeros(self.ndts,dtype=float)   #pre-scribed carbon emission to atmosphere [GtC], in each time step
            self.Pct_Emi    = 0.                                #pre-scribed carbon emissions as percent of carbon already in atmosphere, in each time step
            #flags indicating what to integrat, what forcing
            self.IntCC      = 'true'     #integrate carbon-cycle ['true' | 'false']
            self.IntClim    = 'true'     #integrate climate (temperature) equation ['true' | 'false']
            self.FCO2       = 'CC'       #CO2 Forcing based on carbon-cycle / associated change of carbon in atmosphere ['CC' | 'ppmCO2' | 'Xx2CO2']
            self.FVar       = 'None'     #Non-CO2 forcings ['None' | 'DICE' | 'Fac' ]    ['DICE' = as hard wired in DICE2016] ['Fac' = constant factor FVarFac of CO2 forcing]
            self.FVarFac    = 0.         #Non-CO2 forcings equal to FVarFac*CO2 forcings if FVar='Fac'
            
        return
    

    #modify the problem set up
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def ModProb(self,TalkTalk=0,**kwargs):

        """Modify Problem SetUp """

        #**kwargs is one of (pairs of)
        # beg_yr_old / beg_yr_new : start year of integration
        # M_ini                   : GtC in each of the three reservoirse in start year of integration
        # M_puls                  : GtC puls to each of the three reservoirs in start year of integration
        # T_ini                   : inital temperature in each of two EB layers
        # IntCC                   : integrate Carbon Cylce 'true' or 'false'
        # IntClim                 : integrate climate / temperature 'true' or 'false'
        # X_x_fco22x              : multiple of frocing from '2 times CO2', fco22x
        #

        self.beg_yr_old = self.beg_yr

        #go through valid key-words, check what user desires
        for key in ('beg_yr', 'M_ini', 'M_puls', 'T_ini', 'IntCC', 'IntClim', 'X_x_fco22x', 'FVar', 'FVarFac'):
            if key in kwargs:
                if (TalkTalk==1): print('ModProb: changing '+str(key)+' from '+str(getattr(self,key))+' to '+str(kwargs[key]))
                setattr(self, key, kwargs[key])

        #if start year changed, adapt dependent quantities:
        if (self.beg_yr_old != self.beg_yr):
            #re-set begin and end year of integration
            self.end_yr = self.beg_yr + self.ndts*self.dys
            #re-compute time dependent carbon emissions

        return
    

    #modify the problem set up
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def ModCarbEmi(self,TalkTalk=0,**kwargs):

        """Modify Time Dependent Carbon Emissions for Carbon Cycle"""

        #**kwargs is one of
        # fix_GtC_per_year : fixed GtC/yr per reservoir each year, np.array([atmos, upper ocean, lower ocean])
        # fix_pct_per_year : fixed percent of each reservoir each year, np.array([atmos, upper ocean, lower ocean])
        # emi_pyr          : time series of emissions per time step; if pre-scribed time-series is too short, last value is copied to fill GtC_Emi[0,:] array
        # emi_con_ext      : time series of emissions or concentrations per time step from external file, for CMIP5 or CMIP6
        #                    choice of CMIP5 or CMIP6 via [RCP26 | RCP45 | RCP60 | RCP85 | SSP26 | SSP45 | SSP85]
        #                    automatically augmented by compatible 'historical' to cover range beg_yr to end_yr
        #                    all adapted for time step self.dys and retruned via self.GtC_Emi
        #                    if data from file is insufficient to cover date range beg_yr to end_yr, first | last values of available data is used to fill self.GtC_Emi
        #
        # Emissions are automatically mapped to current time step (dys), number of years (nys), start year [beg_yr]
        # Emissions read from file are, if necessary, kept constant beyond time range within file

        #what keyword to translate into acction?
        key = 'fix_GtC_per_year'
        if key in kwargs:
            tmp = kwargs[key]
            self.GtC_Emi[:] = tmp

        key = 'fix_pct_per_year'
        if key in kwargs: 
            tmp = kwargs[key]
            self.Pct_Emi = tmp

        key = 'emi_pyr'
        if key in kwargs: 
            tmp  = kwargs[key]
            ntmp = max(tmp.shape)
            nemi = max(self.GtC_Emi.shape)
            ni   = min(nemi,ntmp)
            for i in range(0,ni):
                self.GtC_Emi[i] = tmp[i]
            if (nemi > ntmp):
                for i in range(ni,nemi):
                    self.GtC_Emi[i] = tmp[ntmp-1]

        key = 'emi_con_ext'
        if key in kwargs: 
            tmp  = kwargs[key]
            #print('tmp='+str(tmp))
            EorC = 'C'
            if 'EorC' in kwargs: EorC = kwargs['EorC']
            CCC.LoadEmiAndConcData(self)                         #load emission and concentration data files
            if (EorC=='C'): self.ppmCO2  = CCC.ReMapTdEmiConc(self, EorC='C', in_val=tmp,TalkTalk=2)
            if (EorC=='E'): self.GtC_Emi = CCC.ReMapTdEmiConc(self, EorC='E', in_val=tmp,TalkTalk=2)

        return

    

    #modify the coefficients of the transfer matrix
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def ModIntCoef(self,TalkTalk=0, **kwargs):

        """Modify Coefficients of Integration Cosistently [Timestepping, Transfer Matrix, Climate Equations]"""

        #**kwargs is one of (pairs of)
        # dys               : time step for integration, in years
        # nys               : total number of years to integrate, in years
        # b12               : Carbon Cycle: transfer coefficient atmosphere to upper ocean
        # b23               : Carbon Cycle: transfer coefficient upper to deep ocean
        # M_eq              : Carbon Cycle: GtC in each of the three reservoirs in equilibrium
        # c1                : Temperature: c1 in new formulation of DICE; inverse of effective heat capacity of upper layer (see G13)
        # c2                : Temperature: c2 in new formulation of DICE; fco22x/t2xco2 = lambda = climate sensitivity parameter (see G13)
        # c3                : Temperature: c3 in new formulation of DICE; gamma = transfer coefficient from upper to lower level (see G13)
        # c4                : Temperature: c4 in new formulation of DICE; gamma/C0 with C0 the effective heat capacity of the lower layer (see G13)
        # fco22x            : Temperature: forcing from a doubling of CO2 (wrt pre-industrial conditions) in W/m2
        # t2xco2            : Temperature: ECS in Kelvin
        # D2G13_C           : Temperature: alternative way to set c1 = 1/D2G13_C
        # D2G13_gamma       : Temperature: alterntive way to set c3 = D2G13_gamma
        # D2G13_C0          : Temperature: alterntive way to set c4 = c3/D2G13_C0
        # If any of the D2G13_* is passed, they are evaluated in the following series: D2G13_C -> c1, D2G13_lambda -> c2, D2G13_gamma -> c3, D2G13_C0 -> c4
        # If, in addition, any c* are passed, they are evaluated subsequently and overwrite the D2G13_*

        #Transfer Matrix A:
        #From DICE2016 (gams-code):
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #* Flow paramaters
        #        b12      Carbon cycle transition matrix         /.12   /
        #        b23      Carbon cycle transition matrix         /0.007 /
        #* Parameters for long-run consistency of carbon cycle
        #        b11 = 1 - b12;
        #        b21 = b12*MATEQ/MUEQ;
        #        b22 = 1 - b21 - b23;
        #        b32 = b23*mueq/mleq;
        #        b33 = 1 - b32 ;
        #
        #Our insight:
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #*We may change b12 and / or b23 
        #*We may change the time step from dys_old to dys_new, upon which 
        #        b12 -> b12*dys_new/dys_old
        #        b23 -> b23*dys_new/dys_old
        #*We may change M_eq (MATEQ, MUEQ, MLEQ), the (assumed!) mass of carbon in the three reservoirs at equilibrium
        #*Then re-compute all coefficients using the above relations
        
        #save current settings - if modified we may need the old values later
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #time stepping
        self.dys_old          = self.dys
        self.nys_old          = self.nys
        self.ndts_old         = self.ndts
        #time dependent input
        self.GtC_Emi_old      = self.GtC_Emi
        self.ppmCO2_old       = self.ppmCO2
        #carbon cycle
        self.A_old            = self.A
        self.b12_old          = self.b12
        self.b23_old          = self.b23
        self.M_eq_old         = self.M_eq
        #temperature equation
        self.fco22x_old       = self.fco22x
        self.t2xco2_old       = self.t2xco2
        self.c1_old           = self.c1
        self.c2_old           = self.c2
        self.c3_old           = self.c3
        self.c4_old           = self.c4
        #alternative expressions for temperature equation coefficients; if c* and D2G13* are provided, c* overwrite D2G13*
        self.D2G13_C_old      = self.D2G13_C
        self.D2G13_gamma_old  = self.D2G13_gamma
        self.D2G13_C0_old     = self.D2G13_C0

        #go through valid key-words, check what user desires
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        for key in ('dys', 'nys', 'b12', 'b23','M_eq', 'fco22x', 't2xco2', 'c1', 'c3', 'c4', 'D2G13_C', 'D2G13_gamma', 'D2G13_C0'):
            if key in kwargs:
                if (TalkTalk==1): print('ModIntCoef: changing '+str(key)+' from '+str(getattr(self,key))+' to '+str(kwargs[key]))
                setattr(self, key, kwargs[key])

        #Any changes to temperature equation coefficients?
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #rules of precendence / overwriting:
        #  changes to c2 only via changes to fco22x and / or t2xco2
        #  changes to c1, c3, or c4 overwrite changes via D2G13 ---> accept changes from D2G13* only "if c*_old == c*"
        if np.any((self.fco22x != self.fco22x_old) or (self.t2xco2 != self.t2xco2_old)):
            self.c2 = self.fco22x/self.t2xco2
        if (self.c1 == self.c1_old):
            if (self.D2G13_C != self.D2G13_C_old): self.c1 = 1./self.D2G13_C
        if (self.c3 == self.c3_old): 
            if (self.D2G13_gamma != self.D2G13_gamma_old): self.c3 = self.D2G13_gamma
        if (self.c4 == self.c4_old):
            if np.any((self.D2G13_gamma != self.D2G13_gamma_old) or (self.D2G13_C0 != self.D2G13_C0_old)): self.c4 = self.c3/self.D2G13_C0
        #c* all updated by now (if uptdated at all...), make sure D2G13* have correct, corresponding values
        self.D2G13_C      = 1./self.c1        #translation of DICE coefficients to G13 coefficients: c1      -> C
        self.D2G13_gamma  = self.c3           #translation of DICE coefficients to G13 coefficients: c3      -> gamma
        self.D2G13_C0     = self.c3/self.c4   #translation of DICE coefficients to G13 coefficients: c3 & c4 -> C0
        if (TalkTalk==1):
            print('fco22x new / old : '+str(self.fco22x)+' / '+str(self.fco22x_old))
            print('t2xco2 new / old : '+str(self.t2xco2)+' / '+str(self.t2xco2_old))
            print('    c1 new / old : '+str(self.c1)+' / '+str(self.c1_old))
            print('    c2 new / old : '+str(self.c2)+' / '+str(self.c2_old))
            print('    c3 new / old : '+str(self.c3)+' / '+str(self.c3_old))
            print('    c4 new / old : '+str(self.c4)+' / '+str(self.c4_old))

        #Any changes to time stepping? 
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #compute ratio of new to old time step if time step changed, set to 1 else
        self.dys_new2old = self.dys/self.dys_old if (self.dys != self.dys_old) else 1.
        
        #if time step or number of years of integration changed, need to adapt:
        #number of time steps, array containing time dependent emissions, transfer matrix
        if np.any((self.dys != self.dys_old) or (self.nys != self.nys_old)):
            #re-compute number of time steps dys needed to cover a total of nys of integration
            self.ndts_old    = self.ndts
            self.ndts        = int(self.nys/self.dys)+1
            self.end_yr      = self.beg_yr + self.nys
            self.GtC_Emi_new = CCC.ReMapTdEmiConc(self, EorC='E', in_val=self.GtC_Emi, in_dys=self.dys_old, in_ndts=self.ndts_old, out_dys=self.dys, out_ndts=self.ndts)
            #blabla = CCC.ReMapTdEmi(self, in_emi=self.GtC_Emi, in_dys=self.dys_old, in_ndts=self.ndts_old, out_dys=self.dys, out_ndts=self.ndts)
            self.GtC_Emi     = self.GtC_Emi_new            
        
        #Any changes to carbon cycle coefficients?
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #if there are changes to either time step, b12, b23, or M_eq:
        #re-compute coefficients of transfer matrix and re-fill matrix
        if np.any((self.dys != self.dys_old) or (self.b12 != self.b12_old) or (self.b23 != self.b23_old) or (self.M_eq != self.M_eq_old)):
            if (self.WhichCCInt == 'new'):
                self.b12 = self.b12*self.dys_new2old
                self.b23 = self.b23*self.dys_new2old
            self.b11 = 1. - self.b12
            self.b21 = self.b12*self.M_eq[0]/self.M_eq[1]
            self.b22 = 1. - self.b21 - self.b23
            self.b32 = self.b23*self.M_eq[1]/self.M_eq[2]
            self.b33 = 1. - self.b32
            self.b31 = 0.
            self.b13 = 0.
            self.A[0,0]=self.b11;     self.A[0,1]=self.b21;     self.A[0,2]=self.b31
            self.A[1,0]=self.b12;     self.A[1,1]=self.b22;     self.A[1,2]=self.b32
            self.A[2,0]=self.b13;     self.A[2,1]=self.b23;     self.A[2,2]=self.b33

        #self.dys  = kwargs.get('dys')

        return 


    #Remap time dependent emission or concentration data from one time range & discretization to another time range & discretization
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def ReMapTdEmiConc(self, EorC='N', TalkTalk=0, **kwargs):

        """Remap time dependent emission or concentration data from one time range & discretization to another time range & discretization"""

        #keywords:
        #'in_val'     :source of data to be remapped;             defaults to copy of self.GtC_Emi (EorC='E') or self.ppmCO2 (EorC='C'); data from file if in_val=='RCP45'  etc.
        #'in_dys'     :time step of incoming data;                defaults to copy of self.dys or is 'guessed from data' if in_val points to 'data from file';
        #'in_ndts'    :number of time steps of incoming data;     defaults to copy of self.ndts or is 'guessed from data' if in_val points to 'data from file';
        #'in_beg_yr'  :start year of incoming data;               defaults to copy of self.beg_yr or is 'guessed from data' if in_val points to 'data from file';
        #'out_dys'    :time step of outgoing data;                defaults to copy of self.dys
        #'out_ndts'   :number of time steps of outgoing data;     defaults to copy of self.ndts
        #'out_beg_yr' :start year of outgoing data;               defaults to copy of self.beg_yr
        #
        #output variable: re-mapped, time dependent emissions
        #'out_val'    :where remapped data goes to;               new array, np.empty(self.out_ndts,dtype=float)

        #check for valid selection of what is to be remapped:
        #  emissions ('EorC'=='E', respect time integrated emission, i.e. in_val*in_dys = out_val*out_dys)
        #  concentrations ('EorC'=='C', use linear interpolation in time)
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if ((EorC != 'E') and (EorC != 'C')):
            print('!!!WARNING!!! NO VALID SELECTION IN ReMapTdEmiConc!!! ASSUMING EMISSION REMAPPING, EorC=E...')
            EorC = 'E'

        #assigne default input and output values, modify according to key words, set up derived quantities
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #default values for input and output data, may all be modified below depending on kwargs, and some short hands
        if (EorC=='E'): self.in_val = np.copy(self.GtC_Emi)          #input data for remapping; maybe modified below via kwargs; 'data from file' if type(in_val)==str
        if (EorC=='C'): self.in_val = np.copy(self.ppmCO2)           #input data for remapping; maybe modified below via kwargs; 'data from file' if type(in_val)==str
        self.in_dys     = np.copy(self.dys)                          #input time step
        self.in_ndts    = np.copy(self.ndts)                         #input number of time steps
        self.in_beg_yr  = np.copy(self.beg_yr)                       #input start year
        self.in_end_yr  = np.copy(self.end_yr)                       #input end year 
        self.out_dys    = np.copy(self.dys)                          #output time step
        self.out_ndts   = np.copy(self.ndts)                         #output number of time steps
        self.out_beg_yr = np.copy(self.beg_yr)                       #output start year
        self.out_end_yr = np.copy(self.end_yr)                       #output end year
        self.out_val    = np.empty(self.out_ndts,dtype=float)        #newly defined: output array to hold re-mapped data
        
        #modify default assignments based on **kwargs
        for key in ('in_val', 'in_dys', 'in_ndts', 'in_beg_yr', 'out_dys', 'out_ndts', 'out_beg_yr'):
            if key in kwargs:
                if (TalkTalk==1): print('ReMapTdEmiConc: changing '+str(key)+' from '+str(getattr(self,key))+' to '+str(kwargs[key]))
                setattr(self, key, kwargs[key])

        #modify assignements again if key word 'in_val' points to 'RCP45_EMI' or likewise, i.e., 'input data read from file'
        if (type(self.in_val) == str):
            #emissions from external input file
            if (EorC=='E'):
                if np.any((self.in_val == 'C5HIST_EMI')\
                          or (self.in_val == 'RCP26_EMI')\
                          or (self.in_val == 'RCP45_EMI')\
                          or (self.in_val == 'RCP60_EMI')\
                          or (self.in_val == 'RCP85_EMI')):
                    idf = 0   #search for data frame idf (to be determined) that contains desired emission data set
                    for i in range(len(self.df_emi)):
                        tmp = self.df_emi['DataTag'][i]
                        if (tmp == self.in_val): idf=i
                    #get data for desired data frame
                    TimeRange  = self.df_emi['TimeRange'][idf];    self.in_beg_yr = TimeRange[0];      self.in_end_yr = TimeRange[1]
                    TimeStep   = self.df_emi['TimeStep'][idf];     self.in_dys    = TimeStep
                    Years      = self.df_emi['Years'][idf];        self.in_ndts   = len(Years)
                    GtC_fossil = self.df_emi['GtC_fossil'][idf]
                    GtC_other  = self.df_emi['GtC_other'][idf]
                    GtC_tot    = self.df_emi['GtC_tot'][idf];      self.in_val    = GtC_tot
                    #if (TalkTalk==2): print('ReMapTdEmiConc : emission data '+str(self.df_emi['DataTag'][idf])+' from '+str(self.in_beg_yr)+' to '+str(self.in_end_yr))
            #concentrations from external input file
            if (EorC=='C'):
                if np.any((self.in_val=='C5PICT_CONC')\
                          or (self.in_val=='C5HIST_CONC')\
                          or (self.in_val=='RCP26_CONC')\
                          or (self.in_val=='RCP45_CONC')\
                          or (self.in_val=='RCP60_CONC')\
                          or (self.in_val=='RCP85_CONC')):
                    idf = 0   #search for data frame idf (to be determined) that contains desired concentration data set
                    for i in range(len(self.df_con)):
                        tmp = self.df_con['DataTag'][i]
                        if (tmp == self.in_val): idf=i
                    #get data for desired data frame
                    TimeRange  = self.df_con['TimeRange'][idf];    self.in_beg_yr = TimeRange[0];      self.in_end_yr = TimeRange[1]
                    TimeStep   = self.df_con['TimeStep'][idf];     self.in_dys    = TimeStep
                    Years      = self.df_con['Years'][idf];        self.in_ndts   = len(Years)
                    CO2        = self.df_con['CO2'][idf];          self.in_val    = CO2
                    #if (TalkTalk==2): print('ReMapTdEmiConc : concentration data '+str(self.df_con['DataTag'][idf])+' from '+str(self.in_beg_yr)+' to '+str(self.in_end_yr))
                    
        #loop through output array
        #if time step out_dys > in_dys, step size of loop is ts_out=1 and in_val is averaged over ts_in=int(out_dys/in_dys) time steps to give out_val
        #if time step out_dys < in_dys, step size of loop is ts_out=int(in_dys/out_dys) and out_val is interpolated from in_val[idx] and in_val[idx+1]
        #if out_beg < in_beg, in_val[0] is copie to out_val till out_beg == in_beg is reached
        #if out_end > in_end, out_val[self.out_ndts] is copied to out_val till entire out_val array is filled

        #ratio of output time step (out_dys) to input time step (in_dys); if out_dys==in_dys, set self.dys_out2in = 1
        self.dys_out2in = self.out_dys/self.in_dys if (self.out_dys != self.in_dys) else 1.
        #if emissions are re-mapped, need to take into account time step change to guarantee that time integrated emissions remain unchanged; Not needed for concentrations
        Fac4EorC = self.dys_out2in if (EorC == 'E') else 1.
        
        #loop increments for stepping through output array; increment of input array to compute output array
        ts_in  = 1;  ts_out = 1;  #default: if in_dys == out_dys, one input time step corresponds to one output time step, ts_in = ts_out = 1
        if (self.dys_out2in > 1): ts_in=int(self.out_dys/self.in_dys); ts_out=1   #out_dys > in_dys: loop time step ts_out=1, average in_val over ts_in time steps
        if (self.dys_out2in < 1): ts_in=1; ts_out=int(self.in_dys/self.out_dys)   #out_dys < in_dys: loop time step ts_out>1, interpolate in_val time steps separated by ts_in = 1
        #start and end index of outer loop for regular filling, i.e., averaging or interpolation
        it_out_beg = 0              #default start index of output array for regular filling from input array
        it_out_end = self.out_ndts  #default end index of output array for regular filling from input array
        if (self.out_beg_yr < self.in_beg_yr): it_out_beg = int( (self.in_beg_yr-self.out_beg_yr+0.1)/self.out_dys ) #no input data for output entries up to it_out_beg 
        if (self.out_end_yr > self.in_end_yr): it_out_end = int( (self.in_end_yr-self.out_beg_yr-0.1)/self.out_dys ) #no input data for output onwards from it_out_end

        #loop for regular filling of out_val 
        for it_out in range(it_out_beg,it_out_end,ts_out):
            yr_out = self.out_beg_yr + it_out*self.out_dys  #current year of output data
            it_in = int( (yr_out - self.in_beg_yr) / self.in_dys )  #array index of in_val with input year closest to desired output year
            #as long as we are within re-mapping range in input and output data: re-map!
            if ((it_out <= self.out_ndts) and (it_in+ts_in <= self.in_ndts)):
                #if out_dys > in_dys: average ts_in entries from in_val onto out_val
                if (ts_out == 1):
                    self.out_val[it_out] = np.mean(self.in_val[it_in:it_in+ts_in])*Fac4EorC
                #if out_dys < in_dys: interpolate ts_out entries of out_val from successive (ts_in = 1) entries of in_val
                if (ts_out > 1):
                    din_by_dtsout = float(in_val[it_in+ts_in] - in_val[it_in]) / float(ts_in) / float(ts_out)
                    self.out_val[it_out:it_out+ts_out] = self.in_val[it_in] + din_by_dtsout*float(np.arange(0,ts_out))

        #if neccessary, fill first and / or last few years of out_val; distinction between 'emissions' and 'concentrations' is inherited from regularly filled out_val
        #if self.out_beg_yr < self.in_beg_yr: fill remainig first few years of out_val
        if (it_out_beg > 0):
            self.out_val[0:it_out_beg-1] = self.out_val[it_out_beg]

        #if self.out_end_yr > self.in_end_yr: fill remainig last few years of out_val; 
        if (it_out_end < self.out_ndts):
            self.out_val[it_out_end+1:self.out_ndts] = self.out_val[it_out_end]

        return self.out_val
    


    #time integration of equations (temperature and carbon mass) as done in DICE2016
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def TimeIntDICE(self,TalkTalk=1):

        """Time Integration following DICE2016"""

        #some short hands
        ndts   = self.ndts
        dys    = self.dys
        fco22x = self.fco22x
        t2xco2 = self.t2xco2
        c1     = self.c1
        c2     = fco22x/t2xco2
        c3     = self.c3
        c4     = self.c4
        A      = self.A
        fex0   = CCC.fex0_DICE
        fex1   = CCC.fex1_DICE
        #print('WhichClimInt='+str(self.WhichClimInt))
        #define arrays for integration
        self.n_timestep = np.empty(ndts)                                 #timestep
        self.n_year     = np.empty(ndts)                                 #year
        self.M_of_t     = np.empty(3*ndts,dtype=float).reshape(3,ndts)   #carbon mass in each reservoir
        self.T_of_t     = np.empty(2*ndts,dtype=float).reshape(2,ndts)   #temperature of atmosphere / upper ocean & lower ocean
        self.FCO2_of_t  = np.empty(ndts,dtype=float)                     #forcing from CO2
        self.FVar_of_t  = np.empty(ndts,dtype=float)                     #forcing from other agents
        self.F_of_t     = np.empty(ndts,dtype=float)                     #total forcing, from CO2 plus from other agents
        #forcing before perturbing system
        self.F_ini = 0.
        if (self.FCO2 == 'CC'):     self.F_ini = self.fco22x * np.log((self.M_ini[0]/self.M_eq[0]))/np.log(2)
        if (self.FCO2 == 'Xx2CO2'): self.F_ini = self.fco22x * self.X_x_fco22x
        if (self.FCO2 == 'ppmCO2'): self.F_ini = self.fco22x * np.log( (self.ppmCO2[0]/CCC.ppmCO2_eq_1850) )/np.log(2)
        #values at start time
        self.n_timestep[0] = 0
        self.n_year[0]     = self.beg_yr
        self.M_of_t[:,0]   = self.M_ini[:]
        self.M_of_t[0,0]   = self.M_of_t[0,0] + self.M_puls 
        #self.M_of_t[0,0]   = self.M_of_t[0,0] + self.M_puls + self.GtC_Emi[0] + self.M_ini[0]*self.Pct_Emi
        self.T_of_t[:,0]   = self.T_ini[:]
        if (self.FCO2 == 'CC'):     self.FCO2_of_t[0] = self.fco22x * np.log((self.M_of_t[0,0]/self.M_eq[0]))/np.log(2)
        if (self.FCO2 == 'Xx2CO2'): self.FCO2_of_t[0] = self.fco22x * self.X_x_fco22x
        if (self.FCO2 == 'ppmCO2'): self.FCO2_of_t[0] = self.fco22x * np.log( (self.ppmCO2[0]/CCC.ppmCO2_eq_1850) )/np.log(2)
        #if (self.FCO2 == 'ppmCO2'): self.FCO2_of_t[0] = self.fco22x * (self.ppmCO2[0] - CCC.ppmCO2_eq_1850) / CCC.ppmCO2_eq_1850
        if (self.FVar == 'none'):   self.FVar_of_t[0] = 0.
        if (self.FVar == 'DICE'):   self.FVar_of_t[0] = fex0 + np.max([0.,  np.min([(self.n_year[0]-2015.)/(2100.-2015.),  1.])])*(fex1-fex0)  #hard wired this way in DICE2016
        if (self.FVar == 'Fac'):    self.FVar_of_t[0] = self.FCO2_of_t[0]*self.FVarFac
        if (self.FVar == 'Fac2'):
            rlx = 1./15.*float(self.n_year[0]-2000)
            FacFac = 0.3
            if (self.n_year[0] < 2015): FacFac = (1.-rlx)*self.FVarFac + rlx*0.3
            if (self.n_year[0] < 2000): FacFac = self.FVarFac
            self.FVar_of_t[0] = self.FCO2_of_t[0]*FacFac
        if (self.FVar == 'MIP'):
            dip = -0.2 #net non-CO2 forcings following Mengis & Matthews, Nature Comm. (2020), Fig. 1; maximum dip between 1960 and 1970
            rlx = 1./35.*float(self.n_year[0]-1980) #relaxation parameter used from 1980 to 2015 [0 in 1980, 1 in 2015]
            self.FVar_of_t[0] = self.FCO2_of_t[0]*self.FVarFac                                          #net non-CO2 forcing equal to (about) 30% of CO2 forcing
            if (self.n_year[0] < 2015): self.FVar_of_t[0] = rlx*self.FCO2_of_t[0]*self.FVarFac        #net non-CO2 forcing relaxing from zero to 30% of CO2 focring
            if (self.n_year[0] < 1980): self.FVar_of_t[0] = dip - dip/10.*float(self.n_year[0]-1970)  #net non-CO2 forcing going from dip to zero
            if (self.n_year[0] < 1970): self.FVar_of_t[0] = dip                                       #net non-CO2 forcing leveling at dip
            if (self.n_year[0] < 1960): self.FVar_of_t[0] = dip/10.*float(self.n_year[0]-1950)        #net non-CO2 forcing going from zero to dip
            if (self.n_year[0] < 1950): self.FVar_of_t[0] = 0.0                                       #net non-CO2 forcing (about) zero before 1950
        self.F_of_t[0]     = self.FCO2_of_t[0] + self.FVar_of_t[0]
        #update mass in diagnostic fashion for problems where atmospheric CO2 concentrations are prescribed (instead of emissions or just the forcing as such)
        if np.any( (self.WhichSelProb == '1pctCO2') or  (self.WhichSelProb == 'TD_ppmCO2') ): self.M_of_t[0,0] = self.ppmCO2[0]/CCC.gtc2ppmco2

        #now integrate
        #print('now integrating with WhichClimInt = '+str(self.WhichClimInt))
        #print('c1, c2, c3, c4 : '+str(c1)+', '+str(c2)+', '+str(c3)+', '+str(c4))
        for i in range(1,ndts):
            self.n_timestep[i] = i
            self.n_year[i]     = self.n_year[i-1] + dys
            self.M_of_t[:,i]   = self.M_of_t[:,i-1]      #in case CC is not integrated, make sure to have M_of_t filled anyway
            self.T_of_t[:,i]   = self.T_of_t[:,i-1]      #in case climate is not integrated, make sure to have T_of_t filled anyway
            #self.F_of_t[i]     = self.F_of_t[i-1]        #in case force is not updated, make sure to have F_of_t filled anyway
            #update mass in diagnostic fashion for problems where atmospheric CO2 concentrations are prescribed (instead of emissions or just the forcing as such)
            if np.any( (self.WhichSelProb == '1pctCO2') or  (self.WhichSelProb == 'TD_ppmCO2') ): self.M_of_t[0,i] = self.ppmCO2[i]/CCC.gtc2ppmco2
            #update mass in prognostic fashion via carbon-cycle
            if (self.IntCC == 'true'):
                tmp                = np.matmul(A,self.M_of_t[:,i-1])
                self.M_of_t[:,i]   = tmp[:]
                if (self.WhichSelProb == 'DM4MConst'): self.GtC_Emi[i-1] = self.M_of_t[0,i-1] - self.M_of_t[0,i] #diagnose what emissions are needed to keep M_of_t[0,:]=M_ini[0]
                self.M_of_t[0,i]   = self.M_of_t[0,i] + self.GtC_Emi[i-1] + self.M_of_t[0,i-1]*self.Pct_Emi
                #if (self.WhichSelProb == 'DM4MConst'): self.GtC_Emi[i] = self.M_of_t[0,i-1] - self.M_of_t[0,i] #diagnose what emissions are needed to keep M_of_t[0,:]=M_ini[0]
                #self.M_of_t[0,i]   = self.M_of_t[0,i] + self.GtC_Emi[i] + self.M_of_t[0,i-1]*self.Pct_Emi
            #update forcing
            self.FCO2_of_t[i] = 0.
            self.FVar_of_t[i] = 0.
            if (self.FCO2 == 'CC'):     self.FCO2_of_t[i] = self.fco22x * np.log((self.M_of_t[0,i]/self.M_eq[0]))/np.log(2)
            if (self.FCO2 == 'Xx2CO2'): self.FCO2_of_t[i] = self.fco22x * self.X_x_fco22x
            if (self.FCO2 == 'ppmCO2'): self.FCO2_of_t[i] = self.fco22x * np.log( (self.ppmCO2[i]/CCC.ppmCO2_eq_1850) )/np.log(2)
            if (self.FVar == 'none'):   self.FVar_of_t[i] = 0.
            if (self.FVar == 'DICE'):   self.FVar_of_t[i] = fex0 + np.max([0.,  np.min([(self.n_year[i]-2015.)/(2100.-2015.),  1.])])*(fex1-fex0)  #hard wired this way in DICE2016
            if (self.FVar == 'Fac'):    self.FVar_of_t[i] = self.FCO2_of_t[i]*self.FVarFac
            if (self.FVar == 'Fac2'):
                rlx = 1./15.*float(self.n_year[i]-2000)
                FacFac = 0.3
                if (self.n_year[i] < 2015): FacFac = (1.-rlx)*self.FVarFac + rlx*0.3
                if (self.n_year[i] < 2000): FacFac = self.FVarFac
                self.FVar_of_t[i] = self.FCO2_of_t[i]*FacFac
            if (self.FVar == 'MIP'):
                dip = -0.2 #net non-CO2 forcings following Mengis & Matthews, Nature Comm. (2020), Fig. 1; maximum dip between 1960 and 1970
                rlx = 1./35.*float(self.n_year[i]-1980) #relaxation parameter used from 1980 to 2015 [0 in 1980, 1 in 2015]
                self.FVar_of_t[i] = self.FCO2_of_t[i]*self.FVarFac                                          #net non-CO2 forcing equal to (about) 30% of CO2 forcing
                if (self.n_year[i] < 2015): self.FVar_of_t[i] = rlx*self.FCO2_of_t[i]*self.FVarFac        #net non-CO2 forcing relaxing from zero to 30% of CO2 focring
                if (self.n_year[i] < 1980): self.FVar_of_t[i] = dip - dip/10.*float(self.n_year[i]-1970)  #net non-CO2 forcing going from dip to zero
                if (self.n_year[i] < 1970): self.FVar_of_t[i] = dip                                       #net non-CO2 forcing leveling at dip
                if (self.n_year[i] < 1960): self.FVar_of_t[i] = dip/10.*float(self.n_year[i]-1950)        #net non-CO2 forcing going from zero to dip
                if (self.n_year[i] < 1950): self.FVar_of_t[i] = 0.0                                       #net non-CO2 forcing (about) zero before 1950
                #print(str(self.n_year[i])+'   '+str(self.FVar_of_t[i]))
            self.F_of_t[i] = self.FCO2_of_t[i] + self.FVar_of_t[i]
            #if (i==ndts-1): print('Ftot / FCO2 / FVar ='+str(self.F_of_t[i])+' / '+str(self.FCO2_of_t[i])+' / '+str(self.FVar_of_t[i]))
            #update climate
            if (self.IntClim == 'true'):
                if (self.WhichClimInt == 'new'):
                    #print('integrating! i='+str(i))
                    self.T_of_t[0,i]   = self.T_of_t[0,i-1] + dys * c1*( self.F_of_t[i] - c2*self.T_of_t[0,i-1] - c3*(self.T_of_t[0,i-1] - self.T_of_t[1,i-1]) )
                    self.T_of_t[1,i]   = self.T_of_t[1,i-1] + dys * c4*( self.T_of_t[0,i-1] - self.T_of_t[1,i-1] )
                if (self.WhichClimInt == 'old'):
                    self.T_of_t[0,i]   = self.T_of_t[0,i-1] +       c1*( self.F_of_t[i] - c2*self.T_of_t[0,i-1] - c3*(self.T_of_t[0,i-1] - self.T_of_t[1,i-1]) )
                    self.T_of_t[1,i]   = self.T_of_t[1,i-1] +       c4*( self.T_of_t[0,i-1] - self.T_of_t[1,i-1] )
            
        return



    #CMIP data: load emissions & concentrations from file, file name governs what is read, what is returned
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def LoadEmiAndConcData(self,Path2Files='../EmiAndConcData',TalkTalk=0):

        """Load data from file, file name governs what is read, what is returned"""

        #Wish list of files to be loaded, time dependent emission and concentration data
        Wish2Load = []; DataTagTmp = []; NHeadTmp = []   #List of files to be loaded, associated tags, number of header lines; existence checked below
        Wish2Load.append("20THCENTURY_EMISSIONS.csv");   DataTagTmp.append("C5HIST_EMI");    NHeadTmp.append(38)   #CMPI5, 20th century emissions
        Wish2Load.append("RCP26_EMISSIONS.csv");         DataTagTmp.append("RCP26_EMI");     NHeadTmp.append(39)   #CMPI5, RCP26 emissions, originally RCP3PD_EMISSIONS.csv
        Wish2Load.append("RCP45_EMISSIONS.csv");         DataTagTmp.append("RCP45_EMI");     NHeadTmp.append(39)   #CMPI5, RCP45 emissions
        Wish2Load.append("RCP60_EMISSIONS.csv");         DataTagTmp.append("RCP60_EMI");     NHeadTmp.append(39)   #CMPI5, RCP60 emissions
        Wish2Load.append("RCP85_EMISSIONS.csv");         DataTagTmp.append("RCP85_EMI");     NHeadTmp.append(39)   #CMPI5, RCP85 emissions
        Wish2Load.append("PICNTRL_MIDYR_CONC.DAT");      DataTagTmp.append("C5PICT_CONC");   NHeadTmp.append(40)   #CMPI5, piControl concentrations
        Wish2Load.append("PRE2005_MIDYR_CONC.DAT");      DataTagTmp.append("C5HIST_CONC");   NHeadTmp.append(40)   #CMPI5, historical concentrations [i.e., till 2005]
        Wish2Load.append("RCP26_MIDYR_CONC.DAT");        DataTagTmp.append("RCP26_CONC");    NHeadTmp.append(40)   #CMPI5, RCP26 concentrations, originally RCP3PD_MIDYR_CONC.DAT
        Wish2Load.append("RCP45_MIDYR_CONC.DAT");        DataTagTmp.append("RCP45_CONC");    NHeadTmp.append(40)   #CMPI5, RCP45 concentrations
        Wish2Load.append("RCP60_MIDYR_CONC.DAT");        DataTagTmp.append("RCP60_CONC");    NHeadTmp.append(40)   #CMPI5, RCP60 concentrations
        Wish2Load.append("RCP85_MIDYR_CONC.DAT");        DataTagTmp.append("RCP85_CONC");    NHeadTmp.append(40)   #CMPI5, RCP85 concentrations

        #Check that files from wish list exist; If so, add to Files2Load list; If not so, warn user
        Files2Load = []; DataTag = []; NHead = []   #List of files to be loaded, associated tags, number of header lines
        nW2L = len(Wish2Load)
        for i in range(nW2L):
            if os.path.isfile(Path2Files+'/'+Wish2Load[i]):
                Files2Load.append(Wish2Load[i])
                DataTag.append(DataTagTmp[i])
                NHead.append(NHeadTmp[i])
            else:
                print ("WARNING!!! MISSING DATA INPUT FILE : "+Wish2Load[i])

        #Actually load the data; for loading and ranging into pandas data frams (and for later use): distinguish between emissions and concentrations
        nF2L = len(Files2Load)
        if (nF2L == 0): print("WARNING!!! NO DATA INPUT FILES FOUND!!!")
        if (nF2L > 0):
            emi_keys = ['FileName', 'DataTag', 'TimeRange', 'TimeStep', 'Units', 'Years', 'NYears', 'GtC_fossil', 'GtC_other', 'GtC_tot'] #data-frame keys, emission data
            emi_data = []
            con_keys = ['FileName', 'DataTag', 'TimeRange', 'TimeStep', 'Units', 'Years', 'NYears', 'CO2', 'CH4', 'N2O'] #data-frame keys, concentration data
            con_data = []
            for i in range(nF2L):
                
                #CMIP5 emissions, historical, RCP26, RCP45, RCP60, RCP85:
                #37 header rows till data; 'what data' in row 36, 'units' in row 35;
                #only use first three columns: year, CO2 Fossil, CO2 Other
                #RCPs contain historical emissions
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if np.any((Files2Load[i] == "20THCENTURY_EMISSIONS.csv") or\
                          (Files2Load[i] == "RCP26_EMISSIONS.csv") or\
                          (Files2Load[i] == "RCP45_EMISSIONS.csv") or\
                          (Files2Load[i] == "RCP60_EMISSIONS.csv") or\
                          (Files2Load[i] == "RCP85_EMISSIONS.csv")):
                    #get units (row 35)
                    tmp_un = pd.read_csv(Path2Files+'/'+Files2Load[i],skiprows=NHead[i]-4, nrows=2,usecols=[0,1,2])
                    #get data, including column headers containing 'what data' (row 36)
                    tmp_df = pd.read_csv(Path2Files+'/'+Files2Load[i],skiprows=NHead[i]-2,usecols=[0,1,2])  #data frame with 'what data' in header
                    #extract what we want to keep 
                    TimeRange  = np.array([tmp_df.iloc[0,0], tmp_df.iloc[tmp_df.shape[0]-1,0]])       #start and end year of data in file
                    TimeStep   = int(tmp_df.iloc[1,0]) - int(tmp_df.iloc[0,0])                        #time step of data
                    Units      = list(tmp_un.iloc[0,:])
                    Years      = np.array(tmp_df.iloc[:,0])
                    NYears     = len(Years)
                    GtC_fossil = np.array(tmp_df.iloc[:,1])
                    GtC_other  = np.array(tmp_df.iloc[:,2])
                    GtC_tot    = GtC_fossil + GtC_other
                    emi_data.append([Files2Load[i], DataTag[i], TimeRange, TimeStep, Units, Years, NYears, GtC_fossil, GtC_other, GtC_tot])
                    if (TalkTalk==1): print('LoadEmiAndConcData: i / Files2Load[i] / TimeRange : '\
                                            +str(i)+'   /   '+str(Files2Load[i])+'   /   '+str(TimeRange[0])+'   /   '+str(TimeRange[1]))
                    
                #CMIP5 concentrations, historical, RCP26, RCP45, RCP60, RCP85:
                #39 header rows till data; 'what data' in row 38, 'units' in row 37;
                #only use columns 0,3,4,5: year, CO2, CH4, N20
                #RCPs contain historical emissions
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                if np.any((Files2Load[i] == "PICNTRL_MIDYR_CONC.DAT") or\
                          (Files2Load[i] == "PRE2005_MIDYR_CONC.DAT") or\
                          (Files2Load[i] == "RCP26_MIDYR_CONC.DAT") or\
                          (Files2Load[i] == "RCP45_MIDYR_CONC.DAT") or\
                          (Files2Load[i] == "RCP60_MIDYR_CONC.DAT") or\
                          (Files2Load[i] == "RCP85_MIDYR_CONC.DAT")):
                    #get units (row 35)
                    tmp_un = pd.read_csv(Path2Files+'/'+Files2Load[i],skiprows=NHead[i]-4,nrows=2,usecols=[0,3,4,5],delimiter=r"\s+")
                    #get data, including column headers containing 'what data' (row 36)
                    tmp_df = pd.read_csv(Path2Files+'/'+Files2Load[i],skiprows=NHead[i]-2,usecols=[0,3,4,5],delimiter=r"\s+")  #data frame with 'what data' in header
                    #extract what we want to keep 
                    TimeRange  = np.array([tmp_df.iloc[0,0], tmp_df.iloc[tmp_df.shape[0]-1,0]])       #start and end year of data in file
                    TimeStep   = int(tmp_df.iloc[1,0]) - int(tmp_df.iloc[0,0])                        #time step of data
                    Units      = list(tmp_un.iloc[0,:])
                    Years      = np.array(tmp_df.iloc[:,0])
                    NYears     = len(Years)
                    CO2_ppm    = np.array(tmp_df.iloc[:,1])
                    CH4_ppb    = np.array(tmp_df.iloc[:,2])
                    N2O_ppb    = np.array(tmp_df.iloc[:,3])
                    con_data.append([Files2Load[i], DataTag[i], TimeRange, TimeStep, Units, Years, NYears, CO2_ppm, CH4_ppb, N2O_ppb])
                    if (TalkTalk==1): print('LoadEmiAndConcData: i / Files2Load[i] / TimeRange : '\
                                            +str(i)+'   /   '+str(Files2Load[i])+'   /   '+str(TimeRange[0])+'   /   '+str(TimeRange[1]))
            
            #put emission and concentration data in associated data frames, for later us in ModCarbEmi | ModCarbCon
            self.df_emi=pd.DataFrame.from_records(emi_data, columns=emi_keys);   #pandas data frame containing GHG emission data loaded from file(s)
            self.df_con=pd.DataFrame.from_records(con_data, columns=con_keys);   #pandas data frame containing GHG concentration data loaded from file(s)

        return



    #CMIP data as benchmark: load temperature data from CMIP experiments for comparison with DICE results
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def LoadTempData(self,Path2Dirs='../DataFromCMIP',TalkTalk=0):

        """Benchmark: Load temperature data from CMIP experiments for comparison with DICE results"""

        #Wish list of directories containing files to be loaded; time dependent global annual mean temperature data
        #with list of associated tags, pattern matching ids, and variable ids for the netcdf load; existence of directories / files checked below
        Wish2Load = []; DataTagTmp = [];  FileIdTmp = []; VarIdTmp = [] 
        Wish2Load.append("1pctCO2");            DataTagTmp.append("1pctCO2");       FileIdTmp.append("*_am_*nc");   VarIdTmp.append("ts");  #CMPI5, 1 pct CO2 increase per year
        Wish2Load.append("historical_rcp26");   DataTagTmp.append("RCP26_CONC");    FileIdTmp.append("*_am_*nc");   VarIdTmp.append("ts");  #CMPI5, historical plus rcp26
        Wish2Load.append("historical_rcp45");   DataTagTmp.append("RCP45_CONC");    FileIdTmp.append("*_am_*nc");   VarIdTmp.append("ts");  #CMPI5, historical plus rcp45
        Wish2Load.append("historical_rcp60");   DataTagTmp.append("RCP60_CONC");    FileIdTmp.append("*_am_*nc");   VarIdTmp.append("ts");  #CMPI5, historical plus rcp60
        Wish2Load.append("historical_rcp85");   DataTagTmp.append("RCP85_CONC");    FileIdTmp.append("*_am_*nc");   VarIdTmp.append("ts");  #CMPI5, historical plus rcp85

        #Check that directories from wish list exist and contain files whose names match FileIdTmp; If so, add directory to Dirs2Load list; If not so, warn user
        Dirs2Load = []; DataTag = []; FileId = []; VarId = [];   #List of directories to be loaded, associated tags, file identifiers, variable ids
        nW2L = len(Wish2Load)
        for i in range(nW2L):
            if os.path.isdir(Path2Dirs+'/'+Wish2Load[i]):
                tmp = glob.glob(Path2Dirs+'/'+Wish2Load[i]+'/'+FileIdTmp[i])
                if (len(tmp)>0):
                    Dirs2Load.append(Wish2Load[i])
                    DataTag.append(DataTagTmp[i])
                    FileId.append(FileIdTmp[i])
                    VarId.append(VarIdTmp[i])
            else:
                print ("WARNING!!! MISSING DATA INPUT DIRECTORY : "+Wish2Load[i])

        #Actually load the data: CMIP5 global annual mean temperature time series for experiments
        #One percent CO2, historical+rcp26, historical+rcp45, historical+rcp60, historical+rcp85
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        nD2L = len(Dirs2Load)
        if (nD2L == 0): print("WARNING!!! NO DATA INPUT DIRECTORIES FOUND!!!")
        if (nD2L > 0):
            clim_keys = ['DirName', 'DataTag', 'NFiles', 'FileName', 'ModelName', 'TimeRange', 'TimeStep', 'Years', 'NYears', 'Temperature'] #data-frame keys, emission data
            clim_data = []
            for i in range(nD2L):                
                #load individual data files
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if (TalkTalk==2): print('loading global mean temperature from files in directory '+str(Path2Dirs)+'/'+str(Dirs2Load[i]))
                tmp = sorted(glob.glob(Path2Dirs+'/'+Dirs2Load[i]+'/'+FileId[i]))  #list files in directory that match desired FileId pattern
                NFiles = len(tmp)  #how many such files do we have?
                for j in range(NFiles):
                    #get the data from each file
                    ds          = nc.Dataset(tmp[j])
                    #extract data we want to keep
                    parts       = tmp[j].split('/')
                    FileName    = parts[len(parts)-1]
                    parts       = FileName.split('_')
                    ModelName   = parts[0]
                    Years       = (np.array(ds['time'])/1.e4).astype('int')           #years at which we have data; time comes as 18500701.25 etc.
                    TimeRange   = np.array([Years[0], Years[len(Years)-1]])           #time range covered by data
                    TimeStep    = Years[1] - Years[0]                                 #time step
                    NYears      = len(Years)                                          #number of years of data
                    Temperature = np.array(ds[VarId[i]]).reshape(len(ds[VarId[i]]))   #the data, temperature, as such
                    clim_data.append([Dirs2Load[i], DataTag[i], NFiles, FileName, ModelName, TimeRange, TimeStep, Years, NYears, Temperature])
                    if (TalkTalk==1): print('LoadEmiAndConcData: i / Files2Load[i] / TimeRange : '\
                                        +str(i)+'   /   '+str(Files2Load[i])+'   /   '+str(TimeRange[0])+'   /   '+str(TimeRange[1]))
            
            #put emission and concentration data in associated data frames, for later us in ModCarbEmi | ModCarbCon
            self.df_clim=pd.DataFrame.from_records(clim_data, columns=clim_keys);   #pandas data frame containing GHG emission data loaded from file(s)
        
        return



    #benchmark: load CMIP data to compare / plot [global annual mean temp. time series goes to T_of_t; input emi./conc. go to M_of_t]
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def BenchMarkCMIP(self,prb="TD_emiCO2",CMIP="RCP45_EMI",TalkTalk=1):

        """Benchmark: load CMIP data to compare / plot """

        #simu = cld.CCC()
        #simu.LoadTempData()        
        #simu.df_clim['FileName'][:]
        #simu.df_clim['Time'][1][0:10]
        #simu.df_clim['Years'][1][1:10]
        #simu.df_clim['Temperature'][1][250]-273.15
        
        #print('BenchMarkCMIP: prb is '+str(prb))

        CCC.LoadTempData(self)         #load all CMIP output, global annual mean tempearture time series ---> df_clim, DataTag=*_CONC or 1pctCO2
        CCC.LoadEmiAndConcData(self)   #load all CMIP input, emission and concentration data files ---> df_con and df_emi, but use here only df_con, DataTag=*_CONC or 1pctCO2

        UBMD=CMIP                                  #what benchmark data (RCP) to use? Temp. (CMIP output) and associated ppm CO2 (input); UBMD defaults to CMIP key word
        if (CMIP=="RCP26_EMI"): UBMD="RCP26_CONC"  #adapt UBMD if CMIP key word points to *_EMI; this because CMIP5 worked with CO2 concentrations
        if (CMIP=="RCP45_EMI"): UBMD="RCP45_CONC"
        if (CMIP=="RCP60_EMI"): UBMD="RCP60_CONC"
        if (CMIP=="RCP85_EMI"): UBMD="RCP85_CONC"
        
        self.tmp_temp = self.df_clim[self.df_clim['DataTag']==UBMD]        #from all CMIP output, select desired data frame; contains temperature ---> T_of_t
        self.tmp_eacd = self.df_con[self.df_con['DataTag']=='RCP45_CONC']  #from all CMIP input, select as default RCP45_CONC; needed for concentration in 1850 for 1pctCO2
        if ((prb=="TD_emiCO2") or (prb=="TD_ppmCO2")):
            self.tmp_eacd = self.df_con[self.df_con['DataTag']==UBMD]      #from all CMIP input, select desired data frame if problem is not "1pctCO2"; contains CO2 ---> M_of_t

        #define arrays to hold variables for plotting the CMIP bench mark data
        nts_temp = len(self.tmp_temp)                #number of time series, CMIP output data, plus 1 for the multi-model-mean (MMM) over common years
        nym_temp = max(self.tmp_temp['NYears'])      #maximum number of years in the different CMIP output data time series
        ts1      = min(self.tmp_temp['TimeStep'])    #minimum time step of CMIP output data
        ts2      = max(self.tmp_temp['TimeStep'])    #maximum time step of CMIP output data
        ts3      = self.tmp_eacd['TimeStep'].iloc[0] #time step of CMIP input data
        if np.any( (ts1 != ts2) or (ts2 != ts3) or (ts3 != ts1) ):
            print('BenchMarkCMIP, WARNING: NON-UNIQUE TIME STEP SIZE')                                #currently assume / can deal only with equal time steps
        self.n_year      = np.empty(nym_temp*(nts_temp+1),dtype=float).reshape(nym_temp,nts_temp+1)   #time axis, years of data
        self.n_year[:,:] = np.nan
        self.T_of_t      = np.empty(nym_temp*(nts_temp+1),dtype=float).reshape(nym_temp,nts_temp+1)   #atmospheric temperature 
        self.M_of_t      = np.empty(nym_temp*(nts_temp+1),dtype=float).reshape(nym_temp,nts_temp+1)   #atmospheric mass
        self.T_ini       = np.empty(nts_temp+1,dtype=float)                                           #initial atmospheric temperature 
        self.M_ini       = np.empty(nts_temp+1,dtype=float)                                           #initial atmospheric mass
        self.MoNa        = self.tmp_temp['ModelName']

        #loop over selected CMIP output data time series to fill arrays T_of_t (from CMIP output) and M_of_t (from CMIP input)
        minnyte=10000
        for i in range(nts_temp):
            #print('BLABLA i = '+str(i))
            nyte                  = self.tmp_temp['NYears'].iloc[i]               #number of years of temperature time series 'i' (TSi)
            minnyte               = np.min([nyte,minnyte])
            self.n_year[0:nyte,i] = self.tmp_temp['Years'].iloc[i][0:nyte]        #TSi: actual years for which we have temperature
            if (prb=="1pctCO2"): self.n_year[0:nyte,i] = self.n_year[0:nyte,i] - self.n_year[0,i] + 1850   #for "1pctCO2" must ascertain that time axis starts in 1850
            self.T_of_t[0:nyte,i] = self.tmp_temp['Temperature'].iloc[i][0:nyte]  #TSi: actual atmospheric temperature (CMIP output)
            #to link CMIP output to  CMIP input (emissions / concentrations) we need to find appropriate years in input data
            #---> find index imiyrC / imayrC of start / end year in CO2 concentration data to go with temperature data
            miyrT                 = min(self.n_year[0:nyte,i])                    #TSi: minimum year for which there is temperature data (CMIP output)
            mayrT                 = max(self.n_year[0:nyte,i])                    #TSi: maximum year for which there is temperature data (CMIP output)
            nyec                  = self.tmp_eacd['NYears'].iloc[0]               #number of years of input data
            imiyrC                = 0                                             #default: start index of CMIP output on CMIP input time series
            imayrC                = nyec-1                                        #default: end index of CMIP output on CMIP input time series
            for j in range(nyec-1):
                if (self.tmp_eacd['Years'].iloc[0][j] == miyrT): imiyrC = j       #index in emi / conc data corresponding to start year of temperature data
                if (self.tmp_eacd['Years'].iloc[0][j] == mayrT): imayrC = j       #index in emi / conc data corresponding to end year of temperature data

            self.M_of_t[0:nyte,i] = self.tmp_eacd['CO2'].iloc[0][imiyrC:imayrC+1]/CCC.gtc2ppmco2     #TSi: input, atmos. CO2 conc., converted to GtC, from ppm-data
            #if problem is "1pctCO2", concentrations can be computed on the fly
            if (prb=="1pctCO2"):
                self.M_of_t[0,i] = self.tmp_eacd['CO2'].iloc[0][imiyrC]
                for j in range(1,nyte): self.M_of_t[j,i]=self.M_of_t[j-1,i]*np.power(1.01,ts1)  #one percent increase of CO2 concentration each year
                self.M_of_t[:,i] = self.M_of_t[:,i]/CCC.gtc2ppmco2                              #convert the CO2 ppm concentration to GtC carbon mass
            #there are a few models [GFDL-CM3, GFDL-ESM2G, GFDL-ESM2M, HadGEM2-AO, HadGEM2-CC, MRI-ESM1] whose CMIP5 output starts only after 1850
            #if (nyte<251): print('MoNa='+str(self.tmp_temp['ModelName'].iloc[i])+'...minyear='+str(np.nanmin(self.n_year[:,i]))+'...maxyear='+str(np.nanmax(self.n_year[:,i])))
            if (prb!="1pctCO2"):
                if (np.nanmin(self.n_year[:,i])>1850):
                    dyr                         = int(np.nanmin(self.n_year[:,i])-1850.)
                    minnyte                     = np.max([nyte+dyr,minnyte])
                    self.n_year[dyr:nyte+dyr,i] = self.tmp_temp['Years'].iloc[i][0:nyte]
                    self.T_of_t[dyr:nyte+dyr,i] = self.tmp_temp['Temperature'].iloc[i][0:nyte]
                    self.M_of_t[dyr:nyte+dyr,i] = self.tmp_eacd['CO2'].iloc[0][imiyrC:imayrC+1]/CCC.gtc2ppmco2 
                    self.n_year[0:dyr-1,i] = np.arange(1850,1850+dyr-1,dtype=int)
                    self.T_of_t[0:dyr-1,i] = self.T_of_t[dyr,i]
                    self.M_of_t[0:dyr-1,i] = self.M_of_t[dyr,i]
                    #print('MoNa='+str(self.tmp_temp['ModelName'].iloc[i]))
            #fill initial values: mean over first 20 years (arbitrary choice!) or first year in the case of "1pctCO2"
            self.T_ini[i] = np.mean(self.T_of_t[0:20,i])
            self.M_ini[i] = np.mean(self.M_of_t[0:20,i])
            if (prb=="1pctCO2"):
                self.T_ini[i] = np.mean(self.T_of_t[0:10,i])
                self.M_ini[i] = np.mean(self.M_of_t[0:10,i])
            #print(str(self.MoNa[i])+': i='+str(i)+'...T_of_t='+str(self.T_of_t[0,i]-self.T_ini[i])+'...'+str(self.T_of_t[120,i]-self.T_ini[i]))

        #finally, compute multi-model-mean (MMM)
        #nymmm = min(self.tmp_temp['NYears'])      #maximum number of years in the different CMIP output data time series
        nymmm = minnyte-1
        immm  = nts_temp
        for i in range(nymmm):
            self.n_year[i,immm] = self.n_year[i,0]
            self.T_of_t[i,immm] = np.mean(self.T_of_t[i,0:nts_temp-1])
            self.M_of_t[i,immm] = np.mean(self.M_of_t[i,0:nts_temp-1])
        self.T_ini[immm]        = np.mean(self.T_of_t[0:50,immm])
        self.M_ini[immm]        = np.mean(self.M_of_t[0:50,immm])
        if (prb=="1pctCO2"):
            self.T_ini[immm] = self.T_of_t[0,immm]
            self.M_ini[immm] = self.M_of_t[0,immm]

        return



    #benchmark: 4xCO2 into atmosphere of 2010, Geoffrey at al (2013)
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def BenchMarkGeoffrey(self,TalkTalk=1):

        """Benchmark: 4xCO2 in 2010, Geoffrey et al. (2013)"""

        #Constants from Geoffrey et al. 2013
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        self.mona     = ['BCC-CSM1-1','BNU-ESM','CanESM2','CCSM4','CNRM-CM5','CSIRO-Mk.3.6.0','FGOALS-s2','GFDL-ESM2M','GISS-E2-R',\
                         'HadGEM2-ES','INM-CM4','IPSL-CM5A-LR','MIROC5','MPI-ESM-LR','MRI-CGCM3','NorESM1-M','MulModMea']
        self.f4co2 = np.array([ 6.7,  7.4,  7.6,  7.2,  7.3,  5.1,  7.5,  6.6,  7.3,  5.9,  6.2,  6.4,  8.5,  8.2,  6.6,  6.2,  6.9])
        self.t4co2 = np.array([ 5.6,  8.0,  7.4,  5.8,  6.5,  8.3,  8.5,  4.9,  4.3,  9.1,  4.1,  8.1,  5.4,  7.3,  5.2,  5.6,  6.5])
        self.catm  = np.array([ 7.6,  7.4,  7.3,  6.1,  8.4,  6.0,  7.0,  8.1,  4.7,  6.5,  8.6,  7.7,  8.3,  7.3,  8.5,  8.0,  7.3])
        self.coce  = np.array([ 53.,  90.,  71.,  69.,  99.,  69., 127., 105., 126.,  82., 317.,  95., 145.,  71.,  64., 105., 106.])
        self.gamma = np.array([0.67, 0.53, 0.59, 0.93, 0.50, 0.88, 0.76, 0.90, 1.16, 0.55, 0.65, 0.59, 0.76, 0.72, 0.66, 0.88, 0.73])
        self.rgeo  = np.array([ 0.0,  0.6,  1.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.8,  0.0,  0.8,  0.0,  0.7,  0.0,  0.7])  #for plotting: red channel
        self.ggeo  = np.array([ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  1.0,  0.6,  0.8,  0.5,  0.8,  0.0,  0.7,  0.0,  0.0,  0.7])  #for plotting: green channel
        self.bgeo  = np.array([ 0.0,  0.0,  0.0,  1.0,  1.0,  0.6,  1.0,  0.0,  0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.7,  0.7])  #for plotting: blue channel
        self.ngeof = len(self.gamma)
        self.ngl   = self.ngeof-1

        #some short hands
        ndts              = self.ndts
        dys               = self.dys
        #keep some data from each model
        self.coefs_geof = np.empty(7*self.ngeof).reshape(7,self.ngeof) 
        #initialize time stepping arrays
        self.n_timestep = np.empty(ndts)
        self.n_year     = np.empty(ndts)
        self.M_of_t     = np.zeros(3*ndts).reshape(3,ndts)   #not used, but should be defined as plotting function might search for it
        self.T_of_t     = np.empty(2*ndts*self.ngeof,dtype=float).reshape(2,ndts,self.ngeof) #temp. change of atmos.+upper ocean / lower ocean since 1900
        self.F_of_t     = np.zeros(ndts)                     #not used, but should be defined as plotting function might search for it
        #loop over all models
        for j in range(self.ngeof):
            #some short hands
            fco22x = 0.5*self.f4co2[j]
            t2xco2 = 0.5*self.t4co2[j]
            c1     = 1./self.catm[j]
            c2     = fco22x/t2xco2
            c3     = self.gamma[j]
            c4     = self.gamma[j]/self.coce[j]
            #remember the above for later comparison / use
            self.coefs_geof[0:7,j] = np.array([c1, c2, c3, c4, fco22x, t2xco2, c2])  #could I make this a dictionary? Pandas list?
            #set values for time step 0 and some constant values
            self.n_timestep[0] = 0
            self.n_year[0]     = 0
            self.T_of_t[0,0,j] = self.T_ini[0]         #change in atmospheric+upper ocean temperature since 1900
            self.T_of_t[1,0,j] = self.T_ini[1]         #change in lower ocean temperature since 1900
            F_of_t             = fco22x * self.X_x_fco22x
            #now integrate
            for i in range(1, ndts):
                self.n_timestep[i] = i
                self.n_year[i]     = dys*i
                self.T_of_t[0,i,j] = self.T_of_t[0,i-1,j] + dys * c1*( F_of_t - c2*self.T_of_t[0,i-1,j] - c3*(self.T_of_t[0,i-1,j] - self.T_of_t[1,i-1,j]) )
                self.T_of_t[1,i,j] = self.T_of_t[1,i-1,j] + dys * c4*( self.T_of_t[0,i-1,j] - self.T_of_t[1,i-1,j] )

        return


    #benchmark: 100 GtC to atmosphere in 2015, Joos et al. (2013)
    #= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    def BenchMarkJoos(self,TalkTalk=1):

        """Benchmark: 100 GtC puls in 2015, Joos et al. (2013)"""

        #NOTE: Joos et al. (2013) show that the fraction of CO2 remaining in the atmosphere depends on
        #      the background condition and on the pulse height. Particularly interesting are:
        #      Fig.1: climate-carbon-cycle response to 100GtC to PD conditions
        #      Fig.4: Influence of background conditions, climate-carbon-cycle response to 100GtC to PD or PI setup
        #      Fig.6: Influence of pulse size, climate-carbon-cycle response to 100GtC to PI setup
        #      Fig.7: Influence of pulse size and climate-carbon-cycle feedback under PI conditions
        #      More specifically, the fraction of CO2 remaining in the atmosphere ranges around
        #      Fig.1 ---> 0.6       / 0.5       / 0.4         after 20 / 40 / 100 years, for 100GtC to PD conditions, the two sigma range is about +/-0.1 
        #      Fig.4 ---> 0.55-0.70 / 0.45-0.60 / 0.35-0.50   after 20 / 40 / 100 years, for 100GtC to PD conditions
        #      Fig.4 ---> 0.40-0.55 / 0.35-0.45 / 0.25-0.35   after 20 / 40 / 100 years, for 100GtC to PI conditions
        #      Fig.6 ---> 0.40-0.55 / 0.30-0.45 / 0.25-0.35   after 20 / 40 / 100 years, for 100GtC to PI conditions
        #      Fig.6 ---> 0.80-0.90 / 0.70-0.90 / 0.60-0.80   after 20 / 40 / 100 years, for 5000GtC to PI conditions
        #      Fig.7 ---> 0.55      / 0.45      / 0.35        after 20 / 40 / 100 years, for 100GtC to PI conditions with climate-carbon-cycle
        #      Fig.7 ---> 0.45      / 0.35      / 0.25        after 20 / 40 / 100 years, for 100GtC to PI conditions without climate-carbon-cycle
        #      Fig.7 ---> 0.90      / 0.85      / 0.80        after 20 / 40 / 100 years, for 5000GtC to PI conditions with climate-carbon-cycle
        #      Fig.7 ---> 0.80      / 0.70      / 0.60        after 20 / 40 / 100 years, for 5000GtC to PI conditions without climate-carbon-cycle
        #
        #      100GtC into PD atmosphere  -> ~58% / ~48% / ~42% remaining after 20 / 40 / 60 years (Fig.8)
        #      1000GtC into PD atmosphere -> ~65% / ~58% / ~52% remaining after 20 / 40 / 60 years (Fig.8)
        #      100GtC into PI atmosphere  -> ~48% / ~38% / ~32% remaining after 20 / 40 / 60 years (Fig.4)
        #
        # Entries are irf-fit-coefs for
        #    atmosphere for individual models                                                    [Table S1 in J13]    [given in first line below,  nati=16 in total]
        #    atmosphere for multi model mean (MMM)                                               [Table 5 in J13]     [given in second line below, natm=1  in total]
        #    atmosphere for Bern3D-LPJ specific simulations PI & PD & w & w/o clim. feedback     [Table S2 in J13]    [given in second line belwo, natb=4  in total]
        #    ocean, land, and sat multi model mean (MMM)                                         [Table 5 in J13]     [given in second line below, noth=3  in total]
        # Units: IRF(CO2) atmosphere, IRF(GtC) ocean, IRF(GtC) land, IRF(Celsius) SAT
        # The individual models are:
        # NCAR       CSM1.4    HadGEM2-ES    MPI-ESM    Bern3D-LPJ-r    Bern3D-LPJ-e    CLIMBER2-LPJ    DCESS    GENIEe ...
        # LOVECLIM   MESMO     UVic2.9       ACC2       Bern-SAR        MAGICC6e        TOTEM2
        self.ja0 = np.array([2.935e-7, 0.4340, 1.252e-7,   6.345e-10,  0.2796, 0.2362,   0.2318, 0.2159, 0.2145, 8.539e-8, 0.2848, 0.3186, 0.1779, 0.1994, 0.2051, 7.177e-6, \
                             0.2173,   0.1266, 0.1332,     0.6345e-10, 0.2123, 60.29, 17.07, 0.1383])
        self.ja1 = np.array([0.3665,   0.1973, 0.5846,     0.5150,     0.2382, 9.866e-2, 0.2756, 0.2912, 0.2490, 0.3606,   0.2938, 0.1748, 0.1654, 0.1762, 0.2533, 0.2032,   \
                             0.2240,   0.2607, 0.1663,     0.5150,     0.2444, -26.48,   332.1,  0.05789])
        self.ja2 = np.array([0.3542,   0.1889, 0.1826,     0.2631,     0.2382, 0.3850,   0.4900, 0.2410, 0.1924, 0.4503,   0.2382, 0.1921, 0.3796, 0.3452, 0.3318, 0.6995,   \
                             0.2824,   0.2909, 0.3453,     0.2631,     0.3360, -17.45,  -334.1, -0.06729])
        self.ja3 = np.array([0.2793,   0.1798, 0.2310,     0.2219,     0.2440, 0.2801,   2.576e-3, 0.2518, 0.3441, 0.1891,   0.1831, 0.3145, 0.2772, 0.2792, 0.2098, 9.738e-2, \
                             0.2763,   0.3218, 0.3551,     0.2219,     0.2073, -16.35,  -15.09, -0.1289])
        self.jt1 = np.array([1691.,    23.07,  178.1,      1955.,      276.2,  232.1,    272.6,  379.9,  270.1,  1596.,    454.3,  304.6,  386.2,  333.1,  596.1,  85770.,   \
                             394.4,    302.8,  313.3,      1955.,      336.4,  390.5,    74.76,  264.0])
        self.jt2 = np.array([28.36,    23.07,  9.039,      45.83,      38.45,  58.50,    6.692,  36.31,  39.32,  21.71,    25.00,  26.56,  36.89,  39.69,  21.97,  111.8,    \
                             36.54,    31.61,  29.99,      45.83,      27.89,  100.5,    70.31,  5.818])
        self.jt3 = np.array([5.316,    3.922,  8.989,      3.872,      4.928,  2.587,    6.692,  3.398,  4.305,  2.281,    2.014,  3.800,  3.723,  4.110,  2.995,  1.5832e-2,\
                             4.304,    4.240,  4.601,      3.872,      4.055,  4.551,    6.139,  0.8062])
        self.nati=16;    self.natm=1;    self.natb=4;    self.noth=3;
        self.nirfa = self.nati+self.natm+self.natb    #number of atmospheric models, including MMM and 4 from Bern
        self.nirf  = self.nirfa+self.noth;            #number of impuls response functions, all atmosphereic plus 3 more for ocean, land, sat

        #some short hands
        ndts  = self.ndts
        nirf  = self.nirf                       #total number of irfs, i.e., atmosphere & ocean, land, sat (three more than atmosphere only)
        nirfa = self.nirfa                      #number of irfs related to atmosphere ---> dimension for M_of_t[0,:,nirfa]
        jmmm  = self.nati                       #index of multimodel mean; needed to fill M_of_t[1,:,jmmm] and M_of_t[2,:,jmmm] for ocean and land carbon mass
        A     = self.A
        #define arrays for integration
        self.n_timestep = np.empty(ndts)                                             #timestep
        self.n_year     = np.empty(ndts)                                             #year
        self.M_of_t     = np.empty(3*ndts*nirfa,dtype=float).reshape(3,ndts,nirfa)   #carbon mass in each reservoir
        self.T_of_t     = np.empty(ndts,dtype=float)                                 #atmos.temp. and - to be filled in TestDef.py - of atmos.temp. for fixed carbon mass of 851 GtC
        self.F_of_t     = np.zeros(ndts)                                             #not used, but should be defined as plotting function might search for it
        self.irf        = np.empty(ndts*nirf,dtype=float).reshape(ndts,nirf)         #impulse response functions
        #values at start time
        self.n_timestep[0] = 0
        self.n_year[0]     = self.beg_yr
        #now integrate
        for i in range(0, ndts):
            self.n_timestep[i] = i
            self.n_year[i]     = self.dys*i
            #all impuls response functions
            for j in range(0,nirf):
                self.irf[i,j] = self.ja0[j] + self.ja1[j]*np.exp(-self.n_year[i]/self.jt1[j]) +\
                                              self.ja2[j]*np.exp(-self.n_year[i]/self.jt2[j]) +\
                                              self.ja3[j]*np.exp(-self.n_year[i]/self.jt3[j]) 
            #carbon in atmosphere [GtC]
            for j in range(0,nirfa):
                self.M_of_t[0,i,j] = self.M_ini[0] + self.M_puls*self.irf[i,j]
            #carbon in ocean [GtC]
            self.M_of_t[1,i,jmmm]  = self.M_ini[1]
            #carbon in land [GtC]
            self.M_of_t[2,i,jmmm]  = self.M_ini[2]
            #surface air temperature [Celsius]
            self.T_of_t[i]       = self.T_ini[0] + self.irf[i,nirf-1]

        return

    
