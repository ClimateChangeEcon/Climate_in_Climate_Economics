# Calibration Data for Climate Emulators

The folder contains data and codes used for the calibration of the CE in the CDICE paper, arranged in three sub-folders:

- ['Code'](Code) contains the Python codes used in the CDICE paper to calibrate the climate.
- ['EmiAndConcData'](EmiAndConcData) contains emission data for the different RCPs, as input for the CE.
- ['DataFromCMIP'](DataFromCMIP) contains CMIP5 benchmark data for the different RCPs and the 1pctCO2.

Please see the Readme in the respective folders for details.

    
## Pre-requisites to run the python code

Next to the *standard* Python libraries, we require the following libraries 

- [netCDF4](https://pypi.org/project/netCDF4/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [pandas](https://pypi.org/project/pandas/)
- [importlib](https://pypi.org/project/importlib/)

To install, run for instance:

```
pip install netCDF4
```

For the python code to access the necessary data, make sure to preserve the folder structure of this repo, i.e.: 

```
Code
DataFromCMIP
EmiAndConcData
```


## Usage

We provide implementations that use python 3.

The code consists of the following python scripts

- Figs4Paper.py is the user front end, where you may choose which figures to plot.
- TestDefs.py is called by Figs4Paper, it sets up the simulation to be run for the desired figure.
- ClimDICE.py integrates the CE with a simple forward Euler scheme. 
- Table1.py produces Table 1 in the manuscript.
- Table3.py produces Table 3 in the manuscript.

Technical details for each script are given in the headers the individual *.py files located in ['Code'](Code).

To use the code / reproduce figure panels from the paper:
- edit the file Figs4Paper.py, choose which figure(s) you want to simulate / plot.
- launch python
- run the Figs4Paper.py script

At your command prompt, this may look like this:

```
$ cd Code
$ python
$ exec(open("./Figs4Paper.py").read())
```

