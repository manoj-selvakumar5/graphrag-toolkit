#!/bin/bash

# Deploy GraphRAG Toolkit CloudFormation Stack
# Fix SSL issues by updating certificates and using no-verify-ssl if needed

# Try with SSL verification first
aws cloudformation create-stack \
  --stack-name graphrag-toolkit-stack \
  --template-body file://examples/lexical-graph/cloudformation-templates/graphrag-toolkit-neptune-analytics-opensearch-serverless.json \
  --parameters ParameterKey=ApplicationId,ParameterValue=my-graphrag \
               ParameterKey=ProvisionedMemory,ParameterValue=16 \
               ParameterKey=NotebookInstanceType,ParameterValue=ml.m5.xlarge \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region ${AWS_DEFAULT_REGION:-us-east-1} \
  --no-cli-pager

# If above fails with SSL error, uncomment the line below:
# --no-verify-ssl \

echo "Stack deployment initiated. Check status with:"
echo "aws cloudformation describe-stacks --stack-name graphrag-toolkit-stack"