#!/usr/bin/env zsh
scriptdir=$(dirname "${0}")
if [ -z "${CMSSW_BASE}" ]; then
  echo "No CMSSW_BASE, please run cmsenv inside a project area first (or use setup_nano.sh to set one up)"
  return 1
fi
localbase="/nfs/scratch/fynu/pdavid/ttWNanoAODv4TestInputs"
noHiggsSTXSRivetLines="'process.particleLevelSequence.remove(process.genParticles2HepMCHiggsVtx);process.particleLevelSequence.remove(process.rivetProducerHTXS);process.particleLevelTables.remove(process.HTXSCategoryTable)'"
cp "${scriptdir}/nanoGhentMVADebug.py" .

echo "---> Running 100 events of 2016 ttW MC (Summer16MiniAODv3)"
cmsDriver.py ttWSync_MCSummer16MiniAODv3_dbg -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --processName 14Dec2018 --conditions 94X_mcRun2_asymptotic_v3 --era Run2_2016,run2_nanoAOD_94X2016 --customise_commands "${noHiggsSTXSRivetLines}" --customise "nanoGhentMVADebug.py" --filein "file:${localbase}/TTWJetsToLNu_RunIISummer16MiniAODv3_test_MINIAODSIM.root" -n 100 &> "nano_mc2016_100.log"
if [ $? -ne 0 ]; then
  echo "Problem in running on 2016 MC, please check nano_mc2016_100.log for more information"
  return 1
fi
grep -A2 "MSG-d MVAValueMapProducer" "debugs.log" | grep ", ) -> " > "nano_mc2016_dbgLepMVA.log"
"${scriptdir}/synchroFromNanoAOD.py" --leptonJet --era 2016 -o "nano_mc2016.json" "ttWSync_MCSummer16MiniAODv3_dbg_NANO.root"

echo "---> Running 100 events of 2017 ttW MC (Fall17MiniAODv2)"
cmsDriver.py ttWSync_MCFall17MiniAODv2_dbg -s NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --processName 14Dec2018 --conditions 102X_mc2017_realistic_v6 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise_commands "${noHiggsSTXSRivetLines}" --customise "nanoGhentMVADebug.py" --filein "file:${localbase}/TTWJetsToLNu_RunIIFall17MiniAODv2_test_MINIAODSIM.root" -n 100 &> "nano_mc2017_100.log"
if [ $? -ne 0 ]; then
  echo "Problem in running on 2017 MC, please check ghent_mc2017_100.log for more information"
  return 1
fi
grep -A2 "MSG-d MVAValueMapProducer" "debugs.log" | grep ", ) -> " > "nano_mc2017_dbgLepMVA.log"
"${scriptdir}/synchroFromNanoAOD.py" --leptonJet --era 2017 -o "nano_mc2017.json" "ttWSync_MCFall17MiniAODv2_dbg_NANO.root"
