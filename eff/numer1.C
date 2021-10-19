{

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
  nbins = 13; width = 1.;
  //nbins = 3; width = 4.;
  
//  std::string bdt;
//  std::string sel;
//  sel += "bmatchMC==1";                                                         // GEN-match to signal
//  sel += " && abs(k_svip3d) < 0.06 && fit_Bcos2D > 0.95";                       // Analysis pre-selection
//  bdt  = " && analysisBdtO > 8."; sel += bdt;                                   // Analysis BDT cut
//  sel += " && (mll_fullfit*mll_fullfit)>1.1 && (mll_fullfit*mll_fullfit)<6.25"; // Low q2 requirement
//  sel += " && abs(tag_eta) < 1.2 && abs(probe_eta) < 1.2"; //@@ EXTRA: RECO eta selection
  
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

  // Misc histos (probably not useful...)
  TH2F numer_reco("numer_reco","numer_reco",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n1 = t->Draw("tag_pt:probe_pt>>numer_reco",sel_all.c_str(),"goff");
  std::cout << "processed numer reco: " << n1 << std::endl;

  TH2F numer_gen_all("numer_gen_all","numer_gen_all",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n2 = t->Draw("tag_ptMc:probe_ptMc>>numer_gen_all",sel_all.c_str(),"goff");
  std::cout << "processed numer_gen_all: " << n2 << std::endl;

  // Histos GEN pT (e1,e2) after sel_lq2 for lead, sub, and sum
  std::string sel1_lq2 = "tag_ptMc>=probe_ptMc && " + sel_lq2;
  TH2F numer_lq2_gen_lead("numer_lq2_gen_lead","numer_lq2_gen_lead",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n3_lq2 = t->Draw("tag_ptMc:probe_ptMc>>numer_lq2_gen_lead",sel1_lq2.c_str(),"goff");
  std::cout << "processed numer_lq2_gen_lead: " << n3_lq2 << std::endl;
  std::string sel2_lq2 = "tag_ptMc<probe_ptMc && " + sel_lq2;
  TH2F numer_lq2_gen_sub("numer_lq2_gen_sub","numer_lq2_gen_sub",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n4_lq2 = t->Draw("probe_ptMc:tag_ptMc>>numer_lq2_gen_sub",sel2_lq2.c_str(),"goff");
  std::cout << "processed numer_lq2_gen_sub: " << n4_lq2 << std::endl;
  TH2F* numer_lq2_gen_sum = (TH2F*)numer_lq2_gen_lead.Clone("numer_lq2_gen_sum");
  numer_lq2_gen_sum->Add(&numer_lq2_gen_sub,1.);

  std::cout << "entries numer_lq2_gen_lead: " << numer_lq2_gen_lead.GetEntries() << std::endl;
  std::cout << "entries numer_lq2_gen_sub: " << numer_lq2_gen_sub.GetEntries() << std::endl;
  std::cout << "entries numer_lq2_gen_sum: " << numer_lq2_gen_sum->GetEntries() << std::endl;

  // Histos GEN pT (e1,e2) after sel_eta for lead, sub, and sum
  std::string sel1_eta = "tag_ptMc>=probe_ptMc && " + sel_eta;
  TH2F numer_eta_gen_lead("numer_eta_gen_lead","numer_eta_gen_lead",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n3_eta = t->Draw("tag_ptMc:probe_ptMc>>numer_eta_gen_lead",sel1_eta.c_str(),"goff");
  std::cout << "processed numer_eta_gen_lead: " << n3_eta << std::endl;
  std::string sel2_eta = "tag_ptMc<probe_ptMc && " + sel_eta;
  TH2F numer_eta_gen_sub("numer_eta_gen_sub","numer_eta_gen_sub",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n4_eta = t->Draw("probe_ptMc:tag_ptMc>>numer_eta_gen_sub",sel2_eta.c_str(),"goff");
  std::cout << "processed numer_eta_gen_sub: " << n4_eta << std::endl;
  TH2F* numer_eta_gen_sum = (TH2F*)numer_eta_gen_lead.Clone("numer_eta_gen_sum");
  numer_eta_gen_sum->Add(&numer_eta_gen_sub,1.);

  // Histos GEN pT (e1,e2) after sel_ana for lead, sub, and sum
  std::string sel1_ana = "tag_ptMc>=probe_ptMc && " + sel_ana;
  TH2F numer_ana_gen_lead("numer_ana_gen_lead","numer_ana_gen_lead",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n3_ana = t->Draw("tag_ptMc:probe_ptMc>>numer_ana_gen_lead",sel1_ana.c_str(),"goff");
  std::cout << "processed numer_ana_gen_lead: " << n3_ana << std::endl;
  std::string sel2_ana = "tag_ptMc<probe_ptMc && " + sel_ana;
  TH2F numer_ana_gen_sub("numer_ana_gen_sub","numer_ana_gen_sub",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n4_ana = t->Draw("probe_ptMc:tag_ptMc>>numer_ana_gen_sub",sel2_ana.c_str(),"goff");
  std::cout << "processed numer_ana_gen_sub: " << n4_ana << std::endl;
  TH2F* numer_ana_gen_sum = (TH2F*)numer_ana_gen_lead.Clone("numer_ana_gen_sum");
  numer_ana_gen_sum->Add(&numer_ana_gen_sub,1.);

  // Histos GEN pT (e1,e2) after sel_bdt selection for lead, sub, and sum
  std::string sel1_bdt = "tag_ptMc>=probe_ptMc && " + sel_bdt;
  TH2F numer_bdt_gen_lead("numer_bdt_gen_lead","numer_bdt_gen_lead",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n3_bdt = t->Draw("tag_ptMc:probe_ptMc>>numer_bdt_gen_lead",sel1_bdt.c_str(),"goff");
  std::cout << "processed numer_bdt_gen_lead: " << n3_bdt << std::endl;
  std::string sel2_bdt = "tag_ptMc<probe_ptMc && " + sel_bdt;
  TH2F numer_bdt_gen_sub("numer_bdt_gen_sub","numer_bdt_gen_sub",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n4_bdt = t->Draw("probe_ptMc:tag_ptMc>>numer_bdt_gen_sub",sel2_bdt.c_str(),"goff");
  std::cout << "processed numer_bdt_gen_sub: " << n4_bdt << std::endl;
  TH2F* numer_bdt_gen_sum = (TH2F*)numer_bdt_gen_lead.Clone("numer_bdt_gen_sum");
  numer_bdt_gen_sum->Add(&numer_bdt_gen_sub,1.);

  // Histo (BDT score, GEN pT sublead) after sel_ana selection for each sulead (tag or probe) and sum
  std::string sel3 = "tag_pt<probe_ptMc && " + sel_ana; // tag is sub, probe is lead
  TH2F numer_bdt_sub_tag("numer_bdt_sub_tag","numer_bdt_sub_tag",nbins, 0. ,nbins*width, 20, -20., 20.);
  int n5 = t->Draw("tag_ptMc:analysisBdtO>>numer_bdt_sub_tag",sel3.c_str(),"goff");
  std::cout << "processed numer_bdt_sub_tag: " << n5 << std::endl;
  std::string sel4 = "tag_ptMc>=probe_ptMc && " + sel_ana; // probe is sub, tag is lead
  TH2F numer_bdt_sub_probe("numer_bdt_sub_probe","numer_bdt_sub_probe",nbins, 0. ,nbins*width, 20, -20., 20.);
  int n6 = t->Draw("probe_ptMc:analysisBdtO>>numer_bdt_sub_probe",sel4.c_str(),"goff");
  std::cout << "processed numer_bdt_sub_probe: " << n6 << std::endl;
  TH2F* numer_bdt_sub_sum = (TH2F*)numer_bdt_sub_tag.Clone("numer_bdt_sub_sum");
  numer_bdt_sub_sum->Add(&numer_bdt_sub_probe,1.);

  TH1F bdt_inc("bdt_inc","bdt_inc",20, -20., 20.);
  t->Draw("analysisBdtO>>bdt_inc","","goff");
  TH1F bdt_lq2("bdt_lq2","bdt_lq2",20, -20., 20.);
  t->Draw("analysisBdtO>>bdt_lq2",sel_lq2.c_str(),"goff");
  TH1F bdt_ana("bdt_ana","bdt_ana",20, -20., 20.);
  t->Draw("analysisBdtO>>bdt_ana",sel_ana.c_str(),"goff");

  // Write to file
  TFile fw("latest/numer.root","RECREATE");
  //
  numer_reco.Write();
  numer_gen_all.Write();
  //
  numer_bdt_gen_lead.Write();
  numer_bdt_gen_sub.Write();
  //
  numer_lq2_gen_sum->Write();
  numer_eta_gen_sum->Write();
  numer_ana_gen_sum->Write();
  numer_bdt_gen_sum->Write();
  //
  numer_bdt_sub_tag.Write();
  numer_bdt_sub_probe.Write();
  numer_bdt_sub_sum->Write();
  //
  bdt_inc.Write();
  bdt_lq2.Write();
  bdt_ana.Write();
  //
  fw.Close();
  std::cout << "done!" << std::endl;
}
