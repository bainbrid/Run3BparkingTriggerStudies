import os, math, sys
import ROOT
import math
import numpy as np
from array import array
from ROOT import TFile, TTree, Double, TLorentzVector
from DataFormats.FWLite import Events, Handle
from files_BuToKee_v3 import files_v3
from files_inclusive import indices

################################################################################
#

files_dict = {}

# Exclusive samples, with tag-side muon selection (pT > 5 GeV, |eta| < 2.5)
prefix='root://cms-xrd-global.cern.ch/'
files_dict["incl"]=[ prefix+"{:s}".format(f) for f in files_v3 ][:1] # 1 file, ~25k events?

files_dict["incl"]=['root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18MiniAOD/BuToKee_Mufilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/MINIAODSIM/Custom_RK_BParking_for_RK_102X_upgrade2018_realistic_v15-v2/110000/76EF89AB-1EFF-2C43-BF66-6CA048A2F7B5.root']

# Fully inclusive w.r.t. tag-side muon
path='/eos/cms/store/group/phys_bphys/trigger/BparkingTriggerStudy_nomufilter/AOD_BparkingTriggerStudy_nomufilter_'
files_dict["incl"]=[ path+"{:.0f}.root".format(index) for index in indices ][:100] # 100 files, ~23.6k events?

# Select here
sample = "incl"
files = files_dict[sample]

################################################################################
#
def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res

def deltaR2( e1, p1, e2=None, p2=None):
    """Take either 4 arguments (eta,phi, eta,phi) or two objects that have 'eta', 'phi' methods)"""
    if (e2 == None and p2 == None):
        return deltaR2(e1.eta(),e1.phi(), p1.eta(), p1.phi())
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp

def deltaR( *args ):
    return math.sqrt( deltaR2(*args) )

################################################################################
#
root_dtype = {float:'D',int:'I',bool:'O','f':'D','i':'I','?':'O','b':'b','v':'D','s':'s'}
num_dtype = {'D':'f','I':'i','O':'?','b':'b'}

class TreeProducerCommon(object):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name, **kwargs):
        print('TreeProducerCommon is called for', name)
        self.name       = name
        # TREE
        self.outputfile = ROOT.TFile(name, 'RECREATE')
        self.tree       = ROOT.TTree('tree','tree')

    def addBranch(self, name, dtype='f', default=None):
        """Add branch with a given name, and create an array of the same name as address."""
        if hasattr(self,name):
            print("ERROR! TreeProducerCommon.addBranch: Branch of name '%s' already exists!"%(name))
            exit(1)
        if isinstance(dtype,str):
            if dtype.lower()=='f': # 'f' is only a 'float32', and 'F' is a 'complex64', which do not work for filling float branches
                dtype = float        # float is a 'float64' ('f8')
            elif dtype.lower()=='i': # 'i' is only a 'int32'
                dtype = int            # int is a 'int64' ('i8')
        setattr(self,name,np.zeros(1,dtype=dtype))
        self.tree.Branch(name, getattr(self,name), '%s/%s'%(name,root_dtype[dtype]))
        if default!=None:
          getattr(self,name)[0] = default
    
    def endJob(self):
        """Write and close files after the job ends."""
        self.outputfile.Write()
        self.outputfile.Close()
        
################################################################################
#
class TreeProducerGen(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducerGen is called for', name)
        super(TreeProducerGen, self).__init__(name,**kwargs)
        self.addBranch('gen_e1_pt','f')
        self.addBranch('gen_e1_eta','f')
        self.addBranch('gen_e1_phi','f')
        self.addBranch('gen_e2_pt','f')
        self.addBranch('gen_e2_eta','f')
        self.addBranch('gen_e2_phi','f')
        self.addBranch('gen_dr','f')
        self.addBranch('gen_mass','f')
        self.addBranch('gen_b_pt','f')
        self.addBranch('gen_b_eta','f')
        self.addBranch('gen_b_phi','f')
        self.addBranch('ngenmuons','i')
        self.addBranch('ngenelectrons','i')
        #self.addBranch('trigger','i')

    def finalDaughters(particle, daughters):
        '''Fills daughters with all the daughters of particle.
        Recursive function.'''
        if particle.numberOfDaughters() == 0:
            daughters.append(particle)
        else:
            foundDaughter = False
            for i in range( particle.numberOfDaughters() ):
                dau = particle.daughter(i)
                if dau.status() >= 1:
                    daughters = finalDaughters( dau, daughters )
                    foundDaughter = True
            if not foundDaughter:
                daughters.append(particle)
        return daughters

    def addBranches(self,branches,type='i'):
        for branch in branches: self.addBranch(branch,type)

################################################################################
#

print(files)
print 'Processing {:.0f} files...'.format(len(files))

events = Events(files)
nevent = int(events.size())
print 'Number of files processed: {:.0f}, total number of events processed: {:.0f}'.format(len(files),nevent)

handle = Handle('std::vector<reco::GenParticle>')
label = ("prunedGenParticles") if sample=="excl" else ("genParticles") if sample=="incl" else None
out = TreeProducerGen('ntuple.root')

## Trigger collections
#triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
#triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
#triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"
#
## Trigger info
#hlt_paths=[
#    "HLT_Mu7_IP4",
#    "HLT_Mu8_IP6",
#    "HLT_Mu8_IP5",
#    "HLT_Mu8_IP3",
#    "HLT_Mu8p5_IP3p5",
#    "HLT_Mu9_IP6",
#    "HLT_Mu9_IP5",
#    "HLT_Mu9_IP4",
#    "HLT_Mu10p5_IP3p5",
#    "HLT_Mu12_IP6"
#    ]
#
## Add branches
#hlt_paths = list(set(hlt_paths))
#out.addBranches(hlt_paths)
#
#trigger_indices=None
#trigger_debug=0

print "Starting event loop..."

nanalyzed = 0
ndropped = 0
for ievent,ev in enumerate(events):
    #if ievent > 1000 : break
    if ievent%100==0: print('{0:.1f}% processed'.format(Double(ievent)/Double(nevent)*100.))
    #print('{0:.0f} processed'.format(Double(ievent)))

#    # Get trigger collections
#    ev.getByLabel(triggerBitLabel, triggerBits)
#    ev.getByLabel(triggerObjectLabel, triggerObjects)
#    ev.getByLabel(triggerPrescaleLabel, triggerPrescales)
#
#    # Identify trigger indices (Assumes they don't change? So let's check every N events!)
#    if ievent%100000==0 or trigger_indices==None:
#        print "determine trigger indices..."
#        path_indices = []
#        trigger_indices = []
#        names = ev.object().triggerNames(triggerBits.product())
#        for iname in xrange(triggerBits.product().size()):
#            for ipath,path in enumerate(hlt_paths):
#                if path in names.triggerName(iname):
#                    trigger_indices.append(iname)
#                    path_indices.append(ipath)
#        trigger_indices = list(set(trigger_indices))
#        print "trigger_indices",trigger_indices
#        print "path_indices",path_indices
#        print "hlt_paths",hlt_paths
#
#    # Check if BParking trigger path fired
#    triggered_ = []
#    triggered = False
#    for idx,index in enumerate(trigger_indices):
#        if triggerBits.product().accept(index):
#            triggered = True
#            triggered_.append(hlt_paths[path_indices[idx]])
#            if trigger_debug>0:
#                prescale = triggerPrescales.product().getPrescaleForIndex(index)
#                print "BParking trigger FIRED with path",\
#                    "{:s} and index {:.0f} and prescale {:.0f} in event {:.0f}!".format(names.triggerName(index),
#                                                                                        index,
#                                                                                        prescale,
#                                                                                        ievent)
#
#    if trigger_debug>1 and triggered:
#        print "\n === BPARKING PATHS ==="
#        names = ev.object().triggerNames(triggerBits.product())
#        for index in xrange(triggerBits.product().size()):
#            for path in hlt_paths:
#                if path in names.triggerName(index) and triggerBits.product().accept(index):
#                    print "BParking trigger ",\
#                        names.triggerName(index),\
#                        ", index ",\
#                        index,\
#                        ", prescale ",\
#                        triggerPrescales.product().getPrescaleForIndex(index), ": ",\
#                        ("PASS" if triggerBits.product().accept(index) else "fail (or not run)") 
#
#    # Some trigger debug
#    if trigger_debug>2 :
#        # Print trigger debug info
#        print "\nEvent %d: run %6d, lumi %4d, event %12d" % (ievent,ev.eventAuxiliary().run(),
#                                                             ev.eventAuxiliary().luminosityBlock(),
#                                                             ev.eventAuxiliary().event())
#        print "\n === TRIGGER PATHS ==="
#        names = ev.object().triggerNames(triggerBits.product())
#        for i in xrange(triggerBits.product().size()):
#            print "Trigger ",\
#                names.triggerName(i),\
#                ", index ",\
#                i,\
#                ", prescale ",\
#                triggerPrescales.product().getPrescaleForIndex(i), ": ",\
#                ("PASS" if triggerBits.product().accept(i) else "fail (or not run)") 
#
#    if trigger_debug>3 :
#        print "\n === TRIGGER OBJECTS ==="
#        for j,to in enumerate(triggerObjects.product()):
#            to.unpackPathNames(names)
#            to.unpackFilterLabels(ev.object(),triggerBits.product())
#            print "Trigger object pt %6.2f eta %+5.3f phi %+5.3f  " % (to.pt(),to.eta(),to.phi())
#            print "   collection: ", to.collection()
#            print "   type ids: ", ", ".join([str(f) for f in to.filterIds()])
#            print "   filters: ", ", ".join([str(f) for f in to.filterLabels()])
#            pathslast = set(to.pathNames(True))
#            print "   paths:   ", ", ".join([("%s*" if f in pathslast else "%s")%f for f in to.pathNames()]) 

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

#    triggered_ = list(set(triggered_))
#    out.trigger[0] = triggered
#    for path in hlt_paths:
#        attr = getattr(out,path,None)
#        if attr is not None:
#            if path in triggered_: attr[0] = 1
#            if path not in triggered_: attr[0] = 0

    out.tree.Fill()
    nanalyzed += 1

print 'Number of events analyzed: {:.0f}, number of events dropped: {:.0f}'.format(nanalyzed,ndropped)
out.endJob()
