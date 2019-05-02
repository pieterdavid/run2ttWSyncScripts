# no shebang, should be sourced
startdir="$(pwd)"
scriptdir=$(dirname "${0}")
wget https://raw.githubusercontent.com/GhentAnalysis/heavyNeutrino/master/setup.sh
source setup.sh
hndir=$(pwd) ## should be $CMSSW_BASE/src/heavyNeutrino
patch -p1 -i "${scriptdir}/addDebug_GhentMVA.patch"
USER_CXXFLAGS="-DEDM_ML_DEBUG" scram b
cd "${startdir}"
