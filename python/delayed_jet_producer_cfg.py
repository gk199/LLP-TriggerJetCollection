# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --python_filename HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-AOD_2_cfg.py --eventcontent RECOSIM,AODSIM --datatier GEN-SIM-RECO,AODSIM --fileout file:/eos/cms/store/group/dpg_hcal/comm_hcal/gillian/LLP_Run3/112X_TDC74pt8/HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-AOD.root --conditions auto:phase1_2021_realistic --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:/eos/cms/store/group/dpg_hcal/comm_hcal/gillian/LLP_Run3/112X_TDC74pt8/HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-digi.root --era Run3 --no_exec --mc -n 2000
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
import FWCore.ParameterSet.VarParsing as VarParsing # ADDED
import FWCore.Utilities.FileUtils as FileUtils # ADDED

process = cms.Process('RAW2DIGI',Run3)

#from Configuration.Eras.Era_Run3_cff import Run3

#process = cms.Process('RECO',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.RecoSim_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('DelayedJetCollection.L1DelayedJet.DelayedL1Jet_cfi')
process.load('EventFilter.L1TXRawToDigi.caloLayer1Stage2Digis_cfi')
process.load('L1Trigger.L1TCaloLayer1.simCaloStage2Layer1Digis_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/eos/cms/store/group/dpg_hcal/comm_hcal/gillian/LLP_Run3/112X_TDC74pt8/HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-digi.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(1)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:50'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

process.LLPjet = cms.EDProducer('L1DelayedJet'
                                ,src = cms.InputTag('delayedJet')
)
# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:/eos/cms/store/group/dpg_hcal/comm_hcal/gillian/LLP_Run3/112X_TDC74pt8/HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-GEN-SIM-RECO_LLPjet_small.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,# cms.untracked.vstring("keep *_delayedJet_*"),
    splitLevel = cms.untracked.int32(0)
)

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
    fileName = cms.untracked.string('file:/eos/cms/store/group/dpg_hcal/comm_hcal/gillian/LLP_Run3/112X_TDC74pt8/HTo2LongLivedTo4b_MH-125_MFF-50_CTau-3000mm_TuneCP5_13TeV_pythia8_cff-AODSIM_LLPjet_small.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands#, cms.untracked.vstring("keep *_delayedJet_*")
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.recosim_step = cms.Path(process.recosim)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.p = cms.Path(process.caloStage2Digis * process.l1tCaloLayer1Digis * process.DelayedL1Jet) #process.LLPjet) # this is to include delayed jet collections, python config that calls the EDProducer

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.recosim_step,process.eventinterpretaion_step,process.endjob_step,process.RECOSIMoutput_step,process.AODSIMoutput_step,process.p)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Customisation of the process
# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulMCFromRAWSimHcalTP 

#call to customisation function L1TReEmulMCFromRAWSimHcalTP imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulMCFromRAWSimHcalTP(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
#from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAWsimHcalTP 

#call to customisation function L1TReEmulFromRAWsimHcalTP imported from L1Trigger.Configuration.customiseReEmul
#process = L1TReEmulFromRAWsimHcalTP(process)

# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAWEMU 
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleGEN

#call to customisation function L1NtupleRAWEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
process = L1NtupleRAWEMU(process)
process = L1NtupleGEN(process) 

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseSettings
from L1Trigger.Configuration.customiseSettings import L1TSettingsToCaloParams_2018_v1_3 

#call to customisation function L1TSettingsToCaloParams_2018_v1_3 imported from L1Trigger.Configuration.customiseSettings
process = L1TSettingsToCaloParams_2018_v1_3(process)

# End of customisation functions


# Customisation from command line
#process.load("SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff")

#process.simHcalTriggerPrimitiveDigis.numberOfFilterPresamplesHBQIE11 = 1
#process.simHcalTriggerPrimitiveDigis.numberOfFilterPresamplesHEQIE11 = 1
#process.simHcalTriggerPrimitiveDigis.weightsQIE11 = {
#    "ieta1" :  [-0.47, 1.0],
#    "ieta2" :  [-0.47, 1.0],
#    "ieta3" :  [-0.47, 1.0],
#    "ieta4" :  [-0.47, 1.0],
#    "ieta5" :  [-0.47, 1.0],
#    "ieta6" :  [-0.47, 1.0],
#    "ieta7" :  [-0.47, 1.0],
#    "ieta8" :  [-0.47, 1.0],
#    "ieta9" :  [-0.47, 1.0],
#    "ieta10" : [-0.47, 1.0],
#    "ieta11" : [-0.47, 1.0],
#    "ieta12" : [-0.47, 1.0],
#    "ieta13" : [-0.47, 1.0],
#    "ieta14" : [-0.47, 1.0],
#    "ieta15" : [-0.47, 1.0],
#    "ieta16" : [-0.47, 1.0],
#    "ieta17" : [-0.47, 1.0],
#    "ieta18" : [-0.47, 1.0],
#    "ieta19" : [-0.47, 1.0],
#    "ieta20" : [-0.47, 1.0],
#    "ieta21" : [-0.43, 1.0],
#    "ieta22" : [-0.43, 1.0],
#    "ieta23" : [-0.43, 1.0],
#    "ieta24" : [-0.43, 1.0],
#    "ieta25" : [-0.43, 1.0],
#    "ieta26" : [-0.43, 1.0],
#    "ieta27" : [-0.43, 1.0],
#    "ieta28" : [-0.43, 1.0]
#}

#process.HcalTPGCoderULUT.contain1TSHB = True
#process.HcalTPGCoderULUT.contain1TSHE = True

# Pick one of the pairs of lines below based on the intended scenario for running
#process.HcalTPGCoderULUT.containPhaseNSHB = 1.0 # For Run3 MC
#process.HcalTPGCoderULUT.containPhaseNSHE = 1.0 # For Run3 MC


#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion


