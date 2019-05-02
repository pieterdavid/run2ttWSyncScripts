#!/usr/bin/env python2

import argparse
parser = argparse.ArgumentParser(description="Generate synchronization JSON from a Ghent HeavyNeutrino tree")
parser.add_argument("inputfile", type=str, nargs=1, help="Input file with tree")
parser.add_argument("-t", "--treename", type=str, default="blackJackAndHookers/blackJackAndHookersTree", help="Name of the tree inside the file")
parser.add_argument("--era", type=str, default="2016", help="era (data-taking year)")
parser.add_argument("-n", "--numevents", type=int, default=-1, help="Number of events to process (default: all)")
parser.add_argument("-o", "--output", type=str, default="test.json", help="Output filename")
parser.add_argument("--leptonJet", action="store_true", help="Add lepton-jet variables")
args = parser.parse_args()

import ROOT
LorentzVector = getattr(ROOT, "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<float> >")
tup = ROOT.TChain(args.treename)
for infn in args.inputfile:
    tup.Add(infn)

import functools
def getCont(tree, index, prefix, varName):
    return getattr(tree, "{0}{1}".format(prefix, varName))[index]

def fillLeptonCommon(getL):
    lepton = {"p4": (getL("lPt"), getL("lEta"), getL("lPhi"), getL("lE"))}
    lepton["IP"] = {
            "dxy": getL("dxy"), "dz": getL("dz"),
            "sip3d": getL("3dIPSig")
            }
    lepton["ISO"] = {
            "miniCh" : getL("miniIsoCharged"),
            "miniNeu": getL("miniIso")-getL("miniIsoCharged")
            }
    if args.leptonJet:
        lepton["JET"] = {
                "trackMult": int(getL("selectedTrackMult")),
                "ptRel": getL("ptRel"),
                "ptRatio": getL("ptRatio"),
                "Btag": getL("closestJetDeepCsv_b")+getL("closestJetDeepCsv_bb")
                }
    lepton["MVA"] = {
            "ttVtZq": (getL("leptonMvatZqTTV16") if args.era == "2016" else getL("leptonMvatZqTTV17"))
            }

    return lepton

nEvts = args.numevents
if nEvts < 0:
    nEvts = tup.GetEntries()
events = []
for i in range(nEvts):
    tup.GetEntry(i)

    evt = {"id" : (tup._runNb, tup._lumiBlock, tup._eventNb)}

    evt["muons"] = []
    for li in range(tup._nMu):
        getL = functools.partial(getCont, tup, li, "_")
        ## passLooseMu is already applied here
        lepton = fillLeptonCommon(getL)
        lepton["ID"] = { "segmentCompatibility": getL("lMuonSegComp") }
        lepton["ISO"]["rel"] = getL("relIso") ## TODO ??
        evt["muons"].append(lepton)
    evt["electrons"] = []
    for li in range(tup._nEle):
        getL = functools.partial(getCont, tup, tup._nMu+li, "_")
        ## passLooseEl is already applied here
        lepton = fillLeptonCommon(getL)
        lepton["ID"] = { "MVAIdForLepMVA": getL("lElectronMvaSummer16GP") if args.era == "2016" else getL("lElectronMvaFall17v1NoIso") }
        evt["electrons"].append(lepton)

    evt["jets"] = []
    for iJ in range(tup._nJets):
        getJ = functools.partial(getCont, tup, iJ, "_jet")
        ## isLoose already is already applied here
        if getJ("Pt") > 25.:
            jet = {"p4": (getJ("Pt"), getJ("Eta"), getJ("Phi"), getJ("E"))}
            ## TODO add more
            evt["jets"].append(jet)

    if len(evt["electrons"])+len(evt["muons"]) >= 2:
        events.append(evt)

import json
with open(args.output, "w") as outF:
    json.dump({"Events": events}, outF)
