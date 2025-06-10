#!/bin/bash
_includeFile=$(type -p overrides.inc)
_ocFunctions=$(type -p ocFunctions.inc)
if [ ! -z ${_includeFile} ]; then
  . ${_ocFunctions}
  . ${_includeFile}
else
  _red='\033[0;31m'; _yellow='\033[1;33m'; _nc='\033[0m'; echo -e \\n"${_red}overrides.inc could not be found on the path.${_nc}\n${_yellow}Please ensure the openshift-developer-tools are installed on and registered on your path.${_nc}\n${_yellow}https://github.com/BCDevOps/openshift-developer-tools${_nc}"; exit 1;
fi

if createOperation; then
  # Ask the user to supply the sensitive parameters ...
  readParameter "LEDGER_SEED - Please provide the ledger monitor seed for the environment.  If left blank, a seed will be randomly generated using openssl:" LEDGER_SEED $(generateSeed) "false"
else
  # Secrets are removed from the configurations during update operations ...
  printStatusMsg "Update operation detected ...\nSkipping the prompts for LEDGER_SEED secret ... \n"
  writeParameter "LEDGER_SEED" "prompt_skipped" "false"
fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}
# ================================================================================================================
