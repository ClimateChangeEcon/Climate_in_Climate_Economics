import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np


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
econ_defs = ['con', 'Omega', 'ygross', 'ynet', 'inv', 'Eind', 'scc', 'carbontax'
            'Dam', 'Emissions']
states = ['kx', 'MATx', 'MUOx', 'MLOx', 'TATx', 'TOCx']
p_states = ['muy']

############################ FEX = original #################################################
### READING THE DATA from cdice
path = '../DEQN_for_IAMs/dice_generic/optimal_results/cdice/'
exparams_new = pd.read_csv(path + 'exoparams.csv')
states_new = pd.read_csv(path +'states.csv')
ps_new = pd.read_csv(path +'ps.csv')
def_new = pd.read_csv(path +'defs.csv')
time_new = pd.read_csv(path +'time.csv')


### READING THE DATA for dice2016
path_gams = '../DEQN_for_IAMs/dice_generic/optimal_results/dice2016/'
exparams_gams = pd.read_csv(path_gams + 'exoparams.csv')
states_gams = pd.read_csv(path_gams +'states.csv')
ps_gams = pd.read_csv(path_gams +'ps.csv')
def_gams = pd.read_csv(path_gams +'defs.csv')
time_gams = pd.read_csv(path_gams +'time.csv')

############################ FEX = alternative #################################################
### READING THE DATA from cdice
path = '../DEQN_for_IAMs/dice_generic_FEX/appendix_results/CDICE_FEX/'
exparams_new_FEX = pd.read_csv(path + 'exoparams.csv')
states_new_FEX = pd.read_csv(path +'states.csv')
ps_new_FEX = pd.read_csv(path +'ps.csv')
def_new_FEX = pd.read_csv(path +'defs.csv')
time_new_FEX = pd.read_csv(path +'time.csv')


### READING THE DATA from dice2016
path_gams = '../DEQN_for_IAMs/dice_generic_FEX/appendix_results/DICE2016_FEX/'
exparams_gams_FEX = pd.read_csv(path_gams + 'exoparams.csv')
states_gams_FEX = pd.read_csv(path_gams +'states.csv')
ps_gams_FEX = pd.read_csv(path_gams +'ps.csv')
def_gams_FEX = pd.read_csv(path_gams +'defs.csv')
time_gams_FEX = pd.read_csv(path_gams +'time.csv')



ts = time_new['time']
tl = 300
ts_gams = time_gams


###################### Damages ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'Omega'
de_new = def_new[de]
de_gams = def_gams[de]
de_new_FEX = def_new_FEX[de]
de_gams_FEX = def_gams_FEX[de]

x = ts[0:tl]

ax.plot(x, de_new[0:tl], color='blue', ls='solid',linewidth=4, label='CDICE')
ax.plot(x, de_gams[0:tl], color='black', ls='solid',linewidth=1, label='DICE-2016')
ax.plot(x, de_new_FEX[0:tl], color='blue', ls='dashed',linewidth=4, label='CDICE-FEX')
ax.plot(x, de_gams_FEX[0:tl], color='black', ls='dashed',linewidth=1, label='DICE-2016-FEX')

ax.set_xlabel(xlabel)
ax.set_ylabel('GDP share')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig21a.pdf', bbox_inches="tight")
plt.close()



###################### MAT ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'MATx'
de_new = states_new[de]
de_gams = states_gams[de]
de_new_FEX = states_new_FEX[de]
de_gams_FEX = states_gams_FEX[de]

x = ts[0:tl]

ax.plot(x, de_new[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE')
ax.plot(x, de_gams[0:tl], color='black', ls='solid',linewidth=1, label='DICE-2016')
ax.plot(x, de_new_FEX[0:tl], color='blue', ls='dashed',linewidth=4, label='CDICE-FEX')
ax.plot(x, de_gams_FEX[0:tl], color='black', ls='dashed',linewidth=1, label='DICE-2016-FEX')


ax.set_xlabel(xlabel)
ax.set_ylabel('GtC')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig20a.pdf', bbox_inches="tight")
plt.close()

###################### TAT ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'TATx'
de_new = states_new[de]
de_gams = states_gams[de]
de_new_FEX = states_new_FEX[de]
de_gams_FEX = states_gams_FEX[de]

x = ts[0:tl]

ax.plot(x, de_new[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE')
ax.plot(x, de_gams[0:tl], color='black', ls='solid',linewidth=1, label='DICE-2016')
ax.plot(x, de_new_FEX[0:tl], color='blue', ls='dashed',linewidth=4, label='CDICE-FEX')
ax.plot(x, de_gams_FEX[0:tl], color='black', ls='dashed',linewidth=1, label='DICE-2016-FEX')


ax.set_xlabel(xlabel)
ax.set_ylabel('deg. C')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig20b.pdf', bbox_inches="tight")
plt.close()

###################### SCC ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'scc'
de_new = def_new[de]
de_gams = def_gams[de]
de_new_FEX = def_new_FEX[de]
de_gams_FEX = def_gams_FEX[de]
x = ts[0:tl]

ax.plot(x, de_new[0:tl], color='blue', ls='solid', linewidth=4, label='CDICE')
ax.plot(x, de_gams[0:tl], color='black', ls='solid', linewidth=1, label='DICE-2016')
ax.plot(x, de_new_FEX[0:tl], color='blue', ls='dashed', linewidth=4, label='CDICE-FEX')
ax.plot(x, de_gams_FEX[0:tl], color='black', ls='dashed', linewidth=1, label='DICE-2016-FEX')

ax.set_xlabel(xlabel)
ax.set_ylabel('USD')
ax.legend(loc='upper left')

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig21b.pdf', bbox_inches="tight")
plt.close()
