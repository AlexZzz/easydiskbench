#!/bin/bash

case "$#" in
  0 )
    HOST='localhost'
    DIR="/home/$(logname)"
    ;;
  1 )
    if [[ "help" == "${1}" ]]; then
      echo "Usage: ${0} HOST PATH"
      echo "will do scp HOST:PATH"
      exit 0
    fi
    HOST="${1}"
    DIR="/home/$(logname)"
    ;;
  2 )
    HOST="${1}"
    DIR="${2}"
    ;;
  3 )
    HOST="${2}"
    DIR="${3}"
    REMOTE_USER="${1}"
    ;;
  * )
    echo "Accept only three arguments: ${0} remote_user host path"
    exit 1
    ;;
esac

CREDS="${REMOTE_USER}@${HOST}"
SCP_ARGS="${CREDS}:${DIR}"

fatal() {
  echo Please
  printf "\033[38;5;196mAn error occured!\n"
  printf "Please, cleanup %s on %s manually.\n\033[39m" "${DIR}" "${HOST}"
  exit 1
}

install_fio() {
  echo "No fio command found, trying to install"
  ssh "${CREDS}" 'apt update && apt install fio -y'
}

if [[ -d ./results/${HOST} ]]; then
  echo "./results/${HOST} is already exists"
  echo "Please, delete and re-run ${0}"
  exit 1
fi
mkdir -p ./results/${HOST}

command -v fio > /dev/null 2>&1 || install_fio

scp -r ./tests "${SCP_ARGS}"
if [[ $? != 0 ]]; then
  fatal
fi

ssh "${CREDS}" "
pushd ${DIR}
mkdir ./results
pushd ./results
fio ../basic.fio --filename=../fiofile --output=./base_results
popd
"
if [[ $? != 0 ]]; then
  fatal
fi

scp -r "${SCP_ARGS}"/results/* ./results/${HOST}/
if [[ $? != 0 ]]; then
  fatal
fi

# Cleanup
ssh "${CREDS}" "
pushd ${DIR}
rm -r ./tests ./results ./fiofile
popd
rmdir ${DIR}
"
