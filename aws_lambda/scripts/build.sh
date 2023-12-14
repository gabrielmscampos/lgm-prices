#!/bin/bash

CURRENT_DIR=$(pwd)

while getopts ":s:p:" opt; do
  case $opt in
    s) STAGE="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

SAM_PARAMETERS=$( cat ${CURRENT_DIR}/params.${STAGE}.json | jq -r '[.[] | "\(.ParameterKey)=\(.ParameterValue)"] | join(" ")' )

sam build --parameter-overrides $SAM_PARAMETERS --profile gabrielmscampos
