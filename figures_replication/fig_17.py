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
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/BAU_cdice/'
exparams_cdice = pd.read_csv(path + 'exoparams.csv')
states_cdice = pd.read_csv(path +'states.csv')
ps_cdice = pd.read_csv(path +'ps.csv')
def_cdice = pd.read_csv(path +'defs.csv')
time_cdice = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/BAU_dice2016/'
exparams_dice16 = pd.read_csv(path + 'exoparams.csv')
states_dice16 = pd.read_csv(path +'states.csv')
ps_dice16 = pd.read_csv(path +'ps.csv')
def_dice16 = pd.read_csv(path +'defs.csv')
time_dice16 = pd.read_csv(path +'time.csv')


############################ IES = 2 rho=0.034 r=0.044 #################################################
### READING THE DATA from CDICE
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_mmm_mmm_psi2/'
exparams_cdice_IES2 = pd.read_csv(path + 'exoparams.csv')
states_cdice_IES2 = pd.read_csv(path +'states.csv')
ps_cdice_IES2 = pd.read_csv(path +'ps.csv')
def_cdice_IES2 = pd.read_csv(path +'defs.csv')
time_cdice_IES2 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/IES2/BAU_dice16_psi2/'
exparams_dice16_IES2 = pd.read_csv(path + 'exoparams.csv')
states_dice16_IES2 = pd.read_csv(path +'states.csv')
ps_dice16_IES2 = pd.read_csv(path +'ps.csv')
def_dice16_IES2 = pd.read_csv(path +'defs.csv')
time_dice16_IES2 = pd.read_csv(path +'time.csv')

############################ IES = 0.5 rho=0.004 r=0.044 #################################################
### READING THE DATA from CDICE
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_mmm_mmm_psi05/'
exparams_cdice_IES05 = pd.read_csv(path + 'exoparams.csv')
states_cdice_IES05 = pd.read_csv(path +'states.csv')
ps_cdice_IES05 = pd.read_csv(path +'ps.csv')
def_cdice_IES05 = pd.read_csv(path +'defs.csv')
time_cdice_IES05 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16
path = '../DEQN_for_IAMs/gdice_baseline/bau_results/IES05/BAU_dice16_psi05/'
exparams_dice16_IES05 = pd.read_csv(path + 'exoparams.csv')
states_dice16_IES05 = pd.read_csv(path +'states.csv')
ps_dice16_IES05 = pd.read_csv(path +'ps.csv')
def_dice16_IES05 = pd.read_csv(path +'defs.csv')
time_dice16_IES05 = pd.read_csv(path +'time.csv')

ts = time_cdice['time']
tl = 200


###################### Inverse Discount rate ############################################

fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

# Extracting the data from the solution
de = 'ynet'

ynet_cdice = def_cdice[de]
ynet_dice16 = def_dice16[de]


ynet_cdice_IES2 = def_cdice_IES2[de]
ynet_dice16_IES2 = def_dice16_IES2[de]


ynet_cdice_IES05 = def_cdice_IES05[de]
ynet_dice16_IES05 = def_dice16_IES05[de]

de = 'kx'

kx_cdice = states_cdice[de]
kx_dice16 = states_dice16[de]

kx_cdice_IES2 = states_cdice_IES2[de]
kx_dice16_IES2 = states_dice16_IES2[de]

kx_cdice_IES05 = states_cdice_IES05[de]
kx_dice16_IES05 = states_dice16_IES05[de]

de = 'gr_tfp'

grtfp_cdice = exparams_cdice[de]
grtfp_dice16 = exparams_dice16[de]

grtfp_cdice_IES2 = exparams_cdice_IES2[de]
grtfp_dice16_IES2 = exparams_dice16_IES2[de]

grtfp_cdice_IES05 = exparams_cdice_IES05[de]
grtfp_dice16_IES05 = exparams_dice16_IES05[de]

de = 'gr_lab'

grlab_cdice = exparams_cdice[de]
grlab_dice16 = exparams_dice16[de]

grlab_cdice_IES2 = exparams_cdice_IES2[de]
grlab_dice16_IES2 = exparams_dice16_IES2[de]

grlab_cdice_IES05 = exparams_cdice_IES05[de]
grlab_dice16_IES05 = exparams_dice16_IES05[de]

# Setting up the depreciation rate of capital and capital elasticity
delta = 0.1
alpha = 0.3

# Computing a real interest rate
oneplusr_cdice = alpha * ynet_cdice / kx_cdice + (1 - delta)
oneplusr_dice16 = alpha * ynet_dice16 / kx_dice16 + (1 - delta)

oneplusr_cdice_IES2 = alpha * ynet_cdice_IES2 / kx_cdice_IES2 + (1 - delta)
oneplusr_dice16_IES2 = alpha * ynet_dice16_IES2 / kx_dice16_IES2 + (1 - delta)

oneplusr_cdice_IES05 = alpha * ynet_cdice_IES05 / kx_cdice_IES05 + (1 - delta)
oneplusr_dice16_IES05 = alpha * ynet_dice16_IES05 / kx_dice16_IES05 + (1 - delta)

# Computing g-adjusted interest rate
de_cdice = (1 + grtfp_cdice + grlab_cdice)**(-1) * oneplusr_cdice
de_dice16 = (1 + grtfp_dice16 + grlab_dice16)**(-1) * oneplusr_dice16

de_cdice_IES2 = (1 + grtfp_cdice_IES2 + grlab_cdice_IES2)**(-1) * oneplusr_cdice_IES2
de_dice16_IES2 = (1 + grtfp_dice16_IES2 + grlab_dice16_IES2)**(-1) * oneplusr_dice16_IES2

de_cdice_IES05 = (1 + grtfp_cdice_IES05 + grlab_cdice_IES05)**(-1) * oneplusr_cdice_IES05
de_dice16_IES05 = (1 + grtfp_dice16_IES05 + grlab_dice16_IES05)**(-1) * oneplusr_dice16_IES05

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE, psi=0.69')
ax.plot(x, de_cdice_IES2[0:tl], color='blue', ls='dotted', linewidth=4, label='CDICE, psi=2.')
ax.plot(x, de_cdice_IES05[0:tl], color='blue', ls='dashed', linewidth=4, label='CDICE, psi=0.5')

ax.plot(x, de_dice16[0:tl], color='black', ls='solid', linewidth=1, label='DICE-2016, psi=0.69')
ax.plot(x, de_dice16_IES2[0:tl], color='black', ls='dotted', linewidth=1, label='DICE-2016, psi=2.')
ax.plot(x, de_dice16_IES05[0:tl], color='black', ls='dashed', linewidth=1, label='DICE-2016, psi=0.5')

ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])


fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig17a.pdf', bbox_inches="tight")
plt.close()



###################### Relative SCC ############################################
fig=plt.figure(figsize=(21,5))
ax=fig.add_subplot(1,3,1)


de = 'scc'

scc_cdice = def_cdice[de]
scc_dice16 = def_dice16[de]

scc_cdice_IES2 = def_cdice_IES2[de]
scc_dice16_IES2 = def_dice16_IES2[de]

scc_cdice_IES05 = def_cdice_IES05[de]
scc_dice16_IES05 = def_dice16_IES05[de]

de = 'ynet'

ynet_cdice = def_cdice[de]
ynet_dice16 = def_dice16[de]

ynet_cdice_IES2 = def_cdice_IES2[de]
ynet_dice16_IES2 = def_dice16_IES2[de]

ynet_cdice_IES05 = def_cdice_IES05[de]
ynet_dice16_IES05 = def_dice16_IES05[de]

#Relative scc
de_cdice = scc_cdice / ynet_cdice
de_dice16 = scc_dice16 / ynet_dice16

de_cdice_IES2 = scc_cdice_IES2 / ynet_cdice_IES2
de_dice16_IES2 = scc_dice16_IES2 / ynet_dice16_IES2

de_cdice_IES05 = scc_cdice_IES05 / ynet_cdice_IES05
de_dice16_IES05 = scc_dice16_IES05 / ynet_dice16_IES05


tl = 50
x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE, psi=0.69')
ax.plot(x, de_cdice_IES2[0:tl], color='blue', ls='dotted', linewidth=4, label='CDICE, psi=2.')
ax.plot(x, de_cdice_IES05[0:tl], color='blue', ls='dashed', linewidth=4, label='CDICE, psi=0.5')

ax.plot(x, de_dice16[0:tl], color='black', ls='solid', linewidth=1, label='DICE-2016, psi=0.69')
ax.plot(x, de_dice16_IES2[0:tl], color='black', ls='dotted', linewidth=1, label='DICE-2016, psi=2.')
ax.plot(x, de_dice16_IES05[0:tl], color='black', ls='dashed', linewidth=1, label='DICE-2016, psi=0.5')

ax.set_xlabel(xlabel)
ax.set_ylabel('USD/trillion USD')
ax.legend(loc='upper left')
plt.xlim([0,tl])


fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig17b.pdf', bbox_inches="tight")
plt.close()
