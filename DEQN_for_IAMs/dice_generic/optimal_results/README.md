## What is in the folder

This folder contains the simulation results for optimal solution of each model as well as the files needed for the postprocesing of each model. Simulation results are stored in the ```*.csv``` files and then used in the scripts for [figures_replication](../../../figures_replication).

## How to analyze the pre-computed solutions

For details regarding the postprocessing of optimal results, please go to the README [here](../README.md).

To replicate graphs that are presented in the paper, please refer to [here](../../../figures_replication).

#Note
The solutions for the models: CDICE-GISS-E2-R with psi=0.5 and CDICE-HadGEM2-ES with psi=0.5 are large, thus they are stored in the archives. To access the files needed for postprocessing do following:

1. go to the folder DEQN_for_IAMS/dice_generic/optimal_results/IES05/Opt_mmm_giss_psi05 and unpack the following archive:
```
tar -xf NN_data.tar.xz
```
2. go to the folder DEQN_for_IAMS/dice_generic/optimal_results/IES05/Opt_mmm_hadgem_psi05 and unpack the following archive:
```
tar -xf NN_data.tar.xz
```
To run the postprocessing make sure that the content of the folder ```NN_data``` is stored in the respective folder of the model, otherwise, one needs to modify a postprocessing path ```ABS_PATH_TO_RESTART_FOLDER``` [here](../README.md).
