### source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh

from ROOT import TFile,TH2F,TAxis
import pandas as pd
import numpy as np

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

def model(x, a, b, c, d):
  return a*np.exp(-b*x*x + c*x + d)

if __name__ == "__main__":

  funcs = {
    'pT-2GeV':  lambda x: 4.031*np.exp(-0.111*x*x + 0.012*x + 7.361),
    'pT-5GeV':  lambda x: 2.009*np.exp(-0.044*x*x - 0.531*x + 8.040),
    'pT-10GeV': lambda x: 0.534*np.exp(-0.080*x*x + 0.164*x + 5.432),
    }

  for name,func in funcs.items() :
    for cut in xrange(4,9,1):
      print "name:",name,"cut:",cut,"bkgd counts:",func(cut)

  file_ = TFile('eff.root')
  eff_cen = file_.Get('eff_bdt_vs_pt2_cen_weighted')
  eff_sum = file_.Get('eff_bdt_vs_pt2_sum_weighted')

  bdt_threshold = 8. + 1.e-3
  ybin = eff_cen.GetYaxis().FindBin(bdt_threshold)
  for xbin in xrange(1,eff_sum.GetXaxis().GetNbins()+1):
    print("xbin:",xbin,
          "bdt_threshold:",bdt_threshold,
          "ybin",ybin,
          "eff_sum:",eff_sum.GetBinContent(xbin,ybin)
          )

  xaxis = [4,5,6,7,8,9,10,11,12,]
  yaxis = []
  for pt in [2]:
    for bdt in xaxis:
      xbin = eff_sum.GetXaxis().FindBin(pt+1.e-3)
      ybin = eff_sum.GetYaxis().FindBin(bdt+1.e-3)
      eff = eff_sum.GetBinContent(xbin,ybin)
      signal = eff * 35.
      bkgd = funcs['pT-2GeV'](bdt)
      significance = signal / np.sqrt(signal+bkgd)
      yaxis.append(significance)
      print("pt:",pt,
            "xbin:",xbin,
            "bdt cut:",bdt,
            "ybin:",ybin,
            "eff: {:.2f}".format(eff),
            "signal: {:.2f}".format(signal),
            "bkgd: {:.2f}".format(bkgd),
            "significance: {:.2f}".format(significance)
            ) 
    
  fig, ax = plt.subplots()
  ax.plot(xaxis,yaxis,'bo')#,mec='b',linestyle="",)
  #ax.set_xlim(0.1,1.e5)
  #ax.set_ylim(0.1,1.e5)
  ax.set_xlabel('MVA cut')
  ax.set_ylabel('Significance')
  ax.legend(loc='best')
  fig.savefig('scan.pdf'.format(name), bbox_inches='tight')


