# Delayed Jet Collection
Work to add a delayed jet collection to AOD file, for use in the L1 and HLT delayed jet trigger studies. A EDProducer is made to add the delayed jet collections (delayed, timing, depth) based on the TimingBit (6 bit in this case). 

This is done in a CMSSW area with the timing bit implementation, using HcalUpgradeTriggerPrimitiveSample / HcalUpgradeTriggerPrimitiveDigi. This relies on files: [upgrade git commit](https://github.com/gk199/cmssw/commit/21f40d96995033f3e2337ebebd930df4744e037b) with the [timing bit implementation](https://github.com/gk199/cmssw/commit/d6ecac888e2197d19837e69887c36788fca52ec5) that sets 5 bits for timing, and 1 for depth. This is the initial debugging and testing implementation, but will be altered in the final one (3 bits for timing, and no HcalUpgrade will be used).

## AOD processing
Steps for AOD processing are taken from here: [MC processing git repo](https://github.com/gk199/MonteCarlo_PrivateProduction/tree/master/LLP_TDC). The EDProducer [twiki instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookEDMTutorialProducer#RuN) were followed as well, adding the `process.LLPjet` lines (2 of them). 

## Location on lxplus
This is stored at `/afs/cern.ch/work/g/gkopp/HCAL_Trigger/L1Ntuples/HCAL_TP_TimingBitEmulator/CMSSW_11_2_0/src/DelayedJetCollection/L1DelayedJet`