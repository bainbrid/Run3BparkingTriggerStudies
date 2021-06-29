import copy, math, os
from numpy import array
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TLegend, TGraph, Double
from DisplayManager import DisplayManager, add_Preliminary, add_CMS, add_label, applyLegendSettings
from officialStyle import officialStyle
from array import array

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

from optparse import OptionParser, OptionValueError
usage = "usage: python runTauDisplay_BsTauTau.py"
parser = OptionParser(usage)
parser.add_option("-t", "--type", default='ult', type="string", help="type [rate, eff, anal, ult]", dest="type")
parser.add_option('-w', '--weight', action="store_true", default=True, dest='weight')
parser.add_option("-l", "--lumi", default=1.0, type="float", help="target lumi. with [E34]", dest="lumi")
(options, args) = parser.parse_args()

def draw(name, xtitle, ytitle, graphs, y_min, y_max, option='rt'):

    can = TCanvas('can_' + name, 'can_' + name)
    can.SetLogy()
    can.SetGridx()
    can.SetGridy()
    
    if option=='rt':
        leg = TLegend(0.55, 0.6,0.9,0.88)
    else:
        leg = TLegend(0.2, 0.16,0.6,0.45)

    applyLegendSettings(leg)

    frame = TH2F('frame_' + name, 'frame_' + name, 7, 2,10,100,y_min,y_max)
    frame.GetXaxis().SetTitle(xtitle)
    frame.GetYaxis().SetTitle(ytitle)
    frame.Draw()

    for graph in graphs:
        graph.Draw('plsame')
        leg.AddEntry(graph, graph.GetName(), 'lep')

    leg.Draw()
    can.SaveAs('plots/' + name + '_' + str(options.lumi).replace('.','p') + '.pdf')
    can.SaveAs('plots/' + name + '_' + str(options.lumi).replace(',','p') + '.gif')

def returnGraph(name, eff, rate):
    graph = TGraph()
    graph.SetName(name)
    graph.SetTitle(name)

    idx = 0

    for i in range(eff.GetN()):

#        if i%2==1: continue

        
        x_eff = Double(1)
        y_eff = Double(1)
        
        eff.GetPoint(i, x_eff, y_eff)

        eff_ = y_eff

        x_rate = Double(1)
        y_rate = Double(1)

        rate.GetPoint(i, x_rate, y_rate)

        rate_ = y_rate

#        print i, 
#        print i, rate_singleMu.GetPointY()


        print name, 'point', i, ', (eff, rate) =', eff_, rate_

        graph.SetPoint(idx, eff_, rate_)

        idx+=1

    return copy.deepcopy(graph)


colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1,1]



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
#    h.SetStats(False)

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
    'l1mu_match_eff':{'tree':'tree', 'xvar':'gen_mupt', 'yvar':'l1mu_dr >0 && l1mu_dr < 0.4', 'xnbin':20, 'xmin':0, 'xmax':10, 'ynbin':2, 'ymin':-0.5, 'ymax':1.5, 'xtitle':xtit, 'ytitle':"Matching eff.", 'sel':'1'},

#    'l1mu_dr':{'tree':'tree', 'xvar':'l1mu_dr', 'yvar':'l1mu_dr', 'xnbin':25, 'xmin':0, 'xmax':10, 'ynbin':30, 'ymin':0., 'ymax':0.4, 'xtitle':xtit, 'ytitle':"#DeltaR(l1e, gen)", 'sel':'l1mu_dr > 0 && l1mu_dr<0.4'},
   }

vardict = {
#    'gen_ept':{'tree':'tree', 'var':'gen_ept', 'nbin':20, 'xmin':0, 'xmax':10, 'title':xtit, 'sel':'1'}, 
#    'gen_eta':{'tree':'tree', 'var':'gen_eeta', 'nbin':20, 'xmin':-3, 'xmax':3, 'title':xtit, 'sel':'1'}, 
#    'l1e_pt':{'tree':'tree', 'var':'l1e_pt', 'nbin':20, 'xmin':0, 'xmax':10, 'title':'L1 e pT (GeV)', 'sel':'l1e_dr!=-1'}, 
#    'l1e_eta':{'tree':'tree', 'var':'l1e_eta', 'nbin':20, 'xmin':-2.5, 'xmax':2.5, 'title':'L1 e eta (GeV)', 'sel':'l1e_dr!=-1'}, 
    'l1mu_dr':{'tree':'tree', 'var':'l1mu_dr', 'nbin':30, 'xmin':0, 'xmax':5, 'title':'min. #Delta R (gen, L1)', 'sel':'l1mu_dr!=-1'}, 
#    'res_ept':{'tree':'tree', 'var':'gen_ept - l1e_pt', 'nbin':20, 'xmin':-10, 'xmax':10, 'title':'#Delta p_{T} (gen, L1)', 'sel':'l1e_dr > 0 && l1e_dr < 0.4 && gen_ept > 2.5'}, 
#    'res_eeta':{'tree':'tree', 'var':'gen_eeta - l1e_eta', 'nbin':60, 'xmin':-0.2, 'xmax':0.2, 'title':'#Delta #eta (gen, L1)', 'sel':'l1e_dr > 0 && l1e_dr < 0.4 && gen_ept > 2.5'}, 
#    'res_ephi':{'tree':'tree', 'var':'gen_ephi - l1_phi', 'nbin':30, 'xmin':-1, 'xmax':1, 'title':'#Delta #phi (gen, L1)', 'sel':'l1_mindr < 0.4'}, 

#    'gen_bpt':{'tree':'pairtree', 'var':'gen_bpt', 'nbin':30, 'xmin':0, 'xmax':30, 'title':xtit_b, 'sel':'1'}, 
#    'l1e_dr':{'tree':'pairtree', 'var':'l1e_dr', 'nbin':30, 'xmin':0, 'xmax':6, 'title':'#Delta R(l1e, l1e)', 'sel':'l1e_dr !=9'}, 
    }

ensureDir('plots/')

sfile_eff = TFile('plot_' + options.type + '.root')
sfile_rate = TFile('plot_rate_L' + str(options.lumi).replace('.','p') + '.root')


print sfile_eff, sfile_rate

graphs_singleMu = []

#for ii, vkey in enumerate(['singleMu', 'singleMu_1p5']):
for ii, vkey in enumerate(['singleMu']):

    eff_singleMu = sfile_eff.Get(vkey)
    rate_singleMu = sfile_rate.Get(vkey)

    graph_singleMu = returnGraph(vkey, eff_singleMu, rate_singleMu)

#    graph_singleMu.SetName(vkey)
    graphs_singleMu.append(copy.deepcopy(graph_singleMu))


graphs_singleMuE = []

#for ii, vkey in enumerate(range(3, 10)):
for ii, vkey in enumerate([4]):


    eff_singleMuE = sfile_eff.Get('Mu' + str(vkey))
    rate_singleMuE = sfile_rate.Get('Mu' + str(vkey))

    graph_singleMuE = returnGraph('Mu' + str(vkey), eff_singleMuE, rate_singleMuE)

    applyHistStyle(graph_singleMuE, ii)

#    graph_singleMuE.SetName('muon p_{T} > ' + str(vkey) + ' GeV')
    graphs_singleMuE.append(copy.deepcopy(graph_singleMuE))

graphs_singleMuEE = []
for ii, vkey in enumerate([4]):
    eff_singleMuEE = sfile_eff.Get('MuEE' + str(vkey))
    rate_singleMuEE = sfile_rate.Get('MuEE' + str(vkey))
    graph_singleMuEE = returnGraph('MuEE' + str(vkey), eff_singleMuEE, rate_singleMuEE)
    applyHistStyle(graph_singleMuEE, ii)
    graphs_singleMuEE.append(copy.deepcopy(graph_singleMuEE))

graphs_singleMuEEa = []
for ii, vkey in enumerate([4]):
    for jj, val in enumerate([4,6,8,10]):
        name = 'Mu' + str(vkey) + 'EEa' + str(val)
        eff_singleMuEEa = sfile_eff.Get(name)
        rate_singleMuEEa = sfile_rate.Get(name)
        graph_singleMuEEa = returnGraph(name, eff_singleMuEEa, rate_singleMuEEa)
        applyHistStyle(graph_singleMuEEa, ii)
        graphs_singleMuEEa.append(copy.deepcopy(graph_singleMuEEa))

graphs_DoubleE_dR = []

#for ii, vkey in enumerate(['DoubleE_dR', 'DoubleE_dR_1p5']):
for ii, vkey in enumerate(['DoubleE_dR']):

    eff_DoubleE_dR = sfile_eff.Get(vkey)
    rate_DoubleE_dR = sfile_rate.Get(vkey)

    graph_DoubleE_dR = returnGraph(vkey, eff_DoubleE_dR, rate_DoubleE_dR)

#    graph_DoubleE_dR.SetName(vkey)
    graphs_DoubleE_dR.append(copy.deepcopy(graph_DoubleE_dR))


graphs_DoubleE_dR_dyn = []

#for ii, vkey in enumerate(['DoubleE_dR', 'DoubleE_dR_1p5']):
for ii, vkey in enumerate(['DoubleE_dR_dyn']):

    eff_DoubleE_dR_dyn = sfile_eff.Get(vkey)
    rate_DoubleE_dR_dyn = sfile_rate.Get(vkey)

    graph_DoubleE_dR_dyn = returnGraph(vkey, eff_DoubleE_dR_dyn, rate_DoubleE_dR_dyn)

#    graph_DoubleE_dR.SetName(vkey)
    graphs_DoubleE_dR_dyn.append(copy.deepcopy(graph_DoubleE_dR_dyn))



graphs_MuEE = []
for ipt_mu, pt_mu in enumerate([4]):
        
    eff_MuEE = sfile_eff.Get('MuEE_mu' + str(pt_mu))
    rate_MuEE = sfile_rate.Get('MuEE_mu' + str(pt_mu))

    graph_MuEE = returnGraph('MuEE_mu' + str(pt_mu), eff_MuEE, rate_MuEE)
    
    graphs_MuEE.append(graph_MuEE)


graphs_asymEE = []
for ipt1, pt_e1 in enumerate([7,8,9,10]):
    eff_asymEE = sfile_eff.Get('asym_E' + str(pt_e1))
    rate_asymEE = sfile_rate.Get('asym_E' + str(pt_e1))

    graph_asymEE = returnGraph('asym_E' + str(pt_e1), eff_asymEE, rate_asymEE)
    

    graphs_asymEE.append(graph_asymEE)
    

#if options.type == 'eff':
#
#    ytitle = 'Efficiency'
#
#    ymin = 0.00003
#    ymax = 0.1
#    draw(options.type + '_singleMu', 'Leading muon p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMu, ymin, ymax, 'lb')
#    draw(options.type + '_MuE', 'Leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMuE, ymin, ymax)
#    draw(options.type + '_MuE_1p0', 'Leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMuE_1p0, ymin, ymax)
#    draw(options.type + '_EE', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE, ymin, ymax, 'lb')
#    draw(options.type + '_EE', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE, ymin, ymax, 'lb')
#    draw(options.type + '_EE_dR', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE_dR, ymin, ymax, 'lb')
#
#    
#if options.type == 'rate':
#
#    ytitle = 'Rate @ 1E34'
#    
#    ymin = 1000.
#    ymax = 10000000.
#
#    draw(options.type + '_singleMu', 'Leading muon p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMu, ymin, ymax)
#    draw(options.type + '_MuE', 'Leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMuE, ymin, ymax)
#    draw(options.type + '_MuE_1p0', 'Leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_singleMuE_1p0, ymin, ymax)
#    draw(options.type + '_EE', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE, ymin, ymax, 'lb')
#    draw(options.type + '_EE', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE, ymin, ymax, 'lb')
#    draw(options.type + '_EE_dR', 'Sub-leading electron p_{T}^{gen} > X (GeV)', ytitle, graphs_EE_dR, ymin, ymax)



canvas = TCanvas()
canvas.SetLogy()
canvas.SetLogx()
canvas.SetGridx()
canvas.SetGridy()

frame_roc = None
if options.type == 'ult' and options.weight: 
    frame_roc = TH2F('frame', 'frame', 100, 0.0000005, 0.001, 1000, 1000, 30000000)
else : 
    frame_roc = TH2F('frame', 'frame', 100, 0.00003, 0.1, 1000, 1000, 30000000)

if options.type == 'eff':
    frame_roc.GetXaxis().SetTitle('L1 Trigger efficiency')
elif options.type == 'ult':
    if options.weight:
        frame_roc.GetXaxis().SetTitle('L1 Trigger efficiency x Signal Acc. x Eff.')
    else :
        frame_roc.GetXaxis().SetTitle('L1 Trigger efficiency x Signal Acc.')

frame_roc.GetYaxis().SetTitle('Rate @ ' + str(options.lumi) + 'E34' )
frame_roc.Draw()

leg = TLegend(0.2, 0.7,0.5,0.86)

applyLegendSettings(leg)
leg.SetTextSize(0.03)

#import pdb; pdb.set_trace()

ofile = TFile('test.root', 'recreate')

for graph in graphs_singleMu:
    graph.SetLineColor(1)
    graph.SetMarkerSize(1)
    graph.Write()
    graph.Draw('plsame')
    #leg.AddEntry(graph, 'Single #mu > X GeV, |#eta| < 1.5', 'lep')
    leg.AddEntry(graph, 'Mu (4,1.5)', 'lep')

for graph in graphs_singleMuE:
    graph.SetLineColor(2)
    graph.SetMarkerColor(2)
    graph.SetMarkerStyle(25)
    graph.SetMarkerSize(1)
    graph.Write()
    graph.Draw('plsame')
    #leg.AddEntry(graph, 'mu (p_{T} #geq 4 GeV, #eta < 1.5) + e (p_{T} #geq X GeV, #eta < 1.0)', 'lep')
    leg.AddEntry(graph, 'Mu (4,1.5) + E (X,1.0)', 'lep')

for graph in graphs_singleMuEE:
    graph.SetLineColor(3)
    graph.SetMarkerColor(3)
    graph.SetMarkerStyle(25)
    graph.SetMarkerSize(1)
    graph.Write()
    graph.Draw('plsame')
    leg.AddEntry(graph, 'Mu (4,1.5) + EE (X,1.0;dR<1)', 'lep')

for graph in graphs_DoubleE_dR:
    graph.SetLineColor(4)
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(24)
    graph.SetMarkerSize(1)
    graph.Write()
    graph.Draw('plsame')
    #leg.AddEntry(graph, 'Double e (p_{T} #geq X GeV, #eta < 1.0) + dR < 1', 'lep')
    leg.AddEntry(graph, 'EE (X,1.0;dR<1)', 'lep')

for graph in graphs_DoubleE_dR_dyn:
    graph.SetLineColor(6)
    graph.SetMarkerColor(6)
    graph.SetMarkerStyle(24)
    graph.SetMarkerSize(1)
    graph.Write()
    graph.Draw('plsame')
    leg.AddEntry(graph, 'Double e (p_{T} #geq X GeV, #eta < 1.0) + dR dynamic', 'lep')
    #leg.AddEntry(graph, 'EE (X,1.0;dR<0.4-1.0)', 'lep')

#for graph in graphs_MuEE:
#    graph.SetLineColor(8)
#    graph.SetMarkerColor(8)
#    graph.SetMarkerStyle(24)
#    graph.SetMarkerSize(1)
#    graph.Write()
#    graph.Draw('plsame')
#    leg.AddEntry(graph, 'mu (p_{T} #geq 4 GeV, #eta < 2.4) + Double e (p_{T} #geq X GeV, #eta < 2.4)', 'lep')
#    #leg.AddEntry(graph, 'Mu (4,2.4) + E1 (X,2.4)  + E2 (Y,2.4;Y<X)', 'lep')

###idx = 0
###
###colors = [1, 6, 8, 2]
###
###for graph in graphs_asymEE:
###    graph.SetLineColor(colors[idx])
###    graph.SetMarkerColor(colors[idx])
###    graph.SetLineStyle(2)
###    graph.SetMarkerStyle(24)
###    graph.SetMarkerSize(1)
###    graph.Write()
###    graph.Draw('plsame')
###    leg.AddEntry(graph, 'e1 (p_{T} #geq ' + graph.GetName().replace('asym_E', '') + ' GeV, #eta < 1.0) + e2 (p_{T} #geq Y GeV, #eta < 1.0), dR < 1', 'lep')
###
###    idx+=1
    
leg.Draw()
canvas.SaveAs('plots/roc_' + options.type + '_L' + str(options.lumi).replace('.','p') + '.gif')
canvas.SaveAs('plots/roc_' + options.type + '_L' + str(options.lumi).replace('.','p') + '.pdf')
ofile.Write()
ofile.Close()
