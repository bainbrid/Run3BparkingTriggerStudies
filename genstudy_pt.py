from ROOT import TFile, TTree, Double, TLorentzVector
from DataFormats.FWLite import Events, Handle
from common.deltar import deltaR
from TreeProducerGen import *

#files=['file:./root/MINIAOD.root']
path="root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18MiniAOD/BuToKee_MufilterPt6_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/MINIAODSIM/PUPoissonAve20_BParking_102X_upgrade2018_realistic_v15-v1/"
files=[
    path+'00000/01501E26-9276-7149-A74D-5E4B2E028DC8.root',
    path+"260000/00FD1710-09A4-9A45-B22B-6395B15DA05E.root",
    path+"260000/D368E158-9B9A-F645-A48E-772F29E729D8.root",
    path+"260000/B2A8EC54-1587-AD49-9C4F-C82C0648FADF.root",
    path+"260000/DEB8EE96-CB34-8C40-8C78-BF3F4DA3828E.root",
    path+"260000/0766236A-6FF9-5044-8FEB-2509F498CEF2.root",
    path+"260000/38630A2B-EC5A-2146-AB1C-C1C016A83537.root",
    path+"260000/72E77B37-BF53-D546-9A82-780AC8062350.root",
    path+"260000/86791084-34DA-BB4E-92E3-39FB45FDBA97.root",
    path+"260000/5E4DAFD3-D90F-5C4C-B6FC-2ED49E997014.root",
    path+"260000/F326012E-A5EA-E549-8A03-BA0867C1BD7F.root",
    path+"260000/4FBA2D0E-481B-854A-91DD-FD75DE6C4802.root",
    path+"260000/247806D2-A976-6B40-BB72-6D3A23B47DFC.root",
    path+"130000/2FF74584-E028-B042-8B14-0C1D4C46389B.root",
    path+"280000/C66696E9-DC61-6146-AEED-69B4BE9A10FE.root",
    path+"280000/25CEE19C-3881-7C4D-9BA2-6C5286DFE3F4.root",
    path+"280000/129D7AB9-CC04-014B-AB77-074A395337F3.root",
    path+"280000/1253B701-1703-EB4F-9DCF-DB31A2DF4BD2.root",
    path+"280000/1855AB46-1FB8-BD49-997D-3D5879C58106.root",
    path+"280000/522A856A-77BA-8941-9102-236E6B02E52F.root",
    ]

print 'Processing {:.0f} files...'.format(len(files))

events = Events(files)
nevent = int(events.size())
print 'Number of files processed: {:.0f}, total number of events processed: {:.0f}'.format(len(files),nevent)

handle = Handle('std::vector<reco::GenParticle>')
label = ("prunedGenParticles")
out = TreeProducerGen('root/genstudy_pt.root')

# Trigger collections
triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"

# Trigger info
#hlt_paths=["HLT_Mu7_IP4"]
#hlt_paths=["HLT_Mu12_IP6"]
hlt_paths=["HLT_Mu7_IP4","HLT_Mu8_IP6","HLT_Mu8_IP5","HLT_Mu8_IP3","HLT_Mu8p5_IP3p5","HLT_Mu9_IP6","HLT_Mu9_IP5","HLT_Mu9_IP4","HLT_Mu10p5_IP3p5","HLT_Mu12_IP6"]

trigger_indices=None
trigger_debug=0

print "Starting event loop..."

nanalyzed = 0
ndropped = 0
for ievent,ev in enumerate(events):
    #if ievent > 10 : continue
    if ievent%1000==0: print('{0:.f}% processed'.format(Double(ievent)/Double(nevent)*100.))
    #print('{0:.0f} processed'.format(Double(ievent)))

    # Get trigger collections
    ev.getByLabel(triggerBitLabel, triggerBits)
    ev.getByLabel(triggerObjectLabel, triggerObjects)
    ev.getByLabel(triggerPrescaleLabel, triggerPrescales)

    # Identify trigger indices (Assumes they don't change? So let's check every N events!)
    if ievent%100000==0 or trigger_indices==None:
        print "determine trigger indices..."
        trigger_indices = []
        names = ev.object().triggerNames(triggerBits.product())
        for iname in xrange(triggerBits.product().size()):
            for path in hlt_paths:
                if path in names.triggerName(iname):
                    trigger_indices.append(iname)
        trigger_indices = list(set(trigger_indices))
        print "trigger_indices",trigger_indices

    # Check if BParking trigger path fired
    triggered = False
    for index in trigger_indices:
        if triggerBits.product().accept(index):
            triggered = True
            if trigger_debug>0:
                prescale = triggerPrescales.product().getPrescaleForIndex(index)
                print "BParking trigger FIRED with index",\
                    "{:.0f} and prescale {:.0f} in event {:.0f}!".format(index,prescale,ievent)
            break

    if trigger_debug>1 and triggered:
        print "\n === BPARKING PATHS ==="
        names = ev.object().triggerNames(triggerBits.product())
        for index in xrange(triggerBits.product().size()):
            for path in hlt_paths:
                if path in names.triggerName(index) and triggerBits.product().accept(index):
                    print "BParking trigger ",\
                        names.triggerName(index),\
                        ", index ",\
                        index,\
                        ", prescale ",\
                        triggerPrescales.product().getPrescaleForIndex(index), ": ",\
                        ("PASS" if triggerBits.product().accept(index) else "fail (or not run)") 

    # Some trigger debug
    if trigger_debug>2 :
        # Print trigger debug info
        print "\nEvent %d: run %6d, lumi %4d, event %12d" % (ievent,ev.eventAuxiliary().run(),
                                                             ev.eventAuxiliary().luminosityBlock(),
                                                             ev.eventAuxiliary().event())
        print "\n === TRIGGER PATHS ==="
        names = ev.object().triggerNames(triggerBits.product())
        for i in xrange(triggerBits.product().size()):
            print "Trigger ",\
                names.triggerName(i),\
                ", index ",\
                i,\
                ", prescale ",\
                triggerPrescales.product().getPrescaleForIndex(i), ": ",\
                ("PASS" if triggerBits.product().accept(i) else "fail (or not run)") 
        print "\n === TRIGGER OBJECTS ==="
        for j,to in enumerate(triggerObjects.product()):
            to.unpackPathNames(names)
            #print([names.triggerName(i) for i in range(len(names))])
            #to.unpackFilterLabels([str(names.triggerName(i)) for i in range(len(names))])
            to.unpackFilterLabels(ev.object(),triggerBits.product())
            print "Trigger object pt %6.2f eta %+5.3f phi %+5.3f  " % (to.pt(),to.eta(),to.phi())
            print "   collection: ", to.collection()
            print "   type ids: ", ", ".join([str(f) for f in to.filterIds()])
            print "   filters: ", ", ".join([str(f) for f in to.filterLabels()])
            pathslast = set(to.pathNames(True))
            print "   paths:   ", ", ".join([("%s*" if f in pathslast else "%s")%f for f in to.pathNames()]) 

    # Get GEN info
    ev.getByLabel(label, handle)
    gps = handle.product()
    gen_bs = [p for p in gps if abs(p.pdgId())==521] 
    genmuons = [p for p in gps if abs(p.pdgId()) == 13 and p.status()==1]

    if False : 
        print '-'*80
        for gen in gen_bs:
            print gen.pdgId(), 'ndaughters=', gen.numberOfDaughters()
            for ii in range(gen.numberOfDaughters()):
                print '\t d:', gen.daughter(ii).pdgId()
            print gen.pdgId(), 'nmothers=', gen.numberOfMothers()
            for ii in range(gen.numberOfMothers()):
                print '\t m:', gen.mother(ii).pdgId()

    bs = []
    genelectrons = None
    for p in gen_bs:
        daughters = [p.daughter(ii).pdgId() for ii in range(p.numberOfDaughters())]
        if not ((321 in daughters and 11 in daughters and -11 in daughters) or (-321 in daughters and 11 in daughters and -11 in daughters)): continue
        genelectrons = [p.daughter(ii) for ii in range(p.numberOfDaughters()) if abs(p.daughter(ii).pdgId())==11]
        bs.append(p)
    if len(bs)!=1: 
        ndropped += 1
        continue

    genelectrons = sorted(genelectrons, key = lambda e : e.pt(), reverse = True )
    genmuons = sorted(genmuons, key = lambda mu : mu.pt(), reverse = True )

    #print len(genelectrons)

    out.gen_e1_pt[0] = genelectrons[0].pt()
    out.gen_e1_eta[0] = genelectrons[0].eta()
    out.gen_e2_pt[0] = genelectrons[1].pt()
    out.gen_e2_eta[0] = genelectrons[1].eta()
    out.gen_dr[0] = deltaR(genelectrons[0].eta(), genelectrons[0].phi(), genelectrons[1].eta(), genelectrons[1].phi())
    out.gen_mass[0] = (genelectrons[0].p4() + genelectrons[1].p4()).M()
    out.gen_b_pt[0] = bs[0].pt()
    out.gen_b_eta[0] = bs[0].eta()
    out.gen_b_phi[0] = bs[0].phi()

    out.ngenmuons[0] = len(genmuons)
    out.ngenelectrons[0] = len(genelectrons)

    out.trigger[0] = triggered

    out.tree.Fill()
    nanalyzed += 1

print 'Number of events analyzed: {:.0f}, number of events dropped: {:.0f}'.format(nanalyzed,ndropped)
out.endJob()
