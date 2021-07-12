# Delayed Jet Collection
Work to add a delayed jet collection to AOD file, for use in the L1 and HLT delayed jet trigger studies. A EDProducer is made to add the delayed jet collections (delayed, timing, depth) based on the TimingBit (6 bit in this case, where 2 are reserved for muon bits and 4 are used for timing/depth). 

This is done in a CMSSW area with the [feature bit implementation](https://github.com/gk199/cmssw/tree/LLPTimingBitAlgo/SimCalorimetry/HcalTrigPrimAlgos). Four files are critical:
```
SimCalorimetry/HcalTrigPrimAlgos/interface/HcalFinegrainBit.h
SimCalorimetry/HcalTrigPrimAlgos/interface/HcalTriggerPrimitiveAlgo.h
SimCalorimetry/HcalTrigPrimAlgos/src/ HcalFinegrainBit.cc
SimCalorimetry/HcalTrigPrimAlgos/src/HcalTriggerPrimitiveAlgo.cc
```
In the feature bit implementation, 3 bits are used for timing and 1 for depth.

## AOD processing
Steps for AOD processing are taken from here: [MC processing git repo](https://github.com/gk199/MonteCarlo_PrivateProduction/tree/master/LLP_TDC). The EDProducer [twiki instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEDMTutorialProducer#RuN) were followed as well, adding the `process.LLPjet` lines, statement to `keep *_DelayedL1Jet_*_*`, `process.DelayedL1Jet` in `process.p` to be included in `process.schedule`, and the EDProducer L1DelayedJet that creates the DelayedL1Jet collection. 

## Running
```
cmsenv
scram b -j 8
python python/delayed_jet_producer_cfg.py
cmsRun python/delayed_jet_producer_cfg.py
```
The collection is defined in the cfi file and called DelayedL1Jet, and should show up in the output root files as:
```
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "DelayedJet"  "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_Central_RAW2DIGI
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "DepthJet"    "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_DepthJet_RAW2DIGI
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "TimingJet"   "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_TimingJet_RAW2DIGI
```
which is the type, module, label, process, and full name. This can be seen from `edmDumpEventContent --all --regex DelayedL1Jet <name>.root`. Info on edmDumpEventContent is in [this twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEdmInfoOnDataFile) for reference.

## Location on lxplus
This is stored at `/afs/cern.ch/work/g/gkopp/HCAL_Trigger/L1Ntuples/HCAL_TP_TimingBitEmulator/CMSSW_11_2_0/src/DelayedJetCollection/L1DelayedJet`