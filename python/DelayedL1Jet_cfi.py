import FWCore.ParameterSet.Config as cms

DelayedL1Jet = cms.EDProducer(
    'L1DelayedJet',
    hcalToken = cms.InputTag("HcalUpgradeTriggerPrimitiveDigi"), #delayedJet"), #hcalDigis"), #l1tCaloLayer1Digis"), # simHcalTriggerPrimitiveDigis
    jetToken = cms.InputTag("l1tCaloLayer1Digis")
)
