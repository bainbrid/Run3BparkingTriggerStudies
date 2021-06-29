import math, copy, os
import numpy as np
from ROOT import TFile, TH1F, TH2F, TTree, gROOT, gStyle, TCanvas, TColor, kLightTemperature, TLegend, TGraph, Double, TGaxis, gPad, kRed
from optparse import OptionParser, OptionValueError
#lumis = ['L1p2', 'L1p3', 'L1p4', 'L1p5', 'L1p8']
#runs = [322088, 322088, 322088, 322088, 322079]


from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptStat(0)
gStyle.SetPadBottomMargin(0.2)

graphs = []

const=Double(2544.*11200)

ptrange = np.arange(3, 11, 1).tolist()

file = TFile('/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/Trigger/job/rate.root')
tree = file.Get('tree')


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def effproducer(sel,  hname):

    print 'producing ...', hname

    hist = TH2F(hname, hname, 60,0,2, 2,-0.5,1.5)

    tree.Draw(sel + ':instL' +  '>> ' + hname)

    print hname, '->', tree.GetEntries(sel), '/', tree.GetEntries()

    hprof = hist.ProfileX()
    hprof.Scale(const)
#    hprof.GetXaxis().SetTitle('# of PU')
#    hprof.GetXaxis().SetTitleOffset(1.5)
    hprof.GetYaxis().SetTitle('Trigger Rate')
    hprof.GetYaxis().SetNdivisions(506)
    hprof.SetTitle(hname)
    hprof.SetName(hname)

    can = TCanvas('can_' + hname, 'can_' + hname)
    can.SetGridx()
    can.SetGridy()

    hprof.Draw()
    hprof.Fit("pol3")
    
    func = hprof.GetFunction("pol3")
    func.SetLineColor(kRed)
    func.SetLineStyle(2)
    func.SetLineWidth(3)
    func.Draw('same')
    func.SetTitle(hname + '_fit')
    func.SetName(hname + '_fit')

#    print 'test1', gPad.GetUxmin(), gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUymax()
#    print 'test2', Double(60)*0.0357338

#    axis = TGaxis(gPad.GetUxmin(), gPad.GetUymin(),
#                  gPad.GetUxmax(), gPad.GetUymin(), 0, Double(60)*0.0357338, 510,"+L");
#    delta = hprof.GetMaximum() - hprof.GetMinimum()
#    y = hprof.GetMinimum() - 0.15*delta

#    print delta, y
#    axis = TGaxis(0, y, 2, y, 0, Double(60)*0.0357338-0.0011904, 506, "+L");
#    axis.SetLabelFont(42)
#    axis.SetLabelSize(0.05)
#                  gPad.GetUxmax(), gPad.GetUymin(), 0, Double(60)*0.0357338, 510,"+L");
#   axis->SetLineColor(kRed);
#   axis->SetLabelColor(kRed);
#    axis.Draw();


    can.SaveAs('plots/' + hname + '.pdf')
    can.SaveAs('plots/' + hname + '.gif')

    return copy.deepcopy(hprof), copy.deepcopy(hist), copy.deepcopy(func)




ensureDir('plots/')


usage = "usage: python ratedep.py"
parser = OptionParser(usage)
parser.add_option("-n", "--name", default=None, type="string", help="name", dest="name")
parser.add_option("-s", "--sel", default=None, type="string", help="selection", dest="sel")

(options, args) = parser.parse_args()


graphs = []

if options.sel != None and options.sel!=None:

    print options.sel
    print options.name
    
    hprof, hist, func = effproducer(options.sel, options.name)
    
    graphs.append(hprof)
    graphs.append(func)


    



###for ipt, pt in enumerate(ptrange):
###
###    hname = 'singleMu' + str(pt)
###
###    sel = 'mu1_pt >= ' + str(pt) + ':npu'
###    
###    hprof, hist = effproducer(sel, hname)
###
###
###for ipt_mu, pt_mu in enumerate([4]):
###
####    graph_MuE = createGraph('Mu' + str(pt_mu))
###
###    for ipt_e, pt_e in enumerate(ptrange):
###    
###        hname = 'Mu' + str(pt_mu)  + '_eg' + str(pt_e)
###        sel = 'mu1_pt >= ' + str(pt_mu) + '&& e1_pt >=' + str(pt_e) + ':npu'
###        
###        hprof, hist = effproducer(sel, hname)
###
###
###for ipt_e, pt_e in enumerate(ptrange):
###
###    hname = 'doubleE' + str(pt_e)
###    sel = 'doubleE' + str(pt_e) + '==1:npu'
###
###    hprof, hist = effproducer(sel, hname)
    





#    graph = TGraphErrors()
#    graph.SetName('DoubleEG' + str(pt))
#    graph.SetTitle('DoubleEG' + str(pt))
#    graph.GetXaxis().SetTitle('Luminosity (E34)')
#    graph.GetYaxis().SetTitle('Estimated Rate')
#    
#    
#    idx = 0
#
#    for run, lumi in zip(runs, lumis):
#
#        file = TFile('rate_' + str(run) + '_' + lumi + '.root')
#        tree = file.Get('tree')
#        
#        den = Double(tree.GetEntries())
#        num = Double(tree.GetEntries(req))
#
#       
#        eff = num/den
#
#        print 'num,den', num, den, eff
#
#        efferr = math.sqrt(eff*(1-eff)/den)
#        
#
#
#        graph.SetPoint(idx, Double(lumi.replace('p','.').replace('L','')), eff*const)
#        
#        graph.SetPointError(idx, 0., efferr*const)
#
#        idx += 1
#
#    graphs.append(copy.deepcopy(graph))
        


output = TFile('plots/' + options.name + '.root', 'recreate')

for graph in graphs:

#    graph.SetTitle(options.name)
#    graph.SetName(options.name)

    graph.Write()

output.Write()
output.Close()


    
