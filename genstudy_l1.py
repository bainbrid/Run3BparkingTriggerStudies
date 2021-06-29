from DataFormats.FWLite import Events, Handle
from common.deltar             import deltaR, bestMatch, bestMatchAtVtx
from ROOT import TFile, TTree, Double, TLorentzVector
from array import array
import math, copy
from os import listdir
from os.path import isfile, join
from TreeProducerGen import *

mypath='/eos/user/y/ytakahas/BparkingTriggerStudy_nomufilter/'
onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

#onlyfiles = onlyfiles[0:1000]

events = Events(onlyfiles)
Nevt = int(events.size())
print len(onlyfiles), 'files are analyzed. Total # of events = ', Nevt

handle  = Handle ('std::vector<reco::GenParticle>')
label = ("genParticles")
handle_e  = Handle ('BXVector<l1t::EGamma>')
label_e = ("gtStage2Digis", "EGamma")
handle_mu  = Handle ('BXVector<l1t::Muon>')
label_mu = ("gtStage2Digis", "Muon")

nevents = 0
ndrop = 0
out = TreeProducerGen('genstudy_l1_signal_' + str(len(onlyfiles)) + 'files_'  + str(Nevt) + 'events.root')

ptrange = np.arange(3, 14, 1).tolist() 


dRthr = 0.2

for ev in events:
    if nevents%1000==0: print('{0:.2f}'.format(Double(nevents)/Double(Nevt)*100.), '% processed')

    ####################################
    # gen
    ####################################

    ev.getByLabel(label, handle)
    gps = handle.product()
    gen_bs = [p for p in gps if abs(p.pdgId())==521] 
    genmuons = [p for p in gps if abs(p.pdgId()) == 13 and p.status()==1]
 
    bs = []
    genelectrons = None
    for p in gen_bs:
        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
        genelectrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
        bs.append(p)

    if len(bs)!=1: 
        ndrop += 1
        continue

    genelectrons = sorted(genelectrons, key = lambda e : e.pt(), reverse = True )
    genmuons = sorted(genmuons, key = lambda mu : mu.pt(), reverse = True )

    out.gen_e1_pt[0] = genelectrons[0].pt()
    out.gen_e1_eta[0] = genelectrons[0].eta()
    out.gen_e1_phi[0] = genelectrons[0].phi()
    out.gen_e2_pt[0] = genelectrons[1].pt()
    out.gen_e2_eta[0] = genelectrons[1].eta()
    out.gen_e2_phi[0] = genelectrons[1].phi()
    out.gen_dr[0] = deltaR(genelectrons[0].eta(), genelectrons[0].phi(), genelectrons[1].eta(), genelectrons[1].phi())
    out.gen_mass[0] = (genelectrons[0].p4() + genelectrons[1].p4()).M()
    out.gen_b_pt[0] = bs[0].pt()
    out.gen_b_eta[0] = bs[0].eta()
    out.gen_b_phi[0] = bs[0].phi()

    out.ngenmuons[0] = len(genmuons)
    out.ngenelectrons[0] = len(genelectrons)

    #########################

    ev.getByLabel(label_mu, handle_mu)
    muons = handle_mu.product()
    L1_muons = []
    for jj in range(muons.size(0)):
        L1_muons.append(muons.at(0,jj))

    ev.getByLabel(label_e, handle_e)
    electrons = handle_e.product()
    L1_electrons = []
    for jj in range(electrons.size(0)):
        L1_electrons.append(electrons.at(0,jj))




    L1_muons_eta1p5 = sorted([mu for mu in L1_muons if mu.hwQual() >= 12 and abs(mu.eta()) < 1.5], key = lambda mu : mu.pt(), reverse = True)
    L1_muons_eta2p4 = sorted([mu for mu in L1_muons if mu.hwQual() >= 12 and abs(mu.eta()) < 2.4], key = lambda mu : mu.pt(), reverse = True)

    L1_electrons_eta1p0 = sorted([e for e in L1_electrons if abs(e.eta()) < 1.], key = lambda e : e.pt(), reverse = True)
    L1_electrons_eta1p5 = sorted([e for e in L1_electrons if abs(e.eta()) < 1.5], key = lambda e : e.pt(), reverse = True)
    L1_electrons_eta2p4 = sorted([e for e in L1_electrons if abs(e.eta()) < 2.4], key = lambda e : e.pt(), reverse = True)


    out.nmuons_eta1p5[0] = len(L1_muons_eta1p5)
    out.nmuons_eta2p4[0] = len(L1_muons_eta2p4)
    
    out.nelectrons_eta1p0[0] = len(L1_electrons_eta1p0)
    out.nelectrons_eta1p5[0] = len(L1_electrons_eta1p5)
    out.nelectrons_eta2p4[0] = len(L1_electrons_eta2p4)


            
###    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons)
###    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons)
####    bm_mu, maxdR_mu = bestMatch(genelectrons[1], L1_electrons)
###
###    if bm_e1!=None and maxdR_e1 < dRthr:
###        out.e1_pt[0] = bm_e1.pt()
###        out.e1_eta[0] = bm_e1.eta()
###        out.e1_phi[0] = bm_e1.phi()
###    else:
###        out.e1_pt[0] = -1
###        out.e1_eta[0] = -1
###        out.e1_phi[0] = -1
###        
###    if bm_e2!=None and maxdR_e2 < dRthr:
###        out.e2_pt[0] = bm_e2.pt()
###        out.e2_eta[0] = bm_e2.eta()
###        out.e2_phi[0] = bm_e2.phi()
###    else:
###        out.e2_pt[0] = -1
###        out.e2_eta[0] = -1
###        out.e2_phi[0] = -1



    for ii, pt in enumerate(ptrange):

        flag = False

        for gm in genmuons:

            bm_mu, maxdR_mu = bestMatchAtVtx(gm, L1_muons_eta1p5)

            if bm_mu!=None and maxdR_mu < dRthr and bm_mu.pt() >= pt:
        
                flag = True


        getattr(out, 'singleMu' + str(pt) + '_eta1p5')[0] = flag


    for ii, pt in enumerate(ptrange):
        flag = False
        for gm in genmuons:

            bm_mu, maxdR_mu = bestMatchAtVtx(gm, L1_muons_eta2p4)

            if bm_mu!=None and maxdR_mu < dRthr and bm_mu.pt() >= pt:
        
                flag = True


        getattr(out, 'singleMu' + str(pt) + '_eta2p4')[0] = flag

#        if pt==3:
#            out.singleMu3[0] = flag
#        elif pt==4:
#            out.singleMu4[0] = flag
#        elif pt==5:
#            out.singleMu5[0] = flag
#        elif pt==6:
#            out.singleMu6[0] = flag
#        elif pt==7:
#            out.singleMu7[0] = flag
#        elif pt==8:
#            out.singleMu8[0] = flag
#        elif pt==9:
#            out.singleMu9[0] = flag
#        elif pt==10:
#            out.singleMu10[0] = flag
#        else:
#            print 'Not expected !!!'

    # di-electron seed 

    L1_electrons_dynamic = copy.deepcopy(L1_electrons_eta1p0)
    

    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons_dynamic)

    
    if bm_e1!=None and maxdR_e1 < dRthr:
        L1_electrons_dynamic.remove(bm_e1)

    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons_dynamic)     


    if bm_e1!=None and maxdR_e1 < dRthr:
        out.e1_eta1p0_pt[0] = bm_e1.pt()
        out.e1_eta1p0_eta[0] = bm_e1.eta()
        out.e1_eta1p0_phi[0] = bm_e1.phi()
    else:
        out.e1_eta1p0_pt[0] = -1
        out.e1_eta1p0_eta[0] = -1
        out.e1_eta1p0_phi[0] = -1
        
    if bm_e2!=None and maxdR_e2 < dRthr:
        out.e2_eta1p0_pt[0] = bm_e2.pt()
        out.e2_eta1p0_eta[0] = bm_e2.eta()
        out.e2_eta1p0_phi[0] = bm_e2.phi()
    else:
        out.e2_eta1p0_pt[0] = -1
        out.e2_eta1p0_eta[0] = -1
        out.e2_eta1p0_phi[0] = -1


    if bm_e1!=None and bm_e2!=None:
        out.e1e2_eta1p0_dr[0] = deltaR(bm_e1.eta(), bm_e1.phi(), bm_e2.eta(), bm_e2.phi())
    else:
        out.e1e2_eta1p0_dr[0] = -1




    #################################




    L1_electrons_dynamic = copy.deepcopy(L1_electrons_eta1p5)
    

    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons_dynamic)

    
    if bm_e1!=None and maxdR_e1 < dRthr:
        L1_electrons_dynamic.remove(bm_e1)

    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons_dynamic)     


    if bm_e1!=None and maxdR_e1 < dRthr:
        out.e1_eta1p5_pt[0] = bm_e1.pt()
        out.e1_eta1p5_eta[0] = bm_e1.eta()
        out.e1_eta1p5_phi[0] = bm_e1.phi()
    else:
        out.e1_eta1p5_pt[0] = -1
        out.e1_eta1p5_eta[0] = -1
        out.e1_eta1p5_phi[0] = -1
        
    if bm_e2!=None and maxdR_e2 < dRthr:
        out.e2_eta1p5_pt[0] = bm_e2.pt()
        out.e2_eta1p5_eta[0] = bm_e2.eta()
        out.e2_eta1p5_phi[0] = bm_e2.phi()
    else:
        out.e2_eta1p5_pt[0] = -1
        out.e2_eta1p5_eta[0] = -1
        out.e2_eta1p5_phi[0] = -1


    if bm_e1!=None and bm_e2!=None:
        out.e1e2_eta1p5_dr[0] = deltaR(bm_e1.eta(), bm_e1.phi(), bm_e2.eta(), bm_e2.phi())
    else:
        out.e1e2_eta1p5_dr[0] = -1



    ################################################

    L1_electrons_dynamic = copy.deepcopy(L1_electrons_eta2p4)
    

    bm_e1, maxdR_e1 = bestMatch(genelectrons[0], L1_electrons_dynamic)

    
    if bm_e1!=None and maxdR_e1 < dRthr:
        L1_electrons_dynamic.remove(bm_e1)

    bm_e2, maxdR_e2 = bestMatch(genelectrons[1], L1_electrons_dynamic)     


    if bm_e1!=None and maxdR_e1 < dRthr:
        out.e1_eta2p4_pt[0] = bm_e1.pt()
        out.e1_eta2p4_eta[0] = bm_e1.eta()
        out.e1_eta2p4_phi[0] = bm_e1.phi()
    else:
        out.e1_eta2p4_pt[0] = -1
        out.e1_eta2p4_eta[0] = -1
        out.e1_eta2p4_phi[0] = -1
        
    if bm_e2!=None and maxdR_e2 < dRthr:
        out.e2_eta2p4_pt[0] = bm_e2.pt()
        out.e2_eta2p4_eta[0] = bm_e2.eta()
        out.e2_eta2p4_phi[0] = bm_e2.phi()
    else:
        out.e2_eta2p4_pt[0] = -1
        out.e2_eta2p4_eta[0] = -1
        out.e2_eta2p4_phi[0] = -1


    if bm_e1!=None and bm_e2!=None:
        out.e1e2_eta2p4_dr[0] = deltaR(bm_e1.eta(), bm_e1.phi(), bm_e2.eta(), bm_e2.phi())
    else:
        out.e1e2_eta2p4_dr[0] = -1







#    for ii, pt in enumerate(ptrange):
#
#        flag = False
#
#        if bm_e1!=None and bm_e2!=None and maxdR_e1 < dRthr and maxdR_e2 < dRthr and bm_e1.pt() >= pt and bm_e2.pt() >= pt and deltaR(bm_e1.eta(), bm_e1.phi(), bm_e2.eta(), bm_e2.phi()) < 1.:
#            flag = True
#
#        if pt==3:
#            out.doubleE3[0] = flag
#        elif pt==4:
#            out.doubleE4[0] = flag
#        elif pt==5:
#            out.doubleE5[0] = flag
#        elif pt==6:
#            out.doubleE6[0] = flag
#        elif pt==7:
#            out.doubleE7[0] = flag
#        elif pt==8:
#            out.doubleE8[0] = flag
#        elif pt==9:
#            out.doubleE9[0] = flag
#        elif pt==10:
#            out.doubleE10[0] = flag
#        else:
#            print 'Not expected !!!'

    out.tree.Fill()
    nevents += 1

print nevents, 'has been analyzed, while dropping', ndrop, 'events'
out.endJob()
