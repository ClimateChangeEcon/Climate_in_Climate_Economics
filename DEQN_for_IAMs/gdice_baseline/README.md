## What is in the folder

This folder contains the source code for running a common solution routine for the business-as-usual solution of the climate-economy models. The solution results as well as pretrained models for a replication are stored in the folder [bau_results](bau_results).


## How to run the business-as-usual solution routine
To start the computation from scratch, change the following specifications in the config file (config/config.yaml), while leaving the other entries untouched:

```
defaults:
  - constants: gdice_baseline_XXX
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
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
export USE_CONFIG_FROM_RUN_DIR=<PATH_TO_THE_FOLDER>/Climate_in_Climate_Economics/DEQN_for_IAMS/<MODEL_FOLDER>

python post_process_baseline.py STARTING_POINT=LATEST hydra.run.dir=$USE_CONFIG_FROM_RUN_DIR

```

For more details regarding the postprocessing of results, please go to the README [here](../README.md).

## How can I replicate the same training routine for the neural network?

For some models the neural network cannot be trained from scratch. To solve these models one needs to rely on the pretrained neural network which can be utilized for further training to solve the problem at hand. For each model below it is indicated how to replicate the solution if pretraining is needed. In case pretraining is needed, one should take the solution of another model specified in the instructions as a pretrained neural net. The training process of the pretrained neural net should be restarted from the latest checkpoint with the parameters of the problem at hand. When nothing is mentioned then the model can be solved from scratch.


## Which models can I run with this routine?
This routine can be used to find a business-as-usual solution to the following models:

**CDICE:**

To run the model:

```
  - constants: gdice_baseline_mmm_mmm
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_mmm
```

To postprocess:

```
    <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_cdice
```

********************************************************************************

**CDICE with carbon cycle from DICE-2016:**

To run the model:

```
  - constants: gdice_baseline_dice16_mmm
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_dice16_mmm
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_CDICE_with_DICE16CC
```

********************************************************************************

**DICE-2016:**

To run the model:

```
  - constants: gdice_baseline_2016
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_2016
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_dice2016
```

********************************************************************************

**DICE-2016, ECS=2.15:**

To run the model:

```
  - constants: gdice_baseline_2016_ecs215
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_2016
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_dice2016_ecs215
```

********************************************************************************

**DICE-2016, ECS=4.55:**

To run the model:

```
  - constants: gdice_baseline_2016_ecs455
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_2016
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_dice2016_ecs455
```

********************************************************************************

**CDICE-LOVECLIM-GISS-E2-R:**

To run the model:

```
  - constants: gdice_baseline_loveclim_giss
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_loveclim_giss
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_loveclim_giss
```

To replicate the neural network training:
Use the solution to the BAU CDICE-LOVECLIM model as a pretrained neural network

********************************************************************************

**CDICE-LOVECLIM-HadGEM2-ES:**

To run the model:

```
  - constants: gdice_baseline_loveclim_hadgem
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_loveclim_hadgem
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_loveclim_hadgem
```

To replicate the neural network training:
Use the solution to the BAU CDICE-LOVECLIM model as a pretrained neural network

********************************************************************************

**CDICE-MESMO-GISS-E2-R:**

To run the model:

```
  - constants: gdice_baseline_mesmo_giss
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mesmo_giss
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mesmo_giss
```

To replicate the neural network training:
Use the solution to the BAU CDICE-MESMO model as a pretrained neural network

********************************************************************************

**CDICE-MESMO-HadGEM2-ES:**

To run the model:

```
  - constants: gdice_baseline_mesmo_hadgem
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mesmo_hadgem
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mesmo_hadgem
```

To replicate the neural network training:
Use the solution to the BAU CDICE-MESMO model as a pretrained neural network

********************************************************************************

**CDICE-GISS-E2-R:**

To run the model:

```
  - constants: gdice_baseline_mmm_giss
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_giss
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mmm_giss
```

To replicate the neural network training:
Use the solution to the BAU CDICE model as a pretrained neural network

********************************************************************************

**CDICE-HadGEM2-ES:**

To run the model:

```
  - constants: gdice_baseline_mmm_hadgem
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_hadgem
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mmm_hadgem
```

To replicate the neural network training:
Use the solution to the BAU CDICE model as a pretrained neural network

********************************************************************************

**CDICE-LOVECLIM:**

To run the model:

```
  - constants: gdice_baseline_mmm_loveclim
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_loveclim
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mmm_loveclim
```

********************************************************************************

**CDICE-MESMO:**

To run the model:

```
  - constants: gdice_baseline_mmm_mesmo
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_mesmo
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/BAU_mmm_mesmo
```

********************************************************************************

**DICE-2016, psi=2.:**

To run the model:

```
  - constants: gdice_baseline_2016_psi2
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_2016
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/IES2/BAU_dice16_psi2
```

To replicate the neural network training:
Use the solution to the BAU DICE-2016 model as a pretrained neural network

********************************************************************************

**CDICE, psi=2.:**

To run the model:

```
  - constants: gdice_baseline_mmm_mmm_psi2
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_mmm
```

To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/IES2/BAU_mmm_mmm_psi2
```

To replicate the neural network training:
Use the solution to the BAU CDICE model as a pretrained neural network

********************************************************************************

**DICE-2016, psi=0.5:**

To run the model:

```
  - constants: gdice_baseline_2016_psi05
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_2016
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/IES05/BAU_dice16_psi05
```

********************************************************************************

**CDICE, psi=0.5:**

To run the model:

```
  - constants: gdice_baseline_mmm_mmm_psi05
  - net: gdice_baseline
  - optimizer: gdice_baseline
  - run: gdice_baseline_1yts
  - variables: gdice_baseline_mmm_mmm
```
To postprocess:

```
  <MODEL_FOLDER> = gdice_baseline/bau_results/IES05/BAU_mmm_mmm_psi05
```

To replicate the neural network training:
Use the solution to the BAU CDICE model as a pretrained neural network; train the
model with psi=0.6 and rho=0.01 for the episodes 101-130; train the
model with psi=0.55 and rho=0.007 for the episodes 131-155; train the
model with psi=0.52 and rho=0.005 for the episodes 156-200; train the
model with psi=0.5 and rho=0.004 from the episode 201 on;
