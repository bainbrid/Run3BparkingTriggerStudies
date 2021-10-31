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

  TChain* t = input("numer");
  std::cout << "entries: " << t->GetEntries() << std::endl;
  // entries: TTree = 17050, TChain = 3137854

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts

  // GEN-match to signal
  TCut sel_sig = "bmatchMC==1";
  
  // GEN acceptance
  TCut sel_acc_gen_pt  = "tag_ptMc>0.5 && probe_ptMc>0.5";
  //TCut sel_acc_gen_eta = "abs(tag_etaMc)<2.5 && abs(probe_etaMc)<2.5"; //@@ missing GEN eta ...!
  TCut sel_acc_gen = sel_acc_gen_pt;// && sel_acc_gen_eta;

  // RECO acceptance
  TCut sel_acc_reco_pt  = "tag_pt>0.5 && probe_pt>0.5";
  TCut sel_acc_reco_eta = "abs(tag_eta)<2.5 && abs(probe_eta)<2.5";
  TCut sel_acc_reco = sel_acc_reco_pt && sel_acc_reco_eta;

  // Low q2 requirement
  TCut sel_lq2 = "(mll_fullfit*mll_fullfit)>1.1";
  sel_lq2 += "(mll_fullfit*mll_fullfit)<6.25";

  // Analysis pre-selection
  TCut sel_ana = "abs(k_svip3d)<0.06 && fit_Bcos2D>0.95";

  // Analysis BDT cut
  TCut sel_bdt = "analysisBdtO>8.";

  // "Bin" in electron (RECO) eta
  TCut sel_cen = "abs(tag_eta)<1.2 && abs(probe_eta)<1.2";
  TCut sel_fwd = !sel_cen;

  // Restrict all (RECO) eta reqs to within |eta| < 2.5
  sel_cen += sel_acc_reco_eta;
  sel_fwd += sel_acc_reco_eta;

  // Sanity check
  TCut sel_sum = sel_cen || sel_fwd;

  // Everything
  TCut sel_all = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt && sel_sum;

  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_sig:      " << sel_sig.GetTitle() << std::endl
	    << "  sel_acc_gen:  " << sel_acc_gen.GetTitle() << std::endl
	    << "  sel_acc_reco: " << sel_acc_reco.GetTitle() << std::endl
	    << "  sel_lq2:      " << sel_lq2.GetTitle() << std::endl
	    << "  sel_ana:      " << sel_ana.GetTitle() << std::endl
	    << "  sel_bdt:      " << sel_bdt.GetTitle() << std::endl
	    << "  sel_cen:      " << sel_cen.GetTitle() << std::endl
	    << "  sel_fwd:      " << sel_fwd.GetTitle() << std::endl
	    << "  sel_sum:      " << sel_sum.GetTitle() << std::endl
	    << "  sel_all:      " << sel_all.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histograms

  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections
  TCut sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco;
//  TH2F* numer_pt1_vs_pt2_sig = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_sig",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2;
//  TH2F* numer_pt1_vs_pt2_lq2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_lq2",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana;
//  TH2F* numer_pt1_vs_pt2_ana = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_ana",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt;
//  TH2F* numer_pt1_vs_pt2_bdt = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_bdt",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
  
  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt && sel_cen;
  TH2F* numer_pt1_vs_pt2_cen = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_cen",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt && sel_fwd;
  TH2F* numer_pt1_vs_pt2_fwd = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_fwd",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt && sel_sum;
  TH2F* numer_pt1_vs_pt2_sum = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_sum",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);

//  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_bdt && sel_all;
//  TH2F* numer_pt1_vs_pt2_all = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_all",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);

//  // Histos 2D ("N-1" BDT vs GEN e2 pT) after various selections
//  TH2F* numer_bdt_vs_pt2_sig = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_sig","analysisBdtO",
//						      sel_sig.GetTitle(),
//						      xbins,xmin,xmax,21,-5.,16.);
//  TH2F* numer_bdt_vs_pt2_lq2 = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_lq2","analysisBdtO",
//						      (sel_sig&&sel_lq2).GetTitle(),
//						      xbins,xmin,xmax,21,-5.,16.);
//  TH2F* numer_bdt_vs_pt2_eta = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_eta","analysisBdtO",
//						      (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
//						      xbins,xmin,xmax,21,-5.,16.);
//  TH2F* numer_bdt_vs_pt2_ana = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_ana","analysisBdtO",
//						      (sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle(),
//						      xbins,xmin,xmax,21,-5.,16.);

  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_cen;
  TH2F* numer_bdt_vs_pt2_cen = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_cen","analysisBdtO",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);
  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_fwd;
  TH2F* numer_bdt_vs_pt2_fwd = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_fwd","analysisBdtO",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);
  sel_tmp = sel_sig && sel_acc_gen && sel_acc_reco && sel_lq2 && sel_ana && sel_sum;
  TH2F* numer_bdt_vs_pt2_sum = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_sum","analysisBdtO",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);

//  // Histos 1D ("N-1" BDT) after various selections
//  TH1F numer_bdt_sig = histo_var(t,"numer_bdt_sig","analysisBdtO",
//				       sel_sig.GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_lq2 = histo_var(t,"numer_bdt_lq2","analysisBdtO",
//				       (sel_sig&&sel_lq2).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_eta = histo_var(t,"numer_bdt_eta","analysisBdtO",
//				       (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_ana = histo_var(t,"numer_bdt_ana","analysisBdtO",
//				       (sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_pt2 = histo_var(t,"numer_bdt_pt2","analysisBdtO",
//				       std::string((sel_sig&&sel_lq2&&sel_eta&&sel_ana).GetTitle())+" && probe_ptMc>10.",
//				       21,-5.,16.);

  ////////////////////////////////////////////////////////////////////////////////
  // Output

  // Write to file
  TFile fw("latest/numer.root","RECREATE");
  //
//  numer_pt1_vs_pt2_sig->Write();
//  numer_pt1_vs_pt2_lq2->Write();
//  numer_pt1_vs_pt2_ana->Write();
//  numer_pt1_vs_pt2_bdt->Write();
  numer_pt1_vs_pt2_cen->Write();
  numer_pt1_vs_pt2_fwd->Write();
  numer_pt1_vs_pt2_sum->Write();
  //
//  numer_pt1_vs_pt2_sum->Write();
//  numer_pt1_vs_pt2_all->Write();
//  numer_pt1_vs_pt2_tst->Write();
  //
//  numer_bdt_vs_pt2_sig->Write();
//  numer_bdt_vs_pt2_lq2->Write();
//  numer_bdt_vs_pt2_eta->Write();
//  numer_bdt_vs_pt2_ana->Write();
  numer_bdt_vs_pt2_cen->Write();
  numer_bdt_vs_pt2_fwd->Write();
  numer_bdt_vs_pt2_sum->Write();
//  //
//  numer_bdt_sig.Write();
//  numer_bdt_lq2.Write();
//  numer_bdt_eta.Write();
//  numer_bdt_ana.Write();
//  numer_bdt_pt2.Write();
  //
  fw.Close();
  std::cout << "done!" << std::endl;
}
