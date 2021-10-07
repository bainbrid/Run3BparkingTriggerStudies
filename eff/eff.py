from ROOT import TFile, TH2F, TCanvas, gStyle, gROOT, kTRUE
import copy, math
gROOT.SetBatch(kTRUE)

def addOverflows(his):
    if his.GetSumw2N() == 0 : his.Sumw2(kTRUE)
    xbins = his.GetXaxis().GetNbins()
    ybins = his.GetYaxis().GetNbins()
    entries = his.GetEntries()
    for xbin in range(1,xbins+1):
        content = his.GetBinContent(xbin,ybins)
        outlier = his.GetBinContent(xbin,ybins+1)
        his.SetBinContent(xbin,ybins,content+outlier)
        his.SetBinContent(xbin,ybins+1,0.)
    content = his.GetBinContent(xbin,ybins)
    outlier = his.GetBinContent(xbins+1,ybins+1)
    his.SetBinContent(xbins,ybins,content+outlier)
    his.SetBinContent(xbins+1,ybins+1,0.)
    his.SetEntries(entries)
    return his

def createPdf(his,canvas,eff=True,logy=True,zmax=None):
    canvas.cd()
    his.Draw("TEXT COLZ")
    his.SetStats(0)
    if eff: 
        gStyle.SetPaintTextFormat("4.2f");
        his.SetMinimum(1.e-6)
        #his.SetMaximum(1.)
        his.SetMarkerSize(1.6)
    else: 
        gStyle.SetPaintTextFormat(".0f");
        his.SetMinimum(0.1)
        if zmax is not None : his.SetMaximum(zmax)
        his.SetMarkerSize(1.)
    if logy : canvas.SetLogz()
    return canvas

# numer
print "numer"
numer_file = TFile('latest/numer.root')
numer_histo_lead = numer_file.Get('numer_gen_lead')
numer_histo_sub = numer_file.Get('numer_gen_sub')
numer_histo = numer_histo_lead.Clone("numer")
numer_histo.Add(numer_histo_sub)
numer_histo = addOverflows(numer_histo)
numer_histo.SetTitle("numer")
numer_histo2 = numer_histo.Clone("numer_unweighted")
numer_histo2.SetTitle("numer_unweighted")
# scale
files_available = 79.
files_processed = 5.#77.
numer_histo.Scale(files_available/files_processed)

# denom
print "denom"
denom_file = TFile('latest/denom.root')
denom_histo = denom_file.Get('denom_sel')
denom_histo = addOverflows(denom_histo)
denom_histo.SetTitle("denom")
denom_histo2 = denom_histo.Clone("denom_unweighted")
denom_histo2.SetTitle("denom_unweighted")
# Scale
DAS_entries = 31585558.
entries = denom_file.Get('denom_nosel').GetEntries()
denom_histo.Scale(DAS_entries/entries)

# eff
print "eff"
eff_histo = numer_histo.Clone("eff")
eff_histo.Divide(numer_histo,denom_histo)
eff_histo.SetTitle("Analysis efficiency")
#print "minimum  eff: ", eff_histo.GetMinimum(1.e-9)

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

# output
eff_file = TFile('latest/eff.root','RECREATE')
numer_histo_lead.Write()
numer_histo_sub.Write()
numer_histo.Write()
denom_histo.Write()
eff_histo.Write()

numer_canvas = TCanvas()
numer_canvas = createPdf(numer_histo,numer_canvas,eff=False,zmax=1.e5)
numer_canvas.SaveAs("latest/numer.pdf")

numer_canvas2 = TCanvas()
numer_canvas2 = createPdf(numer_histo2,numer_canvas2,eff=False,zmax=2.e3)
numer_canvas2.SaveAs("latest/numer_unweighted.pdf")

numer_canvas_lead = TCanvas()
numer_canvas_lead = createPdf(numer_histo_lead,numer_canvas_lead,eff=False)
numer_canvas_lead.SaveAs("latest/numer_lead.pdf")

numer_canvas_sub = TCanvas()
numer_canvas_sub = createPdf(numer_histo_sub,numer_canvas_sub,eff=False)
numer_canvas_sub.SaveAs("latest/numer_sub.pdf")

denom_canvas = TCanvas()
denom_canvas = createPdf(denom_histo,denom_canvas,eff=False,zmax=5.e6)
denom_canvas.SaveAs("latest/denom.pdf")

denom_canvas2 = TCanvas()
denom_canvas2 = createPdf(denom_histo2,denom_canvas2,eff=False,zmax=2.e3)
denom_canvas2.SaveAs("latest/denom_unweighted.pdf")

eff_canvas = TCanvas()
eff_canvas = createPdf(eff_histo,eff_canvas,logy=False)
eff_canvas.SaveAs("latest/eff.pdf")
eff_canvas = createPdf(eff_histo,eff_canvas,logy=True)
eff_canvas.SaveAs("latest/eff_log.pdf")

eff_file.Close()
