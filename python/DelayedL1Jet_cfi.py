import FWCore.ParameterSet.Config as cms

DelayedL1Jet = cms.EDProducer(
    'L1DelayedJet',
    hcalToken = cms.InputTag("simHcalTriggerPrimitiveDigis"),# "l1tCaloLayer1Digis"
    jetToken = cms.InputTag("caloStage2Digis")#,"Jet","RECO")
)
