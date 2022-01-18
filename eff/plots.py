from ROOT import TFile
from common import *

################################################################################
# Inputs and outputs

input_2021Dec16 = "latest/histos_2021Dec16.root"
input_2021Dec20 = "latest/histos_2021Dec20.root"
input_incl = "latest/histos_incl.root"
input_excl = "latest/histos_excl.root"
output = TFile('latest/eff.root','RECREATE')
outputs = {}

################################################################################
# Scaling

# Default sample is BuToKee_v3:
#  /BuToKee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen
#  /RunIIAutumn18MiniAOD-Custom_RK_BParking_for_RK_102X_upgrade2018_realistic_v15-v2
#  /MINIAODSIM
# Number of MC events: 5690878
# GEN filter (pT>5,|eta|<2.5) for MC signal sample = 0.0041, taken from:
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/PPD-RunIIFall18GS-00034

# Record number of MC events from partially processed samples
# Comment: pt1_pt2_gen_weighted distrbutions agree to within 2% for Dec16 and Dec20, so use high-stats Dec16 ...
events_2021Dec16 = 4971934. # 98.5% complete (194/197 files), reco only
events_2021Dec20 = 3181200. # 78.2% complete (154/197 files), reco + nano pre-sel
events_incl = 106049.
events_excl = 110252.
print("events_2021Dec16:",events_2021Dec16)
print("events_2021Dec20:",events_2021Dec20)
print("events_incl:",events_incl)
print("events_excl:",events_excl)

# Number of B->Kee signal events per integrated luminosity:
# N = L_int * XS * f_b * BF(b->muX) * BF(b->Kee) 
#   = 41.6 [/fb] * 4.7E8 [pb] *1E3 [fb/pb] * 0.4 * 0.2 * 4.5E-7 = 7.0E5
l_int = 41.6 # [/pb]
xs = 4.7e8 * 1.e3 # [pb]
f_b = 0.4
bf_bmux = 0.0051 # this is b->muX with mu pT > 5 GeV and |eta| < 2.5 (i.e. not the usual 0.2)
bf_bkee = 4.5e-7
exp_incl = l_int * xs * f_b * (1.-(1.-bf_bkee)**2.)       # b->X (natural decay), B->Kee
exp_2021Dec16 = l_int * xs * f_b * bf_bmux * bf_bkee * 2. # b->muX (forced decay), B->Kee, or vice verse (hence "* 2.")
exp_2021Dec20 = exp_2021Dec16
exp_excl = exp_2021Dec20

print("exp_2021Dec16",exp_2021Dec16)
print("exp_2021Dec20",exp_2021Dec20)
print("exp_incl",exp_incl)
print("exp_excl",exp_excl)
print("temp",(1.-(1.-bf_bkee)**2.)/(bf_bmux * bf_bkee))
 
# Determine event weight to normalise the number of MC events to that exp_2021Dec20 from L_int (after GEN filter)
weight_2021Dec16 = exp_2021Dec16 / events_2021Dec16
weight_2021Dec20 = exp_2021Dec20 / events_2021Dec20
weight_incl = exp_incl / events_incl
weight_excl = exp_excl / events_excl
print("weight_2021Dec16:",weight_2021Dec16)
print("weight_2021Dec20:",weight_2021Dec20)
print("weight_incl:",weight_incl)
print("weight_excl:",weight_excl)

histos=[
    # Section 5.3
    (input_incl,"histo_pt1_vs_pt2_inc","hincl_pt1_vs_pt2_inc_weighted",weight_incl,True,None,1.e6,None,None,None),
    # Section 5.4
    (input_2021Dec16,"histo_pt1_vs_pt2_inc","his16_pt1_vs_pt2_inc_weighted",weight_2021Dec16,True,None,1.e6,None,None,None),
    (input_2021Dec16,"histo_pt1_vs_pt2_trg9","his16_pt1_vs_pt2_trg9_weighted",weight_2021Dec16,True,None,1.e6,None,None,None),
    (input_2021Dec16,"histo_pt1_vs_pt2_gen9","his16_pt1_vs_pt2_gen9_weighted",weight_2021Dec16,True,None,1.e6,None,None,None),
    (input_incl,"histo_pt1_vs_pt2_gen_cen","hincl_pt1_vs_pt2_gen_weighted",weight_incl,True,None,1.e6,None,2.,2.),
    # Section 5.5
    (input_2021Dec16,"histo_pt1_vs_pt2_gen9","his16_pt1_vs_pt2_gen9_rebinned",weight_2021Dec16,True,None,1.e6,2,2.,2.),
    (input_2021Dec16,"histo_pt1_vs_pt2_cat9","his16_pt1_vs_pt2_rec9_weighted",weight_2021Dec16,True,None,1.e6,2,2.,2.), #@@ RECO
    (input_2021Dec20,"histo_pt1_vs_pt2_cat9","his20_pt1_vs_pt2_nan9_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.), #@@ NANO
    (input_2021Dec20,"histo_pt1_vs_pt2_pre9","his20_pt1_vs_pt2_pre9_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec20,"histo_pt1_vs_pt2_bdt9","his20_pt1_vs_pt2_bdt9_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec20,"histo_pt1_vs_pt2_qsq9","his20_pt1_vs_pt2_qsq9_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec16,"histo_pt1_vs_pt2_gen_cen","his16_pt1_vs_pt2_gen_rebinned",weight_2021Dec16,True,None,1.e6,2,2.,2.),
    (input_2021Dec16,"histo_pt1_vs_pt2_cat_cen","his16_pt1_vs_pt2_rec_weighted",weight_2021Dec16,True,None,1.e6,2,2.,2.), #@@ RECO
    (input_2021Dec20,"histo_pt1_vs_pt2_cat_cen","his20_pt1_vs_pt2_nan_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.), #@@ NANO
    (input_2021Dec20,"histo_pt1_vs_pt2_pre_cen","his20_pt1_vs_pt2_pre_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec20,"histo_pt1_vs_pt2_bdt_cen","his20_pt1_vs_pt2_bdt_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec20,"histo_pt1_vs_pt2_qsq_cen","his20_pt1_vs_pt2_qsq_weighted",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    # Misc
    (input_2021Dec20,"histo_pt1_vs_pt2_gen9","his20_pt1_vs_pt2_gen9_rebinned",weight_2021Dec20,True,None,1.e6,2,2.,2.),
    (input_2021Dec16,"histo_pt1_vs_pt2_acc9","his16_pt1_vs_pt2_acc9_rebinned",weight_2021Dec16,True,None,1.e6,2,None,None),
    # Appendix
#    (input_incl,"histo_pt1_vs_pt2_inc","hincl_pt1_vs_pt2_inc_unweighted",None,True,None,1.e6,None),
#    (input_2021Dec20,"histo_pt1_vs_pt2_inc","his20_pt1_vs_pt2_inc_weighted",weight_2021Dec20,True,None,1.e6,None),
#    (input_2021Dec20,"histo_pt1_vs_pt2_acc9","his20_pt1_vs_pt2_acc9_unweighted",None,True,None,1.e6,2),
#    (input_2021Dec20,"histo_pt1_vs_pt2_trg9","his20_pt1_vs_pt2_trg9_unweighted",None,True,None,1.e6,2),
#    #
#    (input_2021Dec16,"histo_pt1_vs_pt2_gen_cen","his16_pt1_vs_pt2_gen_unweighted",None,True,None,1.e6,None),
#    (input_2021Dec20,"histo_pt1_vs_pt2_gen_cen","his20_pt1_vs_pt2_gen_unweighted",None,True,None,1.e6,None),
#    #
#    (input_2021Dec16,"histo_pt1_vs_pt2_gen9","his16_pt1_vs_pt2_gen9_unweighted",None,True,None,1.e6,2),
#    (input_2021Dec20,"histo_pt1_vs_pt2_gen9","his20_pt1_vs_pt2_gen9_unweighted",None,True,None,1.e6,2),
#    (input_2021Dec16,"histo_pt1_vs_pt2_cat9","his16_pt1_vs_pt2_rec9_unweighted",None,True,None,1.e6,2), #@@ RECO
#    (input_2021Dec20,"histo_pt1_vs_pt2_cat9","his20_pt1_vs_pt2_nan9_unweighted",None,True,None,1.e6,2), #@@ NANO
#    (input_2021Dec20,"histo_pt1_vs_pt2_pre9","his20_pt1_vs_pt2_pre9_unweighted",None,True,None,1.e6,2),
#    (input_2021Dec20,"histo_pt1_vs_pt2_bdt9","his20_pt1_vs_pt2_bdt9_unweighted",None,True,None,1.e6,2),
#    (input_2021Dec20,"histo_pt1_vs_pt2_qsq9","his20_pt1_vs_pt2_qsq9_unweighted",None,True,None,1.e6,2),
    #
    ]
for input,name,title,scale,logy,zmin,zmax,rebin,xmin,ymin in histos:
    print("histos:",name,title)
    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmin,zmax,rebin=rebin)
    writeHisto(output,input,name,title,scale,logy,zmin,zmax,xcumu="gt",ycumu="gt",rebin=rebin) # cumu plots

effs=[
    # Section 5.4
    ("his16_pt1_vs_pt2_gen9_weighted","his16_pt1_vs_pt2_trg9_weighted","eff_pt1_vs_pt2_gen9_weighted",0.,1.,2.,2.),
    ("hincl_pt1_vs_pt2_gen_weighted","hincl_pt1_vs_pt2_inc_weighted","eff_pt1_vs_pt2_gen_weighted",0.,1.,2.,2.),
    # Section 5.5
    ("his16_pt1_vs_pt2_rec9_weighted","his16_pt1_vs_pt2_gen9_rebinned","eff_pt1_vs_pt2_rec9_weighted",0.,1.,2.,2.), #@@ RECO
    ("his20_pt1_vs_pt2_nan9_weighted","his16_pt1_vs_pt2_rec9_weighted","eff_pt1_vs_pt2_nan9_weighted",0.,1.,2.,2.), #@@ NANO
    ("his20_pt1_vs_pt2_pre9_weighted","his20_pt1_vs_pt2_nan9_weighted","eff_pt1_vs_pt2_pre9_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_bdt9_weighted","his20_pt1_vs_pt2_pre9_weighted","eff_pt1_vs_pt2_bdt9_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_qsq9_weighted","his20_pt1_vs_pt2_bdt9_weighted","eff_pt1_vs_pt2_qsq9_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_qsq9_weighted","his16_pt1_vs_pt2_gen9_rebinned","tot16_pt1_vs_pt2_qsq9_weighted",0.,0.2,2.,2.),
    ("his16_pt1_vs_pt2_rec_weighted","his16_pt1_vs_pt2_gen_rebinned","eff_pt1_vs_pt2_rec_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_nan_weighted","his16_pt1_vs_pt2_rec_weighted","eff_pt1_vs_pt2_nan_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_pre_weighted","his20_pt1_vs_pt2_nan_weighted","eff_pt1_vs_pt2_pre_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_bdt_weighted","his20_pt1_vs_pt2_pre_weighted","eff_pt1_vs_pt2_bdt_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_qsq_weighted","his20_pt1_vs_pt2_bdt_weighted","eff_pt1_vs_pt2_qsq_weighted",0.,1.,2.,2.),
    ("his20_pt1_vs_pt2_qsq_weighted","his16_pt1_vs_pt2_gen_rebinned","tot16_pt1_vs_pt2_qsq_weighted",0.,0.2,2.,2.),
    # Appendix
    ("his16_pt1_vs_pt2_rec9_weighted","his16_pt1_vs_pt2_acc9_rebinned","acc_pt1_vs_pt2_rec9_weighted",0.,1.,None,None), #@@ RECO
    ]
for numer,denom,title,zmin,zmax,xmin,ymin in effs:
    print("effs:",name)
    outputs[title] = writeEffCumu(output,outputs[numer],outputs[denom],title,zmin,zmax,xmin=xmin,ymin=ymin)

#effs=[
#    ("his20_pt1_vs_pt2_nan9_weighted","his16_pt1_vs_pt2_gen9_rebinned","eff16_pt1_vs_pt2_nan9_weighted",0.,1.), #@@ NANO (see below)
#    ("his20_pt1_vs_pt2_nan9_weighted","his20_pt1_vs_pt2_gen9_rebinned","eff20_pt1_vs_pt2_nan9_weighted",0.,1.), #@@ NANO (see below)
#    ("eff20_pt1_vs_pt2_nan9_weighted","eff_pt1_vs_pt2_rec9_weighted","eff_pt1_vs_pt2_nan9_weighted",0.,1.), #@@ NANO (see above)
#    ]
#for numer,denom,title,zmin,zmax in effs:
#    print("effs:",name)
#    outputs[title] = writeEffCumu(output,outputs[numer],outputs[denom],title,zmin,zmax)

#bdt_histos = [
#    (input,"numer_bdt_vs_pt2_cen","numer_bdt_vs_pt2_cen_weighted",numer_scale,True,5.e3,"gt","gt"),
#    ]
#for input,name,title,scale,logy,zmax,xcumu,ycumu in bdt_histos:
#    print("inputs_bdt:",name,xcumu,ycumu)
#    outputs[title] = writeHisto(output,input,name,title,scale,logy,zmax,xcumu,ycumu)
#
#bdt_transformed = [
#    ("numer_bdt_vs_pt2_cen_weighted","numer_pt1_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed"),
#    ]
#for numer,denom,title in bdt_transformed:
#    print("transformed:",numer)
#    outputs[title] = transformDenom(output,numer=outputs[numer],denom=outputs[denom],title=title)
#
#bdt_effs=[
#    ("numer_bdt_vs_pt2_cen_weighted","numer_bdt_vs_pt2_cen_weighted_transformed","eff_bdt_vs_pt2_cen_weighted",0.,1.),
#    ]
#for numer,denom,title,zmin,zmax in bdt_effs:
#    print("effs:",name)
#    outputs[title] = writeEffCumu(output,outputs[numer],outputs[denom],title,zmin,zmax)

output.Close()
