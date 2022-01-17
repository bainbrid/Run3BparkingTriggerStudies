#include "common.C"
#include "TChain.h"
#include "TCut.h"
#include "TEfficiency.h"
#include "TFile.h"
#include "TH2F.h"
#include <iostream>
#include <string>
#include <sstream>

void fwlite() {

  ////////////////////////////////////////////////////////////////////////////////
  // Opening files and config

  std::string sample = "incl";

  std::string path="/Users/bainbrid/Desktop/Trigger/";
  std::vector<std::string> files;
  files.push_back(path+"ntuple_"+sample+".root");

  int nfiles = 1e6;
  TChain* t = input(files,nfiles);
  std::cout << "entries: " << t->GetEntries()
	    << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts

  // Inclusive requirement
  TCut sel_inc = "";
  
  // Tag-side muon in GEN acceptance
  TCut sel_tag_m1 = "m1_gen_pt>5.0 && abs(e1_gen_eta)<2.5";
  TCut sel_tag_m2 = "m2_gen_pt>5.0 && abs(m2_gen_eta)<2.5";
  TCut sel_tag = sel_tag_m1 || sel_tag_m2;
  sel_tag = ""; //@@ OVERRIDE TO REMOVE TAG-SIDE REQ FOR NOW, ONLY NEEDED TO DETERMINE GEN FILTER EFF OF 0.0051

  // Identify B->Kee decay
  TCut sel_kee = ""; //@@ Assumes decay is always found!!!

  // GEN acceptance (pT>0.5, |eta|<2.5)
  TCut sel_acc_pt  = "e1_gen_pt>0.5 && e2_gen_pt>0.5";
  TCut sel_acc_eta = "abs(e1_gen_eta)<2.5 && abs(e2_gen_eta)<2.5";
  TCut sel_acc = sel_acc_pt && sel_acc_eta;
  
  // Extra GEN requirements (pT>2.0, |eta|<2.5)
  TCut sel_gen_pt  = "e1_gen_pt>2.0 && e2_gen_pt>2.0";
  TCut sel_gen_eta = "abs(e1_gen_eta)<2.5 && abs(e2_gen_eta)<2.5";
  TCut sel_gen = sel_gen_pt && sel_gen_eta;

  // "Bin" in electron GEN eta
  TCut sel_cen = "abs(e1_gen_eta)<1.2 && abs(e2_gen_eta)<1.2";
  TCut sel_fwd = !sel_cen;
  sel_cen += sel_gen_eta; // Restrict to GEN eta acceptance
  sel_fwd += sel_gen_eta; // Restrict to GEN eta acceptance
  TCut sel_sum = sel_cen || sel_fwd; // Sanity check
  
  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_inc: " << sel_inc.GetTitle() << std::endl
	    << "  sel_tag: " << sel_tag.GetTitle() << std::endl
	    << "  sel_kee: " << sel_kee.GetTitle() << std::endl
	    << "  sel_acc: " << sel_acc.GetTitle() << std::endl
	    << "  sel_gen: " << sel_gen.GetTitle() << std::endl
	    << "  sel_cen: " << sel_cen.GetTitle() << std::endl
	    << "  sel_fwd: " << sel_fwd.GetTitle() << std::endl
	    << "  sel_sum: " << sel_sum.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections for sum,cen,fwd

  // Inclusive 
  TCut sel_tmp = sel_inc;
  Histos histo_pt1_vs_pt2_inc = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_inc",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  
  // Tag-side muon in GEN acceptance
  sel_tmp = sel_inc&&sel_tag;
  Histos histo_pt1_vs_pt2_tag = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_tag",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  // Find B->Kee decay?
  sel_tmp = sel_inc&&sel_tag&&sel_kee;
  Histos histo_pt1_vs_pt2_kee = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_kee",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  //////////
  // In GEN acc? (pT>0.5, |eta|<2.5)
  sel_tmp = sel_inc&&sel_tag&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  //////////
  // Additional GEN reqs (pT>2.0, |eta|<2.5)
  sel_tmp = sel_inc&&sel_tag&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  
  ////////////////////////////////////////////////////////////////////////////////
  // Output

  // Write to file
  std::stringstream output; 
  if (nfiles>999) { output << "latest/histos_" << sample << ".root"; }
  else { output << "latest/histos_" << nfiles << ".root"; }
  TFile fw(output.str().c_str(),"RECREATE");
  std::cout << "filename: " << output.str().c_str() << std::endl;

  histo_pt1_vs_pt2_inc.sum_->Write();
  histo_pt1_vs_pt2_inc.cen_->Write();
  histo_pt1_vs_pt2_inc.fwd_->Write();
  histo_pt1_vs_pt2_tag.sum_->Write();
  histo_pt1_vs_pt2_tag.cen_->Write();
  histo_pt1_vs_pt2_tag.fwd_->Write();
  histo_pt1_vs_pt2_kee.fwd_->Write();
  histo_pt1_vs_pt2_kee.cen_->Write();
  histo_pt1_vs_pt2_kee.sum_->Write();
  histo_pt1_vs_pt2_acc.sum_->Write();
  histo_pt1_vs_pt2_acc.cen_->Write();
  histo_pt1_vs_pt2_acc.fwd_->Write();
  histo_pt1_vs_pt2_gen.sum_->Write();
  histo_pt1_vs_pt2_gen.cen_->Write();
  histo_pt1_vs_pt2_gen.fwd_->Write();

  fw.Close();
  std::cout << "done!" << std::endl;
}
