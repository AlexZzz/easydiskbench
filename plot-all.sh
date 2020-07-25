#!/bin/bash

case "$#" in
  0 )
    PLOT_DIRS="$(ls -d ./results/*)"
    ;;
  * )
    PLOT_DIRS="${*}"
    ;;
esac

OUTPUT_DIR='./plots'

if [[ -d ${OTPUT_DIR} ]]; then
  echo "${OUTPUT_DIR} is already exists"
  echo "Please, delete and re-run ${0}"
  exit 1
fi
mkdir -p ${OUTPUT_DIR}

PLOT_FILES=''

for d in ${PLOT_DIRS}; do
  for f in $(ls -d ${d}/*); do
    file=$(basename ${f})
    if [[ "${PLOT_FILES}" != *"${file}"* ]]; then
      PLOT_FILES=${PLOT_FILES}" "${file}
    fi
  done
done

for f in ${PLOT_FILES}; do
  PLOT_WITH_PATHS=''
  for d in ${PLOT_DIRS}; do
    PLOT_WITH_PATHS=${PLOT_WITH_PATHS}" "${d}/${f}
  done
  if [[ ${f} == *iops.[0-9]*.log* ]]; then
    ./plot.py -i ${PLOT_WITH_PATHS} --interval 1000 --ylabel IO/s --value-divider 1 --median --per-second -o ${OUTPUT_DIR}/${f}_median.png
  elif [[ ${f} == *bw.[0-9]*.log* ]]; then
    ./plot.py -i ${PLOT_WITH_PATHS} --interval 1000 --ylabel MiB/s --value-divider 1024 --median -o ${OUTPUT_DIR}/${f}_median.png
  elif [[ ${f} == *lat.[0-9]*.log* ]]; then
    ./plot.py -i ${PLOT_WITH_PATHS} --interval 10000 -o ${OUTPUT_DIR}/${f}.png
    ./plot.py -i ${PLOT_WITH_PATHS} --median --interval 10000 -o ${OUTPUT_DIR}/${f}_median.png
  fi
done
