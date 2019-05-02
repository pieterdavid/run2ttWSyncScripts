#!/usr/bin/env python2

import argparse
parser = argparse.ArgumentParser(description="Generate synchronization JSON from NanoAOD")
parser.add_argument("inputfile", type=str, nargs=1, help="Input file with tree")
parser.add_argument("-t", "--treename", type=str, default="Events", help="Name of the tree inside the file")
parser.add_argument("--era", type=str, default="2016", help="era (data-taking year)")
parser.add_argument("-n", "--numevents", type=int, default=-1, help="Number of events to process (default: all)")
parser.add_argument("-o", "--output", type=str, default="test.json", help="Output filename")
parser.add_argument("--leptonJet", action="store_true", help="Add lepton-jet variables")
args = parser.parse_args()

import ROOT
LorentzVector = getattr(ROOT, "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >")
tup = ROOT.TChain(args.treename)
for infn in args.inputfile:
    tup.Add(infn)

import functools
def getCont(tree, index, prefix, varName):
    return getattr(tree, "{0}_{1}".format(prefix, varName))[index]

def passLooseEl(getL):
    return getL("pt") > 7. and abs(getL("eta")) < 2.5 and abs(getL("dxy")) < .05 and abs(getL("dz")) < .1 and ord(getL("lostHits")) <= 2

def passLooseMu(getL):
    return getL("pt") > 5. and abs(getL("eta")) < 2.4 and getL("isPFcand") and ( getL("isGlobal") or getL("isTracker") ) and abs(getL("dxy")) < .05 and abs(getL("dz")) < .1

def fillLeptonCommon(getL, hasJet=False):
    p4 = LorentzVector(getL("pt"), getL("eta"), getL("phi"), getL("mass"))
    lepton = {"p4": (p4.Pt(), p4.Eta(), p4.Phi(), p4.E())}
    lepton["IP"] = {
            "dxy": getL("dxy"), "dz": getL("dz"),
            "sip3d": abs(getL("sip3d"))
            }
    lepton["ISO"] = {
            "miniCh" : getL("miniPFRelIso_chg"),
            "miniNeu": getL("miniPFRelIso_all")-getL("miniPFRelIso_chg")
            }
    if args.leptonJet:
        lepton["JET"] = {
                "trackMult": int(getL("jet_trackMult")),
                "ptRel": getL("jet_pTRel"),
                "ptRatio": getL("jet_ptRatio"),
                "Btag": getL("jet_deepcsv")
                }
    lepton["MVA"] = {
            "ttVtZq": getL("mvaGhent")
            }

    return lepton

nEvts = args.numevents
if nEvts < 0:
    nEvts = tup.GetEntries()
events = []
for i in range(nEvts):
    tup.GetEntry(i)

    evt = {"id" : (tup.run, tup.luminosityBlock, tup.event)}

    evt["electrons"] = []
    for li in range(tup.nElectron):
        getL = functools.partial(getCont, tup, li, "Electron")
        if passLooseEl(getL):
            lepton = fillLeptonCommon(getL)
            lepton["ID"] = { "MVAIdForLepMVA": getL("mvaSpring16GP") if args.era == "2016" else getL("mvaFall17V1noIso") }
            if args.era == "2016":
                lepton["ISO"] = {
                        "miniCh" : getL("miniPFRelIso_chg2"),
                        "miniNeu": getL("miniPFRelIso_all2")-getL("miniPFRelIso_chg2")
                        }
            p4 = lepton["p4"]
            eCorr = getL("eCorr")
            lepton["p4"] = (p4[0]/eCorr, p4[1], p4[2], p4[3]/eCorr)
            evt["electrons"].append(lepton)
    evt["muons"] = []
    for li in range(tup.nMuon):
        getL = functools.partial(getCont, tup, li, "Muon")
        if passLooseMu(getL):
            lepton = fillLeptonCommon(getL)
            lepton["ID"] = { "segmentCompatibility": getL("segmentComp") }
            lepton["ISO"]["rel"] = getL("relIso03_EA") ## only really there for debugging this
            evt["muons"].append(lepton)

    evt["jets"] = []
    for iJ in range(tup.nJet):
        getJ = functools.partial(getCont, tup, iJ, "Jet")
        if ( ( getJ("jetId") & 0x1 ) if args.era == "2016" else ( getJ("jetId") & 0x2 ) ) and getJ("pt") > 25.:
            p4 = LorentzVector(getJ("pt"), getJ("eta"), getJ("phi"), getJ("mass"))
            jet = {"p4": (p4.Pt(), p4.Eta(), p4.Phi(), p4.E())}
            ## TODO add more
            evt["jets"].append(jet)

    if len(evt["electrons"])+len(evt["muons"]) >= 2:
        events.append(evt)

import json
with open(args.output, "w") as outF:
    json.dump({"Events": events}, outF)
