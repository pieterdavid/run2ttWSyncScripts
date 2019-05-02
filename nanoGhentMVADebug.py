import FWCore.ParameterSet.Config as cms

def customise(process):
    if ( not hasattr(process, "MessageLogger") ) or any( not hasattr(process.MessageLogger, attrNm) for attrNm in ("destinations", "categories", "debugModules") ):
        raise RuntimeError("This customise method assumes a configured MessageLogger instance")
    if "debugs" not in process.MessageLogger.destinations:
        process.MessageLogger.destinations.append("debugs")
    if ( not hasattr(process.MessageLogger, "debugs") ) or ( hasattr(process.MessageLogger.debugs, "placeholder") and process.MessageLogger.debugs.placeholder ):
        process.MessageLogger.debugs = cms.untracked.PSet(threshold=cms.untracked.string("DEBUG"))
    process.MessageLogger.categories.append("MVAValueMapProducer")
    process.MessageLogger.debugModules.append("electronMVAGhent")
    process.MessageLogger.debugModules.append("muonMVAGhent")
    return process
