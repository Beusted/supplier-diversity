#!/bin/bash

echo "🚀 Deploying Supplier Diversity Dashboard to AWS App Runner"
echo "============================================================"

# Navigate to CDK directory
cd cdk

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Bootstrap CDK (if not already done)
echo "📦 Bootstrapping CDK..."
cdk bootstrap

# Deploy the stack
echo "🚀 Deploying stack..."
cdk deploy --require-approval never

echo "✅ Deployment complete!"
echo "📊 Your Small Business PO Percentage Dashboard is now live!"
