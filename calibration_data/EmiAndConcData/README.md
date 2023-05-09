# CMIP5 input data, historical and RCPs

The folder contains carbon emissions (GtC, fossile, other, total) and concentrations (CO2) as used in CMIP5 historical and RCP scenarios. 

The data was downloaded from the Potsdam Institute for Climate Impact Reasearch from following [URL](http://www.pik-potsdam.de/~mmalte/rcps/). Note that RCP3PD at PIK corresponds to RCP26. Likewise RCP6 at PIK corresponds to RCP60.

The following files contain annual carbon emissions from 1750 to 2500 for the different RCPs:

- RCP26_EMISSIONS.csv
- RCP45_EMISSIONS.csv
- RCP60_EMISSIONS.csv
- RCP85_EMISSIONS.csv

The following files contain annual mean CO2 concentrations from 1750 to 2500 for the different RCPs:

- RCP26_MIDYR_CONC.DAT
- RCP45_MIDYR_CONC.DAT
- RCP60_MIDYR_CONC.DAT
- RCP85_MIDYR_CONC.DAT

The data is read by the [Code](https://github.com/sischei/dummy_repo_CDICE/blob/main/calibration_data/Code), by the script ClimDICE.py, via the function LoadEmiAndConcData.

