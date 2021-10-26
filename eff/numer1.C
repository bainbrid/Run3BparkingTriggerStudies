#include "common.C"
#include "TChain.h"
#include "TFile.h"
#include "TH2F.h"
#include "TString.h"
#include <iostream>
#include <string>

void numer1() {

  //  TFile f("root/francesca.root");
  //  TTree* t = (TTree*)f.Get("TaPtree");
  
  TChain* t = new TChain("TaPtree");
  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_0_10.root");
  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_100_110.root");
  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_10_20.root");
  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_110_120.root");
  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_120_130.root");
  
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_130_140.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_140_150.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_150_160.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_160_170.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_170_180.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_180_190.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_190_200.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_200_210.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_20_30.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_210_220.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_220_230.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_230_240.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_240_250.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_250_260.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_260_270.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_270_280.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_280_290.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_290_300.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_300_310.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_30_40.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_310_320.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_320_330.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_330_340.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_340_350.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_350_360.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_360_370.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_370_380.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_380_390.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_390_400.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_400_410.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_40_50.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_410_420.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_420_430.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_430_440.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_440_450.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_450_460.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_460_470.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_470_480.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_480_490.root");
//  //t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_490_500.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_500_510.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_50_60.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_510_520.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_520_530.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_530_540.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_540_550.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_550_560.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_560_570.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_570_580.root");
//  //t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_580_590.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_590_600.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_600_610.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_60_70.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_610_620.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_620_630.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_630_640.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_640_650.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_650_660.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_660_670.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_670_680.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_680_690.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_690_700.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_700_710.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_70_80.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_710_720.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_720_730.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_730_740.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_740_750.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_750_760.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_760_770.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_770_780.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_780_787.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_80_90.root");
//  t->Add("/eos/cms/store/group/phys_bphys/cavalari/skimbig/BuToKee_v2_noreg_90_100.root");

  std::cout << "entries: " << t->GetEntries() << std::endl; // entries: TTree = 17050, TChain = 3137854
  
  // Binning for gen pT for e1 and e2
  int nbins = 13; float width = 1.; //nbins = 3; width = 4.;
  int xbins = nbins;
  float xmin = 0.;
  float xmax = nbins*width;
  
  // GEN-match to signal
  std::string sel_sig = "bmatchMC==1";
  // Low q2 requirement
  std::string sel_lq2;
  sel_lq2 += "(mll_fullfit*mll_fullfit)>1.1 && ";
  sel_lq2 += "(mll_fullfit*mll_fullfit)<6.25 && ";
  sel_lq2 += sel_sig;
  //@@ EXTRA: RECO eta selection
  std::string sel_eta;
  sel_eta += "abs(tag_eta) < 1.2 && ";
  sel_eta += "abs(probe_eta) < 1.2 && ";
  sel_eta += sel_lq2;
  // Analysis pre-selection
  std::string sel_ana;
  sel_ana  = "abs(k_svip3d) < 0.06 && fit_Bcos2D > 0.95 && ";
  sel_ana += sel_eta;
  // Analysis BDT cut
  std::string sel_bdt = "analysisBdtO > 8. && ";
  sel_bdt += sel_ana;
  // Everything
  std::string sel_all = sel_bdt;
  
  // List selections
  std::cout << "selections:" << std::endl
	    << "  sel_lq2:    " << sel_lq2 << std::endl
	    << "  sel_ana:    " << sel_ana << std::endl
	    << "  sel_bdt:    " << sel_bdt << std::endl
	    << "  everything: " << sel_all << std::endl;

  // Histos 2D (GEN e1 pT vs GEN e2 pT) after various selections
  TH2F* numer_pt1_vs_pt2_after_lq2 = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_lq2",sel_lq2,xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_eta = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_eta",sel_eta,xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_ana = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_ana",sel_ana,xbins,xmin,xmax,xbins,xmin,xmax);
  TH2F* numer_pt1_vs_pt2_after_bdt = histo_pt1_vs_pt2(t,"numer_pt1_vs_pt2_after_bdt",sel_bdt,xbins,xmin,xmax,xbins,xmin,xmax);

  // Histos 2D ("N-1" BDT vs GEN e2 pT) after various selections
  TH2F* numer_bdt_vs_pt2_after_inc = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_inc","analysisBdtO",sel_sig,xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_lq2 = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_lq2","analysisBdtO",sel_lq2,xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_eta = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_eta","analysisBdtO",sel_eta,xbins,xmin,xmax,21,-5.,16.);
  TH2F* numer_bdt_vs_pt2_after_ana = histo_var_vs_pt2(t,"numer_bdt_vs_pt2_after_ana","analysisBdtO",sel_ana,xbins,xmin,xmax,21,-5.,16.);

  // Histos 1D ("N-1" BDT) after various selections
  TH1F numer_bdt_after_inc = histo_var(t,"numer_bdt_after_inc","analysisBdtO",sel_sig,21,-5.,16.);
  TH1F numer_bdt_after_lq2 = histo_var(t,"numer_bdt_after_lq2","analysisBdtO",sel_lq2,21,-5.,16.);
  TH1F numer_bdt_after_eta = histo_var(t,"numer_bdt_after_eta","analysisBdtO",sel_eta,21,-5.,16.);
  TH1F numer_bdt_after_ana = histo_var(t,"numer_bdt_after_ana","analysisBdtO",sel_ana,21,-5.,16.);
  TH1F numer_bdt_after_pt2 = histo_var(t,"numer_bdt_after_pt2","analysisBdtO",sel_ana+" && probe_ptMc>10.",21,-5.,16.);

  ////////////////////////////////////////////////////////////////////////////////

  // Write to file
  TFile fw("latest/numer.root","RECREATE");
  //
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
