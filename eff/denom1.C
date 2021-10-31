#include "common.C"
#include "TChain.h"
#include "TCut.h"
#include "TFile.h"
#include "TH2F.h"
#include <iostream>
#include <string>

void denom1() { 

  ////////////////////////////////////////////////////////////////////////////////
  // Opening files and config

  TChain* t = input("denom");
  std::cout << "entries: " << t->GetEntries() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts

  // GEN acceptance
  TCut sel_acc_pt  = "gen_e1_pt>0.5 && gen_e2_pt>0.5";
  TCut sel_acc_eta = "abs(gen_e1_eta)<2.5 && abs(gen_e2_eta)<2.5";
  TCut sel_acc = sel_acc_pt && sel_acc_eta;

  // Trigger
  TCut sel_trg = "trigger==1";

  // "Bin" in electron (GEN) eta
  TCut sel_cen = "abs(gen_e1_eta)<1.2 && abs(gen_e2_eta)<1.2";
  TCut sel_fwd = !sel_cen;

  // Restrict all eta reqs to within |eta| < 2.5
  sel_cen += sel_acc_eta;
  sel_fwd += sel_acc_eta;
  
  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_acc: " << sel_acc.GetTitle() << std::endl
	    << "  sel_trg: " << sel_trg.GetTitle() << std::endl
	    << "  sel_cen: " << sel_cen.GetTitle() << std::endl
	    << "  sel_fwd: " << sel_fwd.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histograms

  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections
  TH2F* denom_pt1_vs_pt2_inc = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_inc",
						"",
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  TH2F* denom_pt1_vs_pt2_acc = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_acc",
						sel_acc.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  TH2F* denom_pt1_vs_pt2_trg = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_trg",
						(sel_acc&&sel_trg).GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  TH2F* denom_pt1_vs_pt2_cen = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_cen",
						(sel_acc&&sel_trg&&sel_cen).GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  TH2F* denom_pt1_vs_pt2_fwd = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_fwd",
						(sel_acc&&sel_trg&&sel_fwd).GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  TH2F* denom_pt1_vs_pt2_sum = histo_pt1_vs_pt2(t,"denom_pt1_vs_pt2_sum",
						(sel_acc&&sel_trg&&(sel_cen||sel_fwd)).GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax,
						"gen_e1_pt",
						"gen_e2_pt");
  ////////////////////////////////////////////////////////////////////////////////
  // Output

  TFile fw("latest/denom.root","RECREATE");
  //
  denom_pt1_vs_pt2_inc->Write();
  denom_pt1_vs_pt2_acc->Write();
  denom_pt1_vs_pt2_trg->Write();
  denom_pt1_vs_pt2_cen->Write();
  denom_pt1_vs_pt2_fwd->Write();
  denom_pt1_vs_pt2_sum->Write();
  //
  fw.Close();
  
}
