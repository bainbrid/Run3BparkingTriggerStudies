from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from array import array
import argparse
import sys
import ROOT
import json
import re
from DataFormats.FWLite import Events, Handle
from Analysis.HLTAnalyserPy.EvtData import EvtData, EvtHandles,phaseII_products, add_product,get_objs

import Analysis.HLTAnalyserPy.CoreTools as CoreTools
import Analysis.HLTAnalyserPy.GenTools as GenTools
import Analysis.HLTAnalyserPy.HistTools as HistTools
import Analysis.HLTAnalyserPy.TrigTools as TrigTools
import Analysis.HLTAnalyserPy.L1Tools as L1Tools
from Analysis.HLTAnalyserPy.CoreTools import UnaryFunc
from Analysis.HLTAnalyserPy.NtupTools import TreeVar
from Analysis.HLTAnalyserPy.EvtWeights import EvtWeights

from ROOT import Double


from functools import partial
import itertools

import numpy as num

#    pudata[runnr]
#pudata = None

#with open("pileup_latest.txt") as f:
#    pudata = json.load(f)

gjson = None

with open("/work/ytakahas/work/Trigger/CMSSW_11_1_0/src/Analysis/HLTAnalyserPy/test/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt") as f:
    gjson = json.load(f)
        


class L1Tree:
    def __init__(self,tree_name,evtdata):   
        self.tree = ROOT.TTree(tree_name,'')
        self.evtdata = evtdata
        self.initialised = False
    def _init_tree(self):
        self.evtvars = [
            TreeVar(self.tree,"runnr/i",UnaryFunc("eventAuxiliary().run()")),
            TreeVar(self.tree,"lumiSec/i",UnaryFunc("eventAuxiliary().luminosityBlock()")),
            TreeVar(self.tree,"eventnr/i",UnaryFunc("eventAuxiliary().event()")),        
        ]

        setattr(self, 'instL', num.zeros(1, dtype=float))
        setattr(self, 'npu', num.zeros(1, dtype=float))
        self.tree.Branch('instL', getattr(self, 'instL'), 'instL/D')
        self.tree.Branch('npu', getattr(self, 'npu'), 'npu/D')



 
#        scales_params = L1Tools.make_egscale_dict()
        l1_vars_names = {
            'pt/F' : UnaryFunc("pt()"),
            'eta/F' : UnaryFunc("eta()"),
            'phi/F' : UnaryFunc("phi()"),
            'hwQual/F' : UnaryFunc("hwQual()"),          
            }
        max_l1egs = 2000
        max_l1mus = 2000
        nregs_name = "nrEGs"
        nrmus_name = "nrMuons"
        self.l1eg_nr = TreeVar(self.tree,nregs_name+"/i",UnaryFunc(partial(len)))
        self.l1eg_vars = []
        for name,func in l1_vars_names.iteritems():
            self.l1eg_vars.append(TreeVar(self.tree,"l1eg_"+name,func,max_l1egs,nregs_name)) 

        self.l1mu_nr = TreeVar(self.tree,nrmus_name+"/i",UnaryFunc(partial(len)))
        self.l1mu_vars = []  
        for name,func in l1_vars_names.iteritems():
            self.l1mu_vars.append(TreeVar(self.tree,"l1mu_"+name,func,max_l1mus,nrmus_name))   
       
        self.initialised = True

    def fill(self):
        if not self.initialised:
            self._init_tree()

        for var_ in self.evtvars:
            var_.fill(self.evtdata.event.object())

#        for var_ in self.aux:
#        print  (self.evtdata.event.object().eventAuxiliary().run(), pudata[str(self.evtdata.event.object().eventAuxiliary().run())][2])
        _runnum = str(self.evtdata.event.object().eventAuxiliary().run())
        _ls = str(self.evtdata.event.object().eventAuxiliary().luminosityBlock())


        flag_gjson = False

        if gjson.has_key(_runnum):
            
#            print('runnum found!!!', _runnum, _ls, gjson[_runnum])

            for lrange in gjson[_runnum]:

#                print('\t', lrange, min(lrange), max(lrange))

                if int(_ls) > min(lrange) and int(_ls) < max(lrange):
                    flag_gjson = True
                    break



#        print('golden json', flag_gjson)

        if flag_gjson and rundict.has_key(_runnum) and rundict[_runnum].has_key(_ls):
#            print('test', rundict[_runnum][_ls])

            self.instL[0] = rundict[_runnum][_ls]['instL']
            self.npu[0] = rundict[_runnum][_ls]['npu']
        else:
            self.instL[0] = -1
            self.npu[0] = -1


            

        l1egs_allbx  = self.evtdata.get("egamma")
        l1egs = [l1egs_allbx.at(0,egnr) for egnr in range(0,l1egs_allbx.size(0))]
        self.l1eg_nr.fill(l1egs)
        for objnr,l1eg_obj in enumerate(l1egs):
            for var_ in self.l1eg_vars:
                var_.fill(l1eg_obj,objnr)

        l1mus_allbx  = self.evtdata.get("muon")
        l1mus = [l1mus_allbx.at(0,munr) for munr in range(0,l1mus_allbx.size(0))]
        self.l1mu_nr.fill(l1mus)
        for objnr,l1mu_obj in enumerate(l1mus):
            for var_ in self.l1mu_vars:
                var_.fill(l1mu_obj,objnr)

        self.tree.Fill()

if __name__ == "__main__":
    
    CoreTools.load_fwlitelibs()


    file2read = '/work/ytakahas/work/Trigger/CMSSW_11_1_0/src/Analysis/HLTAnalyserPy/test/LumiData_2018_20200401.csv'
    
    rundict = {}

    run_save = None

    llist = {}

    for line in open(file2read):

        if line.find('STABLE BEAMS')==-1: continue

        line = line.rstrip().split(',')

        run = line[0].split(':')[0]
        ls = line[1].split(':')[0]
        ls_end = line[1].split(':')[1]
        _instL = Double(line[5])*0.0001
        _npu = Double(line[7])


#        if ls!=ls_end: 
#            print(ls, '!=', ls_end, 'detected ... continue')
#            continue

        
        if run_save!=None and run != run_save:
            rundict[run_save] = llist
            llist = {}

        if ls==ls_end: 
            llist[ls] = {'instL':_instL, 'npu':_npu}

        run_save = line[0].split(':')[0]
            


#    print(rundict)



        


        
#        327564:7492,225:225,12/02/18 16:07:37,STABLE BEAMS,6370,0.001585640,0.001554334,0.0,HFOC
        
#        print(line)



    parser = argparse.ArgumentParser(description='example e/gamma HLT analyser')
    parser.add_argument('in_filenames',nargs="+",help='input filename')
    parser.add_argument('--prefix','-p',default='file:',help='file prefix')
    parser.add_argument('--out','-o',default="output.root",help='output filename')
    args = parser.parse_args()
    std_products = []
#    add_product(std_products,"algblk","BXVector<GlobalAlgBlk>","hltGtStage2Digis")
#    add_product(std_products,"extblk","BXVector<GlobalExtBlk>","hltGtStage2Digis")
    add_product(std_products,"egamma","BXVector<l1t::EGamma>","hltGtStage2Digis:EGamma")
#    add_product(std_products,"etsum","BXVector<l1t::EtSum>","hltGtStage2Digis:EtSum")
#    add_product(std_products,"jet","BXVector<l1t::Jet>","hltGtStage2Digis:Jet")
    add_product(std_products,"muon","BXVector<l1t::Muon>","hltGtStage2Digis:Muon")
#    add_product(std_products,"tau","BXVector<l1t::Tau>","hltGtStage2Digis:Tau")
    add_product(std_products,"trig_res","edm::TriggerResults","TriggerResults")

    evtdata = EvtData(std_products,verbose=True)
    
    events = Events(CoreTools.get_filenames(args.in_filenames,args.prefix))
    nrevents = events.size()
    print("number of events",nrevents)
    trig_res = TrigTools.TrigResults(["DST_ZeroBias_v"])
    out_file = ROOT.TFile.Open(args.out,"RECREATE")
    tree = L1Tree("l1Tree",evtdata)

    idx = 0 

    for eventnr,event in enumerate(events):
        if eventnr%50000==0:
#        if eventnr==100:
            print("{}/{}".format(eventnr,nrevents))
#            break
    
        evtdata.get_handles(event)
        trig_res.fill(evtdata)
        if trig_res.result("DST_ZeroBias_v"):
            tree.fill()

        else:
            idx += 1

    out_file.Write()
        

    print(idx, 'rejected out of ', eventnr)
