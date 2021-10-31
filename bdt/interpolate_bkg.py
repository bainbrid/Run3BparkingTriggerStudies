### source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib as mpl
mpl.use('pdf')
from matplotlib import pyplot as plt
from matplotlib import rc
#.Allow for using TeX mode in matplotlib Figures
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman']})
rc('text', usetex=True)
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]

ratio=5.0/7.0
fig_width_pt = 3*246.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = ratio if ratio != 0.0 else (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]

params = {'text.usetex' : True,
        'axes.labelsize': 24,
        'font.size': 24,
        'legend.fontsize': 16,
        'xtick.labelsize': 24,
        'ytick.labelsize': 24,
        'font.family' : 'lmodern',
        'text.latex.unicode': True,
        'axes.grid' : True,
        'text.usetex': True,
        'figure.figsize': fig_size}
plt.rcParams.update(params)

# model: a*exp(-bx^2+cx+d)
def model(x, a, b, c, d):
  return a*np.exp(-b*x*x + c*x + d)

if __name__ == "__main__":

  # read csv file
  df = pd.read_csv('log_kee_bparkPU_v7.2_fullrange_pf.csv')
  # define the range of fit
  df_tofit = df.query('(cut > 4) and (cut < 8)')
  # fit
  popt, pcov = curve_fit(model, df_tofit['cut'], df_tofit['nbkg'])
  print('fit: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt))

  x = np.linspace(0, 10, 1000)
  y = model(x, *popt)

  fig, ax = plt.subplots()
  ax.plot(df['cut'], df['nbkg'], 'bo', mec='b', linestyle="None", label="Data")
  ax.plot(x, y, 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f, d=%5.3f' % tuple(popt))
  ax.set_yscale('log')
  ax.set_xlabel('MVA cut')
  ax.set_ylabel('Number of background')
  ax.legend(loc='best')
  fig.savefig('fit.pdf', bbox_inches='tight')


