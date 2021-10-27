#include "common.C"
#include "TChain.h"
#include "TCut.h"
#include "TFile.h"
#include "TH2F.h"
#include <iostream>
#include <string>

void numer1() {

  ////////////////////////////////////////////////////////////////////////////////
  // Opening files and config

  TChain* t = input("numer",1); // process 1 file    <------------- !!!
  std::cout << "entries: " << t->GetEntries() << std::endl;
  // entries: TTree = 17050, TChain = 3137854

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts
  
  // Binning for gen pT for e1 and e2
  int nbins = 13; float width = 1.; //nbins = 3; width = 4.;
  int xbins = nbins;
  float xmin = 0.;
  float xmax = nbins*width;
  
  // GEN-match to signal
  TCut sel_sig = "bmatchMC==1";

  // Low q2 requirement
  TCut sel_lq2 = "(mll_fullfit*mll_fullfit)>1.1";
  sel_lq2 += "(mll_fullfit*mll_fullfit)<6.25";

  //@@ EXTRA: RECO eta selection
  TCut sel_eta = "abs(tag_eta)<1.2";
  sel_eta += "abs(probe_eta)<1.2";

  // Analysis pre-selection
  TCut sel_ana = "abs(k_svip3d)<0.06 && fit_Bcos2D>0.95";

  // Analysis BDT cut
  TCut sel_bdt = "analysisBdtO>8.";
  sel_bdt += sel_ana;

  // Everything
  TCut sel_all = sel_lq2&&sel_eta&&sel_ana&&sel_bdt;

  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_sig:    " << sel_sig.GetTitle() << std::endl
	    << "  sel_lq2:    " << sel_lq2.GetTitle() << std::endl
	    << "  sel_ana:    " << sel_ana.GetTitle() << std::endl
	    << "  sel_bdt:    " << sel_bdt.GetTitle() << std::endl
	    << "  everything: " << sel_all.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histograms

  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections
  TH2F* numer_pt1_vs_pt2_after_sig = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_sig",
						      sel_sig.GetTitle(),
						      xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_lq2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_lq2",
						      (sel_sig&&sel_lq2).GetTitle(),
						      xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_eta = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_eta",
						      (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
						      xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_ana = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_ana",
						      (sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle(),
						      xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_bdt = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_bdt",
						      (sel_sig&&sel_lq2&&sel_eta&&sel_ana&&sel_bdt).GetTitle(),
						      xbins,xmin,xmax,xbins,xmin,xmax);

  // Histos 2D ("N-1" BDT vs GEN e2 pT) after various selections
  TH2F* numer_bdt_vs_pt2_after_inc = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_inc","analysisBdtO",
						      sel_sig.GetTitle(),
						      xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_lq2 = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_lq2","analysisBdtO",
						      (sel_sig&&sel_lq2).GetTitle(),
						      xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_eta = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_eta","analysisBdtO",
						      (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
						      xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_ana = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_ana","analysisBdtO",
						      (sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle(),
						      xbins,xmin,xmax,21,-5.,16.);

  // Histos 1D ("N-1" BDT) after various selections
  TH1F numer_bdt_after_inc = histo_var(t,"numer_bdt_after_inc","analysisBdtO",
				       sel_sig.GetTitle(),
				       21,-5.,16.);
  TH1F numer_bdt_after_lq2 = histo_var(t,"numer_bdt_after_lq2","analysisBdtO",
				       (sel_sig&&sel_lq2).GetTitle(),
				       21,-5.,16.);
  TH1F numer_bdt_after_eta = histo_var(t,"numer_bdt_after_eta","analysisBdtO",
				       (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
				       21,-5.,16.);
  TH1F numer_bdt_after_ana = histo_var(t,"numer_bdt_after_ana","analysisBdtO",
				       (sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle(),
				       21,-5.,16.);
  TH1F numer_bdt_after_pt2 = histo_var(t,"numer_bdt_after_pt2","analysisBdtO",
				       std::string((sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle())+" && probe_ptMc>10.",
				       21,-5.,16.);

  ////////////////////////////////////////////////////////////////////////////////
  // Output

  // Write to file
  TFile fw("latest/numer.root","RECREATE");
  //
  numer_pt1_vs_pt2_after_sig->Write();
  numer_pt1_vs_pt2_after_lq2->Write();
  numer_pt1_vs_pt2_after_eta->Write();
  numer_pt1_vs_pt2_after_ana->Write();
  numer_pt1_vs_pt2_after_bdt->Write();
  //
  numer_bdt_vs_pt2_after_inc->Write();
  numer_bdt_vs_pt2_after_lq2->Write();
  numer_bdt_vs_pt2_after_eta->Write();
  numer_bdt_vs_pt2_after_ana->Write();
  //
  numer_bdt_after_inc.Write();
  numer_bdt_after_lq2.Write();
  numer_bdt_after_eta.Write();
  numer_bdt_after_ana.Write();
  numer_bdt_after_pt2.Write();
  //
  fw.Close();
  std::cout << "done!" << std::endl;
}
