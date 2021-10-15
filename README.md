# Delayed Jet Collection
Work to add a delayed jet collection to AOD file, for use in the L1 and HLT delayed jet trigger studies. A EDProducer is made to add the delayed jet collections (delayed, timing, depth) based on the TimingBit (6 bit in this case, where 2 are reserved for muon bits and 4 are used for timing/depth). 

This is done in a CMSSW area with the [feature bit implementation](https://github.com/gk199/cmssw/tree/LLPTimingBitAlgo/SimCalorimetry/HcalTrigPrimAlgos). Four files are critical:
```
SimCalorimetry/HcalTrigPrimAlgos/interface/HcalFinegrainBit.h
SimCalorimetry/HcalTrigPrimAlgos/interface/HcalTriggerPrimitiveAlgo.h
SimCalorimetry/HcalTrigPrimAlgos/src/HcalFinegrainBit.cc
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
Running python before cmsRun helps to understand if any issues that arise are config loading problems, or collection access problems.

The collection is defined in the cfi file and called DelayedL1Jet, and should show up in the output root files as:
```
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "DelayedJet"  "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_Central_RAW2DIGI
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "DepthJet"    "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_DepthJet_RAW2DIGI
vector<l1extra::L1JetParticle>      "DelayedL1Jet"   "TimingJet"   "RAW2DIGI"        l1extraL1JetParticles_DelayedL1Jet_TimingJet_RAW2DIGI
```
which is the type, module, label, process, and full name. This can be seen from `edmDumpEventContent --all --regex DelayedL1Jet <name>.root`. Info on edmDumpEventContent is in [this twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEdmInfoOnDataFile) for reference.

Delayed jet is intended to be filled if either the timing or depth flag is passed; Depth jet is intended to be filled only if the depth / amplitude based flag is passed; and Timing jet is intended to be filled only if the delayed timing based flag is passed. 

## Location on lxplus
This is stored at `/afs/cern.ch/work/g/gkopp/HCAL_Trigger/L1Ntuples/HCAL_TP_TimingBitEmulator/CMSSW_11_2_0/src/DelayedJetCollection/L1DelayedJet`

## Useful files to compare with
An example of handling the TP digi collection (Long): in other places it was [tagged like this](https://github.com/cms-sw/cmssw/blob/master/DQM/HcalTasks/python/TPTask.py#L23), and [consumed here](https://github.com/cms-sw/cmssw/blob/master/DQM/HcalTasks/plugins/TPTask.cc#L15). emutpdigi is [unpacked here](https://github.com/cms-sw/cmssw/blob/master/DQM/Integration/python/clients/hcal_dqm_sourceclient-live_cfg.py#L223). This would corespond to the following places in my files: [tagging collection](https://github.com/gk199/LLP-TriggerJetCollection/blob/main/python/DelayedL1Jet_cfi.py#L5) change from simHcalTriggerPrimitiveDigis to emulTPDigis, [consumed](https://github.com/gk199/LLP-TriggerJetCollection/blob/main/plugins/L1DelayedJet.cc#L124) looks similar already, and [unpacked](https://github.com/gk199/LLP-TriggerJetCollection/blob/main/python/delayed_jet_producer_cfg.py#L133) would add *process.emulTPDigis along with adding the definition of that [process](https://github.com/cms-sw/cmssw/blob/master/DQM/Integration/python/clients/hcal_dqm_sourceclient-live_cfg.py#L97-L109). This gave an error:
```
AttributeError: 'Process' object has no attribute 'simHcalTriggerPrimitiveDigis'
```

Resources to starting an EDProducer (from Pallabi): [EDM Tutorial Producer](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEDMTutorialProducer#BaSic). When running the "analysis" config file, call the EDProducer inside process, after the digi step (such as `process.p = cms.Path(process.l1tCaloLayer1Digis*process.simCaloStage2Layer1Digis*process.uct2016EmulatorDigis*process.l1NtupleProducer)` where `uct2016EmulatorDigis` is the EDProducer (the name of the python config that calls the EDProducer, for example [here](https://github.com/isobelojalvo/L1TCaloSummary/blob/master/python/uct2016EmulatorDigis_cfi.py#L3)).

Suggestions to try while debugging (basically a log of work done):
process.LLPjet can be included inside process.schedule  

The EDProducer needs a corresponding cfi file, similar to [here](https://github.com/pallabidas/cmssw/blob/l1t-integration-test-17May/L1Trigger/L1TCaloLayer1/python/simCaloStage2Layer1Digis_cfi.py), in which modules are called. This cfi must be loaded like: ` process.load('L1Trigger.L1TCaloLayer1.simCaloStage2Layer1Digis_cfi')` and then added to the path, and finally schedule. 

A useful comparison is the L1 menu config [mc.py](https://github.com/cms-l1-dpg/L1MenuTools/blob/master/L1Ntuples/mc.py), particularly L22, L113, L117, L123-185. I had to comment out lines L145-L185 to avoid errors though. L8-L12 may also be needed.

In `process.p`, the DelayedL1Jet should be listed last. Errors may come up if a module is missing (such as `process.load('EventFilter.L1TXRawToDigi.caloLayer1Stage2Digis_cfi')` or `process.load('L1Trigger.L1TCaloLayer1.simCaloStage2Layer1Digis_cfi')`. But there are two options: l1tCaloLayer1Digis or SimDigis (the standard). I proceeded with simDigis.

The collections that are expected to be needed are for hcalToken: `simHcalTriggerPrimitiveDigis` and for jetToken: `simCaloStage2Digis`. CaloStage2 has a few categories, so "Jet" must be specified. 

`L1TReEmulFromRAWsimHcalTP` is likely needed since the digi collection needs to be re-emulated from RAW data (it isn't stored by default). The collections are created when running the config file, they are not in the root file. The digi collection tag is a sim digi that mc.py customization function produces.

HcalTriggerPrimitiveDigi is a TPG collection, and is needed to access the fine grain bits. Follow [mc.py](https://github.com/cms-l1-dpg/L1MenuTools/blob/master/L1Ntuples/mc.py) for simHcalTriggerPrimitiveDigis.

The collection name is the one defined in the cfi file [done here]( https://github.com/gk199/LLP-TriggerJetCollection/blob/main/python/DelayedL1Jet_cfi.py#L3), as DelayedL1Jet (analagous to the uct2016EmulatorDigis from above).