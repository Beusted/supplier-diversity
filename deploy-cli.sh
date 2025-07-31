#!/bin/bash

echo "🚀 Deploying Supplier Diversity Dashboard via AWS CLI"
echo "===================================================="

# First, create GitHub connection (one-time setup)
echo "📱 Creating GitHub connection..."
CONNECTION_ARN=$(aws apprunner create-connection \
    --connection-name "supplier-diversity-github" \
    --provider-type "GitHub" \
    --region us-west-2 \
    --query 'Connection.ConnectionArn' \
    --output text)

echo "✅ GitHub connection created: $CONNECTION_ARN"
echo "⚠️  You need to complete the GitHub authorization in the AWS Console"
echo "   Go to: https://console.aws.amazon.com/apprunner/connections"
echo "   Click on your connection and complete the handshake"
echo ""
echo "Press Enter when you've completed the GitHub authorization..."
read

# Create the App Runner service
echo "🚀 Creating App Runner service..."
aws apprunner create-service \
    --service-name "supplier-diversity-dashboard" \
    --source-configuration '{
        "CodeRepository": {
            "RepositoryUrl": "https://github.com/Beusted/supplier-diversity",
            "SourceCodeVersion": {
                "Type": "BRANCH",
                "Value": "main"
            },
            "CodeConfiguration": {
                "ConfigurationSource": "CONFIGURATION_FILE"
            }
        },
        "AutoDeploymentsEnabled": true,
        "AuthenticationConfiguration": {
            "ConnectionArn": "'$CONNECTION_ARN'"
        }
    }' \
    --instance-configuration '{
        "Cpu": "0.25 vCPU",
        "Memory": "0.5 GB"
    }' \
    --region us-west-2

echo "✅ App Runner service created!"
echo "🔗 Check status: aws apprunner describe-service --service-arn <service-arn>"
