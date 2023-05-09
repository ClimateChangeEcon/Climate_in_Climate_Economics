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

To analyze the the raw results presentended in the article (model XYZ), you need to
perform two steps.


```
export USE_CONFIG_FROM_RUN_DIR=PATH_XXX

python post_process_time.py STARTING_POINT=LATEST hydra.run.dir=$USE_CONFIG_FROM_RUN_DIR

```

For more details regarding the postprocessing of results, please go to the README [here](../README.md).

## Which models can I run with this routine?
This routine can be used to find a business-as-usual solution to the following models:

**CDICE-FEX:** 

To run the model:

```
  - constants: dice_generic_mmm_mmm
  - variables: dice_generic_mmm_mmm
```

To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic_FEX/appendix_results/CDICE_FEX
```

**DICE-2016-FEX:**

To run the model:

```
  - constants: dice_generic_2016
  - variables: dice_generic_2016_FEX
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic_FEX/appendix_results/DICE2016_FEX
```

## Note
Current version of the code is generic and covers for both deterministic and stochastic (in a sense of TFP shock) solution of the model. Stochastic shock to TFP can be enabled in Dynamics.py, however, it is not needed for the replication purposes.
