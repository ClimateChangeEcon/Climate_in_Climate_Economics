# Replication of the figures of the manuscript "The Climate in Climate Economics"

* Each Python and Julia script in this folder allows to replicate the respective figure
in the paper. 

* To run the Julia files (fig_8.jl, fig_9a.jl, fig_9b.jl, fig_10.jl), make sure you have the packages "XLSX" and "Plots" installed. You can do this by launching Julia in a terminal, and then type the following commands:

```
julia> using Pkg

julia> Pkg.add("XLSX")
julia> Pkg.add("Plots")
```

* Figures 1-7: The produced figures will be stored in the same folder as the scripts (figs_XYZ.py). They can all be assembled to the format displayed in the manuscript by running the following script in a terminal:
`
```
./assemble_them.sh
```
* The data for the figures 1-7 is located and explained in the folder
[calibration_data](../calibration_data).

* Figures 8-21: The produced figures will be stored in the folder [figs](figs).


* The data for the figures 11-21 is being produced from the solutions of
the models. Replication code for the solutions can be found in the folder
[DEQN_for_IAMs](../DEQN_for_IAMs).

* To replicate the figures please make sure you are in the folder /figures_replication and do following:

**Fig.1**
Run the script fig_1.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_1.py
```

**Fig.2**
Run the script fig_2.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_2.py
```


**Fig.3**
Run the script fig_3.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_3.py
```

**Fig.4**
Run the script fig_4.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_4.py
```

**Fig.5**
Run the script fig_5.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_5.py
```

**Fig.6**
Run the script fig_6.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_6.py
```

**Fig.7**
Run the script fig_7.py. This file requires the two additional files ``ClimDICE.py`` and ``TestDefs.py``, which are also located in the working directory.

```
python fig_7.py
```

**Fig.8**
Run the script fig_8.jl. This file requires an excel file containing the RCP emissions that is entitled ``BAU_emissions_vsRCP.xlsx`` in the working directory.

```
julia fig_8.jl
```


**Fig.9**
Run the script fig_9.jl. This file requires an excel file containing the RCP emissions that is entitled ``BAU_emissions_vsRCP.xlsx`` in the working directory.

```
julia fig_9.jl
```


**Fig.10**
Run the script fig_10.jl. This file requires an excel file containing the RCP emissions that is entitled ``BAU_emissions_vsRCP.xlsx`` in the working directory.

```
julia fig_10.jl
```

**Fig.11(a), fig.11(b), fig.12(a), fig12(b)**
Run the script figs_11_12.py

```
python figs_11_12.py
```

**Fig.13(a), fig.13(b), fig.14(a), fig14(b)**
Run the script figs_13_14.py

```
python figs_13_14.py
```

**Fig.15(a), fig.15(b)**
Run the script fig_15.py

```
python fig_15.py
```

**Fig.16(a), fig.16(b)**
Run the script fig_16.py

```
python fig_16.py
```

**Fig.17(a), fig.17(b)**
Run the script fig_17.py

```
python fig_17.py
```

**Fig.18, fig.19**
Run the script figs_18_19.py

```
python figs_18_19.py
```

**Fig.20(a), fig.20(b), fig.21(a), fig21(b)**
Run the script figs_20_21.py

```
python figs_20_21.py
```
