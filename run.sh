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

set +x
ssh "${HOST}" 'rm ./tests'
scp -r ./tests "${HOST}":/"${DIR}"
ssh "${HOST}" 'fio ./tests/basic.fio'
