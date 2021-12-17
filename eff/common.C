#include "TChain.h"
#include "TCut.h"
#include "TH2F.h"
#include <iostream>
#include <string>
#include <algorithm>

////////////////////////////////////////////////////////////////////////////////
// Binning for histograms (2D)

int nbins = 12; float width = 1.; //nbins = 3; width = 4.;
int xbins = nbins;
float xmin = 0.;
float xmax = nbins*width;

////////////////////////////////////////////////////////////////////////////////
// Return TChain
TChain* input(std::string name, int nfiles=1e6) {
  if (name=="numer") {
    std::string path="/Users/bainbrid/Desktop/Trigger/";
    std::vector<std::string> files;
    //files.push_back(path+"mc_BuToKee_temp.root");
    //files.push_back(path+"mc_BuToKee_2021Dec01.root");
    //files.push_back(path+"mc_BuToKee_2021Dec16_temp.root"); // 1 file
    files.push_back(path+"mc_BuToKee_2021Dec16.root");
    int cntr = 0;
    nfiles = std::min(int(files.size()),nfiles);
    TChain* tree = new TChain("tree");
    for ( int ifile=0; ifile<nfiles; ++ifile) { 
      tree->Add(files[ifile].c_str()); 
      ++cntr; 
      std::cout << "processed " << cntr << " files..." << std::endl;
    }
    return tree;
  } else if (name=="denom") {
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
		       std::string tag="e1_gen_pt",
		       std::string probe="e2_gen_pt"
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
  //std::cout << "processed " << histo_sub.GetName() << ":  " << n2 << std::endl;
  TH2F* histo = (TH2F*)histo_lead.Clone(name.c_str());
  histo->Add(&histo_sub,1.);
  histo->SetTitle(name.c_str());
  std::cout << "processed " << histo->GetName() << ": " << histo->GetEntries() << std::endl;
  return histo;
};

////////////////////////////////////////////////////////////////////////////////
// Return Histos (2D) in GEN ele max(pT1,pT2) vs GEN ele min(pT1,pT2)
struct Histos{
  TH2F* sum_=0;
  TH2F* cen_=0;
  TH2F* fwd_=0;
};
Histos histo_pt1_vs_pt2_all(TChain* tree, std::string name,
			    TCut selection,
			    TCut sel_cen,
			    TCut sel_fwd,
			    int xbins, float xmin, float xmax,
			    int ybins, float ymin, float ymax,
			    std::string tag="e1_gen_pt",
			    std::string probe="e2_gen_pt"
			    ) {
  Histos histos;
  histos.sum_ = histo_pt1_vs_pt2(tree,name,selection.GetTitle(),
				 xbins,xmin,xmax,ybins,ymin,ymax,tag,probe);
  histos.cen_ = histo_pt1_vs_pt2(tree,name+"_cen",(selection&&sel_cen).GetTitle(),
				 xbins,xmin,xmax,ybins,ymin,ymax,tag,probe);
  histos.fwd_ = histo_pt1_vs_pt2(tree,name+"_fwd",(selection&&sel_fwd).GetTitle(),
				 xbins,xmin,xmax,ybins,ymin,ymax,tag,probe);
  return histos;
}

////////////////////////////////////////////////////////////////////////////////
// Histo (2D) of variable vs GEN ele min(pT1,pT2)
TH2F* histo_var_vs_pt2(TChain* tree, std::string name,
		       std::string var, std::string selection,
		       int xbins, float xmin, float xmax,
		       int ybins, float ymin, float ymax,
		       std::string tag="e1_gen_pt",//"tag_ptMc",
		       std::string probe="e2_gen_pt"//"probe_ptMc"
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
