# The Climate in Climate Economics

<p align="center">
<img src="screens/CDICE.png" width="800px"/>
</p>

## Description of programs/code

This Python and Julia-based code repository supplements the work of [Doris Folini](https://iac.ethz.ch/people-iac/person-detail.NDY3MDg=.TGlzdC82MzcsLTE5NDE2NTk2NTg=.html), [Aleksandra Friedl](https://sites.google.com/view/aleksandrafriedl/home), [Felix Kuebler](https://sites.google.com/site/fkubler/), and [Simon Scheidegger](https://sites.google.com/site/simonscheidegger), titled _[The Climate in Climate Economics](#citation)_ (Folini et al.; 2023).

* This repository contains three distinct folders:
  1. ["calibration_data"](calibration_data): Raw data as well as the calibration scripts (written in Python 3) for *Section 3 - A comprehensive framework to calibrate the climate in IAMs*, and *Section 4 -  CDICE - re-calibrating the climate of DICE* of our article.
      - Its content and usage are detailed in the corresponding [README](calibration_data/README.md).

  2. ["DEQN_for_IAMs"](DEQN_for_IAMs): Replication codes for *Section 6 - The social cost of carbon and optimal abatement in the DICE economy*, where non-stationary integrated assessment models (IAMs) are solved by adopting ["Deep Equilibrium Nets (DEQN)"](https://onlinelibrary.wiley.com/doi/epdf/10.1111/iere.12575) to the context of climate economic models. Notice that the codes provided here complement the Online Appendix D of our article, where the formal underpinnings of the code are outlined.
      - How to compute the individual model calibrations is detailed in the various readmes that are linked _[here](#Models)_.
      - The content and usage of the generic Deep Equilibrium Nets for Integrated Assessment Models framework are outlined in the corresponding [README](DEQN_for_IAMs/README.md).

  3. ["figures_replication"](figures_replication): Replication routines for plotting all the figures that are presented in the paper.

  
## Computational requirements

### Software requirements

* We provide implementations that use python 3.10 and Julia 1.9.

* For the  The basic dependencies are [Tensorflow==2.x](https://www.tensorflow.org/), [hydra](https://hydra.cc/) and [Tensorboard](https://www.tensorflow.org/tensorboard) (for monitoring).

* The file ``requirements.txt`` lists the detailed dependencies. Please run "pip install -r requirements.txt" as the first step. See [here](https://pip.pypa.io/en/stable/user_guide/#ensuring-repeatability) for further instructions on creating and using the ``requirements.txt`` file.


### Controlled randomness

The random seed for our computations in *Section 6 - The social cost of carbon and optimal abatement in the DICE economy* is set at ``Climate_in_Climate_Economics/DEQN_for_IAMS/config/config.yaml``, line 10.


### Memory and runtime requirements

* To solve one IAM model as discussed in *Section 6 - The social cost of carbon and optimal abatement in the DICE economy* until full convergence, it requires about 15 min on an ordinary laptop. All those models presented in the paper were solved using our [DEQN library](DEQN_for_IAMs), which we ran on an 8-core Intel compute node on [https://nuvolos.cloud](https://nuvolos.cloud) with 64GB of RAM, and 100Gb of fast local storage (SSD).

* All the postprocessing codes (to produce the summary statistics, plots, and so forth) were run on an ordinary 4-core Intel-based laptop with Ubuntu version 18.04.5 LTS and consume typically few seconds to run.

* The approximate time needed to reproduce all the analyses for this paper on a standard (2023) desktop machine is 1-3 days of human time.


## Instructions to replicators

* To replicate the figures presented in the paper, please follow the instructions given [here](figures_replication/README.md).

* To replicate the solutions of the IAMs with DEQNs, please follow the instructions given [here](DEQN_for_IAMs/README.md) for general guidance on using the DEQN library.


### Models

To replicate the results for individual models discussed in *Section 6 - The social cost of carbon and optimal abatement in the DICE economy*, consider the following configurations:

**dice_generic:** This is a common solution routine for the optimal solution of the climate-economy models. A readme of how to run this routine is given [here](DEQN_for_IAMs/dice_generic). The computed solutions for the models presented in the paper can be found [here](DEQN_for_IAMs/dice_generic/optimal_results).

**gdice_baseline:** This is a common solution routine for the optimal solution of the climate-economy models. A readme of how to run this routine and a list of models solved with this routine is given [here](DEQN_for_IAMs/gdice_baseline). The computed solutions can be found [here](DEQN_for_IAMs/gdice_baseline/bau_results).

**dice_generic_FEX:** This is a common solution routine for the optimal solution of the climate-economy model with alternative exogenous forcings. A readme of how to run this routine a list of models solved with this routine is given [here](DEQN_for_IAMs/dice_generic_FEX). The computed solutions can be found [here](DEQN_for_IAMs/dice_generic_FEX/appendix_results).


## Authors
* [Doris Folini](https://iac.ethz.ch/people-iac/person-detail.NDY3MDg=.TGlzdC82MzcsLTE5NDE2NTk2NTg=.html) (ETH Zuerich, Institute for Atmospheric and Climate Science)
* [Felix Kuebler](https://sites.google.com/site/fkubler/) (the University of Zuerich, Department for Banking and Finance, and Swiss Finance Institute)
* [Aleksandra Friedl](https://sites.google.com/view/aleksandrafriedl/home) (the University of Lausanne, Department of Economics, and ifo Institute)
* [Simon Scheidegger](https://sites.google.com/site/simonscheidegger) (the University of Lausanne, Department of Economics)


### Citation

Please cite [The Climate in Climate Economics](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3885021)
in your publications if it helps your research:

```
@article{Folini_2023,
  title={The climate in climate economics},
  author={Folini, Doris and Friedl, Aleksandra and Kubler, Felix and Scheidegger, Simon},
  journal={Available at SSRN 3885021},
  year={2023}
}
```

## Support

This work was generously supported by grants from the [Swiss National Science Foundation](https://www.snf.ch) under project IDs "Can economic policy mitigate climate change," "New methods for asset pricing with frictions,” and the [Enterprise for Society (E4S)](https://e4s.center).
