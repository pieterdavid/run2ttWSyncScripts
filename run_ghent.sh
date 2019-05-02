#!/usr/bin/env zsh
scriptdir=$(dirname "${0}")
if [ -z "${CMSSW_BASE}" ]; then
  echo "No CMSSW_BASE, please run cmsenv inside a project area first (or use setup_ghent.sh to set one up)"
  return 1
fi
cfgFile="${CMSSW_BASE}/src/heavyNeutrino/multilep/test/multilep.py"
if [ ! -e "${cfgFile}" ]; then
  echo "Config file ${cfgFile} not found, "
  return 1
fi
localbase="/nfs/scratch/fynu/pdavid/ttWNanoAODv4TestInputs"

echo "---> Running 100 events of 2016 ttW MC (Summer16MiniAODv3)"
cmsRun "${cfgFile}" "inputFile=file:${localbase}/TTWJetsToLNu_RunIISummer16MiniAODv3_test_MINIAODSIM.root" "outputFile=dilep_2016MC.root" events=100 &> "ghent_mc2016_100.log"
if [ $? -ne 0 ]; then
  echo "Problem in running on 2016 MC, please check ghent_mc2016_100.log for more information"
fi
grep -A1 -B1 "2016 BDTG" "debugs.log" | grep ", ) -> " > "ghent_mc2016_dbgLepMVA.log"
"${scriptdir}/synchroFromGhent.py" --leptonJet --era 2016 -o "ghent_mc2016.json" "dilep_2016MC.root"

echo "---> Running 100 events of 2017 ttW MC (Fall17MiniAODv2)"
cmsRun "${cfgFile}" "inputFile=file:${localbase}/TTWJetsToLNu_RunIIFall17MiniAODv2_test_MINIAODSIM.root" "outputFile=dilep_2017MC.root" events=100 &> "ghent_mc2017_100.log"
if [ $? -ne 0 ]; then
  echo "Problem in running on 2017 MC, please check ghent_mc2017_100.log for more information"
fi
grep -A1 -B1 "2017 BDTG" "debugs.log" | grep ", ) -> " > "ghent_mc2017_dbgLepMVA.log"
"${scriptdir}/synchroFromGhent.py" --leptonJet --era 2017 -o "ghent_mc2017.json" "dilep_2017MC.root"
