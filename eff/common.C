#include "TChain.h"
#include "TFile.h"
#include "TH2F.h"
#include "TString.h"
#include <iostream>
#include <string>

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
  std::cout << "processed " << histo->GetName() << ": " << histo->GetEntries() << std::endl;
  return histo;
};

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
  std::cout << "processed " << histo_tag.GetName() << ": " << n1 << std::endl;
  std::string sel_probe = tag+">="+probe; if ( !selection.empty() ) sel_probe += " && "+selection;
  TH2F histo_probe(std::string(name+"_probe").c_str(),
		   std::string(name+"_probe").c_str(),
		   xbins, xmin, xmax,
		   ybins, ymin, ymax);
  int n2 = tree->Draw(std::string(var+":"+probe+">>"+name+"_probe").c_str(),sel_probe.c_str(),"goff");
  std::cout << "processed " << histo_probe.GetName() << ": " << n2 << std::endl;
  TH2F* histo = (TH2F*)histo_tag.Clone(name.c_str());
  histo->Add(&histo_probe,1.);
  std::cout << "processed " << histo->GetName() << ": " << histo->GetEntries() << std::endl;
  return histo;
};

TH1F histo_var(TChain* tree, std::string name,
	       std::string var, std::string selection,
	       int xbins, float xmin, float xmax
	       ) {
  TH1F histo(name.c_str(),name.c_str(),xbins, xmin, xmax);
  int n1 = tree->Draw(std::string(var+">>"+name).c_str(),selection.c_str(),"goff");
  std::cout << "processed " << histo.GetName() << ": " << histo.GetEntries() << std::endl;
  return histo;
};
