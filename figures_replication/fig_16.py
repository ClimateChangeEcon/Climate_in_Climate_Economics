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

############################ Reading the data #################################################
### READING THE DATA from CDICE
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice/'
exparams_cdice = pd.read_csv(path + 'exoparams.csv')
states_cdice = pd.read_csv(path +'states.csv')
ps_cdice = pd.read_csv(path +'ps.csv')
def_cdice = pd.read_csv(path +'defs.csv')
time_cdice = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE2016
path = '../DEQN_for_IAMs/dice_generic/optimal_results/dice2016/'
exparams_dice16 = pd.read_csv(path + 'exoparams.csv')
states_dice16 = pd.read_csv(path +'states.csv')
ps_dice16 = pd.read_csv(path +'ps.csv')
def_dice16 = pd.read_csv(path +'defs.csv')
time_dice16 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16 + ecs=2.15
path = '../DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs215/'
exparams_dice16_ecs215 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs215 = pd.read_csv(path +'states.csv')
ps_dice16_ecs215 = pd.read_csv(path +'ps.csv')
def_dice16_ecs215 = pd.read_csv(path +'defs.csv')
time_dice16_ecs215 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16 + ecs=4.55
path = '../DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs455/'
exparams_dice16_ecs455 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs455 = pd.read_csv(path +'states.csv')
ps_dice16_ecs455 = pd.read_csv(path +'ps.csv')
def_dice16_ecs455 = pd.read_csv(path +'defs.csv')
time_dice16_ecs455 = pd.read_csv(path +'time.csv')


## READING THE DATA from cdice + hadgem
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_hadgem/'
exparams_cdice_hadgem = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem = pd.read_csv(path +'states.csv')
ps_cdice_hadgem = pd.read_csv(path +'ps.csv')
def_cdice_hadgem = pd.read_csv(path +'defs.csv')
time_cdice_hadgem = pd.read_csv(path +'time.csv')

## READING THE DATA from cdice + giss
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice_giss/'
exparams_cdice_giss = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss = pd.read_csv(path +'states.csv')
ps_cdice_giss = pd.read_csv(path +'ps.csv')
def_cdice_giss = pd.read_csv(path +'defs.csv')
time_cdice_giss = pd.read_csv(path +'time.csv')


ts = time_cdice['time']
tl = 200



###################### TAT ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'TATx'

de_cdice = states_cdice[de]
de_dice16 = states_dice16[de]
de_cdice_giss = states_cdice_giss[de]
de_cdice_hadgem = states_cdice_hadgem[de]
de_dice16_ecs215 = states_dice16_ecs215[de]
de_dice16_ecs455 = states_dice16_ecs455[de]

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE')
ax.plot(x, de_dice16[0:tl], color='black', ls='solid',linewidth=1, label='DICE-2016')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_dice16_ecs215[0:tl], color='black', ls='dotted', linewidth=1, label='DICE-2016, ECS=2.15')
ax.plot(x, de_dice16_ecs455[0:tl], color='black', ls='dashed', linewidth=1, label='DICE-2016, ECS=4.55')


ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='upper left')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig16b.pdf', bbox_inches="tight")
plt.close()

###################### abatement ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'muy'

de_cdice = ps_cdice[de]
de_dice16 = ps_dice16[de]
de_cdice_giss = ps_cdice_giss[de]
de_cdice_hadgem = ps_cdice_hadgem[de]
de_dice16_ecs215 = ps_dice16_ecs215[de]
de_dice16_ecs455 = ps_dice16_ecs455[de]

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE')
ax.plot(x, de_dice16[0:tl], color='black', ls='solid', linewidth=1, label='DICE-2016')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', linewidth=2, label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', linewidth=3, label='CDICE-HadGEM2-ES')
ax.plot(x, de_dice16_ecs215[0:tl], color='black', ls='dotted',linewidth=1, label='DICE-2016, ECS=2.15')
ax.plot(x, de_dice16_ecs455[0:tl], color='black', ls='dashed',linewidth=1, label='DICE-2016, ECS=4.55')


ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)

plt.savefig('figs/fig16a.pdf', bbox_inches="tight")
plt.close()
