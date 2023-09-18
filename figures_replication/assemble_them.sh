#!/bin/bash
#
# Shell script to bundle individual figures into figures for article / overleaf
#
# Figures come from Figs4Paper.py, which, in turn, exploits TestDefs.py and ClimDICE.py
#
#-append assembles into columns (vertical)
#+append assembles into rows (horizontal)

#Fig.0: CMIP5 concentrations, emissions, forcing from concentrations
convert +append CMIP_RCP_EMI_GtC.png CMIP_RCP_CONC_ppm.png CMIP_RCP_CONC_Forc_Wm2.png CMIP_EMI_CONC_FORC.png

#Fig.1: 4xCO2 G13
convert +append TempBM_4xCO2_on_PI_20yr.png TempBM_4xCO2_on_PI_200yr.png TempBM_4xCO2_on_PI_1000yr.png TempBM_4xCO2_on_PI.png

#Fig.2: 4xCO2 G13, parameter sensitivities
convert +append Mod_TempBM_4xCO2_on_PI_10yr.png Mod_TempBM_4xCO2_on_PI_100yr.png Mod_TempBM_4xCO2_on_PI_1000yr.png Mod_TempBM_4xCO2_on_PI.png

#Fig.3: 1pctCO2
convert +append CMIPBM_1pctCO2_Temp_70yr.png CMIPBM_1pctCO2_Temp_140yr.png CMIPBM_1pctCO2.png

#Fig.4: 100GtC J13
convert +append CCBM_100GtC_Puls_MassFrac_20yr.png CCBM_100GtC_Puls_MassFrac_200yr.png CCBM_100GtC_Puls_MassFrac_1000yr.png CCBM_100GtC_Puls.png

#Fig.5: 100GtC J13, parameter sensitivities
convert +append Mod_CCBM_100GtC_Puls_MassFrac_20yr.png Mod_CCBM_100GtC_Puls_MassFrac_200yr.png Mod_CCBM_100GtC_Puls_MassFrac_1000yr.png Mod_CCBM_100GtC_Puls.png

#Fig.6: CMIP5 comparison, hist+rcp
convert +append CMIPBM_RCP26_EMI_PPM.png CMIPBM_RCP26_CONC_Temp.png CMIPBM_RCP26_EMI_Temp.png row01.png
convert +append CMIPBM_RCP45_EMI_PPM.png CMIPBM_RCP45_CONC_Temp.png CMIPBM_RCP45_EMI_Temp.png row02.png
convert +append CMIPBM_RCP60_EMI_PPM.png CMIPBM_RCP60_CONC_Temp.png CMIPBM_RCP60_EMI_Temp.png row03.png
convert +append CMIPBM_RCP85_EMI_PPM.png CMIPBM_RCP85_CONC_Temp.png CMIPBM_RCP85_EMI_Temp.png row04.png
convert -append row01.png row02.png row03.png row04.png CMIPBM.png

 
