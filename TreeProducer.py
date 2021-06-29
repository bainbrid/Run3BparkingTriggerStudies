import ROOT
import math 
import numpy as np
from TreeProducerCommon import *

ptrange = np.arange(3, 15, 1).tolist() 

class TreeProducer(TreeProducerCommon):
    """Class to create a custom output file & tree; as well as create and contain branches."""

    def __init__(self, name,  **kwargs):
        print('TreeProducer is called for', name)
        super(TreeProducer, self).__init__(name,**kwargs)


        self.addBranch('nmuons_eta1p5',                  'i')
        self.addBranch('nmuons_eta2p4',                  'i')
        self.addBranch('nelectrons_eta1p0',                  'i')
        self.addBranch('nelectrons_eta1p5',                  'i')
        self.addBranch('nelectrons_eta2p4',                  'i')

        self.addBranch('mu1_eta1p5_pt',                  'f')
        self.addBranch('mu1_eta1p5_eta',                  'f')
        self.addBranch('mu1_eta1p5_phi',                  'f')

        self.addBranch('mu1_eta2p4_pt',                  'f')
        self.addBranch('mu1_eta2p4_eta',                  'f')
        self.addBranch('mu1_eta2p4_phi',                  'f')

        self.addBranch('e1_eta1p0_pt',                  'f')
        self.addBranch('e1_eta1p0_eta',                  'f')
        self.addBranch('e1_eta1p0_phi',                  'f')
        self.addBranch('e2_eta1p0_pt',                  'f')
        self.addBranch('e2_eta1p0_eta',                  'f')
        self.addBranch('e2_eta1p0_phi',                  'f')

        self.addBranch('e1_eta1p5_pt',                  'f')
        self.addBranch('e1_eta1p5_eta',                  'f')
        self.addBranch('e1_eta1p5_phi',                  'f')
        self.addBranch('e2_eta1p5_pt',                  'f')
        self.addBranch('e2_eta1p5_eta',                  'f')
        self.addBranch('e2_eta1p5_phi',                  'f')

        self.addBranch('e1_eta2p4_pt',                  'f')
        self.addBranch('e1_eta2p4_eta',                  'f')
        self.addBranch('e1_eta2p4_phi',                  'f')
        self.addBranch('e2_eta2p4_pt',                  'f')
        self.addBranch('e2_eta2p4_eta',                  'f')
        self.addBranch('e2_eta2p4_phi',                  'f')

        self.addBranch('instL',                  'f')
        self.addBranch('npu',                  'f')

        for pt in ptrange:
            self.addBranch('doubleE' + str(pt) + '_eta1p0',                  '?')
            self.addBranch('dyn_doubleE' + str(pt) + '_eta1p0' ,                  '?')
            self.addBranch('doubleE' + str(pt) + '_eta1p5',                  '?')


        for pt1 in ptrange:
            for pt2 in ptrange:

                if pt2 >= pt1: continue

                self.addBranch('E' + str(pt1) + '_eta1p0_E' + str(pt2) + '_eta1p0',                  '?')
