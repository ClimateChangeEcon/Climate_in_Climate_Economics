## How to run the optimal soltuion routine
To start the computation from scratch, change the following specifications in the config file (config/config.yaml),
while leaving the other entries untouched:

```
defaults:
  - constants: dice_generic_XXX
  - net: dice_generic_XXX
  - optimizer: dice_generic
  - run:  dice_generic_1yts
  - variables:  dice_generic_XXX


MODEL_NAME:  dice_generic
```
XXX stands for the specific parametrisation of the model, that are presented below.

Thereafter, make sure you are at the root directory of DEQN (e.g., ~/DEQN_for_IAMs), and
execute:

```
python run_deepnet.py
```
## How to analyze the pre-computed solutions

To analyze the the raw results presentended in the paper (model XXX), you need to perform two steps.

```
export USE_CONFIG_FROM_RUN_DIR=PATH_XXX

python post_process_time.py STARTING_POINT=LATEST hydra.run.dir=$USE_CONFIG_FROM_RUN_DIR

```

For more details regarding the postprocessing of results, please go to the README [here](../README.md).

## Which models can I run with this routine?
This routine can be used to find an optimal solution to the following models:

**CDICE; CDICE, psi=0.69:** 

To run the model:

```
  - constants: dice_generic_mmm_mmm
  - net: dice_generic
  - variables: dice_generic_mmm_mmm
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/cdice
```

**CDICE-GISS-E2-R; CDICE-GISS-E2-R, psi=0.69:**

```
  - constants: dice_generic_mmm_giss
  - net: dice_generic_GISS-E2-R
  - variables: dice_generic_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/cdice_giss
```

**CDICE-HadGEM2-ES; CDICE-HadGEM2-ES, psi = 0.69:**

```
  - constants: dice_generic_mmm_hadgem
  - net: dice_generic_HadGEM2-ES
  - variables: dice_generic_mmm_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/cdice_hadgem
```

**CDICE-MESMO:**

```
  - constants: dice_generic_mmm_mesmo
  - net: dice_generic
  - variables: dice_generic_mmm_mesmo
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/cdice_mesmo
```

**CDICE-LOVECLIM:**

```
  - constants: dice_generic_mmm_loveclim
  - net: dice_generic
  - variables: dice_generic_mmm_loveclim
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/cdice_loveclim
```

**CDICE-MESMO-GISS-E2-R:**

```
  - constants: dice_generic_mesmo_giss
  - net: dice_generic_GISS-E2-R
  - variables: dice_generic_mesmo_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/mesmo_giss
```

**CDICE-MESMO-HadGEM2-ES:**

```
  - constants: dice_generic_mesmo_hadgem
  - net: dice_generic_HadGEM2-ES
  - variables: dice_generic_mesmo_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/mesmo_hadgem
```

**CDICE-LOVECLIM-GISS-E2-R:**

```
  - constants: dice_generic_loveclim_giss
  - net: dice_generic_GISS-E2-R
  - variables: dice_generic_loveclim_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/loveclim_giss
```

**CDICE-LOVECLIM-HadGEM2-ES:**

```
  - constants: dice_generic_loveclim_hadgem
  - net: dice_generic_HadGEM2-ES
  - variables: dice_generic_loveclim_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/loveclim_hadgem
```
**CDICE, psi=2.:**

```
  - constants: dice_generic_mmm_mmm_IES2
  - net: dice_generic
  - variables: dice_generic_mmm_mmm
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_mmm
```

**CDICE-GISS-E2-R, psi=2.:**

```
  - constants: dice_generic_mmm_giss_IES2
  - net: dice_generic_GISS-E2-R
  - variables: dice_generic_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_giss
```

**CDICE-HadGEM2-ES, psi = 2.:**

```
  - constants: dice_generic_mmm_hadgem_IES2
  - net: dice_generic_HadGEM2-ES
  - variables: dice_generic_mmm_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_hadgem
```

**CDICE, psi=0.5:**

```
  - constants: dice_generic_mmm_mmm_IES05
  - net: dice_generic
  - variables: dice_generic_mmm_mmm
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_mmm
```

**CDICE-GISS-E2-R, psi=0.5:**

```
  - constants: dice_generic_mmm_giss_IES05
  - net: dice_generic_GISS-E2-R
  - variables: dice_generic_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_giss
```

**CDICE-HadGEM2-ES, psi = 0.5:**

```
  - constants: dice_generic_mmm_hadgem_IES05
  - net: dice_generic_HadGEM2-ES
  - variables: dice_generic_mmm_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_hadgem
```

**DICE-2016; DICE-2016, psi=0.69:**

```
  - constants: dice_generic_2016
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/dice2016
```

**DICE-2016, ECS=4.55; DICE-2016, psi=0.69, ECS=4.55:**

```
  - constants: dice_generic_2016_ecs455
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs455
```

**DICE-2016, ECS=2.15; DICE-2016, psi=0.69, ECS=2.15:**

```
  - constants: dice_generic_2016_ecs215
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs215
```

**DICE-2016; DICE-2016, psi=2.:**

```
  - constants: dice_generic_2016_IES2
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16
```

**DICE-2016, psi=2., ECS=4.55:**

```
  - constants: dice_generic_2016_ecs455_IES2
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16_ecs455
```

**DICE-2016, psi=2., ECS=2.15:**

```
  - constants: dice_generic_2016_ecs215_IES2
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16_ecs215
```

**DICE-2016; DICE-2016, psi=0.5:**

```
  - constants: dice_generic_2016_IES05
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16
```

**DICE-2016, psi=0.5, ECS=4.55:**

```
  - constants: dice_generic_2016_ecs455_IES05
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16_ecs455
```

**DICE-2016, psi=0.5., ECS=2.15:**

```
  - constants: dice_generic_2016_ecs215_IES05
  - net: dice_generic
  - variables: dice_generic_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16_ecs215
```

## Note
Current version of the code is generic and covers for both deterministic and stochastic (in a sense of TFP shock) solution of the model. Stochastic shock to TFP can be enabled in Dynamics.py, however, it is not needed for the replication purposes.
