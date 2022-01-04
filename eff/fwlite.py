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

print "Starting event loop..."

nanalyzed = 0
ndropped = 0
for ievent,ev in enumerate(events):
    #if ievent > 1000 : break
    if ievent%100==0: print('{0:.1f}% processed'.format(Double(ievent)/Double(nevent)*100.))
    #print('{0:.0f} processed'.format(Double(ievent)))

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

    out.tree.Fill()
    nanalyzed += 1

print 'Number of events analyzed: {:.0f}, number of events dropped: {:.0f}'.format(nanalyzed,ndropped)
out.endJob()
