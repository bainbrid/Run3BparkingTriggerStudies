#include "common.C"
#include "TChain.h"
#include "TCut.h"
#include "TEfficiency.h"
#include "TFile.h"
#include "TH2F.h"
#include <iostream>
#include <string>
#include <sstream>

void histos() {

  ////////////////////////////////////////////////////////////////////////////////
  // Opening files and config
  
  int nfiles = 1e6;
  TChain* t = input(nfiles);
  std::cout << "entries: " << t->GetEntries()
	    << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts

  // Trigger requirement
  TCut sel_trg  = "trg_muon_pt>-1.";
  TCut sel_trg_OR = "trg_muon_pt>0.";
  TCut sel_trg_Mu7 = "HLT_Mu7_IP4>0";
  TCut sel_trg_Mu8 = "HLT_Mu8_IP3>0";
  TCut sel_trg_Mu9 = "HLT_Mu9_IP6>0";
  //TCut sel_trg_Mu9 = "trg_muon_pt>7. && trg_muon_pt<11. && abs(trg_muon_eta)<2.1"; //@@ Replicate BParking proposal selection?
  TCut sel_trg_Mu12 = "HLT_Mu12_IP6>0";
  
  // Identify B->Kee decay
  TCut sel_kee = "isBToKEE==1";

  // GEN acceptance (pT>0.5, |eta|<2.5)
  TCut sel_acc = "inAcc==1";
  
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

  // RECO-to-GEN-match to signal
  TCut sel_sig = "isMatched==1";

  // RECO acceptance (after matching!)
  TCut sel_rec_pt  = "e1_reco_pt>0.5 && e2_reco_pt>0.5";
  TCut sel_rec_eta = "abs(e1_reco_eta)<2.5 && abs(e2_reco_eta)<2.5";
  TCut sel_rec = sel_rec_pt && sel_rec_eta;

  // RECO category (PFPF or other, i.e. PFLP)
  TCut sel_cat = "e1_reco_pf && e2_reco_pf";

  // Analysis pre-selection
  TCut sel_pre = "abs(ip3d)<0.06 && cos2d>0.95";

  // Analysis BDT cut
  TCut sel_bdt = "bdt>8.";

  // Low q2 requirement
  TCut sel_qsq = "(mll*mll)>1.1";
  sel_qsq += "(mll*mll)<6.25";
  
  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_inc: " << sel_trg.GetTitle() << std::endl
	    << "  sel_trg: " << sel_trg.GetTitle() << std::endl
	    << "  sel_kee: " << sel_kee.GetTitle() << std::endl
	    << "  sel_acc: " << sel_acc.GetTitle() << std::endl
	    << "  sel_gen: " << sel_gen.GetTitle() << std::endl
	    << "  sel_cen: " << sel_cen.GetTitle() << std::endl
	    << "  sel_fwd: " << sel_fwd.GetTitle() << std::endl
	    << "  sel_sum: " << sel_sum.GetTitle() << std::endl
	    << "  sel_sig: " << sel_sig.GetTitle() << std::endl
	    << "  sel_rec: " << sel_rec.GetTitle() << std::endl
	    << "  sel_cat: " << sel_cat.GetTitle() << std::endl
	    << "  sel_pre: " << sel_pre.GetTitle() << std::endl
	    << "  sel_bdt: " << sel_bdt.GetTitle() << std::endl
	    << "  sel_qsq: " << sel_qsq.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections for sum,cen,fwd

  // Inclusive 
  TCut sel_tmp = "";
  Histos histo_pt1_vs_pt2_inc = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_inc",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  
  //////////
  // No trigger (trg_muon_pt>-1.)
  sel_tmp = sel_trg;
  Histos histo_pt1_vs_pt2_trg = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trg",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR;
  Histos histo_pt1_vs_pt2_trgOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trgOR",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  // Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7;
  Histos histo_pt1_vs_pt2_trg7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trg7",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8;
  Histos histo_pt1_vs_pt2_trg8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trg8",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9;
  Histos histo_pt1_vs_pt2_trg9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trg9",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12;
  Histos histo_pt1_vs_pt2_trg12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_trg12",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  
  // Find B->Kee decay?
  sel_tmp = sel_trg&&sel_kee;
  Histos histo_pt1_vs_pt2_kee = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_kee",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  //////////
  // In GEN acc? (pT>0.5, |eta|<2.5)
  sel_tmp = sel_trg&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // In GEN acc with "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_accOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_accOR",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  // In GEN acc with Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc7",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // In GEN acc with Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc8",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // In GEN acc with Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc9",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // In GEN acc with Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12&&sel_kee&&sel_acc;
  Histos histo_pt1_vs_pt2_acc12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_acc12",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);

  //////////
  // Additional GEN reqs (pT>2.0, |eta|<2.5)
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // Additional GEN reqs with "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_genOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_genOR",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  // Additional GEN reqs with Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen7",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Additional GEN reqs with Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen8",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Additional GEN reqs with Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen9",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Additional GEN reqs with Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12&&sel_kee&&sel_acc&&sel_gen;
  Histos histo_pt1_vs_pt2_gen12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_gen12",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);

  // GEN-to-RECO matching
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig;
  Histos histo_pt1_vs_pt2_sig = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_sig",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  // RECO reqs (pT>2.0, |eta|<2.5)
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
  Histos histo_pt1_vs_pt2_rec = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_rec",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  //////////
  // Category (PFPF)
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_cat = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_cat",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // Category with "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_catOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_catOR",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  // Category with Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_cat7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_cat7",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Category with Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_cat8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_cat8",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Category with Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_cat9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_cat9",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Category with Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos histo_pt1_vs_pt2_cat12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_cat12",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  
  // Analysis pre-selection
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
  Histos histo_pt1_vs_pt2_pre = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_pre",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  
  //////////
  // Analysis BDT
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdt = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdt",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // Analysis BDT with "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdtOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdtOR",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  // Analysis BDT with Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdt7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdt7",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Analysis BDT with Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdt8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdt8",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Analysis BDT with Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdt9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdt9",
						      sel_tmp,sel_cen,sel_fwd,
						      xbins,xmin,xmax,xbins,xmin,xmax);
  // Analysis BDT with Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos histo_pt1_vs_pt2_bdt12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_bdt12",
						       sel_tmp,sel_cen,sel_fwd,
						       xbins,xmin,xmax,xbins,xmin,xmax);
  
  //////////
  // Low q2 req
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsq = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsq",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  // Low q2 req with "trigger soup" requirement (sel_trg_OR)
  sel_tmp = sel_trg_OR&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsqOR = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsqOR",
							   sel_tmp,sel_cen,sel_fwd,
							   xbins,xmin,xmax,xbins,xmin,xmax);
  // Low q2 req with Mu7_IP4 trigger requirement (sel_trg_Mu7)
  sel_tmp = sel_trg_Mu7&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsq7 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsq7",
							  sel_tmp,sel_cen,sel_fwd,
							  xbins,xmin,xmax,xbins,xmin,xmax);
  // Low q2 req with Mu8_IP3 trigger requirement (sel_trg_Mu8)
  sel_tmp = sel_trg_Mu8&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsq8 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsq8",
							  sel_tmp,sel_cen,sel_fwd,
							  xbins,xmin,xmax,xbins,xmin,xmax);
  // Low q2 req with Mu9_IP6 trigger requirement (sel_trg_Mu9)
  sel_tmp = sel_trg_Mu9&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsq9 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsq9",
							  sel_tmp,sel_cen,sel_fwd,
							  xbins,xmin,xmax,xbins,xmin,xmax);
  // Low q2 req with Mu12_IP6 trigger requirement (sel_trg_Mu12)
  sel_tmp = sel_trg_Mu12&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt&&sel_qsq;
  Histos histo_pt1_vs_pt2_qsq12 = histo_pt1_vs_pt2_all(t,"histo_pt1_vs_pt2_qsq12",
							   sel_tmp,sel_cen,sel_fwd,
							   xbins,xmin,xmax,xbins,xmin,xmax);
  
  ////////////////////////////////////////////////////////////////////////////////

//  // Histos 2D ("N-1" BDT vs GEN e2 pT) after various selections
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
//  TH2F* numer_bdt_vs_pt2_sum = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_sum","bdt",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_cen;
//  TH2F* numer_bdt_vs_pt2_cen = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_cen","bdt",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_fwd;
//  TH2F* numer_bdt_vs_pt2_fwd = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_fwd","bdt",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);
//
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
//  TH2F* numer_pre_vs_pt2_sum = histo_var_vs_pt2(t,"numer_pre_vs_pt2_sum","abs(ip3d)<0.06 && cos2d>0.95",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,2,-0.5,1.5);
//  
//  // Histos 1D ("N-1" BDT) after various selections
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
//  TH1F numer_bdt_sum = histo_var(t,"numer_bdt_pre_sum","bdt",
//				 sel_tmp.GetTitle(),
//				 21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_cen;
//  TH1F numer_bdt_cen = histo_var(t,"numer_bdt_cen","bdt",
//				 sel_tmp.GetTitle(),
//				 21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_fwd;
//  TH1F numer_bdt_fwd = histo_var(t,"numer_bdt_fwd","bdt",
//				 sel_tmp.GetTitle(),
//				 21,-5.,16.);
//
//  // 1D: RECO efficiency vs e2 GEN pt
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
//  TH1F denom_e2_gen_pt = histo_var(t,"denom_e2_gen_pt","e2_gen_pt",
//				   sel_tmp.GetTitle(),
//				   20,0.,10.);
//  sel_tmp += sel_sig&&sel_rec&&sel_cat;
//  TH1F numer_e2_gen_pt = histo_var(t,"numer_e2_gen_pt","e2_gen_pt",
//				   sel_tmp.GetTitle(),
//				   20,0.,10.);
//  
//  // 1D: RECO efficiency vs e12 GEN dR
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
//  TH1F denom_e12_gen_dr = histo_var(t,"denom_e12_gen_dr","e12_gen_dr",
//				    sel_tmp.GetTitle(),
//				    20,0.,2.);
//  sel_tmp += sel_sig&&sel_rec&&sel_cat;
//  TH1F numer_e12_gen_dr = histo_var(t,"numer_e12_gen_dr","e12_gen_dr",
//				    sel_tmp.GetTitle(),
//				    20,0.,2.);
//  
//  // GEN deltaR(e1,e2) vs GEN ele pT2
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
//  TH2F* denom_dr_vs_pt2 = histo_var_vs_pt2(t,"denom_dr_vs_pt2","e12_gen_dr",
//					   sel_tmp.GetTitle(),
//					   xbins,xmin,xmax,10,0.,2.0);
//
//  sel_tmp += sel_sig&&sel_rec&&sel_cat;
//  TH2F* numer_dr_vs_pt2 = histo_var_vs_pt2(t,"numer_dr_vs_pt2","e12_gen_dr",
//					   sel_tmp.GetTitle(),
//					   xbins,xmin,xmax,10,0.,2.0);
  
  ////////////////////////////////////////////////////////////////////////////////
  // Output

  // Write to file
  std::stringstream output; 
  if (nfiles>999) { output << "latest/histos.root"; }
  else { output << "latest/histos_" << nfiles << ".root"; }
  TFile fw(output.str().c_str(),"RECREATE");
  std::cout << "filename: " << output.str().c_str() << std::endl;

  histo_pt1_vs_pt2_inc.sum_->Write();
  histo_pt1_vs_pt2_inc.cen_->Write();
  histo_pt1_vs_pt2_inc.fwd_->Write();

  histo_pt1_vs_pt2_trg.sum_->Write();
  histo_pt1_vs_pt2_trg.cen_->Write();
  histo_pt1_vs_pt2_trg.fwd_->Write();
  histo_pt1_vs_pt2_trgOR.sum_->Write();
  histo_pt1_vs_pt2_trgOR.cen_->Write();
  histo_pt1_vs_pt2_trgOR.fwd_->Write();
  histo_pt1_vs_pt2_trg7.sum_->Write();
  histo_pt1_vs_pt2_trg7.cen_->Write();
  histo_pt1_vs_pt2_trg7.fwd_->Write();
  histo_pt1_vs_pt2_trg8.sum_->Write();
  histo_pt1_vs_pt2_trg8.cen_->Write();
  histo_pt1_vs_pt2_trg8.fwd_->Write();
  histo_pt1_vs_pt2_trg9.sum_->Write();
  histo_pt1_vs_pt2_trg9.cen_->Write();
  histo_pt1_vs_pt2_trg9.fwd_->Write();
  histo_pt1_vs_pt2_trg12.sum_->Write();
  histo_pt1_vs_pt2_trg12.cen_->Write();
  histo_pt1_vs_pt2_trg12.fwd_->Write();

  histo_pt1_vs_pt2_kee.fwd_->Write();
  histo_pt1_vs_pt2_kee.cen_->Write();
  histo_pt1_vs_pt2_kee.sum_->Write();

  histo_pt1_vs_pt2_acc.sum_->Write();
  histo_pt1_vs_pt2_acc.cen_->Write();
  histo_pt1_vs_pt2_acc.fwd_->Write();
  histo_pt1_vs_pt2_accOR.sum_->Write();
  histo_pt1_vs_pt2_accOR.cen_->Write();
  histo_pt1_vs_pt2_accOR.fwd_->Write();
  histo_pt1_vs_pt2_acc7.sum_->Write();
  histo_pt1_vs_pt2_acc7.cen_->Write();
  histo_pt1_vs_pt2_acc7.fwd_->Write();
  histo_pt1_vs_pt2_acc8.sum_->Write();
  histo_pt1_vs_pt2_acc8.cen_->Write();
  histo_pt1_vs_pt2_acc8.fwd_->Write();
  histo_pt1_vs_pt2_acc9.sum_->Write();
  histo_pt1_vs_pt2_acc9.cen_->Write();
  histo_pt1_vs_pt2_acc9.fwd_->Write();
  histo_pt1_vs_pt2_acc12.sum_->Write();
  histo_pt1_vs_pt2_acc12.cen_->Write();
  histo_pt1_vs_pt2_acc12.fwd_->Write();

  histo_pt1_vs_pt2_gen.sum_->Write();
  histo_pt1_vs_pt2_gen.cen_->Write();
  histo_pt1_vs_pt2_gen.fwd_->Write();
  histo_pt1_vs_pt2_genOR.sum_->Write();
  histo_pt1_vs_pt2_genOR.cen_->Write();
  histo_pt1_vs_pt2_genOR.fwd_->Write();
  histo_pt1_vs_pt2_gen7.sum_->Write();
  histo_pt1_vs_pt2_gen7.cen_->Write();
  histo_pt1_vs_pt2_gen7.fwd_->Write();
  histo_pt1_vs_pt2_gen8.sum_->Write();
  histo_pt1_vs_pt2_gen8.cen_->Write();
  histo_pt1_vs_pt2_gen8.fwd_->Write();
  histo_pt1_vs_pt2_gen9.sum_->Write();
  histo_pt1_vs_pt2_gen9.cen_->Write();
  histo_pt1_vs_pt2_gen9.fwd_->Write();
  histo_pt1_vs_pt2_gen12.sum_->Write();
  histo_pt1_vs_pt2_gen12.cen_->Write();
  histo_pt1_vs_pt2_gen12.fwd_->Write();

  histo_pt1_vs_pt2_sig.sum_->Write();
  histo_pt1_vs_pt2_sig.cen_->Write();
  histo_pt1_vs_pt2_sig.fwd_->Write();

  histo_pt1_vs_pt2_rec.sum_->Write();
  histo_pt1_vs_pt2_rec.cen_->Write();
  histo_pt1_vs_pt2_rec.fwd_->Write();

  histo_pt1_vs_pt2_cat.sum_->Write();
  histo_pt1_vs_pt2_cat.cen_->Write();
  histo_pt1_vs_pt2_cat.fwd_->Write();
  histo_pt1_vs_pt2_catOR.sum_->Write();
  histo_pt1_vs_pt2_catOR.cen_->Write();
  histo_pt1_vs_pt2_catOR.fwd_->Write();
  histo_pt1_vs_pt2_cat7.sum_->Write();
  histo_pt1_vs_pt2_cat7.cen_->Write();
  histo_pt1_vs_pt2_cat7.fwd_->Write();
  histo_pt1_vs_pt2_cat8.sum_->Write();
  histo_pt1_vs_pt2_cat8.cen_->Write();
  histo_pt1_vs_pt2_cat8.fwd_->Write();
  histo_pt1_vs_pt2_cat9.sum_->Write();
  histo_pt1_vs_pt2_cat9.cen_->Write();
  histo_pt1_vs_pt2_cat9.fwd_->Write();
  histo_pt1_vs_pt2_cat12.sum_->Write();
  histo_pt1_vs_pt2_cat12.cen_->Write();
  histo_pt1_vs_pt2_cat12.fwd_->Write();

  histo_pt1_vs_pt2_pre.sum_->Write();
  histo_pt1_vs_pt2_pre.cen_->Write();
  histo_pt1_vs_pt2_pre.fwd_->Write();

  histo_pt1_vs_pt2_bdt.sum_->Write();
  histo_pt1_vs_pt2_bdt.cen_->Write();
  histo_pt1_vs_pt2_bdt.fwd_->Write();
  histo_pt1_vs_pt2_bdtOR.sum_->Write();
  histo_pt1_vs_pt2_bdtOR.cen_->Write();
  histo_pt1_vs_pt2_bdtOR.fwd_->Write();
  histo_pt1_vs_pt2_bdt7.sum_->Write();
  histo_pt1_vs_pt2_bdt7.cen_->Write();
  histo_pt1_vs_pt2_bdt7.fwd_->Write();
  histo_pt1_vs_pt2_bdt8.sum_->Write();
  histo_pt1_vs_pt2_bdt8.cen_->Write();
  histo_pt1_vs_pt2_bdt8.fwd_->Write();
  histo_pt1_vs_pt2_bdt9.sum_->Write();
  histo_pt1_vs_pt2_bdt9.cen_->Write();
  histo_pt1_vs_pt2_bdt9.fwd_->Write();
  histo_pt1_vs_pt2_bdt12.sum_->Write();
  histo_pt1_vs_pt2_bdt12.cen_->Write();
  histo_pt1_vs_pt2_bdt12.fwd_->Write();

  histo_pt1_vs_pt2_qsq.sum_->Write();
  histo_pt1_vs_pt2_qsq.cen_->Write();
  histo_pt1_vs_pt2_qsq.fwd_->Write();
  histo_pt1_vs_pt2_qsqOR.sum_->Write();
  histo_pt1_vs_pt2_qsqOR.cen_->Write();
  histo_pt1_vs_pt2_qsqOR.fwd_->Write();
  histo_pt1_vs_pt2_qsq7.sum_->Write();
  histo_pt1_vs_pt2_qsq7.cen_->Write();
  histo_pt1_vs_pt2_qsq7.fwd_->Write();
  histo_pt1_vs_pt2_qsq8.sum_->Write();
  histo_pt1_vs_pt2_qsq8.cen_->Write();
  histo_pt1_vs_pt2_qsq8.fwd_->Write();
  histo_pt1_vs_pt2_qsq9.sum_->Write();
  histo_pt1_vs_pt2_qsq9.cen_->Write();
  histo_pt1_vs_pt2_qsq9.fwd_->Write();
  histo_pt1_vs_pt2_qsq12.sum_->Write();
  histo_pt1_vs_pt2_qsq12.cen_->Write();
  histo_pt1_vs_pt2_qsq12.fwd_->Write();

//  numer_bdt_vs_pt2_sum->Write();
//  numer_bdt_vs_pt2_cen->Write();
//  numer_bdt_vs_pt2_fwd->Write();
//  numer_pre_vs_pt2_sum->Write();

//  numer_bdt_sum.Write();
//  numer_bdt_cen.Write();
//  numer_bdt_fwd.Write();

//  denom_e2_gen_pt.Write();
//  numer_e2_gen_pt.Write();
//
//  denom_e2_gen_dr.Write();
//  numer_e2_gen_dr.Write();
//
//  denom_dr_vs_pt2->Write();
//  numer_dr_vs_pt2->Write();
//
//  numer_e12_gen_dr.Write();
//  denom_e12_gen_dr.Write();
//
//  numer_pt1_vs_pt2_dr.sum_->Write();
//  numer_pt1_vs_pt2_dr.cen_->Write();
//  numer_pt1_vs_pt2_dr.fwd_->Write();
  
  fw.Close();
  std::cout << "done!" << std::endl;
}
