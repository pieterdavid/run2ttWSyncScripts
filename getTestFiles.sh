#!/usr/bin/env zsh
if ( ! $(voms-proxy-info --exists --valid 1:00) ); then
  voms-proxy-init --voms cms -rfc
  if [ $? -ne 0 ]; then
    echo "No valid proxy, so can't download input files"
    return 1
  fi
fi
remotebase="root://xrootd-cms.infn.it/"
localbase="/nfs/scratch/fynu/pdavid/ttWNanoAODv4TestInputs"
if [ ! -d "${localbase}" ]; then
  mkdir -p "${localbase}"
  if [ ! -d "${localbase}" ]; then
    echo "Could not create local directory ${localbase}, plase change it"
    return 1
  fi
fi

function downloadTestFile()
{
  echo "Downloading ${lfn} to ${localbase}/${dest_name}"
  dest_name="${1}"
  lfn="${2}"
  xrdcp "${remotebase}/${lfn}" "${localbase}/${dest_name}"
}

## MC
downloadTestFile "TTWJetsToLNu_RunIISummer16MiniAODv3_test_MINIAODSIM.root" "/store/mc/RunIISummer16MiniAODv3/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/00000/B020C78B-11D1-E811-B413-0242AC130002.root"
downloadTestFile "TTWJetsToLNu_RunIIFall17MiniAODv2_test_MINIAODSIM.root" "/store/mc/RunIIFall17MiniAODv2/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/DE32A3A3-0342-E811-A766-0CC47AF9B306.root"
## DATA
downloadTestFile "MuonEG_Run2016E_test_MINIAOD.root" "/store/data/Run2016E/MuonEG/MINIAOD/17Jul2018-v2/270000/909001DF-06B8-E811-87BD-0025905A48C0.root"
downloadTestFile "MuonEG_Run2017C_test_MINIAOD.root" "/store/data/Run2017C/MuonEG/MINIAOD/31Mar2018-v1/30000/28F13A95-A437-E811-917A-002481CFD184.root"
