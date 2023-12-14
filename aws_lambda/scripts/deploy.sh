#!/bin/bash

ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
CURRENT_DIR=$(pwd)
AWS_DEPLOY_REGION=us-east-1
AWS_STACK_NAME=lgm-prices-api
S3_ARTIFACTS_PREFIX=lgm-prices-api

while getopts ":a:s:p:" opt; do
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

AWS_STACK_NAME="${AWS_STACK_NAME}-${STAGE}"
S3_ARTIFACTS_PREFIX="${S3_ARTIFACTS_PREFIX}-${STAGE}"
IMAGE_RESPOSITORY="${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/lgm-prices-api"
S3_ARTIFACTS_BUCKET=samcli-artifacts

echo "Performing deploy with the following settings:"
echo ""
echo "CURRENT_DIR: ${CURRENT_DIR}"
echo "STAGE: ${STAGE}"
echo "AWS_STACK_NAME: ${AWS_STACK_NAME}"
echo "AWS_DEPLOY_REGION: ${AWS_DEPLOY_REGION}"
echo "S3_ARTIFACTS_PREFIX: ${S3_ARTIFACTS_PREFIX}"
echo "S3_ARTIFACTS_BUCKET: ${S3_ARTIFACTS_BUCKET}"
echo ""

SAM_PARAMETERS=$( cat ${CURRENT_DIR}/params.${STAGE}.json | jq -r '[.[] | "\(.ParameterKey)=\(.ParameterValue)"] | join(" ")' )

sam build --parameter-overrides $SAM_PARAMETERS

cd .aws-sam/build

sam package \
    --region $AWS_DEPLOY_REGION \
    --template-file template.yaml \
    --output-template-file cloudformation.yaml \
    --s3-bucket $S3_ARTIFACTS_BUCKET \
    --s3-prefix $S3_ARTIFACTS_PREFIX \
    --image-repository $IMAGE_RESPOSITORY

sam deploy \
    --region $AWS_DEPLOY_REGION \
    --template-file cloudformation.yaml \
    --stack-name $AWS_STACK_NAME \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --parameter-overrides $SAM_PARAMETERS \
    --image-repository $IMAGE_RESPOSITORY
