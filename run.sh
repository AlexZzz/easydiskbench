#!/bin/bash

HOST=$1
DIR=$2

set +x
ssh "${HOST}" 'rm ./tests'
scp -r ./tests "${HOST}":/"${DIR}"
ssh "${HOST}" 'fio ./tests/basic.fio'
