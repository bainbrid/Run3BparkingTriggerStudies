from ROOT import TFile
from common import *

################################################################################
# Inputs and outputs
outputs = {}
output = TFile('latest/eff.root','RECREATE')

input_denom = "latest/denom.root"
input_numer = "latest/numer.root"

################################################################################
# Denominator histogram, open, no selection
title="denom_pt1_vs_pt2_inc_unweighted"
outputs[title] = writeHisto(output,input_denom,"denom_pt1_vs_pt2_inc",title,zmax=1.e5)

################################################################################
# Scaling

# Denominator
entries=outputs[title].GetEntries()
print("entries:",entries)
DAS_entries = 31585558.
# denom_scale normalises to number of entries in DAS
denom_scale = DAS_entries / entries

# Numerator
files_processed = 76.
files_available = 79.
# numer_scale normalises (implicitly) to number of entries in DAS
numer_scale = ( files_available / files_processed )

# To luminosity:
# N = L_int * XS * f_b * BF(b->muX) * BF(b->Kee) 
#   = 41.6E3 [\fb] * 4.68E8 [fb] * 0.4 * 0.2 * 4.5E-7
#   = 7.0E5
# Let's normalise to 100/fb !!!
# N = 1.69E6
# Account for GEN filter = 0.0011, taken from:
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/BPH-RunIIFall18GS-00245
# N(pT > 6 GeV) = 1.69E6 * 0.0011 = 1857   <-- Normalise to this number!
 
# lumi_scale normalises # entries in DAS to that expected from Lint (after GEN filter)
lumi_scale = 1857. / DAS_entries
denom_scale *= lumi_scale
numer_scale *= lumi_scale

print("numer_scale:",numer_scale,"files_available:",files_available,"files_processed:",files_processed)
print("denom_scale:",denom_scale,"DAS_entries:",DAS_entries,"entries:",entries)

################################################################################
# All numer and denom histograms for pt1_vs_pt2
inputs_pt = [
    # denom, unweighted 
    # for "denom_pt1_vs_pt2_inc_unweighted", see above ^^^
    (input_denom,"denom_pt1_vs_pt2_trg","denom_pt1_vs_pt2_trg_unweighted",None,True,1.e5),
    (input_denom,"denom_pt1_vs_pt2_acc","denom_pt1_vs_pt2_acc_unweighted",None,True,1.e5),
    (input_denom,"denom_pt1_vs_pt2_cen","denom_pt1_vs_pt2_cen_unweighted",None,True,1.e5),
    (input_denom,"denom_pt1_vs_pt2_fwd","denom_pt1_vs_pt2_fwd_unweighted",None,True,1.e5),
    (input_denom,"denom_pt1_vs_pt2_sum","denom_pt1_vs_pt2_sum_unweighted",None,True,1.e5),
    # denom, weighted
    (input_denom,"denom_pt1_vs_pt2_inc","denom_pt1_vs_pt2_inc_weighted",denom_scale,True,3.e2),
    (input_denom,"denom_pt1_vs_pt2_trg","denom_pt1_vs_pt2_trg_weighted",denom_scale,True,3.e2),
    (input_denom,"denom_pt1_vs_pt2_acc","denom_pt1_vs_pt2_acc_weighted",denom_scale,True,3.e2),
    (input_denom,"denom_pt1_vs_pt2_cen","denom_pt1_vs_pt2_cen_weighted",denom_scale,True,3.e2),
    (input_denom,"denom_pt1_vs_pt2_fwd","denom_pt1_vs_pt2_fwd_weighted",denom_scale,True,3.e2),
    (input_denom,"denom_pt1_vs_pt2_sum","denom_pt1_vs_pt2_sum_weighted",denom_scale,True,3.e2),
    # numer, unweighted
    (input_numer,"numer_pt1_vs_pt2_inc","numer_pt1_vs_pt2_inc_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_trg","numer_pt1_vs_pt2_trg_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_acc","numer_pt1_vs_pt2_acc_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_rec","numer_pt1_vs_pt2_rec_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_sig","numer_pt1_vs_pt2_sig_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_pre","numer_pt1_vs_pt2_pre_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_lq2","numer_pt1_vs_pt2_lq2_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_bdt","numer_pt1_vs_pt2_bdt_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_cen","numer_pt1_vs_pt2_cen_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_fwd","numer_pt1_vs_pt2_fwd_unweighted",None,True,2.e4),
    (input_numer,"numer_pt1_vs_pt2_sum","numer_pt1_vs_pt2_sum_unweighted",None,True,2.e4),
    # numer, weighted
    (input_numer,"numer_pt1_vs_pt2_inc","numer_pt1_vs_pt2_inc_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_trg","numer_pt1_vs_pt2_trg_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_acc","numer_pt1_vs_pt2_acc_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_rec","numer_pt1_vs_pt2_rec_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_sig","numer_pt1_vs_pt2_sig_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_pre","numer_pt1_vs_pt2_pre_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_lq2","numer_pt1_vs_pt2_lq2_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_bdt","numer_pt1_vs_pt2_bdt_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_cen","numer_pt1_vs_pt2_cen_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_fwd","numer_pt1_vs_pt2_fwd_weighted",numer_scale,True,3.e2),
    (input_numer,"numer_pt1_vs_pt2_sum","numer_pt1_vs_pt2_sum_weighted",numer_scale,True,3.e2),
]
for input,name,title,scale,logy,zmax in inputs_pt:
    print("inputs_pt:",name,title)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax)

################################################################################
# All numer and denom histograms for bdt_vs_pt2
inputs_bdt = [
    # bdt_vs_pt2, unweighted
    (input_numer,"numer_bdt_vs_pt2_cen","numer_bdt_vs_pt2_cen_weighted",numer_scale,True,5.e3,"gt","gt"),
    (input_numer,"numer_bdt_vs_pt2_fwd","numer_bdt_vs_pt2_fwd_weighted",numer_scale,True,5.e3,"gt","gt"),
    (input_numer,"numer_bdt_vs_pt2_sum","numer_bdt_vs_pt2_sum_weighted",numer_scale,True,5.e3,"gt","gt"),
]
for input,name,title,scale,logy,zmax,xcumu,ycumu in inputs_bdt:
    print("inputs_bdt:",name)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax,xcumu,ycumu)

################################################################################
# denom histo for bdt
inputs_transform = [
    ("numer_bdt_vs_pt2_cen_weighted","denom_pt1_vs_pt2_cen_weighted","denom_pt1_vs_pt2_cen_weighted_transformed"),
    ("numer_bdt_vs_pt2_fwd_weighted","denom_pt1_vs_pt2_fwd_weighted","denom_pt1_vs_pt2_fwd_weighted_transformed"),
    ("numer_bdt_vs_pt2_sum_weighted","denom_pt1_vs_pt2_sum_weighted","denom_pt1_vs_pt2_sum_weighted_transformed"),
]
for numer,denom,title in inputs_transform:
    print("transform_eff:",numer)
    outputs[title] = transformDenom(output,numer=outputs[numer],denom=outputs[denom],title=title)

################################################################################
# All efficiency histograms
inputs_eff = [
    # pt_vs_pt
    ("numer_pt1_vs_pt2_inc_weighted","denom_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_inc_weighted",1.),
    ("numer_pt1_vs_pt2_trg_weighted","denom_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_trg_weighted",1.),
    ("numer_pt1_vs_pt2_acc_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_acc_weighted",1.),
    ("numer_pt1_vs_pt2_rec_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_reco_weighted",1.),
    ("numer_pt1_vs_pt2_sig_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_sig_weighted",1.),
    ("numer_pt1_vs_pt2_pre_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_pre_weighted",1.),
    ("numer_pt1_vs_pt2_lq2_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_lq2_weighted",1.),
    ("numer_pt1_vs_pt2_bdt_weighted","denom_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_bdt_weighted",1.),
    ("numer_pt1_vs_pt2_cen_weighted","denom_pt1_vs_pt2_cen_weighted","eff_pt1_vs_pt2_cen_weighted",1.),
    ("numer_pt1_vs_pt2_fwd_weighted","denom_pt1_vs_pt2_fwd_weighted","eff_pt1_vs_pt2_fwd_weighted",1.),
    ("numer_pt1_vs_pt2_sum_weighted","denom_pt1_vs_pt2_sum_weighted","eff_pt1_vs_pt2_sum_weighted",1.),
    # relative efficiencies
    ("denom_pt1_vs_pt2_trg_weighted","denom_pt1_vs_pt2_inc_weighted","rel_pt1_vs_pt2_trg_weighted",1.),
    ("denom_pt1_vs_pt2_acc_weighted","denom_pt1_vs_pt2_trg_weighted","rel_pt1_vs_pt2_acc_weighted",1.),
    # bdt_vs_pt
    ("numer_bdt_vs_pt2_cen_weighted","denom_pt1_vs_pt2_cen_weighted_transformed","eff_bdt_vs_pt2_cen_weighted",1.),
    ("numer_bdt_vs_pt2_fwd_weighted","denom_pt1_vs_pt2_fwd_weighted_transformed","eff_bdt_vs_pt2_fwd_weighted",1.),
    ("numer_bdt_vs_pt2_sum_weighted","denom_pt1_vs_pt2_sum_weighted_transformed","eff_bdt_vs_pt2_sum_weighted",1.),
]
for numer,denom,title,zmax in inputs_eff:
    print("inputs_eff:",name)
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
