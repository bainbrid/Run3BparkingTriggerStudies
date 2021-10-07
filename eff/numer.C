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

  std::string sel;
  sel += "bmatchMC==1";                                                         // GEN-match to signal
  sel += " && abs(k_svip3d) < 0.06 && fit_Bcos2D > 0.95";                       // Analysis pre-selection
  sel += " && analysisBdtO > 8.";                                               // Analysis BDT cut
  sel += " && (mll_fullfit*mll_fullfit)>1.1 && (mll_fullfit*mll_fullfit)<6.25"; // Low q2 requirement
  //sel += " && abs(tag_eta) < 1.2 && abs(probe_eta) < 1.2"; //@@ EXTRA: RECO eta selection

  nbins = 13; width = 1.;
  //nbins = 3; width = 4.;

  TH2F numer_reco("numer_reco","numer_reco",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n1 = t->Draw("tag_pt:probe_pt>>numer_reco",sel.c_str(),"goff");
  std::cout << "processed numer reco: " << n1 << std::endl;

  TH2F numer_gen_all("numer_gen_all","numer_gen_all",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n2 = t->Draw("tag_ptMc:probe_ptMc>>numer_gen_all",sel.c_str(),"goff");
  std::cout << "processed numer gen_all: " << n2 << std::endl;

  std::string sel1 = "tag_ptMc>=probe_ptMc && " + sel;
  TH2F numer_gen_lead("numer_gen_lead","numer_gen_lead",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n3 = t->Draw("tag_ptMc:probe_ptMc>>numer_gen_lead",sel1.c_str(),"goff");
  std::cout << "processed numer gen_lead: " << n3 << std::endl;

  std::string sel2 = "tag_ptMc<probe_ptMc && " + sel;
  TH2F numer_gen_sub("numer_gen_sub","numer_gen_sub",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width);
  int n4 = t->Draw("probe_ptMc:tag_ptMc>>numer_gen_sub",sel2.c_str(),"goff");
  std::cout << "processed numer gen_sub: " << n4 << std::endl;
  
  TFile fw("latest/numer.root","RECREATE");
  numer_reco.Write();
  numer_gen_all.Write();
  numer_gen_lead.Write();
  numer_gen_sub.Write();
  fw.Close();
  std::cout << "done!" << std::endl;
}
