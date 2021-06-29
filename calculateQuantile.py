import copy, math, os
from numpy import array
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TLegend, TGraph, Double, TArrow, kBlue
from DisplayManager import DisplayManager, add_Preliminary, add_CMS, add_label, applyLegendSettings
from officialStyle import officialStyle
from array import array
import numpy as np

ptrange = np.arange(3, 15, 1).tolist()

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)


file = TFile('root/genstudy_l1_signal_2574files_607052events.root')
tree = file.Get('tree')

for ipt, pt in enumerate(ptrange):

    hname = 'hist_' + str(pt)
    hist = TH1F(hname, hname, 50,0,1.5)
    
    sel = 'e1_eta1p0_pt >= ' + str(pt) + ' && e2_eta1p0_pt >=' + str(pt)

    tree.Draw('e1e2_eta1p0_dr >> ' + hname, sel)
    
    
    can = TCanvas('can_' + str(pt), 'can_' + str(pt))
    
    hist.Draw()
    hist.GetXaxis().SetTitle('#DeltaR(e1, e2)')
    hist.GetYaxis().SetTitle('a.u')

    leg = TLegend(0.5, 0.65,0.9,0.88)
    applyLegendSettings(leg)
    leg.SetTextSize(0.03)

    leg.AddEntry(hist, 'Double E (p_{T} >= ' + str(pt) + ' GeV)', '')

    for ibin in range(1, hist.GetXaxis().GetNbins()+1):
        
        frac = Double(hist.Integral(0, ibin))/Double(hist.GetSumOfWeights())

#        print '\t', ibin, hist.GetBinContent(ibin), frac, hist.Integral(), hist.Integral(0, ibin), hist.GetSumOfWeights()
        
        if frac > 0.95:

            leg.AddEntry(hist, '95% quntile at ' + str(hist.GetXaxis().GetBinLowEdge(ibin)), 'lep')
            arrow = TArrow(hist.GetXaxis().GetBinLowEdge(ibin), hist.GetMinimum(), hist.GetXaxis().GetBinLowEdge(ibin), hist.GetMaximum()*0.6, 0.05, '<')
            arrow.SetLineColor(kBlue)
            arrow.Draw()
            break

        

    leg.Draw()
        
    
    can.SaveAs('plots/dr_' + str(pt) + '.gif')



