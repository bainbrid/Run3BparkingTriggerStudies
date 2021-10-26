{ 
  TFile f("root/genstudy_pt.root");
  TTree* t = (TTree*)f.Get("tree");
  std::cout << "entries: " << t->GetEntries() << std::endl;

  nbins = 13; width = 1.; //nbins = 3; width = 4.;

  TH2F denom_nosel("denom_nosel","denom_nosel",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width );
  int n1 = tree->Draw("gen_e1_pt:gen_e2_pt>>denom_nosel","","goff");
  std::cout << "processed denom nosel: " << n1 << std::endl;

  TH2F denom_sel("denom_sel","denom_sel",nbins, 0. ,nbins*width, nbins, 0. ,nbins*width );
  std::string sel;
  //sel += "gen_e1_pt > 0.5 && gen_e2_pt > 0.5";                 //@@ EXTRA: GEN pT selection
  //sel += " && abs(gen_e1_eta) < 2.5 && abs(gen_e2_eta) < 2.5"; //@@ EXTRA: GEN eta selection
  sel += "trigger==1";                                           // BParking trigger fired
  sel += " && abs(gen_e1_eta) < 1.2 && abs(gen_e2_eta) < 1.2";   //@@ EXTRA: GEN eta selection
  int n2 = tree->Draw("gen_e1_pt:gen_e2_pt>>denom_sel",sel.c_str(),"goff");
  std::cout << "processed denom sel:" << n2 << std::endl;

  TFile fw("latest/denom.root","RECREATE");
  denom_nosel.Write();
  denom_sel.Write();
  fw.Close();
}
