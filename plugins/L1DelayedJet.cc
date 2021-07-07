// -*- C++ -*-
//
// Package:    DelayedJetCollection/L1DelayedJet
// Class:      L1DelayedJet
//
/**\class L1DelayedJet L1DelayedJet.cc DelayedJetCollection/L1DelayedJet/plugins/L1DelayedJet.cc

 Description: The package L1DelayedJet is prepared to create a delayed jet collection based on HCAL timing and depth. 

 Implementation:
     [Notes on implementation]
This creates a delayed jet collection based on the 6 bit timing and depth information saved in SOI_timingbit from the custom timing bit branch used in L1Ntuples for trigger studies. Goal is to use this to create an indication (per event) if the L1 trigger is passed and save this in the AOD file to be used in the offline analysis studies.

*/
//
// Original Author:  Gillian Baron Kopp
//         Created:  Mon, 07 Jun 2021 19:35:48 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/L1Trigger/interface/Jet.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloCollections.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegion.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"

//#include "DataFormats/HcalDigi/interface/HcalUpgradeTriggerPrimitiveDigi.h"
//#include "DataFormats/HcalDigi/interface/HcalUpgradeTriggerPrimitiveSample.h"


using namespace l1extra;

#include "TMath.h"

//
// class declaration
//

class L1DelayedJet : public edm::stream::EDProducer<> {
public:
  explicit L1DelayedJet(const edm::ParameterSet&);
  ~L1DelayedJet();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<HcalTrigPrimDigiCollection> hcalTPSource;
  std::string hcalTPSourceLabel;
  edm::EDGetTokenT<BXVector<l1t::Jet>> jetToken;
  std::string jetTokenLabel;
};

// functions to calculate eta from ieta, phi from iphi, and delta R
double etaVal(int ieta) { // calculate eta given ieta
  double etavl;
  if (ieta <= -24){
    etavl = .1695*ieta + 1.9931;
  }
  else if (ieta <= -1){
    etavl = .0875*ieta + .0489;
  }
  else if (ieta < 24){
    etavl = .0875*ieta - .0489;
  }
  else {
    etavl = .1695*ieta - 1.9931;
  }
  return etavl;
}

double phiVal(int iphi) { // calculate phi given iphi
  double phiBins=72.;
  double phivl;
  phivl=double(iphi)*(2.*TMath::Pi()/phiBins);
  if (iphi > 36) phivl -= 2.*TMath::Pi();
  return phivl;
}

double deltaR(double eta1, double phi1, double eta2, double phi2) { // calculate deltaR given two eta and phi values
  double deta = eta1 - eta2;
  double dphi = deltaPhi(phi1, phi2);
  return sqrt(deta*deta + dphi*dphi);
}

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
L1DelayedJet::L1DelayedJet(const edm::ParameterSet& iConfig) :
  hcalTPSource(consumes<HcalTrigPrimDigiCollection>(iConfig.getParameter<edm::InputTag>("hcalToken"))),
  hcalTPSourceLabel(iConfig.getParameter<edm::InputTag>("hcalToken").label()),
  jetToken(consumes<BXVector<l1t::Jet>>(edm::InputTag("simCaloStage2Digis","",""))), //"Jet","RECO"))),
  jetTokenLabel(edm::InputTag("simCaloStage2Digis","","").label()) //"Jet","RECO").label())
{
  //register your products
/* Examples
  produces<ExampleData2>();

  //if do put with a label
  produces<ExampleData2>("label");

  //if you want to put into the Run
  produces<ExampleData2,InRun>();
*/
  //now do what ever other initialization is needed
  produces< L1JetParticleCollection >( "DelayedJet" ) ;
  produces< L1JetParticleCollection >( "TimingJet" ) ;
  produces< L1JetParticleCollection >( "DepthJet" ) ;

}

L1DelayedJet::~L1DelayedJet() {
  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called to produce the data  ------------
void L1DelayedJet::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  edm::Handle<HcalTrigPrimDigiCollection> hcalTPs;
  iEvent.getByToken(hcalTPSource, hcalTPs);
  edm::Handle<BXVector<l1t::Jet>> jets;
  iEvent.getByToken(jetToken, jets);

  std::unique_ptr<L1JetParticleCollection> DelayedJetCands(new L1JetParticleCollection);
  std::unique_ptr<L1JetParticleCollection> TimingJetCands(new L1JetParticleCollection);
  std::unique_ptr<L1JetParticleCollection> DepthJetCands(new L1JetParticleCollection);

  double eta = -999.;
  double phi = -999.;
  double mass = 0;

  double LLP_TT_Jet[25] = {0};
  double timing_TT_Jet[25] = {0};
  double depth_TT_Jet[25] = {0};

  for ( const auto& hcalTp : *hcalTPs ) {
    int caloEta = hcalTp.id().ieta();
    uint32_t absCaloEta = abs(caloEta);
    int caloPhi = hcalTp.id().iphi();
    // Tower 29 is not used by Layer-1
    if(absCaloEta >= 29) continue;

    double TPeta = etaVal(caloEta);
    double TPphi = phiVal(caloPhi);

    int TimingFlag = 0;
    int DepthFlag = 0;
    //    int Depth1_Timing5 = hcalTp.SOI_timingbit();
    int Depth3_Timing3 = hcalTp.SOI_fineGrain();
    int Ndelayed = (Depth3_Timing3 & 0b010000) / 16;
    int NveryDelayed = (Depth3_Timing3 & 0b100000) / 32;
    int TotalDelayed = Ndelayed + NveryDelayed;
    int PromptVeto = (Depth3_Timing3 & 0b001000) / 8;
    if (TotalDelayed > 0 && PromptVeto == 0) TimingFlag = 1;
    if (Depth3_Timing3 & 0b000001) DepthFlag = 1;

    double min_dR = 100;
    int closest_jet = -1;
    int nJet = 0;

    // need to get jets, and see how many delayed TPs are near the jets
    if (DepthFlag == 1 || TimingFlag == 1) {
      for ( const auto& jet : *jets ) {
	eta = jet.eta(); // is this eta or ieta?
	phi = jet.phi(); // is this phi or iphi?
	if (deltaR(eta, phi, TPeta, TPphi) < min_dR) { 
	  min_dR = deltaR(eta,phi, TPeta, TPphi);
	  closest_jet = nJet;
	}
        nJet++;
      }
    }
    if (min_dR < 0.16) {
      if (DepthFlag == 1 || TimingFlag == 1) LLP_TT_Jet[closest_jet] += 1;
      if (DepthFlag == 1) depth_TT_Jet[closest_jet] += 1;
      if (TimingFlag == 1) timing_TT_Jet[closest_jet] += 1;
    }
  }

  int nJet = 0;
  double JetPt = 0;
  for ( const auto& jet : *jets ) {
    JetPt = jet.pt();
    eta = jet.eta();
    phi = jet.phi();
    if (LLP_TT_Jet[nJet] >= 2 && JetPt > 40) DelayedJetCands->push_back(L1JetParticle(math::PtEtaPhiMLorentzVector(JetPt, eta, phi, mass), L1JetParticle::kUndefined));
    if (depth_TT_Jet[nJet] >= 2 && JetPt > 40) TimingJetCands->push_back(L1JetParticle(math::PtEtaPhiMLorentzVector(JetPt, eta, phi, mass), L1JetParticle::kUndefined));
    if (timing_TT_Jet[nJet] >= 2 && JetPt > 40) DepthJetCands->push_back(L1JetParticle(math::PtEtaPhiMLorentzVector(JetPt, eta, phi, mass), L1JetParticle::kUndefined));
  }

  iEvent.put(std::move(DelayedJetCands), "DelayedJet");
  iEvent.put(std::move(TimingJetCands), "TimingJet");
  iEvent.put(std::move(DepthJetCands), "DepthJet");

/* This is an event example
  //Read 'ExampleData' from the Event
  ExampleData const& in = iEvent.get(inToken_);

  //Use the ExampleData to create an ExampleData2 which 
  // is put into the Event
  iEvent.put(std::make_unique<ExampleData2>(in));
*/

/* this is an EventSetup example
  //Read SetupData from the SetupRecord in the EventSetup
  SetupData& setup = iSetup.getData(setupToken_);
*/
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void L1DelayedJet::beginStream(edm::StreamID) {
  // please remove this method if not needed
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void L1DelayedJet::endStream() {
  // please remove this method if not needed
}

// ------------ method called when starting to processes a run  ------------
/*
void
L1DelayedJet::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
L1DelayedJet::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
L1DelayedJet::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
L1DelayedJet::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void L1DelayedJet::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1DelayedJet);
