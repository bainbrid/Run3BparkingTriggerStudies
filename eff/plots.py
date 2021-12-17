from ROOT import TFile
from common import *

################################################################################
# Inputs and outputs

input = "latest/numer.root"
output = TFile('latest/eff.root','RECREATE')
outputs = {}

################################################################################
# Scaling

# Normalise (approximately) to the number of files in DAS
#files_processed = 97.
#files_available = 195.
#numer_scale = files_available/files_processed
#print("numer_scale:",numer_scale,"files_available:",files_available,"files_processed:",files_processed)

# Normalise to the number of entries in DAS
events_processed = 4971934.
events_available = 5690878.
numer_scale = events_available/events_processed
print("numer_scale:",numer_scale,"events_available:",events_available,"events_processed:",events_processed)

# To luminosity:
# N = L_int * XS * f_b * BF(b->muX) * BF(b->Kee) 
#   = 41.6E3 [\fb] * 4.68E8 [fb] * 0.4 * 0.2 * 4.5E-7
#   = 7.0E5
# Let's normalise to 100/fb !!!
# N = 1.69E6
# Sample: /BuToKee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/RunIIAutumn18MiniAOD-Custom_RK_BParking_for_RK_102X_upgrade2018_realistic_v15-v2/MINIAODSIM 
# Number of MC events: 5690878
# Account for GEN filter = 0.0041, taken from:
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/PPD-RunIIFall18GS-00034
# N(pT>5,|eta|<2.5) = 1.69E6 * 0.0041 = 6929   <-- Normalise to this number!
 
# lumi_scale normalises # entries in DAS to that expected from Lint (after GEN filter)
DAS_entries = 5690878.
lumi_scale = 6929. / DAS_entries
numer_scale *= lumi_scale

################################################################################
# All numer and denom histograms for pt1_vs_pt2
inputs_pt = [
    # numer, unweighted
    (input,"numer_pt1_vs_pt2_inc","numer_pt1_vs_pt2_inc_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_trg","numer_pt1_vs_pt2_trg_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_kee","numer_pt1_vs_pt2_kee_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_acc","numer_pt1_vs_pt2_acc_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_gen","numer_pt1_vs_pt2_gen_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_sig","numer_pt1_vs_pt2_sig_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_rec","numer_pt1_vs_pt2_rec_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_cat","numer_pt1_vs_pt2_cat_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_pre","numer_pt1_vs_pt2_pre_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_bdt","numer_pt1_vs_pt2_bdt_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_gen_cen","numer_pt1_vs_pt2_gen_cen_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_gen_fwd","numer_pt1_vs_pt2_gen_fwd_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_cat_cen","numer_pt1_vs_pt2_cat_cen_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_cat_fwd","numer_pt1_vs_pt2_cat_fwd_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_bdt_cen","numer_pt1_vs_pt2_bdt_cen_unweighted",None,True,1.e6),
    (input,"numer_pt1_vs_pt2_bdt_fwd","numer_pt1_vs_pt2_bdt_fwd_unweighted",None,True,1.e6),
    # numer, weighted
    (input,"numer_pt1_vs_pt2_inc","numer_pt1_vs_pt2_inc_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_trg","numer_pt1_vs_pt2_trg_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_kee","numer_pt1_vs_pt2_kee_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_acc","numer_pt1_vs_pt2_acc_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_gen","numer_pt1_vs_pt2_gen_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_sig","numer_pt1_vs_pt2_sig_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_rec","numer_pt1_vs_pt2_rec_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_cat","numer_pt1_vs_pt2_cat_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_pre","numer_pt1_vs_pt2_pre_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_bdt","numer_pt1_vs_pt2_bdt_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_gen_cen","numer_pt1_vs_pt2_gen_cen_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_gen_fwd","numer_pt1_vs_pt2_gen_fwd_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_cat_cen","numer_pt1_vs_pt2_cat_cen_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_cat_fwd","numer_pt1_vs_pt2_cat_fwd_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_bdt_cen","numer_pt1_vs_pt2_bdt_cen_weighted",numer_scale,True,1.e3),
    (input,"numer_pt1_vs_pt2_bdt_fwd","numer_pt1_vs_pt2_bdt_fwd_weighted",numer_scale,True,1.e3),
    #
    #(input,"numer_pt1_vs_pt2_dr","numer_pt1_vs_pt2_dr_unweighted",None,True,1.e6),
    #(input,"numer_pt1_vs_pt2_dr","numer_pt1_vs_pt2_dr_weighted",numer_scale,True,3.e2),
]
for input,name,title,scale,logy,zmax in inputs_pt:
    print("inputs_pt:",name,title)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax)

################################################################################
# All numer and denom histograms for bdt_vs_pt2
inputs_bdt = [
    # bdt_vs_pt2, unweighted
    (input,"numer_bdt_vs_pt2_sum","numer_bdt_vs_pt2_sum_weighted",numer_scale,True,5.e3,"gt","gt"),
    (input,"numer_pre_vs_pt2_sum","numer_pre_vs_pt2_sum_weighted",numer_scale,True,5.e3,"gt","gt"),
    #(input,"numer_bdt_vs_pt2_cen","numer_bdt_vs_pt2_cen_weighted",numer_scale,True,5.e3,"gt","gt"),
    #(input,"numer_bdt_vs_pt2_fwd","numer_bdt_vs_pt2_fwd_weighted",numer_scale,True,5.e3,"gt","gt"),
    #(input,"numer_dr_vs_pt2","numer_dr_vs_pt2_weighted",numer_scale,True,5.e3,None,"lt"),
    #(input,"denom_dr_vs_pt2","denom_dr_vs_pt2_weighted",numer_scale,True,5.e3,None,"lt"),
]
for input,name,title,scale,logy,zmax,xcumu,ycumu in inputs_bdt:
    print("inputs_bdt:",name,xcumu,ycumu)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax,xcumu,ycumu)

################################################################################
# denom histo for bdt
inputs_transform = [
    #("numer_bdt_vs_pt2_sum_weighted","numer_pt1_vs_pt2_gen_weighted","numer_bdt_vs_pt2_sum_weighted_transformed"),
    ("numer_bdt_vs_pt2_sum_weighted","numer_pt1_vs_pt2_pre_weighted","numer_bdt_vs_pt2_sum_weighted_transformed"),

    #("numer_bdt_vs_pt2_cen_weighted","numer_pt1_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed"),
    #("numer_bdt_vs_pt2_fwd_weighted","numer_pt1_vs_pt2_fwd_weighted","numer_bdt_vs_pt2_fwd_weighted_transformed"),

    #("numer_pre_vs_pt2_sum_weighted","numer_pt1_vs_pt2_gen_weighted","numer_pre_vs_pt2_sum_weighted_transformed"),
    ("numer_pre_vs_pt2_sum_weighted","numer_pt1_vs_pt2_cat_weighted","numer_pre_vs_pt2_sum_weighted_transformed"),
]
for numer,denom,title in inputs_transform:
    print("transform_eff:",numer)
    outputs[title] = transformDenom(output,numer=outputs[numer],denom=outputs[denom],title=title)

################################################################################
# All efficiency histograms
inputs_eff = [
    # pt_vs_pt
    ("numer_pt1_vs_pt2_inc_weighted","numer_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_inc_weighted",1.),
    ("numer_pt1_vs_pt2_trg_weighted","numer_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg_weighted",1.),
    ("numer_pt1_vs_pt2_kee_weighted","numer_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_kee_weighted",1.),
    ("numer_pt1_vs_pt2_acc_weighted","numer_pt1_vs_pt2_kee_weighted","eff_pt1_vs_pt2_acc_weighted",1.),
    ("numer_pt1_vs_pt2_gen_weighted","numer_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_gen_weighted",1.),
    ("numer_pt1_vs_pt2_sig_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_sig_weighted",1.),
    ("numer_pt1_vs_pt2_rec_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_rec_weighted",1.),
    ("numer_pt1_vs_pt2_cat_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_cat_weighted",1.),
    ("numer_pt1_vs_pt2_pre_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_pre_weighted",1.),
    ("numer_pt1_vs_pt2_bdt_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_bdt_weighted",1.),
    ("numer_pt1_vs_pt2_gen_cen_weighted","numer_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_gen_cen_weighted",1.),
    ("numer_pt1_vs_pt2_gen_fwd_weighted","numer_pt1_vs_pt2_acc_weighted","eff_pt1_vs_pt2_gen_fwd_weighted",1.),
    ("numer_pt1_vs_pt2_cat_cen_weighted","numer_pt1_vs_pt2_gen_cen_weighted","eff_pt1_vs_pt2_cat_cen_weighted",1.),
    ("numer_pt1_vs_pt2_cat_fwd_weighted","numer_pt1_vs_pt2_gen_fwd_weighted","eff_pt1_vs_pt2_cat_fwd_weighted",1.),
    ("numer_pt1_vs_pt2_bdt_cen_weighted","numer_pt1_vs_pt2_gen_cen_weighted","eff_pt1_vs_pt2_bdt_cen_weighted",1.),
    ("numer_pt1_vs_pt2_bdt_fwd_weighted","numer_pt1_vs_pt2_gen_fwd_weighted","eff_pt1_vs_pt2_bdt_fwd_weighted",1.),
#    # relative efficiencies                                                                
#    ("denom_pt1_vs_pt2_trg_weighted","denom_pt1_vs_pt2_inc_weighted","rel_pt1_vs_pt2_trg_weighted",1.),
#    ("denom_pt1_vs_pt2_acc_weighted","denom_pt1_vs_pt2_trg_weighted","rel_pt1_vs_pt2_acc_weighted",1.),

    #("numer_pt1_vs_pt2_dr_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_dr_weighted",1.),
                                                                                            
    # bdt_vs_pt
    ("numer_bdt_vs_pt2_sum_weighted","numer_bdt_vs_pt2_sum_weighted_transformed","eff_bdt_vs_pt2_sum_weighted",1.),
    #("numer_bdt_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed","eff_bdt_vs_pt2_cen_weighted",1.),
    #("numer_bdt_vs_pt2_fwd_weighted","numer_bdt_vs_pt2_fwd_weighted_transformed","eff_bdt_vs_pt2_fwd_weighted",1.),
    ("numer_pre_vs_pt2_sum_weighted","numer_pre_vs_pt2_sum_weighted_transformed","eff_pre_vs_pt2_sum_weighted",1.),
    # dr_vs_pt
    #("numer_dr_vs_pt2_weighted","denom_dr_vs_pt2_weighted","eff_dr_vs_pt2_weighted",1.),
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


################################################################################
################################################################################

#    (input,"numer_pt1_vs_pt2_sig","numer_pt1_vs_pt2_sig_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_gen","numer_pt1_vs_pt2_gen_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec","numer_pt1_vs_pt2_rec_unweighted",None,True,1.e6),#@@

#    (input,"numer_pt1_vs_pt2_kee0","numer_pt1_vs_pt2_kee0_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_acc0","numer_pt1_vs_pt2_acc0_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec0","numer_pt1_vs_pt2_rec0_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_kee1","numer_pt1_vs_pt2_kee1_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_acc1","numer_pt1_vs_pt2_acc1_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec1","numer_pt1_vs_pt2_rec1_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_kee2","numer_pt1_vs_pt2_kee2_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_acc2","numer_pt1_vs_pt2_acc2_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec2","numer_pt1_vs_pt2_rec2_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_kee3","numer_pt1_vs_pt2_kee3_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_acc3","numer_pt1_vs_pt2_acc3_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec3","numer_pt1_vs_pt2_rec3_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_kee4","numer_pt1_vs_pt2_kee4_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_acc4","numer_pt1_vs_pt2_acc4_unweighted",None,True,1.e6),#@@
#    (input,"numer_pt1_vs_pt2_rec4","numer_pt1_vs_pt2_rec4_unweighted",None,True,1.e6),#@@

#    ("numer_pt1_vs_pt2_rec_unweighted","numer_pt1_vs_pt2_acc_unweighted","eff_pt1_vs_pt2_rec_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_acc0_unweighted","numer_pt1_vs_pt2_kee0_unweighted","eff_pt1_vs_pt2_acc0_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_rec0_unweighted","numer_pt1_vs_pt2_acc0_unweighted","eff_pt1_vs_pt2_rec0_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_acc1_unweighted","numer_pt1_vs_pt2_kee1_unweighted","eff_pt1_vs_pt2_acc1_unweighted",1.),#@@
#    #("numer_pt1_vs_pt2_acc1_unweighted","numer_pt1_vs_pt2_acc_unweighted","rel_pt1_vs_pt2_acc1_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_rec1_unweighted","numer_pt1_vs_pt2_acc1_unweighted","eff_pt1_vs_pt2_rec1_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_acc2_unweighted","numer_pt1_vs_pt2_kee2_unweighted","eff_pt1_vs_pt2_acc2_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_rec2_unweighted","numer_pt1_vs_pt2_acc2_unweighted","eff_pt1_vs_pt2_rec2_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_acc3_unweighted","numer_pt1_vs_pt2_kee3_unweighted","eff_pt1_vs_pt2_acc3_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_rec3_unweighted","numer_pt1_vs_pt2_acc3_unweighted","eff_pt1_vs_pt2_rec3_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_acc4_unweighted","numer_pt1_vs_pt2_kee4_unweighted","eff_pt1_vs_pt2_acc4_unweighted",1.),#@@
#    ("numer_pt1_vs_pt2_rec4_unweighted","numer_pt1_vs_pt2_acc4_unweighted","eff_pt1_vs_pt2_rec4_unweighted",1.),#@@

