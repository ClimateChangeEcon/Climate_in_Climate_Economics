import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

# --------------------------------------------------------------------------- #
# Plot setting
# --------------------------------------------------------------------------- #
# Get the size of the current terminal
# terminal_size_col = shutil.get_terminal_size().columns

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
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/cdice/'
exparams_cdice = pd.read_csv(path + 'exoparams.csv')
states_cdice = pd.read_csv(path +'states.csv')
ps_cdice = pd.read_csv(path +'ps.csv')
def_cdice = pd.read_csv(path +'defs.csv')
time_cdice = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/dice2016/'
exparams_dice16 = pd.read_csv(path + 'exoparams.csv')
states_dice16 = pd.read_csv(path +'states.csv')
ps_dice16 = pd.read_csv(path +'ps.csv')
def_dice16 = pd.read_csv(path +'defs.csv')
time_dice16 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16+ecs215
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs215/'
exparams_dice16_ecs215 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs215 = pd.read_csv(path +'states.csv')
ps_dice16_ecs215 = pd.read_csv(path +'ps.csv')
def_dice16_ecs215 = pd.read_csv(path +'defs.csv')
time_dice16_ecs215 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16+ecs455
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/dice2016_ecs455/'
exparams_dice16_ecs455 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs455 = pd.read_csv(path +'states.csv')
ps_dice16_ecs455 = pd.read_csv(path +'ps.csv')
def_dice16_ecs455 = pd.read_csv(path +'defs.csv')
time_dice16_ecs455 = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + GISS
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/cdice_giss/'
exparams_cdice_giss = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss = pd.read_csv(path +'states.csv')
ps_cdice_giss = pd.read_csv(path +'ps.csv')
def_cdice_giss = pd.read_csv(path +'defs.csv')
time_cdice_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/cdice_hadgem/'
exparams_cdice_hadgem = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem = pd.read_csv(path +'states.csv')
ps_cdice_hadgem = pd.read_csv(path +'ps.csv')
def_cdice_hadgem = pd.read_csv(path +'defs.csv')
time_cdice_hadgem = pd.read_csv(path +'time.csv')


############################ IES = 2 rho=0.004 r=0.044 #################################################
### READING THE DATA from CDICE
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_mmm/'
exparams_cdice_IES2 = pd.read_csv(path + 'exoparams.csv')
states_cdice_IES2 = pd.read_csv(path +'states.csv')
ps_cdice_IES2 = pd.read_csv(path +'ps.csv')
def_cdice_IES2 = pd.read_csv(path +'defs.csv')
time_cdice_IES2 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16/'
exparams_dice16_IES2 = pd.read_csv(path + 'exoparams.csv')
states_dice16_IES2 = pd.read_csv(path +'states.csv')
ps_dice16_IES2 = pd.read_csv(path +'ps.csv')
def_dice16_IES2 = pd.read_csv(path +'defs.csv')
time_dice16_IES2 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16+ecs215
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16_ecs215/'
exparams_dice16_ecs215_IES2 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs215_IES2 = pd.read_csv(path +'states.csv')
ps_dice16_ecs215_IES2 = pd.read_csv(path +'ps.csv')
def_dice16_ecs215_IES2 = pd.read_csv(path +'defs.csv')
time_dice16_ecs215_IES2 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16+ecs455
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_dice16_ecs455/'
exparams_dice16_ecs455_IES2 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs455_IES2 = pd.read_csv(path +'states.csv')
ps_dice16_ecs455_IES2 = pd.read_csv(path +'ps.csv')
def_dice16_ecs455_IES2 = pd.read_csv(path +'defs.csv')
time_dice16_ecs455_IES2 = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + GISS
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_giss/'
exparams_cdice_giss_IES2 = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss_IES2 = pd.read_csv(path +'states.csv')
ps_cdice_giss_IES2 = pd.read_csv(path +'ps.csv')
def_cdice_giss_IES2 = pd.read_csv(path +'defs.csv')
time_cdice_giss_IES2 = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES2/Opt_mmm_hadgem/'
exparams_cdice_hadgem_IES2 = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem_IES2 = pd.read_csv(path +'states.csv')
ps_cdice_hadgem_IES2 = pd.read_csv(path +'ps.csv')
def_cdice_hadgem_IES2 = pd.read_csv(path +'defs.csv')
time_cdice_hadgem_IES2 = pd.read_csv(path +'time.csv')

############################ IES = 0.5 rho=0.034 r=0.044 #################################################
### READING THE DATA from CDICE
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_mmm/'
exparams_cdice_IES05 = pd.read_csv(path + 'exoparams.csv')
states_cdice_IES05 = pd.read_csv(path +'states.csv')
ps_cdice_IES05 = pd.read_csv(path +'ps.csv')
def_cdice_IES05 = pd.read_csv(path +'defs.csv')
time_cdice_IES05 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16/'
exparams_dice16_IES05 = pd.read_csv(path + 'exoparams.csv')
states_dice16_IES05 = pd.read_csv(path +'states.csv')
ps_dice16_IES05 = pd.read_csv(path +'ps.csv')
def_dice16_IES05 = pd.read_csv(path +'defs.csv')
time_dice16_IES05 = pd.read_csv(path +'time.csv')

## READING THE DATA from DICE16+ecs215
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16_ecs215/'
exparams_dice16_ecs215_IES05 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs215_IES05 = pd.read_csv(path +'states.csv')
ps_dice16_ecs215_IES05 = pd.read_csv(path +'ps.csv')
def_dice16_ecs215_IES05 = pd.read_csv(path +'defs.csv')
time_dice16_ecs215_IES05 = pd.read_csv(path +'time.csv')

### READING THE DATA from DICE16+ecs455
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_dice16_ecs455/'
exparams_dice16_ecs455_IES05 = pd.read_csv(path + 'exoparams.csv')
states_dice16_ecs455_IES05 = pd.read_csv(path +'states.csv')
ps_dice16_ecs455_IES05 = pd.read_csv(path +'ps.csv')
def_dice16_ecs455_IES05 = pd.read_csv(path +'defs.csv')
time_dice16_ecs455_IES05 = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + GISS
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_giss/'
exparams_cdice_giss_IES05 = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss_IES05 = pd.read_csv(path +'states.csv')
ps_cdice_giss_IES05 = pd.read_csv(path +'ps.csv')
def_cdice_giss_IES05 = pd.read_csv(path +'defs.csv')
time_cdice_giss_IES05 = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/dice_generic/optimal_results/IES05/Opt_mmm_hadgem/'
exparams_cdice_hadgem_IES05 = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem_IES05 = pd.read_csv(path +'states.csv')
ps_cdice_hadgem_IES05 = pd.read_csv(path +'ps.csv')
def_cdice_hadgem_IES05 = pd.read_csv(path +'defs.csv')
time_cdice_hadgem_IES05 = pd.read_csv(path +'time.csv')




ts = time_cdice['time']
tl = 200



###################### TAT ############################################
fig=plt.figure(figsize=(21,5))
ax=fig.add_subplot(1,3,1)


de = 'TATx'

de_cdice = states_cdice[de]
de_cdice_giss = states_cdice_giss[de]
de_cdice_hadgem = states_cdice_hadgem[de]
de_dice16 = states_dice16[de]
de_dice16_ecs215 = states_dice16_ecs215[de]
de_dice16_ecs455 = states_dice16_ecs455[de]

de_cdice_IES2 = states_cdice_IES2[de]
de_cdice_giss_IES2 = states_cdice_giss_IES2[de]
de_cdice_hadgem_IES2 = states_cdice_hadgem_IES2[de]
de_dice16_IES2 = states_dice16_IES2[de]
de_dice16_ecs215_IES2 = states_dice16_ecs215_IES2[de]
de_dice16_ecs455_IES2 = states_dice16_ecs455_IES2[de]

de_cdice_IES05 = states_cdice_IES05[de]
de_cdice_giss_IES05 = states_cdice_giss_IES05[de]
de_cdice_hadgem_IES05 = states_cdice_hadgem_IES05[de]
de_dice16_IES05 = states_dice16_IES05[de]
de_dice16_ecs215_IES05 = states_dice16_ecs215_IES05[de]
de_dice16_ecs455_IES05 = states_dice16_ecs455_IES05[de]

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE, psi=0.69')
ax.plot(x, de_cdice_IES05[0:tl], color='blue', ls='dotted', label='CDICE, psi=2.')
ax.plot(x, de_cdice_IES2[0:tl], color='blue', ls='dashed', label='CDICE, psi=0.5')

ax.plot(x, de_dice16[0:tl], color='black', ls='solid', label='DICE-2016, psi=0.69')
ax.plot(x, de_dice16_IES05[0:tl], color='black', ls='dotted', label='DICE-2016, psi=2.')
ax.plot(x, de_dice16_IES2[0:tl], color='black', ls='dashed', label='DICE-2016, psi=0.5')

ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='lower right')
plt.xlim([0,tl])

ax=fig.add_subplot(1,3,2)

ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES, psi=0.69')
ax.plot(x, de_cdice_hadgem_IES05[0:tl], color='#20CBD1', ls='dotted', label='CDICE-HadGEM2-ES, psi=2.')
ax.plot(x, de_cdice_hadgem_IES2[0:tl], color='#20CBD1', ls='dashed', label='CDICE-HadGEM2-ES, psi=0.5')

ax.plot(x, de_dice16_ecs455[0:tl], color='red', ls='solid', label='DICE-2016, ECS=4.55, psi=0.69')
ax.plot(x, de_dice16_ecs455_IES05[0:tl], color='red', ls='dotted', label='DICE-2016, ECS=4.55, psi=2.')
ax.plot(x, de_dice16_ecs455_IES2[0:tl], color='red', ls='dashed', label='DICE-2016, ECS=4.55, psi=0.5')


ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='lower right')
plt.xlim([0,tl])

ax=fig.add_subplot(1,3,3)

ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R, psi=0.69')
ax.plot(x, de_cdice_giss_IES05[0:tl], color='#92F41C', ls='dotted', label='CDICE-GISS-E2-R, psi=2.')
ax.plot(x, de_cdice_giss_IES2[0:tl], color='#92F41C', ls='dashed', label='CDICE-GISS-E2-R, psi=0.5')

ax.plot(x, de_dice16_ecs215[0:tl], color='green', ls='solid', label='DICE-2016, ECS=2.15, psi=0.69')
ax.plot(x, de_dice16_ecs215_IES05[0:tl], color='green', ls='dotted', label='DICE-2016, ECS=2.15, psi=2.')
ax.plot(x, de_dice16_ecs215_IES2[0:tl], color='green', ls='dashed', label='DICE-2016, ECS=2.15, psi=0.5')


ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig19.pdf', bbox_inches="tight")
plt.close()

###################### Abatement ############################################
fig=plt.figure(figsize=(21,5))
ax=fig.add_subplot(1,3,1)

de = 'muy'

de_cdice = ps_cdice[de]
de_cdice_giss = ps_cdice_giss[de]
de_cdice_hadgem = ps_cdice_hadgem[de]
de_dice16 = ps_dice16[de]
de_dice16_ecs215 = ps_dice16_ecs215[de]
de_dice16_ecs455 = ps_dice16_ecs455[de]

de_cdice_IES2 = ps_cdice_IES2[de]
de_cdice_giss_IES2 = ps_cdice_giss_IES2[de]
de_cdice_hadgem_IES2 = ps_cdice_hadgem_IES2[de]
de_dice16_IES2 = ps_dice16_IES2[de]
de_dice16_ecs215_IES2 = ps_dice16_ecs215_IES2[de]
de_dice16_ecs455_IES2 = ps_dice16_ecs455_IES2[de]

de_cdice_IES05 = ps_cdice_IES05[de]
de_cdice_giss_IES05 = ps_cdice_giss_IES05[de]
de_cdice_hadgem_IES05 = ps_cdice_hadgem_IES05[de]
de_dice16_IES05 = ps_dice16_IES05[de]
de_dice16_ecs215_IES05 = ps_dice16_ecs215_IES05[de]
de_dice16_ecs455_IES05 = ps_dice16_ecs455_IES05[de]


x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE, psi=0.69')
ax.plot(x, de_cdice_IES05[0:tl], color='blue', ls='dotted', label='CDICE, psi=2.')
ax.plot(x, de_cdice_IES2[0:tl], color='blue', ls='dashed', label='CDICE, psi=0.5')

ax.plot(x, de_dice16[0:tl], color='black', ls='solid', label='DICE-2016, psi=0.69')
ax.plot(x, de_dice16_IES05[0:tl], color='black', ls='dotted', label='DICE-2016, psi=2.')
ax.plot(x, de_dice16_IES2[0:tl], color='black', ls='dashed', label='DICE-2016, psi=0.5')

ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

ax=fig.add_subplot(1,3,2)

ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES, psi=0.69')
ax.plot(x, de_cdice_hadgem_IES05[0:tl], color='#20CBD1', ls='dotted', label='CDICE-HadGEM2-ES, psi=2.')
ax.plot(x, de_cdice_hadgem_IES2[0:tl], color='#20CBD1', ls='dashed', label='CDICE-HadGEM2-ES, psi=0.5')

ax.plot(x, de_dice16_ecs455[0:tl], color='red', ls='solid', label='DICE-2016, ECS=4.55, psi=0.69')
ax.plot(x, de_dice16_ecs455_IES05[0:tl], color='red', ls='dotted', label='DICE-2016, ECS=4.55, psi=2.')
ax.plot(x, de_dice16_ecs455_IES2[0:tl], color='red', ls='dashed', label='DICE-2016, ECS=4.55, psi=0.5')


ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

ax=fig.add_subplot(1,3,3)

ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R, psi=0.69')
ax.plot(x, de_cdice_giss_IES05[0:tl], color='#92F41C', ls='dotted', label='CDICE-GISS-E2-R, psi=2.')
ax.plot(x, de_cdice_giss_IES2[0:tl], color='#92F41C', ls='dashed', label='CDICE-GISS-E2-R, psi=0.5')

ax.plot(x, de_dice16_ecs215[0:tl], color='green', ls='solid', label='DICE-2016, ECS=2.15, psi=0.69')
ax.plot(x, de_dice16_ecs215_IES05[0:tl], color='green', ls='dotted', label='DICE-2016, ECS=2.15, psi=2.')
ax.plot(x, de_dice16_ecs215_IES2[0:tl], color='green', ls='dashed', label='DICE-2016, ECS=2.15, psi=0.5')


ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)


plt.savefig('figs/fig18.pdf', bbox_inches="tight")
plt.close()
