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
  * )
    echo "Accept only two arguments: ${0} host path"
    exit 1
    ;;
esac

fatal() {
  echo Please
  printf "\033[38;5;196mAn error occured!\n"
  printf "Please, cleanup %s on %s manually.\n\033[39m" "${DIR}" "${HOST}"
  exit 1
}

set -x
scp -r ./tests "${HOST}":"${DIR}"
if [[ $? != 0 ]]; then
  fatal
fi
ssh "${HOST}" "
pushd ${DIR}
mkdir ./results
pushd ./results
fio ../basic.fio
popd
"
if [[ $? != 0 ]]; then
  fatal
fi
scp -r "${HOST}":"${DIR}"/results ./
if [[ $? != 0 ]]; then
  fatal
fi

# Cleanup
ssh "${HOST}" "rm -r ${DIR}"
