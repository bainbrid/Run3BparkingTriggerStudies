from ROOT import TFile
from common import *
#import copy, math

################################################################################
# Outputs
outputs = {}
output = TFile('latest/eff.root','RECREATE')

################################################################################
# Denominator histogram, open, no selection
title="denom_pt1_vs_pt2_after_inc_unweighted"
outputs[title] = writeHisto(output,"latest/denom.root","denom_pt1_vs_pt2_after_inc",title,zmax=5.e3)

################################################################################
# Scaling
entries=outputs[title].GetEntries()
DAS_entries = 31585558.
denom_scale = DAS_entries / entries
files_processed = 5.#77.
files_available = 79.
numer_scale = files_available / files_processed

################################################################################
# All numer and denom histograms for pt1_vs_pt2
inputs_pt = [
    # unweighted (denom_nosel_unweighted is above ^^^)
    ("latest/denom.root","denom_pt1_vs_pt2_after_inc","denom_pt1_vs_pt2_after_inc_unweighted",None,True,1.e5),
    ("latest/denom.root","denom_pt1_vs_pt2_after_cen","denom_pt1_vs_pt2_after_cen_unweighted",None,True,1.e5),
    ("latest/numer.root","numer_pt1_vs_pt2_after_lq2","numer_pt1_vs_pt2_after_lq2_unweighted",None,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_eta","numer_pt1_vs_pt2_after_eta_unweighted",None,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_ana","numer_pt1_vs_pt2_after_ana_unweighted",None,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_bdt","numer_pt1_vs_pt2_after_bdt_unweighted",None,True,5.e3),
    # weighted
    ("latest/denom.root","denom_pt1_vs_pt2_after_inc","denom_pt1_vs_pt2_after_inc_weighted",denom_scale,True,5.e6),
    ("latest/denom.root","denom_pt1_vs_pt2_after_cen","denom_pt1_vs_pt2_after_cen_weighted",denom_scale,True,5.e6),
    ("latest/numer.root","numer_pt1_vs_pt2_after_lq2","numer_pt1_vs_pt2_after_lq2_weighted",numer_scale,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_eta","numer_pt1_vs_pt2_after_eta_weighted",numer_scale,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_ana","numer_pt1_vs_pt2_after_ana_weighted",numer_scale,True,5.e3),
    ("latest/numer.root","numer_pt1_vs_pt2_after_bdt","numer_pt1_vs_pt2_after_bdt_weighted",numer_scale,True,5.e3),
]
for input,name,title,scale,logy,zmax in inputs_pt:
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax)

################################################################################
# All numer and denom histograms for bdt_vs_pt2
inputs_bdt = [
    # bdt_vs_pt2, unweighted
    ("latest/numer.root","numer_bdt_vs_pt2_after_ana","numer_bdt_vs_pt2_after_ana_unweighted",None,True,5.e3,None,"gt"),
    ("latest/numer.root","numer_bdt_vs_pt2_after_ana","numer_bdt_vs_pt2_after_ana_weighted",numer_scale,True,5.e3,None,"gt"),
]
for input,name,title,scale,logy,zmax,xcumu,ycumu in inputs_bdt:
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax,xcumu,ycumu)

################################################################################
# denom histo for bdt
title="denom_pt1_vs_pt2_after_cen_weighted_transformed"
outputs[title] = transformDenom(output,
                                numer=outputs["numer_bdt_vs_pt2_after_ana_weighted"],
                                denom=outputs["denom_pt1_vs_pt2_after_cen_weighted"],
                                title=title)

################################################################################
# All efficiency histograms
inputs_eff = [
    # pt_vs_pt
    ("numer_pt1_vs_pt2_after_lq2_weighted","denom_pt1_vs_pt2_after_cen_weighted","eff_pt1_vs_pt2_cumu_lq2_weighted",1.),
    ("numer_pt1_vs_pt2_after_eta_weighted","denom_pt1_vs_pt2_after_cen_weighted","eff_pt1_vs_pt2_cumu_eta_weighted",1.),
    ("numer_pt1_vs_pt2_after_ana_weighted","denom_pt1_vs_pt2_after_cen_weighted","eff_pt1_vs_pt2_cumu_ana_weighted",1.),
    ("numer_pt1_vs_pt2_after_bdt_weighted","denom_pt1_vs_pt2_after_cen_weighted","eff_pt1_vs_pt2_cumu_bdt_weighted",1.),
    # bdt_vs_pt
    ("numer_bdt_vs_pt2_after_ana_weighted","denom_pt1_vs_pt2_after_cen_weighted_transformed","eff_bdt_vs_pt2_after_ana_weighted",1.),
]
for numer,denom,title,zmax in inputs_eff:
    outputs[title] = writeEff(output,outputs[numer],outputs[denom],title,zmax)

################################################################################
# Outputs 
print(inputs_pt)
print(inputs_bdt)
print(inputs_eff)
print(outputs)
output.Close()

## debug
#xbin = 2
#ybin = 2
#print "xbin",xbin,"ybin",ybin
#print "denom:",
#xlow = denom_histo.GetXaxis().GetBinLowEdge(xbin)
#ylow = denom_histo.GetYaxis().GetBinLowEdge(xbin)
#print "xlow",xlow,"ylow",ylow,
#denom = denom_histo.GetBinContent(xbin,ybin)
#unwei = denom_histo2.GetBinContent(xbin,ybin)
#print "wei",denom,"unw",unwei,"ratio",denom/unwei
#print "numer:",
#xlow = numer_histo.GetXaxis().GetBinLowEdge(xbin)
#ylow = numer_histo.GetYaxis().GetBinLowEdge(xbin)
#print "xlow",xlow,"ylow",ylow,
#numer = numer_histo.GetBinContent(xbin,ybin)
#unwei = numer_histo2.GetBinContent(xbin,ybin)
#print "wei",numer,"unw",unwei,"ratio",numer/unwei
#print "eff",numer/denom
