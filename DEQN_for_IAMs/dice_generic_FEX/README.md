## What is in the folder

This folder contains the source code for running a common solution routine for the optimal solution of the climate-economy models presented in the appendix. The solution results as well as pretrained models for a replication are stored in the folder [appendix_results](appendix_results).

## How to run the optimal solution with an alternative exogenous forcings function routine
To start the computation from scratch, change the following specifications in the config file (config/config.yaml),
while leaving the other entries untouched:

```
defaults:
  - constants: dice_generic_XXX
  - net: dice_generic
  - optimizer: dice_generic
  - run:  dice_generic_1yts
  - variables: dice_generic_XXX


MODEL_NAME:  dice_generic_FEX
```
XXX stands for the specific parametrisation of the model, that are presented below.

Thereafter, make sure you are at the root directory of DEQN (e.g., ~/DEQN_for_IAMs), and
execute:

```
python run_deepnet.py
```

## How to analyze the pre-computed solutions

To analyze the the raw results presentended in the article (model XXX), you need to
perform two steps.


```
export USE_CONFIG_FROM_RUN_DIR=<PATH_TO_THE_FOLDER>/Climate_in_Climate_Economics/DEQN_for_IAMS/<MODEL_FOLDER>

python post_process_generic.py STARTING_POINT=LATEST hydra.run.dir=$USE_CONFIG_FROM_RUN_DIR

```

For more details regarding the postprocessing of results, please go to the README [here](../README.md).

## Which models can I run with this routine?
This routine can be used to find an optimal solution to the following models:

**CDICE-FEX:**

To run the model:

```
  - constants: dice_generic_mmm_mmm
  - net: dice_generic
  - optimizer: dice_generic
  - run:  dice_generic_1yts
  - variables: dice_generic_mmm_mmm
```

To postprocess:

```
  <MODEL_FOLDER> = dice_generic_FEX/appendix_results/CDICE_FEX
```

********************************************************************************

**DICE-2016-FEX:**

To run the model:

```
  - constants: dice_generic_2016
  - net: dice_generic
  - optimizer: dice_generic
  - run:  dice_generic_1yts
  - variables: dice_generic_2016
```
To postprocess:

```
  <MODEL_FOLDER> = dice_generic_FEX/appendix_results/DICE2016_FEX
```
