import FWCore.ParameterSet.Config as cms

DelayedL1Jet = cms.EDProducer(
    'L1DelayedJet',
#    hcalToken = cms.untracked.InputTag("emulTPDigis"),
    hcalToken = cms.InputTag("simHcalTriggerPrimitiveDigis"),# "l1tCaloLayer1Digis"
    jetToken = cms.InputTag("simCaloStage2Digis")#,"Jet","RECO")
)
