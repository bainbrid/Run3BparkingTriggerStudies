from ROOT import TFile, TH2F, TCanvas, gStyle, gROOT, kTRUE, TLatex
#import copy, math
gROOT.SetBatch(kTRUE)

################################################################################
# 
def addOverflows(histo):
    if histo.GetSumw2N() == 0 : histo.Sumw2(kTRUE)
    xbins = histo.GetXaxis().GetNbins()
    ybins = histo.GetYaxis().GetNbins()
    entries = histo.GetEntries()
    for xbin in range(1,xbins+1):
        # x lower
        #content = histo.GetBinContent(xbin,1)
        #outlier = histo.GetBinContent(xbin,0)
        #histo.SetBinContent(xbin,1,content+outlier)
        #histo.SetBinContent(xbin,0,0.)
        # x higher
        content = histo.GetBinContent(xbin,ybins)
        outlier = histo.GetBinContent(xbin,ybins+1)
        histo.SetBinContent(xbin,ybins,content+outlier)
        histo.SetBinContent(xbin,ybins+1,0.)
    for ybin in range(1,ybins+1):
        # y lower
        #content = histo.GetBinContent(1,ybin)
        #outlier = histo.GetBinContent(0,ybin)
        #histo.SetBinContent(1,ybin,content+outlier)
        #histo.SetBinContent(0,ybin,0.)
        # y upper
        content = histo.GetBinContent(xbins,ybin)
        outlier = histo.GetBinContent(xbins+1,ybin)
        histo.SetBinContent(xbins,ybin,content+outlier)
        histo.SetBinContent(xbins+1,ybin,0.)
    # x upper / y upper
    content = histo.GetBinContent(xbin,ybins)
    outlier = histo.GetBinContent(xbins+1,ybins+1)
    histo.SetBinContent(xbins,ybins,content+outlier)
    histo.SetBinContent(xbins+1,ybins+1,0.)
    # 
    histo.SetEntries(entries)
    return histo

################################################################################
# 
def getHisto(input,name,title):
    file = TFile(input)
    #print("find?",file.FindObject(name))
    #if file.FindObject(name)==False : print("cannot find {:s}".format(name)); return None    
    histo = file.Get(name)
    histo = addOverflows(histo)
    histo.SetName(title)
    histo.SetTitle(title)
    histo.SetDirectory(0)
    return histo

################################################################################
# use "gt" (greater than) or "lt" (less than) or "int" (integrate) for xcumu and ycumu
# diag refers to whether to require ybin>xbin or not
def cumuHisto(histo,xcumu=None,ycumu=None,diag=False):
    #print("cumuHisto:",histo,xcumu,ycumu,diag)
    if xcumu == None and ycumu == None : return histo
    cumu = histo.Clone(histo.GetName()+"_cumu")
    cumu.SetTitle(histo.GetName()+"_cumu")
    xbins = cumu.GetNbinsX()+2 # 0=underflow, n+1=overflow
    ybins = cumu.GetNbinsY()+2 # 0=underflow, n+1=overflow
    for xbin in range(xbins):
        for ybin in range(ybins):
            if diag and xbin>ybin : continue
            if xcumu is None: 
                if ycumu is "gt" : cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbin,ybin,ybins))
                elif ycumu is "lt": cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbin,0,ybin-1))
                elif ycumu is "int": cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbin,0,ybins)) # integrate over y
                else: print("unknown parameter values",xcumu,ycumu)
            elif ycumu is None:
                if xcumu is "gt" : cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbins,ybin,ybin))
                elif xcumu is "lt": cumu.SetBinContent(xbin,ybin,histo.Integral(0,xbin-1,ybin,ybin))
                elif xcumu is "int": cumu.SetBinContent(xbin,ybin,histo.Integral(0,xbins,ybin,ybin)) # integrate over x
                else: print("unknown parameter values",xcumu,ycumu)
            elif xcumu is not None and ycumu is not None:
                if   xcumu is "gt" and ycumu is "gt": cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbins,ybin,ybins))
                elif xcumu is "gt" and ycumu is "lt": cumu.SetBinContent(xbin,ybin,histo.Integral(xbin,xbins,0,ybin))
                elif xcumu is "lt" and ycumu is "gt": cumu.SetBinContent(xbin,ybin,histo.Integral(0,xbin,ybin,ybins))
                elif xcumu is "lt" and ycumu is "lt": cumu.SetBinContent(xbin,ybin,histo.Integral(0,xbin,0,ybin))
                elif xcumu is "int" and ycumu is "int": cumu.SetBinContent(xbin,ybin,histo.Integral(0,xbins,0,ybins)) # over x and y
                else: print("unknown parameter values",xcumu,ycumu)
            else: print("unknown parameter values",xcumu,ycumu)
    return cumu

################################################################################
# 
def drawHisto(histo,eff=False,logy=True,zmax=None):
    canvas = TCanvas()
    canvas.cd()
    histo.Draw("TEXT COLZ")
    histo.SetStats(0)
    histo.GetXaxis().SetTitle("Sub-leading electron p_{T}^{gen} [GeV]")
    histo.GetXaxis().SetTitleOffset(1.3)
    histo.GetYaxis().SetTitle("Leading electron p_{T}^{gen} [GeV]")
    # Title
    histo.SetTitle("")
    text = TLatex()
    text.SetNDC()
    text.SetTextSize(0.04)
    text.DrawLatex(0.10,0.92,"#scale[1.2]{CMS} #it{Simulation (Internal)}")
    text.DrawLatex(0.55,0.92,"#scale[1.2]{L_{int} = 100 fb^{-1}, #sqrt{s} = 13 TeV}")
    if eff: 
        gStyle.SetPaintTextFormat("5.3f");
        histo.SetMinimum(1.e-4)
        if zmax is not None : histo.SetMaximum(zmax)
        else : histo.SetMaximum(1.)
        histo.SetMarkerSize(1.6)
    else: 
        gStyle.SetPaintTextFormat(".1f");
        histo.SetMinimum(0.1)
        if zmax is not None : histo.SetMaximum(zmax)
        histo.SetMarkerSize(1.)
        # Labels
        text.SetTextSize(0.03)
        text.DrawLatex(0.7,0.25,"Entries: {:.1f}".format(histo.GetEntries())) 
        text.DrawLatex(0.7,0.2,"Integral: {:.1f}".format(histo.Integral())) 
    if logy : canvas.SetLogz()
    return canvas

################################################################################
# 
def writeHisto(output,input,name,title,scale=None,logy=True,zmax=None,xcumu=None,ycumu=None):
    histo = getHisto(input,name,title)
    if scale != None : histo.Scale(scale)
    canvas = drawHisto(histo,False,logy,zmax)
    canvas.SaveAs("latest/{:s}.pdf".format(title)) 
    output.cd()
    histo.Write()
    if xcumu != None or ycumu != None :
        cumu = cumuHisto(histo,xcumu=xcumu,ycumu=ycumu)
        canvas = drawHisto(cumu,False,logy,zmax)
        canvas.SaveAs("latest/{:s}_cumu.pdf".format(title)) 
        output.cd()
        cumu.Write()
        return cumu
    return histo

################################################################################
# 
def writeEff(output,numer,denom,title,zmax=None,cumu=False):
    if cumu :
        numer = cumuHisto(numer,xcumu="gt",ycumu="gt",diag=True)
        denom = cumuHisto(denom,xcumu="gt",ycumu="gt",diag=True)
    print("title:",title)
    print("numer entries:",numer.GetBinContent(numer.GetXaxis().GetNbins(),
                                               numer.GetYaxis().GetNbins()),
          numer.GetName(),numer.GetTitle())
    print("denom entries:",denom.GetBinContent(denom.GetXaxis().GetNbins(),
                                               denom.GetYaxis().GetNbins()),
          denom.GetName(),denom.GetTitle())
    eff = numer.Clone(title)
    eff.SetDirectory(0)
    eff.SetTitle(title)
    eff.Divide(numer,denom)
    print("eff val      :",eff.GetBinContent(eff.GetXaxis().GetNbins(),
                                             eff.GetYaxis().GetNbins()))
    suffix = "_cumu" if cumu else ""
    canvas = drawHisto(eff,True,False,zmax)
    canvas.SaveAs("latest/{:s}{:s}.pdf".format(title,suffix)) 
    canvas = drawHisto(eff,True,True,zmax)
    canvas.SaveAs("latest/{:s}{:s}_log.pdf".format(title,suffix)) 
    output.cd()
    eff.Write()
    return eff

################################################################################
# 
def writeEffCumu(output,numer,denom,title,zmax=None):
    writeEff(output,numer,denom,title,zmax,True)
    return writeEff(output,numer,denom,title,zmax,False) # return NON-cumu plot!

################################################################################
# 
def transformDenom(output,numer,denom,title):
    #cumu = cumuHisto(denom,xcumu=None,ycumu="int") # Diff in pT
    cumu = cumuHisto(denom,xcumu="gt",ycumu="gt") # Cumu in pT
    #cumu = cumuHisto(denom,xcumu="int",ycumu="int") # Cumu in pT
    denom = numer.Clone(title)
    denom.SetDirectory(0)
    denom.SetTitle(title)
    xbins = numer.GetNbinsX()+2
    ybins = numer.GetNbinsY()+2
    for xbin in range(xbins):
        for ybin in range(ybins):
            #denom.SetBinContent(xbin,ybin,cumu.GetBinContent(xbin,1)) # Diff in pT
            denom.SetBinContent(xbin,ybin,cumu.GetBinContent(xbin,xbin)) # Cumu in pT
    canvas = drawHisto(denom)
    canvas.SaveAs("latest/{:s}.pdf".format(title))
    output.cd()
    denom.Write()
    return denom
