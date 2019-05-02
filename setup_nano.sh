# no shebang, should be sourced
scriptdir=$(dirname "${0}")
RELEASE=CMSSW_10_2_13
scram project CMSSW "${RELEASE}"
pushd "${RELEASE}/src"
eval $(scram runtime -sh)
git cms-init
git cms-merge-topic pieterdavid:GhentLeptonMVA_102
scram b -j3
patch -p1 -i "${scriptdir}/addDebug_NanoMVA.patch"
USER_CXXFLAGS="-DEDM_ML_DEBUG" scram b
popd
