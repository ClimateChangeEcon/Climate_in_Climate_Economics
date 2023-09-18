import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

# --------------------------------------------------------------------------- #
# Plot setting
# --------------------------------------------------------------------------- #

# Use TeX font
rc('font', **{'family': 'sans-serif', 'serif': ['Helvetica']})
rc('text', usetex=True)
lb_discrete = r'Discrete, 5 years step'
xbeg, xend = 2000, 2500
xlabel = 'Year'
xticks = np.arange(xbeg, xend, 100)
# Font size
plt.rcParams["font.size"] = 12
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["legend.title_fontsize"] = 8
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.linestyle"] = 'dotted'

fsize = (9, 6)
line_args = {'markerfacecolor': 'None', 'color': 'tab:green', 'marker': None,
             'linestyle': '-'}
distribution_args = {'markerfacecolor': 'None', 'color': 'tab:green',
                     'marker': '.', 'linestyle': 'None'}
exparams = ['tfp', 'lab', 'sigma', 'theta1', 'Eland']
econ_defs = ['con', 'Omega', 'ygross', 'ynet', 'inv', 'Eind', 'scc',
            'Dam', 'Emissions']
states = ['kx', 'MATx', 'MUOx', 'MLOx', 'TATx', 'TOCx']
p_states = ['muy']

############################ rho = 0.015 #################################################
### READING THE DATA from CDICE
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice/'
exparams_cdice = pd.read_csv(path + 'exoparams.csv')
states_cdice = pd.read_csv(path +'states.csv')
ps_cdice = pd.read_csv(path +'ps.csv')
def_cdice = pd.read_csv(path +'defs.csv')
time_cdice = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + GISS
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_giss/'
exparams_cdice_giss = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss = pd.read_csv(path +'states.csv')
ps_cdice_giss = pd.read_csv(path +'ps.csv')
def_cdice_giss = pd.read_csv(path +'defs.csv')
time_cdice_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + hadgem
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_hadgem/'
exparams_cdice_hadgem = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem = pd.read_csv(path +'states.csv')
ps_cdice_hadgem = pd.read_csv(path +'ps.csv')
def_cdice_hadgem = pd.read_csv(path +'defs.csv')
time_cdice_hadgem = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + mesmo
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_mesmo/'
exparams_cdice_mesmo = pd.read_csv(path + 'exoparams.csv')
states_cdice_mesmo = pd.read_csv(path +'states.csv')
ps_cdice_mesmo = pd.read_csv(path +'ps.csv')
def_cdice_mesmo = pd.read_csv(path +'defs.csv')
time_cdice_mesmo = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + loveclim
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_loveclim/'
exparams_cdice_loveclim = pd.read_csv(path + 'exoparams.csv')
states_cdice_loveclim = pd.read_csv(path +'states.csv')
ps_cdice_loveclim = pd.read_csv(path +'ps.csv')
def_cdice_loveclim = pd.read_csv(path +'defs.csv')
time_cdice_loveclim = pd.read_csv(path +'time.csv')

## READING THE DATA from new mesmo + hadgem
path = '../DEQN_for_IAMs/dice_generic/optimal_results/mesmo_hadgem/'
exparams_mesmo_hadgem = pd.read_csv(path + 'exoparams.csv')
states_mesmo_hadgem = pd.read_csv(path +'states.csv')
ps_mesmo_hadgem = pd.read_csv(path +'ps.csv')
def_mesmo_hadgem = pd.read_csv(path +'defs.csv')
time_mesmo_hadgem = pd.read_csv(path +'time.csv')

## READING THE DATA from new mesmo + giss
path = '../DEQN_for_IAMs/dice_generic/optimal_results/mesmo_giss/'
exparams_mesmo_giss = pd.read_csv(path + 'exoparams.csv')
states_mesmo_giss = pd.read_csv(path +'states.csv')
ps_mesmo_giss = pd.read_csv(path +'ps.csv')
def_mesmo_giss = pd.read_csv(path +'defs.csv')
time_mesmo_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from new loveclim + hadgem
path = '../DEQN_for_IAMs/dice_generic/optimal_results/loveclim_hadgem/'
exparams_loveclim_hadgem = pd.read_csv(path + 'exoparams.csv')
states_loveclim_hadgem = pd.read_csv(path +'states.csv')
ps_loveclim_hadgem = pd.read_csv(path +'ps.csv')
def_loveclim_hadgem = pd.read_csv(path +'defs.csv')
time_loveclim_hadgem = pd.read_csv(path +'time.csv')

### READING THE DATA from new loveclim + giss
path = '../DEQN_for_IAMs/dice_generic/optimal_results/loveclim_giss/'
exparams_loveclim_giss = pd.read_csv(path + 'exoparams.csv')
states_loveclim_giss = pd.read_csv(path +'states.csv')
ps_loveclim_giss = pd.read_csv(path +'ps.csv')
def_loveclim_giss = pd.read_csv(path +'defs.csv')
time_loveclim_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from RCP
path = '../DEQN_for_IAMs/RCP_data/'
rcp_data = pd.read_csv(path + 'RCP_import.csv')
name = 'RCP26_ind'
rcp26_ind = rcp_data[name]
name = 'RCP26_land'
rcp26_land = rcp_data[name]

name = 'RCP45_ind'
rcp45_ind = rcp_data[name]
name = 'RCP45_land'
rcp45_land = rcp_data[name]

name = 'RCP60_ind'
rcp60_ind = rcp_data[name]
name = 'RCP60_land'
rcp60_land = rcp_data[name]

name = 'RCP85_ind'
rcp85_ind = rcp_data[name]
name = 'RCP85_land'
rcp85_land = rcp_data[name]



ts = time_cdice['time']
tl = 300




###################### Emissions ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'Emissions'

de_cdice = def_cdice[de]
de_cdice_giss = def_cdice_giss[de]
de_cdice_hadgem = def_cdice_hadgem[de]
de_cdice_mesmo = def_cdice_mesmo[de]
de_cdice_loveclim = def_cdice_loveclim[de]
de_mesmo_giss = def_mesmo_giss[de]
de_mesmo_hadgem = def_mesmo_hadgem[de]
de_loveclim_giss = def_loveclim_giss[de]
de_loveclim_hadgem = def_loveclim_hadgem[de]
rcp26 = rcp26_ind + rcp26_land
rcp45 = rcp45_ind + rcp45_land

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=1, label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', linewidth=1, label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', linewidth=1, label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', linewidth=2, label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', linewidth=3, label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', linewidth=2, label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', linewidth=3, label='CDICE-LOVECLIM-HadGEM2-ES')
ax.plot(x, rcp26[0:tl], color='red', ls='solid',  linewidth=4, label='RCP 2.6')
ax.plot(x, rcp45[0:tl], color='orange', ls='solid',  linewidth=6, label='RCP 4.5')

ax.set_xlabel(xlabel)
ax.set_ylabel('GtCO2')
ax.legend(loc='upper right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig13b.pdf', bbox_inches="tight")
plt.close()


###################### TAT ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'TATx'

de_cdice = states_cdice[de]
de_cdice_giss = states_cdice_giss[de]
de_cdice_hadgem = states_cdice_hadgem[de]
de_cdice_mesmo = states_cdice_mesmo[de]
de_cdice_loveclim = states_cdice_loveclim[de]
de_mesmo_giss = states_mesmo_giss[de]
de_mesmo_hadgem = states_mesmo_hadgem[de]
de_loveclim_giss = states_loveclim_giss[de]
de_loveclim_hadgem = states_loveclim_hadgem[de]

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid',  linewidth=1, label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', linewidth=1, label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', linewidth=1, label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', linewidth=2, label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', linewidth=3, label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', linewidth=2, label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', linewidth=3, label='CDICE-LOVECLIM-HadGEM2-ES')


ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig14a.pdf', bbox_inches="tight")
plt.close()

###################### SCC ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

# ax.set_title("SCC, BAU case")
de = 'scc'

de_cdice = def_cdice[de]
de_cdice_giss = def_cdice_giss[de]
de_cdice_hadgem = def_cdice_hadgem[de]
de_cdice_mesmo = def_cdice_mesmo[de]
de_loveclim_giss = def_loveclim_giss[de]
de_loveclim_hadgem = def_loveclim_hadgem[de]
de_cdice_loveclim = def_cdice_loveclim[de]
de_mesmo_giss = def_mesmo_giss[de]
de_mesmo_hadgem = def_mesmo_hadgem[de]
de_loveclim_giss = def_loveclim_giss[de]
de_loveclim_hadgem = def_loveclim_hadgem[de]

tl = 50
x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=1, label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', linewidth=1, label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', linewidth=1, label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', linewidth=2, label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', linewidth=3, label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', linewidth=2, label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', linewidth=3, label='CDICE-LOVECLIM-HadGEM2-ES')



ax.set_xlabel(xlabel)
ax.set_ylabel('USD')
ax.legend(loc='upper left')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)


plt.savefig('figs/fig14b.pdf', bbox_inches="tight")
plt.close()
###################### abatement ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'muy'

de_cdice = ps_cdice[de]
de_cdice_giss = ps_cdice_giss[de]
de_cdice_hadgem = ps_cdice_hadgem[de]
de_cdice_mesmo = ps_cdice_mesmo[de]
de_loveclim_giss = ps_loveclim_giss[de]
de_loveclim_hadgem = ps_loveclim_hadgem[de]
de_cdice_loveclim = ps_cdice_loveclim[de]
de_mesmo_giss = ps_mesmo_giss[de]
de_mesmo_hadgem = ps_mesmo_hadgem[de]
de_loveclim_giss = ps_loveclim_giss[de]
de_loveclim_hadgem = ps_loveclim_hadgem[de]

tl = 300
x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=1, label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', linewidth=1, label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', linewidth=1, label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', linewidth=2, label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', linewidth=3, label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', linewidth=2, label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', linewidth=3, label='CDICE-LOVECLIM-HadGEM2-ES')



ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)


plt.savefig('figs/fig13a.pdf', bbox_inches="tight")
plt.close()
