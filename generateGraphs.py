import copy, math, os
from numpy import array
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TGraphErrors, Double
from DisplayManager import DisplayManager, add_Preliminary, add_CMS, add_label
from officialStyle import officialStyle
from array import array
import numpy as np

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

from optparse import OptionParser, OptionValueError
usage = "usage: python runTauDisplay_BsTauTau.py"
parser = OptionParser(usage)

parser.add_option("-t", "--type", default='ult', type="string", help="type [rate, eff, anal, ult]", dest="type")
parser.add_option("-l", "--lumi", default=1, type="float", help="target lumi. with [E34]", dest="lumi")
parser.add_option('-w', '--weight', action="store_true", default=True, dest='weight')
parser.add_option("-q", "--q2", default='low', type="string", help="q2 [low, high]", dest="q2")
parser.add_option("-p", "--plot", action="store_true", default=False, dest="plot")

(options, args) = parser.parse_args()

print options

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]

#drdict = {
#    3:1,
#    4:1,
#    5:1,
#    6:1,
#    7:1,
#    8:0.8,
#    9:0.7,
#    10:0.65,
#    11:0.6,
#    12:0.55,
#    13:0.5,
#    14:0.45,
#}

drdict = {
    3:1,
    4:1,
    5:0.9,
    6:0.8,
    7:0.75,
    8:0.7,
    9:0.65,
    10:0.6,
    11:0.55,
    12:0.5,
    13:0.45,
    14:0.4,
}



gen_pt  = 'gen_e1_pt > 0.5 && gen_e2_pt > 0.5'
gen_eta = 'abs(gen_e1_eta) < 2.4 && abs(gen_e2_eta) < 2.4'
#gen_q2  = '(gen_mass*gen_mass) > 1.1 && (gen_mass*gen_mass) < 6.25'

#if options.q2 =='high': gen_q2 = 'gen_mass*gen_mass > 14.82'

gencut = ' && '.join([gen_pt, gen_eta]) #, gen_q2]) # don't apply gen_ q2 req.
print 'gencut = ', gencut

eff_histo = None
if options.weight:
    eff_file = TFile('root/eff.root')
    eff_histo = eff_file.Get('eff')
    print eff_histo, 'detected'

def calc(name, num, den):
    eff = num/den
    efferr = 0.
    if num!=0:
        efferr = math.sqrt(eff*(1-eff)/den)
    print "name:", name, " numer: ",num, " denom: ", den, " eff: ", eff, " err: ", efferr
    return eff, efferr

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def createGraph(name):

    graph = TGraphErrors()            
    graph.SetName(name)
    graph.SetTitle(name)

    return copy.deepcopy(graph)


def fillGraph(rootfile, type, fitname, sel, gencut, graph, ipt, pt):


    
#    sf = Double(1.)

    if type!='rate':
        tree = rootfile.Get('tree')

        den = Double(tree.GetEntries())
        num = Double(tree.GetEntries(sel))

        if type=='anal': 
            den = Double(tree.GetEntries(sel))
            num = Double(tree.GetEntries(sel + ' && ' + gencut))

        if type=='eff': 
            num = Double(tree.GetEntries(sel))

        if type=='ult': 
            if not options.weight:
                num = Double(tree.GetEntries(sel + ' && ' + gencut))
            else:
                num = 0
                ybins = eff_histo.GetYaxis().GetNbins()
                xbins = eff_histo.GetXaxis().GetNbins()
                for ybin in range(1,ybins+1):
                    for xbin in range(1,xbins+1):
                        if xbin > ybin : continue
                        eff = eff_histo.GetBinContent(xbin,ybin)
                        y_down = eff_histo.GetYaxis().GetBinLowEdge(ybin)
                        y_up = eff_histo.GetYaxis().GetBinLowEdge(ybin) + eff_histo.GetYaxis().GetBinWidth(ybin)
                        x_down = eff_histo.GetXaxis().GetBinLowEdge(xbin)
                        x_up = eff_histo.GetXaxis().GetBinLowEdge(xbin) + eff_histo.GetXaxis().GetBinWidth(xbin)
                        gen_e1_pt = 'gen_e1_pt > ' + str(y_down)
                        if ybin < ybins : gen_e1_pt += ' && ' + 'gen_e1_pt < ' + str(y_up)
                        gen_e2_pt = 'gen_e2_pt > ' + str(x_down)
                        if xbin < xbins : gen_e2_pt += ' && ' + 'gen_e2_pt < ' + str(x_up)
                        newgencut = ' && '.join([gen_e1_pt, gen_e2_pt, gen_eta])
                        entry = Double(tree.GetEntries(sel + ' && ' + newgencut))
                        num += entry*eff
                
        print '-'*80
        eff, efferr = calc(graph.GetName(), num, den)

    if type == 'rate':
#        sf = Double(2544*11200/1.8)
        eff = rootfile.Get(fitname + '_fit').Eval(options.lumi)
        efferr = 0
        
    graph.SetPoint(ipt, pt, eff)
    graph.SetPointError(ipt, 0, efferr)

ensureDir('plots/')
#file2read = 'root/genstudy_l1_bugfix.root' # 'root/genstudy_l1.root'
file2read = 'root/genstudy_l1_signal_2574files_607052events.root'


if options.type == 'rate':
    #file2read = 'root/rate_322079_L1p8.root'
    file2read = 'root/ratedict.root'

sfile = TFile(file2read)

#tree = sfile.Get('tree')

hists = []
titles = []
ptrange = np.arange(3, 11, 1).tolist()

# singleMu triggers 
graph_singleMu = createGraph('singleMu')
for ipt, pt in enumerate(ptrange):
    sel = 'singleMu' + str(pt) + '_eta1p5==1'
    fillGraph(sfile, options.type, 'singleMu' + str(pt), sel, gencut, graph_singleMu, ipt, pt)


# MuEG triggers 
graphs_MuE = []
for ipt_mu, pt_mu in enumerate([4]):
    graph_MuE = createGraph('Mu' + str(pt_mu))
    for ipt_e, pt_e in enumerate(ptrange):
        sel = 'singleMu' + str(pt_mu) + '_eta1p5==1 && (e1_eta1p0_pt >= ' + str(pt_e) + ' || e2_eta1p0_pt >= ' + str(pt_e) + ') '

        fillGraph(sfile, options.type, 'mu' + str(pt_mu) +'_eg' + str(pt_e), sel, gencut, graph_MuE, ipt_e, pt_e)
    graphs_MuE.append(graph_MuE)

# DoubleEG triggers 
graph_DoubleE_dR = createGraph('DoubleE_dR')
for ipt_e, pt_e in enumerate(ptrange):
    sel = 'e1_eta1p0_pt >= ' + str(pt_e) + ' && e2_eta1p0_pt >=' + str(pt_e) + ' && e1e2_eta1p0_dr <= 1'
    fillGraph(sfile, options.type, 'DoubleE' + str(pt_e), sel, gencut, graph_DoubleE_dR, ipt_e, pt_e)

graph_DoubleE_dR_dyn = createGraph('DoubleE_dR_dyn')
for ipt_e, pt_e in enumerate(ptrange):
    sel = 'e1_eta1p0_pt >= ' + str(pt_e) + ' && e2_eta1p0_pt >=' + str(pt_e) + ' && e1e2_eta1p0_dr <= ' + str(drdict[pt_e])
    print sel
    fillGraph(sfile, options.type, 'dyn_DoubleE' + str(pt_e), sel, gencut, graph_DoubleE_dR_dyn, ipt_e, pt_e)

graphs_MuEE = []
for ipt_mu, pt_mu in enumerate([4]):
    graph_MuEE = createGraph('MuEE_mu' + str(pt_mu))
    for ipt_e, pt_e in enumerate(ptrange):
        sel = 'singleMu' + str(pt_mu) + '_eta2p4==1 && e1_eta2p4_pt >= ' + str(pt_e) + ' && e2_eta2p4_pt >= ' + str(pt_e)
        fillGraph(sfile, options.type, 'mu' + str(pt_mu) +'_eta2p4_DoubleE_eta2p4_' + str(pt_e), sel, gencut, graph_MuEE, ipt_e, pt_e)
    graphs_MuEE.append(graph_MuEE)

## MuEE triggers 
#graphs_MuEE = []
#for ipt_mu, pt_mu in enumerate([4]): # ptrange
#    graph_MuEE = createGraph('MuEE' + str(pt_mu))
#    for ipt_e, pt_e in enumerate(ptrange):
#        sel = 'singleMu' + str(pt_mu) + '==1 && doubleE' + str(pt_e) + '==1'
#        if options.type=='rate':
#            sel = 'mu1_pt >= ' + str(pt_mu) + '&& doubleE' + str(pt_e) + '==1'
#        fillGraph(tree, options.type, sel, gencut, graph_MuEE, ipt_e, pt_e)
#    graphs_MuEE.append(graph_MuEE)

graphs_asymEE = []
for ipt1, pt_e1 in enumerate([7,8,9,10]):
    graph_asymEE = createGraph('asym_E' + str(pt_e1))
    for ipt2, pt_e2 in enumerate([3,4,5,6,7,8,9,10]):
        if pt_e2 >= pt_e1: continue
        sel = '((e1_eta1p0_pt >= ' + str(pt_e1) + ' && e2_eta1p0_pt >=' + str(pt_e2) + ') || (e1_eta1p0_pt >=' + str(pt_e2) + ' && e2_eta1p0_pt >=' + str(pt_e1) + ')) && e1e2_eta1p0_dr >=0 && e1e2_eta1p0_dr <= 1'
        fillGraph(sfile, options.type, 'E' + str(pt_e1) +'_eta1p0_E' + str(pt_e2) + '_eta1p0', sel, gencut, graph_asymEE, ipt2, pt_e2)
    graphs_asymEE.append(graph_asymEE)

#for ipt_e, pt_e in enumerate(ptrange):
#    sel = 'doubleE' + str(pt_e) + '==1'
#    sel = 'e1_ex_pt >= ' + str(pt_e) + ' && e2_ex_pt >=' + str(pt_e) + ' && e1e2_ex_dr >=0 && e1e2_ex_dr <= 1 && '
#    fillGraph(sfile, options.type, 'DoubleE' + str(pt_e), sel, gencut, graph_DoubleE_dR, ipt_e, pt_e)

if options.type=='rate':
    
    out = TFile('plot_' + options.type + '_L' + str(options.lumi).replace('.', 'p') + '.root', 'recreate')
else:
    out = TFile('plot_' + options.type + '.root', 'recreate')

graph_singleMu.Write()
graph_DoubleE_dR.Write()
graph_DoubleE_dR_dyn.Write()

for graph in graphs_MuE:
    graph.Write()

for graph in graphs_MuEE:
    graph.Write()

for graph in graphs_asymEE:
    graph.Write()
    
#############

def createPdf(his,canvas):
    canvas.cd()
    his.Draw("TEXT COLZ")
    his.SetStats(0)
    his.GetXaxis().SetTitle("gen_e2_pt")
    his.GetYaxis().SetTitle("gen_e1_pt")
    gStyle.SetPaintTextFormat(".0f");
    his.SetMinimum(0.1)
    his.SetMarkerSize(1.)
    canvas.SetLogz()
    return canvas

def plotGenPtDistrAfterTrigger(tree) :

    nbins = 13
    #
    mu_histo = TH2F("mu_histo","mu_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = "singleMu9==1"
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>mu_histo",sel,"goff")
    mu_canvas = TCanvas()
    mu_canvas = createPdf(mu_histo,mu_canvas)
    mu_canvas.SaveAs("plots/ele_pt1_pt2_mu9.pdf")
    #
    me_histo = TH2F("me_histo","me_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = 'singleMu4==1 && (e1_pt >= 8. || e2_pt >= 8.)'
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>me_histo",sel,"goff")
    me_canvas = TCanvas()
    me_canvas = createPdf(me_histo,me_canvas)
    me_canvas.SaveAs("plots/ele_pt1_pt2_m4e8.pdf")
    #
    ee_histo = TH2F("ee_histo","ee_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = 'doubleE8==1'
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>ee_histo",sel,"goff")
    ee_canvas = TCanvas()
    ee_canvas = createPdf(ee_histo,ee_canvas)
    ee_canvas.SaveAs("plots/ele_pt1_pt2_ee8.pdf")
    
    #
    mu_histo1 = TH2F("mu_histo1","mu_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = "singleMu6==1"
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>mu_histo1",sel,"goff")
    mu_canvas1 = TCanvas()
    mu_canvas1 = createPdf(mu_histo1,mu_canvas1)
    mu_canvas1.SaveAs("plots/ele_pt1_pt2_mu6.pdf")
    #
    me_histo1 = TH2F("me_histo1","me_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = 'singleMu4==1 && (e1_pt >= 4. || e2_pt >= 4.)'
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>me_histo1",sel,"goff")
    me_canvas1 = TCanvas()
    me_canvas1 = createPdf(me_histo1,me_canvas1)
    me_canvas1.SaveAs("plots/ele_pt1_pt2_m4e4.pdf")
    #
    ee_histo1 = TH2F("ee_histo1","ee_histo",nbins,0.,nbins*1.,nbins,0.,nbins*1.) 
    sel = 'doubleE6==1'
    entry = tree.Draw("gen_e1_pt:gen_e2_pt>>ee_histo1",sel,"goff")
    ee_canvas1 = TCanvas()
    ee_canvas1 = createPdf(ee_histo1,ee_canvas1)
    ee_canvas1.SaveAs("plots/ele_pt1_pt2_ee6.pdf")

if options.type != 'rate' and options.plot : plotGenPtDistrAfterTrigger(tree)
    
out.Write()
out.Close()
