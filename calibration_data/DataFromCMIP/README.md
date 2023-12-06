# CMIP5 output data for Climate Emulator testing

This folder contains benchmark data for the two CMIP5 test cases described in Section 4.4. ('Temperature evolution as atmospheric CO2 increases at 1% per year') and Section 4.5. ('CMIP5 historical and RCP evolution as simulated by CDICE').

The data are based on montly mean global mean surface temperature data from the CMIP5 archive, as downloaded on March 1, 2021, from http://iacweb.ethz.ch/staff/beyerleu/cmip5/. The site offers an easy to use mirror to the full CMIP5 archive at https://esgf-node.llnl.gov/search/cmip5/

The monthly mean data have been aggregated to annual means using cdo (climate data operators, https://code.mpimet.mpg.de/projects/cdo/).
The data comes in netcdf format. 
The number of CMIP5 models available varies with the concrete CMIP5 experiment:

- 27 models for RCP2.6
- 38 models for RCP4.5
- 21 models for RCP6.0
- 40 models for RCP8.5
- 31 models for 1pctCO2

Data from individual model is shown as thin gray lines in Figures 6 (1pctCO2) and 7 (CMIP5 RCPs) of the paper.



