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
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_cdice/'
exparams_cdice = pd.read_csv(path + 'exoparams.csv')
states_cdice = pd.read_csv(path +'states.csv')
ps_cdice = pd.read_csv(path +'ps.csv')
def_cdice = pd.read_csv(path +'defs.csv')
time_cdice = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + GISS
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_giss/'
exparams_cdice_giss = pd.read_csv(path + 'exoparams.csv')
states_cdice_giss = pd.read_csv(path +'states.csv')
ps_cdice_giss = pd.read_csv(path +'ps.csv')
def_cdice_giss = pd.read_csv(path +'defs.csv')
time_cdice_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_hadgem/'
exparams_cdice_hadgem = pd.read_csv(path + 'exoparams.csv')
states_cdice_hadgem = pd.read_csv(path +'states.csv')
ps_cdice_hadgem = pd.read_csv(path +'ps.csv')
def_cdice_hadgem = pd.read_csv(path +'defs.csv')
time_cdice_hadgem = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + mesmo
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_mesmo/'
exparams_cdice_mesmo = pd.read_csv(path + 'exoparams.csv')
states_cdice_mesmo = pd.read_csv(path +'states.csv')
ps_cdice_mesmo = pd.read_csv(path +'ps.csv')
def_cdice_mesmo = pd.read_csv(path +'defs.csv')
time_cdice_mesmo = pd.read_csv(path +'time.csv')

### READING THE DATA from new CDICE + loveclim
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mmm_loveclim/'
exparams_cdice_loveclim = pd.read_csv(path + 'exoparams.csv')
states_cdice_loveclim = pd.read_csv(path +'states.csv')
ps_cdice_loveclim = pd.read_csv(path +'ps.csv')
def_cdice_loveclim = pd.read_csv(path +'defs.csv')
time_cdice_loveclim = pd.read_csv(path +'time.csv')

## READING THE DATA from new mesmo + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mesmo_hadgem/'
exparams_mesmo_hadgem = pd.read_csv(path + 'exoparams.csv')
states_mesmo_hadgem = pd.read_csv(path +'states.csv')
ps_mesmo_hadgem = pd.read_csv(path +'ps.csv')
def_mesmo_hadgem = pd.read_csv(path +'defs.csv')
time_mesmo_hadgem = pd.read_csv(path +'time.csv')

## READING THE DATA from new mesmo + giss
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_mesmo_giss/'
exparams_mesmo_giss = pd.read_csv(path + 'exoparams.csv')
states_mesmo_giss = pd.read_csv(path +'states.csv')
ps_mesmo_giss = pd.read_csv(path +'ps.csv')
def_mesmo_giss = pd.read_csv(path +'defs.csv')
time_mesmo_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from new loveclim + hadgem
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_loveclim_hadgem/'
exparams_loveclim_hadgem = pd.read_csv(path + 'exoparams.csv')
states_loveclim_hadgem = pd.read_csv(path +'states.csv')
ps_loveclim_hadgem = pd.read_csv(path +'ps.csv')
def_loveclim_hadgem = pd.read_csv(path +'defs.csv')
time_loveclim_hadgem = pd.read_csv(path +'time.csv')

### READING THE DATA from new loveclim + giss
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/gdice_baseline/bau_results/BAU_loveclim_giss/'
exparams_loveclim_giss = pd.read_csv(path + 'exoparams.csv')
states_loveclim_giss = pd.read_csv(path +'states.csv')
ps_loveclim_giss = pd.read_csv(path +'ps.csv')
def_loveclim_giss = pd.read_csv(path +'defs.csv')
time_loveclim_giss = pd.read_csv(path +'time.csv')

### READING THE DATA from RCP
path = '/home/alexmalova/Documents/dummy_repo_CDICE/DEQN_for_IAMs/RCP_data/'
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



###################### Inverse Discount rate ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'ynet'

ynet_cdice = def_cdice[de]
ynet_cdice_giss = def_cdice_giss[de]
ynet_cdice_hadgem = def_cdice_hadgem[de]
ynet_cdice_mesmo = def_cdice_mesmo[de]
ynet_cdice_loveclim = def_cdice_loveclim[de]
ynet_mesmo_giss = def_mesmo_giss[de]
ynet_mesmo_hadgem = def_mesmo_hadgem[de]
ynet_loveclim_giss = def_loveclim_giss[de]
ynet_loveclim_hadgem = def_loveclim_hadgem[de]

de = 'kx'

kx_cdice = states_cdice[de]
kx_cdice_giss = states_cdice_giss[de]
kx_cdice_hadgem = states_cdice_hadgem[de]
kx_cdice_mesmo = states_cdice_mesmo[de]
kx_cdice_loveclim = states_cdice_loveclim[de]
kx_mesmo_giss = states_mesmo_giss[de]
kx_mesmo_hadgem = states_mesmo_hadgem[de]
kx_loveclim_giss = states_loveclim_giss[de]
kx_loveclim_hadgem = states_loveclim_hadgem[de]

de = 'gr_tfp'

grtfp_cdice = exparams_cdice[de]
grtfp_cdice_giss = exparams_cdice_giss[de]
grtfp_cdice_hadgem = exparams_cdice_hadgem[de]
grtfp_cdice_mesmo = exparams_cdice_mesmo[de]
grtfp_cdice_loveclim = exparams_cdice_loveclim[de]
grtfp_mesmo_giss = exparams_mesmo_giss[de]
grtfp_mesmo_hadgem = exparams_mesmo_hadgem[de]
grtfp_loveclim_giss = exparams_loveclim_giss[de]
grtfp_loveclim_hadgem = exparams_loveclim_hadgem[de]

de = 'gr_lab'

grlab_cdice = exparams_cdice[de]
grlab_cdice_giss = exparams_cdice_giss[de]
grlab_cdice_hadgem = exparams_cdice_hadgem[de]
grlab_cdice_mesmo = exparams_cdice_mesmo[de]
grlab_cdice_loveclim = exparams_cdice_loveclim[de]
grlab_mesmo_giss = exparams_mesmo_giss[de]
grlab_mesmo_hadgem = exparams_mesmo_hadgem[de]
grlab_loveclim_giss = exparams_loveclim_giss[de]
grlab_loveclim_hadgem = exparams_loveclim_hadgem[de]

delta = 0.1
alpha = 0.3

oneplusr_cdice = alpha * ynet_cdice / kx_cdice + (1 - delta)
oneplusr_cdice_giss =  alpha * ynet_cdice_giss / kx_cdice_giss + (1 - delta)
oneplusr_cdice_hadgem = alpha * ynet_cdice_hadgem / kx_cdice_hadgem + (1 - delta)
oneplusr_cdice_mesmo = alpha * ynet_cdice_mesmo / kx_cdice_mesmo + (1 - delta)
oneplusr_cdice_loveclim = alpha * ynet_cdice_loveclim / kx_cdice_loveclim + (1 - delta)
oneplusr_mesmo_giss = alpha * ynet_mesmo_giss / kx_mesmo_giss + (1 - delta)
oneplusr_mesmo_hadgem = alpha * ynet_mesmo_hadgem / kx_mesmo_hadgem + (1 - delta)
oneplusr_loveclim_giss = alpha * ynet_loveclim_giss / kx_loveclim_giss + (1 - delta)
oneplusr_loveclim_hadgem = alpha * ynet_loveclim_hadgem / kx_loveclim_hadgem + (1 - delta)

de_cdice = (1 + grtfp_cdice + grlab_cdice)**(-1) * oneplusr_cdice
de_cdice_giss = (1 + grtfp_cdice_giss + grlab_cdice_giss)**(-1) * oneplusr_cdice_giss
de_cdice_hadgem = (1 + grtfp_cdice_hadgem + grlab_cdice_hadgem)**(-1) * oneplusr_cdice_hadgem
de_cdice_mesmo = (1 + grtfp_cdice_mesmo + grlab_cdice_mesmo)**(-1) * oneplusr_cdice_mesmo
de_cdice_loveclim = (1 + grtfp_cdice_loveclim + grlab_cdice_loveclim)**(-1) * oneplusr_cdice_loveclim
de_mesmo_giss = (1 + grtfp_mesmo_giss + grlab_mesmo_giss)**(-1) * oneplusr_mesmo_giss
de_mesmo_hadgem = (1 + grtfp_mesmo_hadgem + grlab_mesmo_hadgem)**(-1) * oneplusr_mesmo_hadgem
de_loveclim_giss = (1 + grtfp_loveclim_giss + grlab_loveclim_giss)**(-1) * oneplusr_loveclim_giss
de_loveclim_hadgem = (1 + grtfp_loveclim_hadgem + grlab_loveclim_hadgem)**(-1) * oneplusr_loveclim_hadgem

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', label='CDICE-LOVECLIM-HadGEM2-ES')

ax.set_xlabel(xlabel)
ax.set_ylabel('Fraction')
ax.legend(loc='lower right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig11b.pdf', bbox_inches="tight")
plt.close()



###################### Damages ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'Omega'

de_cdice = def_cdice[de]
de_cdice_giss = def_cdice_giss[de]
de_cdice_hadgem = def_cdice_hadgem[de]
de_cdice_mesmo = def_cdice_mesmo[de]
de_cdice_loveclim = def_cdice_loveclim[de]
de_mesmo_giss = def_mesmo_giss[de]
de_mesmo_hadgem = def_mesmo_hadgem[de]
de_loveclim_giss = def_loveclim_giss[de]
de_loveclim_hadgem = def_loveclim_hadgem[de]

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', label='CDICE-LOVECLIM-HadGEM2-ES')

ax.set_xlabel(xlabel)
ax.set_ylabel('GDP share, percent')
ax.legend(loc='upper left')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig12a.pdf', bbox_inches="tight")
plt.close()
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
rcp85 = rcp85_ind + rcp85_land
rcp60 = rcp60_ind + rcp60_land

x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', label='CDICE-LOVECLIM-HadGEM2-ES')
ax.plot(x, rcp85[0:tl], color='red', ls='solid', label='RCP 8.5')
ax.plot(x, rcp60[0:tl], color='orange', ls='solid', label='RCP 6.0')

ax.set_xlabel(xlabel)
ax.set_ylabel('GtCO2')
ax.legend(loc='upper right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig11a.pdf', bbox_inches="tight")
plt.close()



###################### scc over gdp ############################################
fig=plt.figure(figsize=(15,10))
ax=fig.add_subplot(2,2,1)

de = 'ynet'

ynet_cdice = def_cdice[de]
ynet_cdice_giss = def_cdice_giss[de]
ynet_cdice_hadgem = def_cdice_hadgem[de]
ynet_cdice_mesmo = def_cdice_mesmo[de]
ynet_cdice_loveclim = def_cdice_loveclim[de]
ynet_mesmo_giss = def_mesmo_giss[de]
ynet_mesmo_hadgem = def_mesmo_hadgem[de]
ynet_loveclim_giss = def_loveclim_giss[de]
ynet_loveclim_hadgem = def_loveclim_hadgem[de]

de = 'scc'

scc_cdice = def_cdice[de]
scc_cdice_giss = def_cdice_giss[de]
scc_cdice_hadgem = def_cdice_hadgem[de]
scc_cdice_mesmo = def_cdice_mesmo[de]
scc_loveclim_giss = def_loveclim_giss[de]
scc_loveclim_hadgem = def_loveclim_hadgem[de]
scc_cdice_loveclim = def_cdice_loveclim[de]
scc_mesmo_giss = def_mesmo_giss[de]
scc_mesmo_hadgem = def_mesmo_hadgem[de]
scc_loveclim_giss = def_loveclim_giss[de]
scc_loveclim_hadgem = def_loveclim_hadgem[de]


de_cdice = scc_cdice / ynet_cdice
de_cdice_giss =  scc_cdice_giss / ynet_cdice_giss
de_cdice_hadgem = scc_cdice_hadgem / ynet_cdice_hadgem
de_cdice_mesmo =  scc_cdice_mesmo / ynet_cdice_mesmo
de_cdice_loveclim =  scc_cdice_loveclim / ynet_cdice_loveclim
de_mesmo_giss =  scc_mesmo_giss / ynet_mesmo_giss
de_mesmo_hadgem = scc_mesmo_hadgem / ynet_mesmo_hadgem
de_loveclim_giss = scc_loveclim_giss / ynet_loveclim_giss
de_loveclim_hadgem = scc_loveclim_hadgem / ynet_loveclim_hadgem

tl = 30
x = ts[0:tl]

ax.plot(x, de_cdice[0:tl], color='blue', ls='solid', label='CDICE')
ax.plot(x, de_cdice_giss[0:tl], color='#92F41C', ls='solid', label='CDICE-GISS-E2-R')
ax.plot(x, de_cdice_hadgem[0:tl], color='#20CBD1', ls='solid', label='CDICE-HadGEM2-ES')
ax.plot(x, de_cdice_mesmo[0:tl], color='blue', ls='dotted', label='CDICE-MESMO')
ax.plot(x, de_cdice_loveclim[0:tl], color='blue', ls='dashed', label='CDICE-LOVECLIM')
ax.plot(x, de_mesmo_giss[0:tl], color='#92F41C', ls='dotted', label='CDICE-MESMO-GISS-E2-R')
ax.plot(x, de_mesmo_hadgem[0:tl], color='#20CBD1', ls='dotted', label='CDICE-MESMO-HadGEM2-ES')
ax.plot(x, de_loveclim_giss[0:tl], color='#92F41C', ls='dashed', label='CDICE-LOVECLIM-GISS-E2-R')
ax.plot(x, de_loveclim_hadgem[0:tl], color='#20CBD1', ls='dashed', label='CDICE-LOVECLIM-HadGEM2-ES')

ax.set_xlabel(xlabel)
ax.set_ylabel('USD')
ax.legend(loc='upper right')
plt.xlim([0,tl])

fig.tight_layout(pad = 2.0)
plt.savefig('figs/fig12b.pdf', bbox_inches="tight")
plt.close()
