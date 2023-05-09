# The Climate in Climate Economics

<p align="center">
<img src="screens/CDICE.png" width="800px"/>
</p>

This Python-based code repository supplements the work of [Doris Folini](https://iac.ethz.ch/people-iac/person-detail.NDY3MDg=.TGlzdC82MzcsLTE5NDE2NTk2NTg=.html), [Aleksandra Friedl](https://sites.google.com/view/aleksandrafriedl/home), [Felix Kuebler](https://sites.google.com/site/fkubler/), and [Simon Scheidegger](https://sites.google.com/site/simonscheidegger), titled _[The Climate in Climate Economics](#citation)_ (Folini et al.; 2023).

* This repository contains two distinct folders:
  1. ["calibration_data"](calibration_data): Raw data as well as the calibration scripts (written in Python 3) for *Section 3 - A comprehensive framework to calibrate the climate in IAMs*, and *Section 4 -  CDICE - re-calibrating the climate of DICE* of our article.
      - Its content and usage are detailed in the corresponding [README](calibration_data/README.md).

  2. ["DEQN_for_IAMs"](DEQN_for_IAMs): Replication codes for *Section 6 - The social cost of carbon and optimal abatement in the DICE economy*, where non-stationary integrated assessment models (IAMs) are solved by adopting ["Deep Equilibrium Nets"](https://onlinelibrary.wiley.com/doi/epdf/10.1111/iere.12575) to the context of climate economic models. Notice that the codes provided here complement the Online Appendix D of our article, where the formal underpinnings of the code are outlined.
      - How to compute the individual model calibrations is detailed in the various readmes that are linked _[here](#Models)_.
      - The content and usage of the generic Deep Equilibrium Nets for Integrated Assessment Models framework are outlined in the corresponding [README](DEQN_for_IAMs/README.md).

### Authors
* [Doris Folini](https://iac.ethz.ch/people-iac/person-detail.NDY3MDg=.TGlzdC82MzcsLTE5NDE2NTk2NTg=.html) (ETH Zuerich, Institute for Atmospheric and Climate Science)
* [Felix Kuebler](https://sites.google.com/site/fkubler/) (the University of Zuerich, Department for Banking and Finance, and Swiss Finance Institute)
* [Aleksandra Friedl](https://sites.google.com/view/aleksandrafriedl/home) (the University of Lausanne, Department of Economics)
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

### Models

**dice_generic:** This is a common solution routine for the optimal solution of the climate-economy models. A readme of how to run this routine is given [here](DEQN_for_IAMs/dice_generic/README.md). The computed solutions for the models presented in the paper can be found [here](DEQN_for_IAMs/dice_generic/opt_results/README.md).

**gdice_baseline:** This is a common solution routine for the optimal solution of the climate-economy models. A readme of how to run this routine and a list of models solved with this routine is given [here](DEQN_for_IAMs/gdice_baseline/README.md). The computed solutions can be found [here](DEQN_for_IAMs/gdice_baseline/bau_results/README.md).

**dice_generic_FEX:** This is a common solution routine for the optimal solution of the climate-economy model with alternative exogenous forcings. A readme of how to run this routine a list of models solved with this routine is given [here](DEQN_for_IAMs/dice_generic_FEX/README.md). The computed solutions can be found [here](DEQN_for_IAMs/dice_generic_FEX/appendix_results/README.md).


## Usage
We provide implementations that use python 3.


## Support

This work was generously supported by grants from the [Swiss National Science Foundation](https://www.snf.ch) under project IDs "Can economic policy mitigate climate change," "New methods for asset pricing with frictions,” and the [Enterprise for Society (E4S)](https://e4s.center).
