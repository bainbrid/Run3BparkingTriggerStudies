from ROOT import TFile
from common import *

################################################################################
# Inputs and outputs

input = "latest/histos.root"
output = TFile('latest/eff.root','RECREATE')
outputs = {}

################################################################################
# Scaling

# Sample: /BuToKee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/RunIIAutumn18MiniAOD-Custom_RK_BParking_for_RK_102X_upgrade2018_realistic_v15-v2/MINIAODSIM 
# Number of MC events: 5690878

# Number of these MC signal events per integrated luminosity:
# N = L_int * XS * f_b * BF(b->muX) * BF(b->Kee) 
#   = 41.6 [/fb] * 4.7E8 [pb] *1E3 [fb/pb] * 0.4 * 0.2 * 4.5E-7
#   = 7.0E5
# ... but let's normalise to 100/fb!
# N = 7.0E5 * 100./41.6 = 1.69E6

# Normalise to the number of entries in DAS
events_processed_2021Dec16 = 4971934.
events_processed_2021Dec20 = 3181200.
events_processed = events_processed_2021Dec20
events_in_DAS = 5690878.
histo_scale = events_in_DAS/events_processed
print("histo_scale:",histo_scale,"events_in_DAS:",events_in_DAS,"events_processed:",events_processed)

# Account for GEN filter for MC signal sample = 0.0041, taken from:
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/PPD-RunIIFall18GS-00034
# N(pT>5,|eta|<2.5) = 1.69E6 * 0.0041 = 6929   <-- Normalise to 6900 (2 s.f.)!
 
# "lumi_scale" normalises the number of events_in_DAS to that expected from L_int (after GEN filter)
lumi_scale = 6900. / events_in_DAS
histo_scale *= lumi_scale

################################################################################
# All numer and denom histograms for pt1_vs_pt2

inputs_pt = [
    # numer, unweighted
    (input,"histo_pt1_vs_pt2_inc","histo_pt1_vs_pt2_inc_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_trg","histo_pt1_vs_pt2_trg_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_trg_cen","histo_pt1_vs_pt2_trg_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_trg_fwd","histo_pt1_vs_pt2_trg_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_trg9","histo_pt1_vs_pt2_trg9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_trg9_cen","histo_pt1_vs_pt2_trg9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_trg9_fwd","histo_pt1_vs_pt2_trg9_fwd_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_kee","histo_pt1_vs_pt2_kee_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_acc","histo_pt1_vs_pt2_acc_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_acc_cen","histo_pt1_vs_pt2_acc_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_acc_fwd","histo_pt1_vs_pt2_acc_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_acc9","histo_pt1_vs_pt2_acc9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_acc9_cen","histo_pt1_vs_pt2_acc9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_acc9_fwd","histo_pt1_vs_pt2_acc9_fwd_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_gen","histo_pt1_vs_pt2_gen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_gen_cen","histo_pt1_vs_pt2_gen_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_gen_fwd","histo_pt1_vs_pt2_gen_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_gen9","histo_pt1_vs_pt2_gen9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_gen9_cen","histo_pt1_vs_pt2_gen9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_gen9_fwd","histo_pt1_vs_pt2_gen9_fwd_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_sig","histo_pt1_vs_pt2_sig_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_rec","histo_pt1_vs_pt2_rec_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_cat","histo_pt1_vs_pt2_cat_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_cat_cen","histo_pt1_vs_pt2_cat_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_cat_fwd","histo_pt1_vs_pt2_cat_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_cat9","histo_pt1_vs_pt2_cat9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_cat9_cen","histo_pt1_vs_pt2_cat9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_cat9_fwd","histo_pt1_vs_pt2_cat9_fwd_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_pre","histo_pt1_vs_pt2_pre_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_bdt","histo_pt1_vs_pt2_bdt_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_bdt_cen","histo_pt1_vs_pt2_bdt_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_bdt_fwd","histo_pt1_vs_pt2_bdt_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_bdt9","histo_pt1_vs_pt2_bdt9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_bdt9_cen","histo_pt1_vs_pt2_bdt9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_bdt9_fwd","histo_pt1_vs_pt2_bdt9_fwd_unweighted",None,True,1.e6),

    (input,"histo_pt1_vs_pt2_qsq","histo_pt1_vs_pt2_qsq_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_qsq_cen","histo_pt1_vs_pt2_qsq_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_qsq_fwd","histo_pt1_vs_pt2_qsq_fwd_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_qsq9","histo_pt1_vs_pt2_qsq9_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_qsq9_cen","histo_pt1_vs_pt2_qsq9_cen_unweighted",None,True,1.e6),
    (input,"histo_pt1_vs_pt2_qsq9_fwd","histo_pt1_vs_pt2_qsq9_fwd_unweighted",None,True,1.e6),

    # numer, weighted
    (input,"histo_pt1_vs_pt2_inc","histo_pt1_vs_pt2_inc_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_trg","histo_pt1_vs_pt2_trg_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_trg_cen","histo_pt1_vs_pt2_trg_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_trg_fwd","histo_pt1_vs_pt2_trg_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_trg9","histo_pt1_vs_pt2_trg9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_trg9_cen","histo_pt1_vs_pt2_trg9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_trg9_fwd","histo_pt1_vs_pt2_trg9_fwd_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_kee","histo_pt1_vs_pt2_kee_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_acc","histo_pt1_vs_pt2_acc_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_acc_cen","histo_pt1_vs_pt2_acc_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_acc_fwd","histo_pt1_vs_pt2_acc_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_acc9","histo_pt1_vs_pt2_acc9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_acc9_cen","histo_pt1_vs_pt2_acc9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_acc9_fwd","histo_pt1_vs_pt2_acc9_fwd_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_gen","histo_pt1_vs_pt2_gen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_gen_cen","histo_pt1_vs_pt2_gen_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_gen_fwd","histo_pt1_vs_pt2_gen_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_gen9","histo_pt1_vs_pt2_gen9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_gen9_cen","histo_pt1_vs_pt2_gen9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_gen9_fwd","histo_pt1_vs_pt2_gen9_fwd_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_sig","histo_pt1_vs_pt2_sig_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_rec","histo_pt1_vs_pt2_rec_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_cat","histo_pt1_vs_pt2_cat_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_cat_cen","histo_pt1_vs_pt2_cat_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_cat_fwd","histo_pt1_vs_pt2_cat_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_cat9","histo_pt1_vs_pt2_cat9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_cat9_cen","histo_pt1_vs_pt2_cat9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_cat9_fwd","histo_pt1_vs_pt2_cat9_fwd_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_pre","histo_pt1_vs_pt2_pre_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_bdt","histo_pt1_vs_pt2_bdt_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_bdt_cen","histo_pt1_vs_pt2_bdt_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_bdt_fwd","histo_pt1_vs_pt2_bdt_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_bdt9","histo_pt1_vs_pt2_bdt9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_bdt9_cen","histo_pt1_vs_pt2_bdt9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_bdt9_fwd","histo_pt1_vs_pt2_bdt9_fwd_weighted",histo_scale,True,1.e3),

    (input,"histo_pt1_vs_pt2_qsq","histo_pt1_vs_pt2_qsq_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_qsq_cen","histo_pt1_vs_pt2_qsq_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_qsq_fwd","histo_pt1_vs_pt2_qsq_fwd_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_qsq9","histo_pt1_vs_pt2_qsq9_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_qsq9_cen","histo_pt1_vs_pt2_qsq9_cen_weighted",histo_scale,True,1.e3),
    (input,"histo_pt1_vs_pt2_qsq9_fwd","histo_pt1_vs_pt2_qsq9_fwd_weighted",histo_scale,True,1.e3),
    #
    #(input,"histo_pt1_vs_pt2_dr","histo_pt1_vs_pt2_dr_unweighted",None,True,1.e6),
    #(input,"histo_pt1_vs_pt2_dr","histo_pt1_vs_pt2_dr_weighted",histo_scale,True,3.e2),
]

for input,name,title,scale,logy,zmax in inputs_pt:
    print("inputs_pt:",name,title)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax)

################################################################################
# All numer and denom histograms for bdt_vs_pt2

inputs_bdt = [
#    # bdt_vs_pt2, unweighted
#    (input,"numer_bdt_vs_pt2_sum","numer_bdt_vs_pt2_sum_weighted",numer_scale,True,5.e3,"gt","gt"),
#    (input,"numer_pre_vs_pt2_sum","numer_pre_vs_pt2_sum_weighted",numer_scale,True,5.e3,"gt","gt"),
#    #(input,"numer_bdt_vs_pt2_cen","numer_bdt_vs_pt2_cen_weighted",numer_scale,True,5.e3,"gt","gt"),
#    #(input,"numer_bdt_vs_pt2_fwd","numer_bdt_vs_pt2_fwd_weighted",numer_scale,True,5.e3,"gt","gt"),
#    #(input,"numer_dr_vs_pt2","numer_dr_vs_pt2_weighted",numer_scale,True,5.e3,None,"lt"),
#    #(input,"denom_dr_vs_pt2","denom_dr_vs_pt2_weighted",numer_scale,True,5.e3,None,"lt"),
]

#for input,name,title,scale,logy,zmax,xcumu,ycumu in inputs_bdt:
#    print("inputs_bdt:",name,xcumu,ycumu)
#    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax,xcumu,ycumu)

################################################################################
# denom histo for bdt

inputs_transform = [
#    #("numer_bdt_vs_pt2_sum_weighted","numer_pt1_vs_pt2_gen_weighted","numer_bdt_vs_pt2_sum_weighted_transformed"),
#    ("numer_bdt_vs_pt2_sum_weighted","numer_pt1_vs_pt2_pre_weighted","numer_bdt_vs_pt2_sum_weighted_transformed"),
#
#    #("numer_bdt_vs_pt2_cen_weighted","numer_pt1_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed"),
#    #("numer_bdt_vs_pt2_fwd_weighted","numer_pt1_vs_pt2_fwd_weighted","numer_bdt_vs_pt2_fwd_weighted_transformed"),
#
#    #("numer_pre_vs_pt2_sum_weighted","numer_pt1_vs_pt2_gen_weighted","numer_pre_vs_pt2_sum_weighted_transformed"),
#    ("numer_pre_vs_pt2_sum_weighted","numer_pt1_vs_pt2_cat_weighted","numer_pre_vs_pt2_sum_weighted_transformed"),
]

#for numer,denom,title in inputs_transform:
#    print("transform_eff:",numer)
#    outputs[title] = transformDenom(output,numer=outputs[numer],denom=outputs[denom],title=title)

################################################################################
# All efficiency histograms

inputs_eff = [
    # pt_vs_pt
    ("histo_pt1_vs_pt2_inc_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_inc_weighted",1.),

    ("histo_pt1_vs_pt2_trg_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg_weighted",1.),
    ("histo_pt1_vs_pt2_trg_cen_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg_cen_weighted",1.),
    ("histo_pt1_vs_pt2_trg_fwd_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_trg9_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg9_weighted",1.),
    ("histo_pt1_vs_pt2_trg9_cen_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_trg9_fwd_weighted","histo_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_trg9_fwd_weighted",1.),

    ("histo_pt1_vs_pt2_kee_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_kee_weighted",1.),

    ("histo_pt1_vs_pt2_acc_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_acc_weighted",1.),
    ("histo_pt1_vs_pt2_acc_cen_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_acc_cen_weighted",1.),
    ("histo_pt1_vs_pt2_acc_fwd_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_acc_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_acc9_weighted","histo_pt1_vs_pt2_trg9_weighted","eff_pt1_vs_pt2_acc9_weighted",1.),
    ("histo_pt1_vs_pt2_acc9_cen_weighted","histo_pt1_vs_pt2_trg9_cen_weighted","eff_pt1_vs_pt2_acc9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_acc9_fwd_weighted","histo_pt1_vs_pt2_trg9_fwd_weighted","eff_pt1_vs_pt2_acc9_fwd_weighted",1.),

    ("histo_pt1_vs_pt2_gen_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_gen_weighted",1.),
    ("histo_pt1_vs_pt2_gen_cen_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_gen_cen_weighted",1.),
    ("histo_pt1_vs_pt2_gen_fwd_weighted","histo_pt1_vs_pt2_trg_weighted","eff_pt1_vs_pt2_gen_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_gen9_weighted","histo_pt1_vs_pt2_trg9_weighted","eff_pt1_vs_pt2_gen9_weighted",1.),
    ("histo_pt1_vs_pt2_gen9_cen_weighted","histo_pt1_vs_pt2_trg9_cen_weighted","eff_pt1_vs_pt2_gen9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_gen9_fwd_weighted","histo_pt1_vs_pt2_trg9_fwd_weighted","eff_pt1_vs_pt2_gen9_fwd_weighted",1.),

    ("histo_pt1_vs_pt2_sig_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_sig_weighted",1.),
    ("histo_pt1_vs_pt2_rec_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_rec_weighted",1.),

    ("histo_pt1_vs_pt2_cat_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_cat_weighted",1.),
    ("histo_pt1_vs_pt2_cat_cen_weighted","histo_pt1_vs_pt2_gen_cen_weighted","eff_pt1_vs_pt2_cat_cen_weighted",1.),
    ("histo_pt1_vs_pt2_cat_fwd_weighted","histo_pt1_vs_pt2_gen_fwd_weighted","eff_pt1_vs_pt2_cat_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_cat9_weighted","histo_pt1_vs_pt2_gen9_weighted","eff_pt1_vs_pt2_cat9_weighted",1.),
    ("histo_pt1_vs_pt2_cat9_cen_weighted","histo_pt1_vs_pt2_gen9_cen_weighted","eff_pt1_vs_pt2_cat9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_cat9_fwd_weighted","histo_pt1_vs_pt2_gen9_fwd_weighted","eff_pt1_vs_pt2_cat9_fwd_weighted",1.),

    ("histo_pt1_vs_pt2_pre_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_pre_weighted",1.),

    ("histo_pt1_vs_pt2_bdt_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_bdt_weighted",1.),
    ("histo_pt1_vs_pt2_bdt_cen_weighted","histo_pt1_vs_pt2_gen_cen_weighted","eff_pt1_vs_pt2_bdt_cen_weighted",1.),
    ("histo_pt1_vs_pt2_bdt_fwd_weighted","histo_pt1_vs_pt2_gen_fwd_weighted","eff_pt1_vs_pt2_bdt_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_bdt9_weighted","histo_pt1_vs_pt2_gen9_weighted","eff_pt1_vs_pt2_bdt9_weighted",1.),
    ("histo_pt1_vs_pt2_bdt9_cen_weighted","histo_pt1_vs_pt2_gen9_cen_weighted","eff_pt1_vs_pt2_bdt9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_bdt9_fwd_weighted","histo_pt1_vs_pt2_gen9_fwd_weighted","eff_pt1_vs_pt2_bdt9_fwd_weighted",1.),

    ("histo_pt1_vs_pt2_qsq_weighted","histo_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_qsq_weighted",1.),
    ("histo_pt1_vs_pt2_qsq_cen_weighted","histo_pt1_vs_pt2_gen_cen_weighted","eff_pt1_vs_pt2_qsq_cen_weighted",1.),
    ("histo_pt1_vs_pt2_qsq_fwd_weighted","histo_pt1_vs_pt2_gen_fwd_weighted","eff_pt1_vs_pt2_qsq_fwd_weighted",1.),
    ("histo_pt1_vs_pt2_qsq9_weighted","histo_pt1_vs_pt2_gen9_weighted","eff_pt1_vs_pt2_qsq9_weighted",1.),
    ("histo_pt1_vs_pt2_qsq9_cen_weighted","histo_pt1_vs_pt2_gen9_cen_weighted","eff_pt1_vs_pt2_qsq9_cen_weighted",1.),
    ("histo_pt1_vs_pt2_qsq9_fwd_weighted","histo_pt1_vs_pt2_gen9_fwd_weighted","eff_pt1_vs_pt2_qsq9_fwd_weighted",1.),

#    # relative efficiencies                                                                
#    ("denom_pt1_vs_pt2_trg_weighted","denom_pt1_vs_pt2_inc_weighted","rel_pt1_vs_pt2_trg_weighted",1.),
#    ("denom_pt1_vs_pt2_acc_weighted","denom_pt1_vs_pt2_trg_weighted","rel_pt1_vs_pt2_acc_weighted",1.),

    #("numer_pt1_vs_pt2_dr_weighted","numer_pt1_vs_pt2_gen_weighted","eff_pt1_vs_pt2_dr_weighted",1.),
                                                                                            
#    # bdt_vs_pt
#    ("numer_bdt_vs_pt2_sum_weighted","numer_bdt_vs_pt2_sum_weighted_transformed","eff_bdt_vs_pt2_sum_weighted",1.),
#    #("numer_bdt_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed","eff_bdt_vs_pt2_cen_weighted",1.),
#    #("numer_bdt_vs_pt2_fwd_weighted","numer_bdt_vs_pt2_fwd_weighted_transformed","eff_bdt_vs_pt2_fwd_weighted",1.),
#    ("numer_pre_vs_pt2_sum_weighted","numer_pre_vs_pt2_sum_weighted_transformed","eff_pre_vs_pt2_sum_weighted",1.),
#    # dr_vs_pt
#    #("numer_dr_vs_pt2_weighted","denom_dr_vs_pt2_weighted","eff_dr_vs_pt2_weighted",1.),
]

for numer,denom,title,zmax in inputs_eff:
    print("inputs_eff:",name)
    outputs[title] = writeEffCumu(output,outputs[numer],outputs[denom],title,zmax)

################################################################################
# Outputs 

print(inputs_pt)
print(inputs_bdt)
print(inputs_eff)
print(outputs)
output.Close()
