#include "common.C"
#include "TChain.h"
#include "TCut.h"
#include "TEfficiency.h"
#include "TFile.h"
#include "TH2F.h"
#include <iostream>
#include <string>
#include <sstream>

void numer1() {

  ////////////////////////////////////////////////////////////////////////////////
  // Opening files and config
  
  int nfiles = 1e6;
  TChain* t = input("numer",nfiles);
  std::cout << "entries: " << t->GetEntries() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Cuts

  // Trigger requirement
  TCut sel_trg  = "trg_muon_pt>-1.";
  TCut sel_trg0 = "trg_muon_pt>0.";
  TCut sel_trg1 = "HLT_Mu7_IP4>0 && HLT_Mu8_IP3>0";
  TCut sel_trg2 = "HLT_Mu7_IP4>0";
  TCut sel_trg3 = "HLT_Mu9_IP6>0";
  TCut sel_trg4 = "HLT_Mu12_IP6>0";
  
  // Identify B->Kee decay
  TCut sel_kee = "isBToKEE==1";

  // GEN acceptance (pT > 0.5, |eta| < 2.5)
  TCut sel_acc = "inAcc==1";
  
  // GEN acceptance (before matching!)
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
  TCut sel_cat = "e1_reco_pf && e2_reco_pf"; // && e1_reco_overlap || e2_reco_overlap)";
  //TCut sel_cat = "(e1_reco_pf || e1_reco_overlap) && (e2_reco_pf || e2_reco_overlap)";

  //(l.l1isPF == 1 and l.l2isPF == 0 and l.l2isPFoverlap==0) 
  //or
  //(l.l1isPF == 0 and l.l2isPF == 1 and l.l1isPFoverlap==0)

  // Analysis pre-selection
  TCut sel_pre = "abs(ip3d)<0.06 && cos2d>0.95";

  // Analysis BDT cut
  TCut sel_bdt = "bdt>8.";

  // Low q2 requirement
  TCut sel_lq2 = "(mll_fullfit*mll_fullfit)>1.1";
  sel_lq2 += "(mll_fullfit*mll_fullfit)<6.25";
  
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
	    << "  sel_lq2: " << sel_lq2.GetTitle() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////
  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections

  // Incl, trigger, Kee decay, acceptance
  TCut sel_tmp = "";
  TH2F* numer_pt1_vs_pt2_inc = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_inc",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg;
  TH2F* numer_pt1_vs_pt2_trg = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee;
  TH2F* numer_pt1_vs_pt2_kee = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc;
  TH2F* numer_pt1_vs_pt2_acc = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,xbins,xmin,xmax);

  // Return sum,cen,fwd in a struct
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
  Histos numer_pt1_vs_pt2_gen = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_gen",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig;
  Histos numer_pt1_vs_pt2_sig = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_sig",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
  Histos numer_pt1_vs_pt2_rec = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_rec",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  Histos numer_pt1_vs_pt2_cat = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_cat",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
  Histos numer_pt1_vs_pt2_pre = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_pre",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_bdt;
  Histos numer_pt1_vs_pt2_bdt = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_bdt",
						     sel_tmp,sel_cen,sel_fwd,
						     xbins,xmin,xmax,xbins,xmin,xmax);

  ////////////////////////////////////////////////////////////////////////////////

  // Histos 2D ("N-1" BDT vs GEN e2 pT) after various selections
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
  TH2F* numer_bdt_vs_pt2_sum = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_sum","bdt",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_cen;
  TH2F* numer_bdt_vs_pt2_cen = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_cen","bdt",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_fwd;
  TH2F* numer_bdt_vs_pt2_fwd = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_fwd","bdt",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,21,-5.,16.);

  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat;
  TH2F* numer_pre_vs_pt2_sum = histo_var_vs_pt2(t,"numer_pre_vs_pt2_sum","abs(ip3d)<0.06 && cos2d>0.95",
						sel_tmp.GetTitle(),
						xbins,xmin,xmax,2,-0.5,1.5);
  
  // Histos 1D ("N-1" BDT) after various selections
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre;
  TH1F numer_bdt_sum = histo_var(t,"numer_bdt_pre_sum","bdt",
				 sel_tmp.GetTitle(),
				 21,-5.,16.);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_cen;
  TH1F numer_bdt_cen = histo_var(t,"numer_bdt_cen","bdt",
				 sel_tmp.GetTitle(),
				 21,-5.,16.);
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_cat&&sel_pre&&sel_fwd;
  TH1F numer_bdt_fwd = histo_var(t,"numer_bdt_fwd","bdt",
				 sel_tmp.GetTitle(),
				 21,-5.,16.);

  ////////////////////////////////////////////////////////////////////////////////

  // 1D: RECO efficiency vs e2 GEN pt
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
  TH1F denom_e2_gen_pt = histo_var(t,"denom_e2_gen_pt","e2_gen_pt",
				   sel_tmp.GetTitle(),
				   20,0.,10.);
  sel_tmp += sel_sig&&sel_rec&&sel_cat;
  TH1F numer_e2_gen_pt = histo_var(t,"numer_e2_gen_pt","e2_gen_pt",
				   sel_tmp.GetTitle(),
				   20,0.,10.);
  
  // 1D: RECO efficiency vs e12 GEN dR
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
  TH1F denom_e12_gen_dr = histo_var(t,"denom_e12_gen_dr","e12_gen_dr",
				    sel_tmp.GetTitle(),
				    20,0.,2.);
  sel_tmp += sel_sig&&sel_rec&&sel_cat;
  TH1F numer_e12_gen_dr = histo_var(t,"numer_e12_gen_dr","e12_gen_dr",
				    sel_tmp.GetTitle(),
				    20,0.,2.);
  
  // GEN deltaR(e1,e2) vs GEN ele pT2
  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen;
  TH2F* denom_dr_vs_pt2 = histo_var_vs_pt2(t,"denom_dr_vs_pt2","e12_gen_dr",
					   sel_tmp.GetTitle(),
					   xbins,xmin,xmax,10,0.,2.0);

  sel_tmp += sel_sig&&sel_rec&&sel_cat;
  TH2F* numer_dr_vs_pt2 = histo_var_vs_pt2(t,"numer_dr_vs_pt2","e12_gen_dr",
					   sel_tmp.GetTitle(),
					   xbins,xmin,xmax,10,0.,2.0);

//  TCut sel_gen_dr = "e12_gen_dr>0.3";
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_gen_dr;
//  Histos numer_pt1_vs_pt2_dr = histo_pt1_vs_pt2_all(t,"numer_pt1_vs_pt2_dr",
//						    sel_tmp,sel_cen,sel_fwd,
//						    xbins,xmin,xmax,xbins,xmin,xmax);
  


//  // 1D efficiency (e2)
//  sel_rec_e1 = "e1_reco_pt>0.5 && abs(e1_reco_eta)<2.5";// && (e1_reco_pf)";// || e1_reco_overlap)";
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec_e1;
//  TH1F denom_e2_gen_pt = histo_var(t,"e2_denom_gen_pt","e2_gen_pt",
//				sel_tmp.GetTitle(),
//				20,0.,10.);
//  sel_rec_e2 = "e2_reco_pt>0.5 && abs(e2_reco_eta)<2.5";// && (e2_reco_pf)";// || e2_reco_overlap)";
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec_e1&&sel_rec_e2;
//  TH1F numer_e2_gen_pt = histo_var(t,"e2_numer_gen_pt","e2_gen_pt",
//				sel_tmp.GetTitle(),
//				20,0.,10.);
//  TEfficiency eff_e2_gen_pt(numer_e2_gen_pt,denom_e2_gen_pt);
  
  ////////////////////////////////////////////////////////////////////////////////
  // Output

  // Write to file
  std::stringstream output; 
  if (nfiles>999) { output << "latest/numer.root"; }
  else { output << "latest/numer_" << nfiles << ".root"; }
  TFile fw(output.str().c_str(),"RECREATE");
  std::cout << "filename: " << output.str().c_str() << std::endl;

  ////////////////////////////////////////////////////////////////////////////////

  numer_pt1_vs_pt2_inc->Write();
  numer_pt1_vs_pt2_trg->Write();
  numer_pt1_vs_pt2_kee->Write();
  numer_pt1_vs_pt2_acc->Write();

  numer_pt1_vs_pt2_gen.sum_->Write();
  numer_pt1_vs_pt2_gen.cen_->Write();
  numer_pt1_vs_pt2_gen.fwd_->Write();
  numer_pt1_vs_pt2_sig.sum_->Write();
  numer_pt1_vs_pt2_sig.cen_->Write();
  numer_pt1_vs_pt2_sig.fwd_->Write();
  numer_pt1_vs_pt2_rec.sum_->Write();
  numer_pt1_vs_pt2_rec.cen_->Write();
  numer_pt1_vs_pt2_rec.fwd_->Write();
  numer_pt1_vs_pt2_cat.sum_->Write();
  numer_pt1_vs_pt2_cat.cen_->Write();
  numer_pt1_vs_pt2_cat.fwd_->Write();
  numer_pt1_vs_pt2_pre.sum_->Write();
  numer_pt1_vs_pt2_pre.cen_->Write();
  numer_pt1_vs_pt2_pre.fwd_->Write();
  numer_pt1_vs_pt2_bdt.sum_->Write();
  numer_pt1_vs_pt2_bdt.cen_->Write();
  numer_pt1_vs_pt2_bdt.fwd_->Write();

  numer_bdt_vs_pt2_sum->Write();
  numer_bdt_vs_pt2_cen->Write();
  numer_bdt_vs_pt2_fwd->Write();
  numer_pre_vs_pt2_sum->Write();

  numer_bdt_sum.Write();
  numer_bdt_cen.Write();
  numer_bdt_fwd.Write();

  ////////////////////////////////////////////////////////////////////////////////

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





////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

//  //@@
//  sel_tmp = sel_trg0;
//  TH2F* numer_pt1_vs_pt2_trg0 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg0",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg0&&sel_kee;
//  TH2F* numer_pt1_vs_pt2_kee0 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee0",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg0&&sel_kee&&sel_acc;
//  TH2F* numer_pt1_vs_pt2_acc0 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc0",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg0&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
//  TH2F* numer_pt1_vs_pt2_rec0 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_rec0",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//
//  //@@
//  sel_tmp = sel_trg1;
//  TH2F* numer_pt1_vs_pt2_trg1 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg1",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg1&&sel_kee;
//  TH2F* numer_pt1_vs_pt2_kee1 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee1",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg1&&sel_kee&&sel_acc;
//  TH2F* numer_pt1_vs_pt2_acc1 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc1",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg1&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
//  TH2F* numer_pt1_vs_pt2_rec1 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_rec1",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//
//  //@@
//  sel_tmp = sel_trg2;
//  TH2F* numer_pt1_vs_pt2_trg2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg2",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg2&&sel_kee;
//  TH2F* numer_pt1_vs_pt2_kee2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee2",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg2&&sel_kee&&sel_acc;
//  TH2F* numer_pt1_vs_pt2_acc2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc2",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg2&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
//  TH2F* numer_pt1_vs_pt2_rec2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_rec2",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//
//  //@@
//  sel_tmp = sel_trg3;
//  TH2F* numer_pt1_vs_pt2_trg3 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg3",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg3&&sel_kee;
//  TH2F* numer_pt1_vs_pt2_kee3 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee3",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg3&&sel_kee&&sel_acc;
//  TH2F* numer_pt1_vs_pt2_acc3 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc3",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg3&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
//  TH2F* numer_pt1_vs_pt2_rec3 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_rec3",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//
//  //@@
//  sel_tmp = sel_trg4;
//  TH2F* numer_pt1_vs_pt2_trg4 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_trg4",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg4&&sel_kee;
//  TH2F* numer_pt1_vs_pt2_kee4 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_kee4",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg4&&sel_kee&&sel_acc;
//  TH2F* numer_pt1_vs_pt2_acc4 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_acc4",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg4&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec;
//  TH2F* numer_pt1_vs_pt2_rec4 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_rec4",
//						 sel_tmp.GetTitle(),
//						 xbins,xmin,xmax,xbins,xmin,xmax);

//  // TMP!!
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_cen;
//  TH2F* numer_pt1_vs_pt2_cen = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_cen",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_fwd;
//  TH2F* numer_pt1_vs_pt2_fwd = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_fwd",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);

//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_pre&&sel_bdt&&sel_sum;
//  TH2F* numer_pt1_vs_pt2_sum = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_sum",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_pre&&sel_bdt&&sel_lq2;
//  TH2F* numer_pt1_vs_pt2_lq2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_lq2",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,xbins,xmin,xmax);

//  sel_tmp = sel_all;
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
//  TH2F* numer_bdt_vs_pt2_pre = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_pre","analysisBdtO",
//						      (sel_sig&&sel_lq2&&sel_eta&&sel_pre).GetTitle(),
//						      xbins,xmin,xmax,21,-5.,16.);

//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_pre&&sel_cen;
//  TH2F* numer_bdt_vs_pt2_cen = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_cen","analysisBdtO",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_pre&&sel_fwd;
//  TH2F* numer_bdt_vs_pt2_fwd = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_fwd","analysisBdtO",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);
//  sel_tmp = sel_trg&&sel_kee&&sel_acc&&sel_gen&&sel_sig&&sel_rec&&sel_pre&&sel_sum;
//  TH2F* numer_bdt_vs_pt2_sum = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_sum","analysisBdtO",
//						sel_tmp.GetTitle(),
//						xbins,xmin,xmax,21,-5.,16.);

//  // Histos 1D ("N-1" BDT) after various selections //@@ SELECTIONS NEED UPDATING !!
//  TH1F numer_bdt_sig = histo_var(t,"numer_bdt_sig","analysisBdtO",
//				       sel_sig.GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_lq2 = histo_var(t,"numer_bdt_lq2","analysisBdtO",
//				       (sel_sig&&sel_lq2).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_eta = histo_var(t,"numer_bdt_eta","analysisBdtO",
//				       (sel_sig&&sel_lq2&&sel_eta).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_pre = histo_var(t,"numer_bdt_pre","analysisBdtO",
//				       (sel_sig&&sel_lq2&&sel_eta&&sel_pre).GetTitle(),
//				       21,-5.,16.);
//  TH1F numer_bdt_pt2 = histo_var(t,"numer_bdt_pt2","analysisBdtO",
//				       std::string((sel_sig&&sel_lq2&&sel_eta&&sel_pre).GetTitle())+" && probe_ptMc>10.",
//				       21,-5.,16.);


//  //@@ DEBUG
//  numer_pt1_vs_pt2_trg0->Write();
//  numer_pt1_vs_pt2_kee0->Write();
//  numer_pt1_vs_pt2_acc0->Write();
//  numer_pt1_vs_pt2_rec0->Write();
//  numer_pt1_vs_pt2_trg1->Write();
//  numer_pt1_vs_pt2_kee1->Write();
//  numer_pt1_vs_pt2_acc1->Write();
//  numer_pt1_vs_pt2_rec1->Write();
//  numer_pt1_vs_pt2_trg2->Write();
//  numer_pt1_vs_pt2_kee2->Write();
//  numer_pt1_vs_pt2_acc2->Write();
//  numer_pt1_vs_pt2_rec2->Write();
//  numer_pt1_vs_pt2_trg3->Write();
//  numer_pt1_vs_pt2_kee3->Write();
//  numer_pt1_vs_pt2_acc3->Write();
//  numer_pt1_vs_pt2_rec3->Write();
//  numer_pt1_vs_pt2_trg4->Write();
//  numer_pt1_vs_pt2_kee4->Write();
//  numer_pt1_vs_pt2_acc4->Write();
//  numer_pt1_vs_pt2_rec4->Write();

//  numer_pt1_vs_pt2_sum->Write();
//  numer_pt1_vs_pt2_lq2->Write();

//  numer_pt1_vs_pt2_sum->Write();
//  numer_pt1_vs_pt2_all->Write();
//  numer_pt1_vs_pt2_tst->Write();



