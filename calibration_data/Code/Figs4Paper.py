#
# Python script to produce figures for paper "The climate of DICE"
# Input:  what figures to do
# Output: the figures, as pngs
# To run: exec(open("./Figs4Paper.py").read())
#
# The script relies on TestDefs.py
# Figures / Tests are hard wired
# User can choose (yes/no) what pre-defined figures to actually produce
#
# i=0
# sisi=df2['simu'][i]
# sisi.dys
#
#import libraries we will need
#========================================================================================
import importlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ClimDICE as cld
import TestDefs as td

importlib.reload(cld)
importlib.reload(td)

#user defined input starts here
#========================================================================================

#what sets of figures to plot / not plot? ('yes'/'no')

#CE calibration and associated sensitivity, Joos et al. (2013) for carbon cycle and Geoffroy et al. (2013) for temperature
F_G13     = 'yes'   #G13 test; Figs: temp.
F_G13S    = 'no'   #G13 param.sens; Figs: temp.
F_J13     = 'yes'   #J13 test; Figs: mass frac. puls / CO2 conc. / temp.
F_J13M    = 'no'   #J13 test, modified DICE params; Figs: mass frac. puls / CO2 conc. / temp. 

#test case: one percent per year increase of atmospheric CO2 concentration; temperature response
F_1pctCO2 = 'no'   #CMIP5, 1pctCO2; Figs: temp.

#test cases: CMIP5 RCPS, using CO2 concentrations as input to the CE
F_RCP26C  = 'no'   #CMIP5, RCP26 from conc.; Figs: temp.
F_RCP45C  = 'no'   #CMIP5, RCP45 from conc.; Figs: temp.
F_RCP60C  = 'no'   #CMIP5, RCP60 from conc.; Figs: temp.
F_RCP85C  = 'no'   #CMIP5, RCP85 from conc.; Figs: temp.

#test cases: CMIP5 RCPS, using carbon emissions as input to the CE
F_RCP26E  = 'no'   #CMIP5, RCP26 from emi.; Figs: temp. / CO2 conc.
F_RCP45E  = 'no'   #CMIP5, RCP45 from emi.; Figs: temp. / CO2 conc.
F_RCP60E  = 'no'   #CMIP5, RCP60 from emi.; Figs: temp. / CO2 conc.
F_RCP85E  = 'no'   #CMIP5, RCP85 from emi.; Figs: temp. / CO2 conc.

#various plots illustrating additional variables (forcing, sensitivity of temperature to F_Ext term...)
F_FEX26C  = 'no'  #CMIP5, RCP26 from conc., sensitivity to non-co2 forcing; Figs: temp.
F_FEX45C  = 'no'  #CMIP5, RCP45 from conc., sensitivity to non-co2 forcing; Figs: temp.
F_FEX60C  = 'no'  #CMIP5, RCP60 from conc., sensitivity to non-co2 forcing; Figs: temp.
F_FEX85C  = 'no'  #CMIP5, RCP85 from conc., sensitivity to non-co2 forcing; Figs: temp.
F_FEX26E  = 'no'  #CMIP5, RCP26 from emi., sensitivity to non-co2 forcing; Figs: temp.
F_FEX45E  = 'no'  #CMIP5, RCP45 from emi., sensitivity to non-co2 forcing; Figs: temp.
F_FEX60E  = 'no'  #CMIP5, RCP60 from emi., sensitivity to non-co2 forcing; Figs: temp.
F_FEX85E  = 'no'  #CMIP5, RCP85 from emi., sensitivity to non-co2 forcing; Figs: temp.

F_ERCPE   = 'no'  #plot carbon emissions for different hist+RCPs, emissions as input
F_FRCPE   = 'no'  #plot forcing for different hist+RCPs, emission fed, emissions as input
F_CRCPC   = 'no'  #plot CO2 concentrations different hist+RCPs, CO2 concentrations as input
F_FRCPC   = 'no'  #plot forcing for different hist+RCPs, emission fed, CO2 concentrations as input

#user defined input ends here
#========================================================================================


#testing only the climate (temperature) part of DICE [CO2 concentrations prescribed]
#========================================================================================
#4xCO2 benchmark from Geoffrey et al. (2013)
if (F_G13 == 'yes'):
    #del df2
    df2 = td.BenchMark4xCO2()
    td.Plot4xCO2Temp(df2, axis_range=[0.,20.,0.,9.0], fout='TempBM_4xCO2_on_PI_20yr.png')
    td.Plot4xCO2Temp(df2, axis_range=[0.,200.,0.,9.0], leg='no', fout='TempBM_4xCO2_on_PI_200yr.png')
    td.Plot4xCO2Temp(df2, axis_range=[0.,1000.,0.,9.0], leg='no', fout='TempBM_4xCO2_on_PI_1000yr.png')

#4xCO2 benchmark from Geoffrey et al. (2013), sensitivity to parameters
if (F_G13S == 'yes'):
    #del df2
    df2 = td.BenchMark4xCO2Mod()
    #td.Plot4xCO2Temp(df2,axis_range=[0.,10.,0.,4.0],geoff_yn='yes',geoff_indi='no',leg='yes',fout='Mod_TempBM_4xCO2_on_PI_10yr.png')
    td.Plot4xCO2Temp(df2,axis_range=[0.,10.,0.,4.0],geoff_yn='yes',geoff_indi='no',leg='yes',fsl=10,lsp=-0.05,fout='Mod_TempBM_4xCO2_on_PI_10yr.png')
    td.Plot4xCO2Temp(df2,axis_range=[0.,100.,0.,6.0],geoff_yn='yes',geoff_indi='no',leg='no',fout='Mod_TempBM_4xCO2_on_PI_100yr.png')
    td.Plot4xCO2Temp(df2,axis_range=[0.,1000.,0.,8.0],geoff_yn='yes',geoff_indi='no',leg='no',fout='Mod_TempBM_4xCO2_on_PI_1000yr.png')
    #td.Plot4xCO2Temp(df2,axis_range=[0.,1000.,0.,9.0],geoff_yn='yes',geoff_indi='no',leg='no',fout='Mod_TempBM_4xCO2_on_PI_1000yr.png')

#CMIP5, 1pct CO2 increase from 1850 onward
if (F_1pctCO2 == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='1pctCO2')
    td.PlotTDTemp(df2,axis_range=[0.,70.,-0.2,3.],avyr=10,pad=1.8,fsl=11, fout="CMIPBM_1pctCO2_Temp_70yr.png")
    td.PlotTDTemp(df2,axis_range=[0.,140.,-0.2,6.],avyr=10,pad=1.8,leg='no',fout="CMIPBM_1pctCO2_Temp_140yr.png")
    td.PlotTDMassPPM(df2,axis_range=[0.,140.,250.,1200.],skip_simu=[1,2,3,4,5,6],pm5pct='no',fout="CMIPBM_1pctCO2_PPM.png")

#CMIP5, historical plus RCP26 from CO2 concentrations
if (F_RCP26C == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP26_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,3.5],avyr=50,fout="CMIPBM_RCP26_CONC_Temp.png", fsl=11, leg='yes')

#CMIP5, historical plus RCP45 from CO2 concentrations
if (F_RCP45C == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP45_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,4.5],avyr=50,fout="CMIPBM_RCP45_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP60 from CO2 concentrations
if (F_RCP60C == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP60_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,5.],avyr=50,fout="CMIPBM_RCP60_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP85 from CO2 concentrations
if (F_RCP85C == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP85_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,6.],avyr=50,fout="CMIPBM_RCP85_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP26 from CO2 concentrations, sensitivity to external, non-co2 forcing
if (F_FEX26C == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP26_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,3.5],avyr=50,fout="CMIPBM_FEXT_RCP26_CONC_Temp.png", fsl=11, leg='yes')

#CMIP5, historical plus RCP45 from CO2 concentrations, sensitivity to external, non-co2 forcing
if (F_FEX45C == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP45_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,4.5],avyr=50,fout="CMIPBM_FEXT_RCP45_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP60 from CO2 concentrations, sensitivity to external, non-co2 forcing
if (F_FEX60C == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP60_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,5.],avyr=50,fout="CMIPBM_FEXT_RCP60_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP85 from CO2 concentrations, sensitivity to external, non-co2 forcing
if (F_FEX85C == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP85_CONC')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,6.],avyr=50,fout="CMIPBM_FEXT_RCP85_CONC_Temp.png", leg='no')

#CMIP5, historical plus RCP, CO2 concentrations, concentrations as input
if (F_CRCPC == 'yes'):
    df_26=td.BenchMarkTDEmiOrConc(CMIP='RCP26_CONC')
    df_45=td.BenchMarkTDEmiOrConc(CMIP='RCP45_CONC')
    df_60=td.BenchMarkTDEmiOrConc(CMIP='RCP60_CONC')
    df_85=td.BenchMarkTDEmiOrConc(CMIP='RCP85_CONC')
    td.PlotConcCMIPppm(df_26, df_45, df_60, df_85,axis_range=[1850.,2100.,250.,950.],skip_simu=[0,2,3,4,5,6,7,8,9],fout="CMIP_RCP_CONC_ppm.png", leg='no')

#CMIP5, historical plus RCP, forcing, CO2 concentrations as input
if (F_FRCPC == 'yes'):
    df_26=td.BenchMarkTDEmiOrConc(CMIP='RCP26_CONC')
    df_45=td.BenchMarkTDEmiOrConc(CMIP='RCP45_CONC')
    df_60=td.BenchMarkTDEmiOrConc(CMIP='RCP60_CONC')
    df_85=td.BenchMarkTDEmiOrConc(CMIP='RCP85_CONC')
    td.PlotForcWm2CMIP(df_26, df_45, df_60, df_85,axis_range=[1850.,2100.,0.,8.],skip_simu=[0,2,3,4,5,6,7,8,9],fout="CMIP_RCP_CONC_Forc_Wm2.png", leg='no')



    
#testing the carbon cycle part of DICE (including climate part, but DICE only couples CC -> temp)
#========================================================================================
#100GtC puls to PD atmosphere benchmark from  Joos et al. (2013)
if (F_J13 == 'yes'): 
    #del df2
    df2 = td.BenchMarkPuls()
    td.PlotPulsMassFrac(df2, axis_range=[0.,20.,0.1,1.0], fout='CCBM_100GtC_Puls_MassFrac_20yr.png', joos_yn='yes',joos_indi='yes',fsl=11,lsp=0.08,leg='yes')
    td.PlotPulsMassFrac(df2, axis_range=[0.,200.,0.1,1.0], fout='CCBM_100GtC_Puls_MassFrac_200yr.png', joos_yn='yes',joos_indi='yes',fsl=11,lsp=0.08,leg='no')
    td.PlotPulsMassFrac(df2, axis_range=[0.,1000.,0.1,1.0], fout='CCBM_100GtC_Puls_MassFrac_1000yr.png', joos_yn='yes',joos_indi='yes',fsl=11,lsp=0.08,leg='no')
    #td.PlotPulsMassPPM(df2, axis_range=[0.,150.,10.,50.], fout='CCBM_100GtC_Puls_PPM.png', skip_simu=[2], joos_yn='yes',leg='no')  #Fig. 3 in Dietz et al. (2020)
    #td.PlotPulsTemp(df2, axis_range=[0.,150.,0.,0.3], fout='CCBM_100GtC_Puls_Temp.png', skip_simu=[2], joos_yn='yes',leg='no')
    #td.PlotAbsForcWm2(df2)


#100GtC puls to PD atmosphere benchmark from  Joos et al. (2013)
if (F_J13M == 'yes'):
    #del df2
    df2 = td.BenchMarkPulsMod()
    #td.PlotPulsMassPPM(df2, axis_range=[0.,200.,0.,50.], fout='Mod_CCBM_100GtC_Puls_PPM.png', joos_yn='yes')
    td.PlotPulsMassFrac(df2, axis_range=[0.,20.,0.2,1.0], fout='Mod_CCBM_100GtC_Puls_MassFrac_20yr.png',joos_yn='yes',joos_indi='yes',joos_indi2='no',fsl=12,lsp=0.08,leg='yes')
    td.PlotPulsMassFrac(df2, axis_range=[0.,200.,0.2,1.0], fout='Mod_CCBM_100GtC_Puls_MassFrac_200yr.png', joos_yn='yes', joos_indi='yes', joos_indi2='no', leg='no')
    td.PlotPulsMassFrac(df2, axis_range=[0.,1000.,0.2,1.0], fout='Mod_CCBM_100GtC_Puls_MassFrac_1000yr.png', joos_yn='yes', joos_indi='yes', joos_indi2='no', leg='no')
    #td.PlotPulsTemp(df2, axis_range=[0.,20.,0.,0.3], fout='Mod_CCBM_100GtC_Puls_Temp_20yr.png', skip_simu=[], joos_yn='yes', leg='no')
    #td.PlotPulsTemp(df2, axis_range=[0.,200.,0.,0.3], fout='Mod_CCBM_100GtC_Puls_Temp_200yr.png', skip_simu=[], joos_yn='yes', leg='no')
    #td.PlotPulsTemp(df2, axis_range=[0.,1000.,0.,0.3], fout='Mod_CCBM_100GtC_Puls_Temp_1000yr.png', skip_simu=[], joos_yn='yes', leg='no')

#CMIP5, historical plus RCP26 from carbon emissions
if (F_RCP26E == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP26_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,3.5],avyr=50,fout="CMIPBM_RCP26_EMI_Temp.png", fsl=11, leg='yes')
    td.PlotTDMassPPM(df2,axis_range=[1850.,2100.,250.,550.],skip_simu=[2,3,6,7,8,9],cmip_indi='no',pm5pct='yes',fout="CMIPBM_RCP26_EMI_PPM.png", fsl=11, leg='yes')

#CMIP5, historical plus RCP45 from carbon emissions
if (F_RCP45E == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP45_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,4.5],avyr=50,fout="CMIPBM_RCP45_EMI_Temp.png", leg='no')
    td.PlotTDMassPPM(df2,axis_range=[1850.,2100.,250.,700.],skip_simu=[2,3,6,7,8,9],cmip_indi='no',pm5pct='yes',fout="CMIPBM_RCP45_EMI_PPM.png", leg='no')

#CMIP5, historical plus RCP60 from carbon emissions
if (F_RCP60E == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP60_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,5.],avyr=50,fout="CMIPBM_RCP60_EMI_Temp.png", leg='no')
    td.PlotTDMassPPM(df2,axis_range=[1850.,2100.,250.,800.],skip_simu=[2,3,6,7,8,9],cmip_indi='no',pm5pct='yes',fout="CMIPBM_RCP60_EMI_PPM.png", leg='no')

#CMIP5, historical plus RCP85 from carbon emissions
if (F_RCP85E == 'yes'):
    df2=td.BenchMarkTDEmiOrConc(CMIP='RCP85_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,6.],avyr=50,fout="CMIPBM_RCP85_EMI_Temp.png", leg='no')
    td.PlotTDMassPPM(df2,axis_range=[1850.,2100.,250.,1100.],skip_simu=[2,3,6,7,8,9],cmip_indi='no',pm5pct='yes',fout="CMIPBM_RCP85_EMI_PPM.png", leg='no')

#CMIP5, historical plus RCP26 from carbon emissions, sensitivity to external, non-co2 forcing
if (F_FEX26E == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP26_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,3.5],avyr=50,fout="CMIPBM_FEXT_RCP26_EMI_Temp.png", leg='no')

#CMIP5, historical plus RCP45 from carbon emissions, sensitivity to external, non-co2 forcing
if (F_FEX45E == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP45_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,4.5],avyr=50,fout="CMIPBM_FEXT_RCP45_EMI_Temp.png", leg='no')

#CMIP5, historical plus RCP60 from carbon emissions, sensitivity to external, non-co2 forcing
if (F_FEX60E == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP60_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,5.],avyr=50,fout="CMIPBM_FEXT_RCP60_EMI_Temp.png", leg='no')

#CMIP5, historical plus RCP85 from carbon emissions, sensitivity to external, non-co2 forcing
if (F_FEX85E == 'yes'):
    df2=td.BenchMarkFextCMIP(CMIP='RCP85_EMI')
    td.PlotTDTemp(df2,axis_range=[1850.,2100.,-0.5,6.],avyr=50,fout="CMIPBM_FEXT_RCP85_EMI_Temp.png", leg='no')

#CMIP5, historical plus RCP, carbon emissions, emissions as input
if (F_ERCPE == 'yes'):
    df_26=td.BenchMarkTDEmiOrConc(CMIP='RCP26_EMI')
    df_45=td.BenchMarkTDEmiOrConc(CMIP='RCP45_EMI')
    df_60=td.BenchMarkTDEmiOrConc(CMIP='RCP60_EMI')
    df_85=td.BenchMarkTDEmiOrConc(CMIP='RCP85_EMI')
    td.PlotEmiCMIPGtC(df_26, df_45, df_60, df_85,axis_range=[1850.,2100.,-1.,30.],skip_simu=[0,2,3,4,5,6,7,8,9],fout="CMIP_RCP_EMI_GtC.png", leg='yes')

#CMIP5, historical plus RCP, forcing, emissions as input
if (F_FRCPE == 'yes'):
    df_26=td.BenchMarkTDEmiOrConc(CMIP='RCP26_EMI')
    df_45=td.BenchMarkTDEmiOrConc(CMIP='RCP45_EMI')
    df_60=td.BenchMarkTDEmiOrConc(CMIP='RCP60_EMI')
    df_85=td.BenchMarkTDEmiOrConc(CMIP='RCP85_EMI')
    td.PlotForcWm2CMIP(df_26, df_45, df_60, df_85,axis_range=[1850.,2100.,0.,8.],skip_simu=[0,2,3,4,5,6,7,8,9],fout="CMIP_RCP_EMI_Forc_Wm2.png", leg='no')


