#include "TChain.h"
#include "TH2F.h"
#include <iostream>
#include <string>
#include <algorithm>

////////////////////////////////////////////////////////////////////////////////
// Binning for histograms (2D)

int nbins = 13; float width = 1.; //nbins = 3; width = 4.;
int xbins = nbins;
float xmin = 0.;
float xmax = nbins*width;

////////////////////////////////////////////////////////////////////////////////
// Return TChain
TChain* input(std::string name, int nfiles=1e6) {

  std::string path="/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_";
  std::vector<std::string> files;
  files.push_back(path+"0_10.root");
  files.push_back(path+"100_110.root");
  files.push_back(path+"10_20.root");
  files.push_back(path+"110_120.root");
  files.push_back(path+"120_130.root");
  files.push_back(path+"130_140.root");
  files.push_back(path+"140_150.root");
  files.push_back(path+"150_160.root");
  files.push_back(path+"160_170.root");
  files.push_back(path+"170_180.root");
  files.push_back(path+"180_190.root");
  files.push_back(path+"190_200.root");
  files.push_back(path+"200_210.root");
  files.push_back(path+"20_30.root");
  files.push_back(path+"210_220.root");
  files.push_back(path+"220_230.root");
  files.push_back(path+"230_240.root");
  files.push_back(path+"240_250.root");
  files.push_back(path+"250_260.root");
  files.push_back(path+"260_270.root");
  files.push_back(path+"270_280.root");
  files.push_back(path+"280_290.root");
  files.push_back(path+"290_300.root");
  files.push_back(path+"300_310.root");
  files.push_back(path+"30_40.root");
  files.push_back(path+"310_320.root");
  files.push_back(path+"320_330.root");
  files.push_back(path+"330_340.root");
  files.push_back(path+"340_350.root");
  files.push_back(path+"350_360.root");
  files.push_back(path+"360_370.root");
  files.push_back(path+"370_380.root");
  files.push_back(path+"380_390.root");
  files.push_back(path+"390_400.root");
  files.push_back(path+"400_410.root");
  files.push_back(path+"40_50.root");
  files.push_back(path+"410_420.root");
  files.push_back(path+"420_430.root");
  files.push_back(path+"430_440.root");
  files.push_back(path+"440_450.root");
  files.push_back(path+"450_460.root");
  files.push_back(path+"460_470.root");
  files.push_back(path+"470_480.root");
  files.push_back(path+"480_490.root");
  //files.push_back(path+"490_500.root"); //@@ corrupt!
  files.push_back(path+"500_510.root");
  files.push_back(path+"50_60.root");
  files.push_back(path+"510_520.root");
  files.push_back(path+"520_530.root");
  files.push_back(path+"530_540.root");
  files.push_back(path+"540_550.root");
  files.push_back(path+"550_560.root");
  files.push_back(path+"560_570.root");
  files.push_back(path+"570_580.root");
  //files.push_back(path+"580_590.root"); //@@ corrupt!
  files.push_back(path+"590_600.root");
  files.push_back(path+"600_610.root");
  files.push_back(path+"60_70.root");
  files.push_back(path+"610_620.root");
  files.push_back(path+"620_630.root");
  files.push_back(path+"630_640.root");
  files.push_back(path+"640_650.root");
  files.push_back(path+"650_660.root");
  files.push_back(path+"660_670.root");
  files.push_back(path+"670_680.root");
  files.push_back(path+"680_690.root");
  files.push_back(path+"690_700.root");
  files.push_back(path+"700_710.root");
  files.push_back(path+"70_80.root");
  files.push_back(path+"710_720.root");
  files.push_back(path+"720_730.root");
  files.push_back(path+"730_740.root");
  files.push_back(path+"740_750.root");
  files.push_back(path+"750_760.root");
  files.push_back(path+"760_770.root");
  files.push_back(path+"770_780.root");
  files.push_back(path+"780_787.root");
  files.push_back(path+"80_90.root");
  files.push_back(path+"90_100.root");

  if (name=="numer") {
    //  TFile f("root/francesca.root");
    //  TTree* t = (TTree*)f.Get("TaPtree");
    int cntr = 0;
    nfiles = std::min(int(files.size()),nfiles);
    TChain* tree = new TChain("TaPtree");
    for ( int ifile=0; ifile<nfiles; ++ifile) { 
      tree->Add(files[ifile].c_str()); 
      ++cntr; 
      std::cout << "processed " << cntr << " files..." << std::endl;
    }
    return tree;
  } else if (name=="denom") {
    //TFile f("root/genstudy_pt.root");
    //TTree* t = (TTree*)f.Get("tree");
    TChain* tree = new TChain("tree");
    tree->Add("root/genstudy_pt.root");
    return tree;
  } else {
    std::cout << "unknown input!" << std::endl;
    return 0;
  }

}

////////////////////////////////////////////////////////////////////////////////
// Histo (2D) in GEN ele max(pT1,pT2) vs GEN ele min(pT1,pT2)
TH2F* histo_pt1_vs_pt2(TChain* tree, std::string name,
		       std::string selection,
		       int xbins, float xmin, float xmax,
		       int ybins, float ymin, float ymax,
		       std::string tag="tag_ptMc",
		       std::string probe="probe_ptMc"
		       ) {
  std::string sel_lead = tag+">="+probe; if ( !selection.empty() ) sel_lead += " && "+selection;
  TH2F histo_lead(std::string(name+"_lead").c_str(),
		  std::string(name+"_lead").c_str(),
		  xbins, xmin, xmax,
		  ybins, ymin, ymax);
  int n1 = tree->Draw(std::string(tag+":"+probe+">>"+name+"_lead").c_str(),sel_lead.c_str(),"goff");
  //std::cout << "processed " << histo_lead.GetName() << ": " << n1 << std::endl;
  std::string sel_sub = tag+"<"+probe; if ( !selection.empty() ) sel_sub += " && "+selection;
  TH2F histo_sub(std::string(name+"_sub").c_str(),
		 std::string(name+"_sub").c_str(),
		 xbins, xmin, xmax,
		 ybins, ymin, ymax);
  int n2 = tree->Draw(std::string(probe+":"+tag+">>"+name+"_sub").c_str(),sel_sub.c_str(),"goff");
  //std::cout << "processed " << histo_sub.GetName() << ": " << n2 << std::endl;
  TH2F* histo = (TH2F*)histo_lead.Clone(name.c_str());
  histo->Add(&histo_sub,1.);
  histo->SetTitle(name.c_str());
  std::cout << "processed " << histo->GetName() << ": " << histo->GetEntries() << std::endl;
  return histo;
};

////////////////////////////////////////////////////////////////////////////////
// Histo (2D) of variable vs GEN ele min(pT1,pT2)
TH2F* histo_var_vs_pt2(TChain* tree, std::string name,
		       std::string var, std::string selection,
		       int xbins, float xmin, float xmax,
		       int ybins, float ymin, float ymax,
		       std::string tag="tag_ptMc",
		       std::string probe="probe_ptMc"
		       ) {
  std::string sel_tag = tag+"<"+probe; if ( !selection.empty() ) sel_tag += " && "+selection;
  TH2F histo_tag(std::string(name+"_tag").c_str(),
		 std::string(name+"_tag").c_str(),
		 xbins, xmin, xmax,
		 ybins, ymin, ymax);
  int n1 = tree->Draw(std::string(var+":"+tag+">>"+name+"_tag").c_str(),sel_tag.c_str(),"goff");
  //std::cout << "processed " << histo_tag.GetName() << ": " << n1 << std::endl;
  std::string sel_probe = tag+">="+probe; if ( !selection.empty() ) sel_probe += " && "+selection;
  TH2F histo_probe(std::string(name+"_probe").c_str(),
		   std::string(name+"_probe").c_str(),
		   xbins, xmin, xmax,
		   ybins, ymin, ymax);
  int n2 = tree->Draw(std::string(var+":"+probe+">>"+name+"_probe").c_str(),sel_probe.c_str(),"goff");
  //std::cout << "processed " << histo_probe.GetName() << ": " << n2 << std::endl;
  TH2F* histo = (TH2F*)histo_tag.Clone(name.c_str());
  histo->Add(&histo_probe,1.);
  histo->SetTitle(name.c_str());
  std::cout << "processed " << histo->GetName() << ": " << histo->GetEntries() << std::endl;
  return histo;
};

////////////////////////////////////////////////////////////////////////////////
// Histo (1D) of variable
TH1F histo_var(TChain* tree, std::string name,
	       std::string var, std::string selection,
	       int xbins, float xmin, float xmax
	       ) {
  TH1F histo(name.c_str(),name.c_str(),xbins, xmin, xmax);
  int n1 = tree->Draw(std::string(var+">>"+name).c_str(),selection.c_str(),"goff");
  std::cout << "processed " << histo.GetName() << ": " << histo.GetEntries() << std::endl;
  return histo;
};
