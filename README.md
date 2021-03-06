ttW synchronisation
===================

This package contains helper scripts to synchronize the tZqTTV lepton MVA between the Ghent heavyNeutrino framework, NanoAODv4, and the Louvain llbb framework

 - the `getTestFiles.sh` script downloads the necessary MiniAOD input files for testing (this needs the GRID environment, notably the `voms-proxy-init`, `voms-proxy-info`, and `xrdcp` commands)
 - the `setup_*.sh` scripts set up a CMSSW project area for the different cases (these should be executed with `source` because they also setup the shell environment)
 - the `run_*.sh` scripts (which need to run in after setting up a CMSSW environment) run sample configurations and produce some output files for each (JSON and text)
 - the `checkSynchronization.py` script compares the JSON files from the previous step, and prints any remaining differences

The changes to add the tZqTTV lepton MVA to NanoAODv4 are in [this branch](https://github.com/cms-sw/cmssw/compare/CMSSW_10_2_13...pieterdavid:GhentLeptonMVA_102)
(work in progress); the [`run_nano.sh`](run_nano.sh) script above contains typical commands to run it (with some additional patches to store more information for debugging).
