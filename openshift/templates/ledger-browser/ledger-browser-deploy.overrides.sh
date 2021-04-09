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
  readParameter "WALLET_ENCRYPTION_KEY - Please provide the wallet encryption key for the environment.  If left blank, a 48 character long base64 encoded value will be randomly generated using openssl:" WALLET_ENCRYPTION_KEY $(generateKey) "true"

  _walletPrefix="VN"
  readParameter "INDY_WALLET_SEED - Please provide the indy wallet seed for the environment.  If left blank, a seed will be randomly generated using openssl:" INDY_WALLET_SEED $(generateSeed ${_walletPrefix}) "true"
  readParameter "INDY_WALLET_DID - Please provide the indy wallet did for the environment.  The default is an empty string:" INDY_WALLET_DID "" "true"
else
  # Secrets are removed from the configurations during update operations ...
  printStatusMsg "Update operation detected ...\nSkipping the prompts for WALLET_ENCRYPTION_KEY, INDY_WALLET_SEED and INDY_WALLET_DID secrets ... \n"
  writeParameter "WALLET_ENCRYPTION_KEY" "prompt_skipped" "false"
  writeParameter "INDY_WALLET_SEED" "prompt_skipped" "false"
  writeParameter "INDY_WALLET_DID" "prompt_skipped" "false"
fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}
# ================================================================================================================
