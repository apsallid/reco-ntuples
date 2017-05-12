import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("Demo")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoLocalCalo.HGCalRecProducers.HGCalLocalRecoSequence_cff')

from FastSimulation.Event.ParticleFilter_cfi import *

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_9_1_0_pre1/RelValTTbar_14TeV/GEN-SIM-RECO/PU25ns_90X_upgrade2023_realistic_v9_D4TPU200r3-v1/00000/02E3478F-3D22-E711-80C4-0CC47A4D7654.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.ana = cms.EDAnalyzer('HGCalAnalysis',
                             detector = cms.string("all"),
                             rawRecHits = cms.bool(True),
                             readOfficialReco = cms.bool(True),
                             readCaloParticles = cms.bool(False),
                             layerClusterPtThreshold = cms.double(-1),  # All LayerCluster belonging to a multicluster are saved; this Pt threshold applied to the others
                             TestParticleFilter = ParticleFilterBlock.ParticleFilter
)

process.ana.TestParticleFilter.protonEMin = cms.double(100000)
process.ana.TestParticleFilter.etaMax = cms.double(3.1)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("twogamma_pt5_eta2_nosmear_calib_ntuple.root")

                                   )

reRunClustering = False

if reRunClustering:
    process.hgcalLayerClusters.minClusters = cms.uint32(0)
    process.hgcalLayerClusters.realSpaceCone = cms.bool(True)
    process.hgcalLayerClusters.multiclusterRadius = cms.double(2.)  # in cm if realSpaceCone is true
    process.hgcalLayerClusters.dependSensor = cms.bool(True)
    process.hgcalLayerClusters.ecut = cms.double(3.)  # multiple of sigma noise if dependSensor is true
    process.hgcalLayerClusters.kappa = cms.double(9.)  # multiple of sigma noise if dependSensor is true
    #process.hgcalLayerClusters.deltac = cms.vdouble(2.,3.,5.) #specify delta c for each subdetector separately
    process.p = cms.Path(process.hgcalLayerClusters+process.ana)
else:
    process.p = cms.Path(process.ana)
