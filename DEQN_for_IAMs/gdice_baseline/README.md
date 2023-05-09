## How to run the business-as-usual soltuion routine
To start the computation from scratch, change the following specifications in the config file (config/config.yaml),
while leaving the other entries untouched:

```
defaults:
  - constants: gdice_baseline_XXX
  - net: gdice_baseline_XXX
  - optimizer: gdice_baseline
  - run:  gdice_baseline_1yts
  - variables: gdice_baseline_XXX


MODEL_NAME:  gdice_baseline
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
export USE_CONFIG_FROM_RUN_DIR=PATH_XXX

python post_process_baseline.py STARTING_POINT=LATEST hydra.run.dir=$USE_CONFIG_FROM_RUN_DIR

```

For more details regarding the postprocessing of results, please go to the README [here](../README.md).


## Which models can I run with this routine?
This routine can be used to find a business-as-usual solution to the following models:

**CDICE; CDICE, psi=0.69:** 

To run the model:

```
  - constants: gdice_baseline_mmm_mmm
  - net: gdice_baseline
  - variables: gdice_baseline_mmm_mmm
```

To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_cdice
```

**CDICE-GISS-E2-R; CDICE-GISS-E2-R, psi=0.69:**

To run the model:

```
  - constants: gdice_baseline_mmm_giss
  - net: gdice_baseline_GISS-E2-R
  - variables: gdice_baseline_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_giss
```

**CDICE-HadGEM2-ES; CDICE-HadGEM2-ES, psi = 0.69:**

To run the model:

```
  - constants: gdice_baseline_mmm_hadgem
  - net: gdice_baseline_HadGEM2-ES
  - variables: gdice_baseline_mmm_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_hadgem
```

**CDICE-MESMO:**

To run the model:

```
  - constants: gdice_baseline_mmm_mesmo
  - net: gdice_baseline
  - variables: gdice_baseline_mmm_mesmo
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_mesmo
```

**CDICE-LOVECLIM:**

To run the model:

```
  - constants: gdice_baseline_mmm_loveclim
  - net: gdice_baseline
  - variables: gdice_baseline_mmm_loveclim
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_loveclim
```

**CDICE-MESMO-GISS-E2-R:**

To run the model:

```
  - constants: gdice_baseline_mesmo_giss
  - net: gdice_baseline_GISS-E2-R
  - variables: gdice_baseline_mesmo_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mesmo_giss
```

**CDICE-MESMO-HadGEM2-ES:**

To run the model:

```
  - constants: gdice_baseline_mesmo_hadgem
  - net: gdice_baseline_HadGEM2-ES
  - variables: gdice_baseline_mesmo_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mesmo_hadgem
```

**CDICE-LOVECLIM-GISS-E2-R:**

To run the model:

```
  - constants: gdice_baseline_loveclim_giss
  - net: gdice_baseline_GISS-E2-R
  - variables: gdice_baseline_loveclim_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_loveclim_giss
```

**CDICE-LOVECLIM-HadGEM2-ES:**

To run the model:

```
  - constants: gdice_baseline_loveclim_hadgem
  - net: gdice_baseline_HadGEM2-ES
  - variables: gdice_baseline_loveclim_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_loveclim_hadgem
```

**DICE-2016; DICE-2016, psi=0.69:**

To run the model:

```
  - constants: gdice_baseline_2016
  - net: gdice_baseline
  - variables: gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_dice2016
```

**CDICE with carbon cycle from DICE-2016:**

To run the model:

```
  - constants: gdice_baseline_dice16_mmm
  - net: gdice_baseline
  - variables: gdice_baseline_dice16_mmm
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_CDICE_with_DICE16CC
```

**DICE-2016, ECS=4.55; DICE-2016, psi=0.69, ECS=4.55:**

To run the model:

```
  - constants: gdice_baseline_2016_ecs455
  - net: gdice_baseline
  - variables: gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_dice2016_ecs455
```

**DICE-2016, ECS=2.15; DICE-2016, psi=0.69, ECS=2.15:**

To run the model:

```
  - constants: gdice_baseline_2016_ecs215
  - net: gdice_baseline
  - variables: gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/BAU_dice2016_ecs215
```

**CDICE, psi=2.:**

To run the model:

```
  - constants: gdice_baseline_mmm_mmm_IES2
  - net: gdice_baseline
  - variables: gdice_baseline_mmm_mmm
```

To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_mmm_mmm
```

**CDICE-GISS-E2-R, psi=2.:**

To run the model:

```
  - constants: gdice_baseline_mmm_giss_IES2
  - net: gdice_baseline_GISS-E2-R
  - variables: gdice_baseline_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_mmm_giss
```

**CDICE-HadGEM2-ES, psi = 2.:**

To run the model:

```
  - constants: gdice_baseline_mmm_hadgem_IES2
  - net: gdice_baseline_HadGEM2-ES
  - variables: gdice_baseline_mmm_hadgem
```

To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_mmm_hadgem
```

**CDICE, psi=0.5:**

To run the model:

```
  - constants: gdice_baseline_mmm_mmm_IES05
  - net: gdice_baseline
  - variables: gdice_baseline_mmm_mmm
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_mmm_mmm
```

**CDICE-GISS-E2-R, psi=0.5:**

To run the model:

```
  - constants: gdice_baseline_mmm_giss_IES05
  - net: gdice_baseline_GISS-E2-R
  - variables: gdice_baseline_mmm_giss
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_mmm_giss
```

**CDICE-HadGEM2-ES, psi = 0.5:**

To run the model:

```
  - constants: gdice_baseline_mmm_hadgem_IES05
  - net: gdice_baseline_HadGEM2-ES
  - variables: gdice_baseline_mmm_hadgem
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_mmm_hadgem
```

**DICE-2016, psi=2..:**

To run the model:

```
  - constants: gdice_baseline_2016_ies2
  - net: gdice_baseline
  - variables: gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_dice16
```


**DICE-2016, psi=2., ECS=4.55:**

To run the model:

```
  - constants: gdice_baseline_2016_ies2_ecs455
  - net: gdice_baseline
  - variables: gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_dice16_ecs455
```

**DICE-2016, psi=2., ECS=2.15:**

To run the model:

```
  - constants: gdice_baseline_2016_ies2_ecs215
  - net: gdice_baseline
  - variables:  gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_dice16_ecs215
```

**DICE-2016, psi=0.5.:**

To run the model:

```
  - constants: gdice_baseline_2016_ies05
  - net: gdice_baseline
  - variables:  gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_dice16
```

**DICE-2016, psi=0.5, ECS=4.55:**

To run the model:

```
  - constants: gdice_baseline_2016_ies05_ecs455
  - net: gdice_baseline
  - variables:  gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_dice16_ecs455
```

**DICE-2016, psi=0.5., ECS=2.15:**

To run the model:

```
  - constants: gdice_baseline_2016_ies05_ecs215
  - net: gdice_baseline
  - variables:  gdice_baseline_2016
```
To postprocess:

```
  PATH_XXX = DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_dice16_ecs215
```

## Note
Current version of the code is generic and covers for both deterministic and stochastic (in a sense of TFP shock) solution of the model. Stochastic shock to TFP can be enabled in Dynamics.py, however, it is not needed for the replication purposes.
