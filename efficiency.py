import copy, math, os
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TGraphErrors, Double
from DisplayManager import DisplayManager, add_Preliminary, add_CMS, add_label
from officialStyle import officialStyle
from array import array
import numpy as np

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)



colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]



def calc(num, den):
    eff = num/den

    efferr = 0.


    if num!=0:
        efferr = math.sqrt(eff*(1-eff)/num)

#    print num, den, eff, efferr

    return eff, efferr



def set_palette(name="palette", ncontours=999):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.20, 0.2, 0.2, 0.2, 0.2]
#        red   = [0.1, 0.2, 0.3, 0.4, 0.5]
        green = [0.1, 0.1, 0.1, 0.1, 0.1]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]
#        blue  = [0.1, 0.2, 0.3, 0.4, 0.5]

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    gStyle.SetNumberContours(ncontours)



def applyHistStyle(h, i):
#    print h, i
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(3)
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def comparisonPlots(hists, titles, isLog=False, pname='sync.pdf', isEff = False, isRatio=False, isLegend=False, x=None, y=None, label="test"):

    display = DisplayManager(pname, isLog, isRatio, 0.6, 0.7, x, y, label)
    display.draw_legend = isLegend
    display.isEff = isEff
    
    display.Draw(hists, titles)


def sproducer(key, rootfile, name, ivar, addsel = '1'):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + '&&' + addsel + ')'
        
    tree = rootfile.Get(ivar['tree'])

#    print ivar['var'] + ' >> ' + hist.GetName(), exp
    
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['title'])
    hist.GetYaxis().SetTitle('a.u.')
    hist.GetYaxis().SetNdivisions(506)
        
    return copy.deepcopy(hist)



def effproducer(key, rootfile, name, ivar, addsel='1'):

    hist = TH2F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['xnbin'], ivar['xmin'], ivar['xmax'],
                ivar['ynbin'], ivar['ymin'], ivar['ymax'])


    hist.Sumw2()
    exp = '(' + ivar['sel'] + '&&' + addsel + ')'
        
    tree = rootfile.Get(ivar['tree'])

#    print ivar['var'], 'effstr = ', effstr + ' >> ' + hist.GetName(), exp
    
    tree.Draw(ivar['yvar'] + ':' + ivar['xvar'] + ' >> ' + hist.GetName(), exp)
    
    hprof = hist.ProfileX()
    hprof.SetMaximum(ivar['ymax'])
#    hprof.SetMaximum(1.2)
    hprof.SetMinimum(ivar['ymin'])
    hprof.GetXaxis().SetTitle(ivar['xtitle'])
    hprof.GetYaxis().SetTitle(ivar['ytitle'])
    hprof.GetYaxis().SetNdivisions(506)

    if name.find('eff')!=-1:
        hprof.SetMaximum(1.)
        hprof.SetMinimum(0)

    if name.find('res')!=-1:
#        print '!!!!!!!!!!!!!!!!!!!!!'
        hprof.SetMaximum(1.)
        hprof.SetMinimum(-1.)

    return copy.deepcopy(hprof), copy.deepcopy(hist)





xtit = "Generator-level electron p_{T} [GeV]"
xtit_b = "Generator-level B p_{T} [GeV]"

effvardict = {
#    'l1e_match_eff':{'tree':'tree', 'xvar':'gen_ept', 'yvar':'l1_mindr < 0.4', 'xnbin':25, 'xmin':0, 'xmax':25, 'ynbin':2, 'ymin':-0.5, 'ymax':1.5, 'xtitle':xtit, 'ytitle':"Matching eff.", 'sel':'1'},

#    'l1e_dr':{'tree':'pairtree', 'xvar':'gen_bpt', 'yvar':'l1e_dr', 'xnbin':25, 'xmin':0, 'xmax':50, 'ynbin':30, 'ymin':0., 'ymax':5, 'xtitle':xtit_b, 'ytitle':"#DeltaR(l1e, l1e)", 'sel':'l1e_dr!=9'},
#    'mu':{'tree':'tree', 'xvar':None, 'yvar':'l1e_dr', 'xnbin':25, 'xmin':0, 'xmax':50, 'ynbin':30, 'ymin':0., 'ymax':5, 'xtitle':xtit_b, 'ytitle':"#DeltaR(l1e, l1e)", 'sel':'l1e_dr!=9'},
   }

#vardict = {
#    'gen_ept':{'tree':'tree', 'var':'gen_ept', 'nbin':30, 'xmin':0, 'xmax':20, 'title':xtit, 'sel':'1'}, 
#    'l1_mindr':{'tree':'tree', 'var':'l1_mindr', 'nbin':30, 'xmin':0, 'xmax':10, 'title':'min. #Delta R (gen, L1)', 'sel':'1'}, 
#    'res_ept':{'tree':'tree', 'var':'gen_ept - l1_pt', 'nbin':30, 'xmin':-10, 'xmax':10, 'title':'#Delta p_{T} (gen, L1)', 'sel':'l1_mindr < 0.4'}, 
#    'res_eeta':{'tree':'tree', 'var':'gen_eeta - l1_eta', 'nbin':30, 'xmin':-0.2, 'xmax':0.2, 'title':'#Delta #eta (gen, L1)', 'sel':'l1_mindr < 0.4'}, 
#    'res_ephi':{'tree':'tree', 'var':'gen_ephi - l1_phi', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'#Delta #phi (gen, L1)', 'sel':'l1_mindr < 0.4'}, 
#
#    'gen_bpt':{'tree':'pairtree', 'var':'gen_bpt', 'nbin':30, 'xmin':0, 'xmax':30, 'title':xtit_b, 'sel':'1'}, 
#    'l1e_dr':{'tree':'pairtree', 'var':'l1e_dr', 'nbin':30, 'xmin':0, 'xmax':6, 'title':'#Delta R(l1e, l1e)', 'sel':'l1e_dr !=9'}, 
#    }

ensureDir('plots/')
sfile = TFile('genstudy_signal_1285files_303513events.root')
tree = sfile.Get('tree')

#for vkey, ivar in vardict.iteritems():
#
#    hists = []
#    titles = []
#
#    addsel = '1'
#
#    hist = sproducer('hist', sfile, vkey, ivar, addsel)
#    
#    hists.append(copy.deepcopy(hist))
#    titles.append('Kee inclusive Sig.')
#
#    for ii, ihist in enumerate(hists):
#        applyHistStyle(ihist, ii)
#
#        ihist.Scale(1./ihist.GetSumOfWeights())
#        ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
#
#    comparisonPlots(hists, titles, False, 'plots/dist_' + vkey + '.pdf', False, False, False)


#for vkey, ivar in effvardict.iteritems():

# efficiecny to find muon with pT > X GeV

hists = []
titles = []

ptrange = np.arange(0, 12.1, 0.2).tolist()

graph_singleMu = TGraphErrors()            
graph_singleMu.SetName('singleMuon')
graph_singleMu.SetTitle('singleMuon')

den = Double(tree.GetEntries())

for ipt, pt in enumerate(ptrange):
    
    num = Double(tree.GetEntries('mu1_pt > ' + str(pt)))

#    print num, den


    eff, efferr = calc(num, den)
    
    print 'singleMu (ipt, pt) = ', ipt, pt, ', (num, den, eff, efferr) = ', num, den, eff, efferr

#    eff = num/den

#    efferr = 0.

#    if num!=0:
#        efferr = math.sqrt(eff*(1-eff)/num)
    
    graph_singleMu.SetPoint(ipt, pt, eff)
    graph_singleMu.SetPointError(ipt, 0, efferr)


graphs_MuE = []

for ipt_mu, pt_mu in enumerate([3,4,5,6,7,8,9]):

    graph_MuE = TGraphErrors()
    graph_MuE.SetTitle('Mu' + str(pt_mu))
    graph_MuE.SetName('Mu' + str(pt_mu))


    for ipt_e, pt_e in enumerate([3,4,5,6,7,8,9]):
        
        num = Double(tree.GetEntries('mu1_pt > ' + str(pt_mu) + ' && e1_pt > ' + str(pt_e)))

        eff, efferr = calc(num, den)
    
        graph_MuE.SetPoint(ipt_e, pt_e, eff)
        graph_MuE.SetPointError(ipt_e, 0, efferr)


        print 'MuE (ipt_mu, pt_mu, ipt_e, pt_e) = ', ipt_mu, pt_mu, ipt_e, pt_e, ', (num, den, eff, efferr) = ', num, den, eff, efferr
        
    graphs_MuE.append(graph_MuE)



graphs_EE = []

for ipt_e1, pt_e1 in enumerate([3,4,5,6,7,8,9]):

    graph_EE = TGraphErrors()
    graph_EE.SetTitle('E' + str(pt_e1))
    graph_EE.SetName('E' + str(pt_e1))


    for ipt_e2, pt_e2 in enumerate([3,4,5,6,7,8,9]):
        
        if ipt_e2 > ipt_e1: continue

        num = Double(tree.GetEntries('e1_pt > ' + str(pt_e1) + ' && e2_pt > ' + str(pt_e2) ) )

        eff, efferr = calc(num, den)
    
        graph_EE.SetPoint(ipt_e2, pt_e2, eff)
        graph_EE.SetPointError(ipt_e2, 0, efferr)

        print 'EE (ipt_e1, pt_e1, ipt_e2, pt_e2) = ', ipt_e1, pt_e1, ipt_e2, pt_e2, ', (num, den, eff, efferr) = ', num, den, eff, efferr
        
    graphs_EE.append(graph_EE)




out = TFile('plot.root', 'recreate')

graph_singleMu.Write()

for graph in graphs_MuE:
    graph.Write()

for graph in graphs_EE:
    graph.Write()

out.Write()
out.Close()



#hist, hs = effproducer('hist', sfile, vkey, ivar, addsel)
#hists.append(copy.deepcopy(hist))
#titles.append('Kee inclusive Sig.')

#comparisonPlots(hists, titles, False, 'plots/eff_' + vkey + '.pdf', True, False, False)






