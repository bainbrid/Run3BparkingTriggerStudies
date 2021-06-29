import ROOT
import math 
import numpy as np
from TreeProducerCommon import *

ptrange = np.arange(3, 14, 1).tolist() 

class TreeProducerGen(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducerGen is called for', name)
        super(TreeProducerGen, self).__init__(name,**kwargs)


        self.addBranch('nmuons_eta1p5',                  'i')
        self.addBranch('nmuons_eta2p4',                  'i')
        
        self.addBranch('nelectrons_eta1p0',                  'i')
        self.addBranch('nelectrons_eta1p5',                  'i')
        self.addBranch('nelectrons_eta2p4',                  'i')

#        self.addBranch('mu1_pt',                  'f')
#        self.addBranch('mu1_eta',                  'f')

#        self.addBranch('e1_pt',                  'f')
#        self.addBranch('e1_eta',                  'f')
#        self.addBranch('e1_phi',                  'f')
#        self.addBranch('e2_pt',                  'f')
#        self.addBranch('e2_eta',                  'f')
#        self.addBranch('e2_phi',                  'f')

        for eta in ['eta1p0', 'eta1p5', 'eta2p4']:
            self.addBranch('e1_' + eta + '_pt',                  'f')
            self.addBranch('e1_' + eta + '_eta',                  'f')
            self.addBranch('e1_' + eta + '_phi',                  'f')
            self.addBranch('e2_' + eta + '_pt',                  'f')
            self.addBranch('e2_' + eta + '_eta',                  'f')
            self.addBranch('e2_' + eta + '_phi',                  'f')
            self.addBranch('e1e2_' + eta + '_dr',                  'f')


#        self.addBranch('e1_eta1p5_pt',                  'f')
#        self.addBranch('e1_eta1p5_eta',                  'f')
#        self.addBranch('e1_eta1p5_phi',                  'f')
#        self.addBranch('e2_eta1p5_pt',                  'f')
#        self.addBranch('e2_eta1p5_eta',                  'f')
#        self.addBranch('e2_eta1p5_phi',                  'f')
#
#        self.addBranch('e1e2_eta1p5_dr',                  'f')



        for pt in ptrange:
#            self.addBranch('doubleE' + str(pt),                  '?')
            self.addBranch('singleMu' + str(pt) + '_eta1p5',                  '?')
            self.addBranch('singleMu' + str(pt) + '_eta2p4',                  '?')
            

#        self.addBranch('dr',                  'f')
#        self.addBranch('ismatch',                  'i')



        self.addBranch('gen_e1_pt',                  'f')
        self.addBranch('gen_e1_eta',                  'f')
        self.addBranch('gen_e1_phi',                  'f')
        self.addBranch('gen_e2_pt',                  'f')
        self.addBranch('gen_e2_eta',                  'f')
        self.addBranch('gen_e2_phi',                  'f')
        self.addBranch('gen_dr',                  'f')
        self.addBranch('gen_mass',                  'f')

        self.addBranch('gen_b_pt',                  'f')
        self.addBranch('gen_b_eta',                  'f')
        self.addBranch('gen_b_phi',                  'f')

        self.addBranch('ngenmuons',                  'i')
        self.addBranch('ngenelectrons',                  'i')


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
