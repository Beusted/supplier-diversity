# AWS Services Used in Supplier Diversity Dashboard

**Cal Poly SLO AI Summer Camp - Small Business Procurement Analysis Project**

This document outlines all AWS services utilized in the supplier diversity analysis dashboard and their specific use cases.

---

## 🚀 **Core Compute Services**

### **AWS Lambda**
- **Purpose**: Serverless backend API for dashboard data processing
- **Usage**: 
  - Processes supplier similarity matching algorithms
  - Handles API requests from the frontend dashboard
  - Executes TF-IDF analysis for business matching
  - Returns JSON responses with PO analysis data
- **Files**: `aws-lambda/lambda_function.py` - Main Lambda handler
- **Triggers**: HTTP requests via API Gateway
- **Functions**:
  - `get_summary_stats()` - Dashboard summary statistics
  - `get_po_analysis()` - Purchase order percentage analysis
  - `get_top_matches()` - Supplier similarity matches
  - `get_optimization_plan()` - PO transition scenarios

### **Amazon API Gateway**
- **Purpose**: RESTful API endpoint management
- **Usage**:
  - Provides HTTP endpoints for dashboard data retrieval
  - Routes requests to appropriate Lambda functions
  - Handles CORS for frontend integration
  - Manages API versioning and deployment stages
- **Endpoints**:
  - `/api/summary` - Dashboard summary statistics
  - `/api/po-analysis` - Purchase order percentage analysis
  - `/api/matches` - Top supplier matches with similarity scores
  - `/api/categories` - Business category analysis
  - `/api/small-businesses` - Small business directory
  - `/api/optimization-plan` - PO transition scenarios

---

## 💾 **Data Storage Services**

### **Amazon DynamoDB**
- **Purpose**: NoSQL database for supplier match data
- **Usage**:
  - Stores supplier similarity matches with scores
  - Fast retrieval of top matches for dashboard
  - Scalable storage for large datasets
  - Primary data source for `get_top_matches()` function
- **Table**: `SupplierMatches`
- **Key Attributes**:
  - `Similarity_Score` - Match confidence level
  - Supplier information and business categories
  - Purchase order data and amounts
- **Operations**: `table.scan()` with filtering and sorting
- **Fallback**: S3 CSV files if DynamoDB unavailable

### **Amazon S3 (Simple Storage Service)**
- **Purpose**: Static file storage and backup data hosting
- **Usage**:
  - Stores CSV data files as backup/fallback
  - Hosts analysis results and summary data
  - Static asset storage for web deployment
- **Bucket**: `supplier-diversity-analysis`
- **Key Files**:
  - `demo_summary.csv` - Summary statistics
  - `test_results.csv` - Full PO analysis data
  - `detailed_similarity_analysis.csv` - Supplier matches
  - `sample_small_businesses.csv` - Small business directory

---

## 🔐 **Security & Access Management**

### **AWS IAM (Identity and Access Management)**
- **Purpose**: Security and permissions management
- **Usage**:
  - Lambda execution roles with DynamoDB and S3 permissions
  - API Gateway access policies
  - Cross-service authentication and authorization
- **Required Permissions**:
  - `dynamodb:Scan` - Read supplier matches
  - `dynamodb:Query` - Query specific match data
  - `s3:GetObject` - Read CSV files from S3
  - `logs:CreateLogGroup` - CloudWatch logging
- **Files**: 
  - `backend/iam-policy.json` - IAM policy definitions
  - `backend/trust-policy.json` - Trust relationship policies

---

## 📈 **Monitoring & Logging**

### **Amazon CloudWatch**
- **Purpose**: Application monitoring and logging
- **Usage**:
  - Lambda function execution logs and metrics
  - API Gateway request/response monitoring
  - DynamoDB performance metrics and throttling alerts
  - Error tracking and debugging
- **Log Groups**:
  - `/aws/lambda/supplier-diversity-api`
  - API Gateway access logs
  - DynamoDB operation logs
- **Metrics Tracked**:
  - Lambda duration and memory usage
  - DynamoDB read/write capacity utilization
  - API Gateway response times and error rates

---

## 🔧 **Development & Deployment Tools**

### **AWS CLI**
- **Purpose**: Command-line interface for AWS services
- **Usage**:
  - Deploy Lambda functions
  - Manage DynamoDB tables and data
  - Configure S3 buckets and files
  - Set up API Gateway endpoints

### **Boto3 (AWS SDK for Python)**
- **Purpose**: AWS service integration in Lambda
- **Usage**:
  - `boto3.resource('dynamodb')` - DynamoDB operations
  - `boto3.client('s3')` - S3 file operations
  - Integrated throughout `lambda_function.py`
- **Key Operations**:
  - DynamoDB table scanning and querying
  - S3 object retrieval and CSV parsing
  - Error handling and fallback logic

---

## 📋 **Service Integration Flow**

```
Frontend (Streamlit Dashboard) 
    ↓ HTTP Requests
API Gateway 
    ↓ Triggers
Lambda Functions 
    ↓ Primary Data Source
DynamoDB (SupplierMatches Table)
    ↓ Fallback Data Source
S3 Storage (CSV Files)
    ↓ Logs/Metrics
CloudWatch Monitoring
```

---

## 💡 **Cost Optimization Strategy**

### **Free Tier Usage**:
- **Lambda**: 1M free requests/month + 400,000 GB-seconds compute
- **API Gateway**: 1M API calls/month
- **DynamoDB**: 25GB free storage + 25 RCU/WCU per month
- **S3**: 5GB free storage + 20,000 GET requests
- **CloudWatch**: Basic monitoring included

### **Estimated Monthly Costs** (Beyond Free Tier):
- **Lambda**: ~$0.20 per 1M requests + $0.0000166667 per GB-second
- **API Gateway**: ~$3.50 per 1M requests
- **DynamoDB**: ~$0.25 per GB/month + $0.25 per 1M read units
- **S3**: ~$0.023 per GB/month + $0.0004 per 1,000 requests
- **Total Estimated**: <$15/month for typical usage

---

## 🚀 **Deployment Commands**

### **Lambda Function Deployment**:
```bash
# Package and deploy Lambda function
cd aws-lambda
zip -r ../lambda-function.zip .
aws lambda update-function-code \
  --function-name supplier-diversity-api \
  --zip-file fileb://lambda-function.zip
```

### **DynamoDB Table Setup**:
```bash
# Create DynamoDB table
aws dynamodb create-table \
  --table-name SupplierMatches \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Load sample data (if needed)
aws dynamodb batch-write-item \
  --request-items file://sample-data.json
```

### **S3 Bucket and Data Setup**:
```bash
# Create S3 bucket
aws s3 mb s3://supplier-diversity-analysis

# Upload CSV data files
aws s3 sync backend/ s3://supplier-diversity-analysis/ \
  --exclude "*.py" --include "*.csv"
```

### **API Gateway Deployment**:
```bash
# Deploy API changes to production stage
aws apigateway create-deployment \
  --rest-api-id YOUR_API_ID \
  --stage-name prod \
  --description "Supplier Diversity API deployment"
```

---

## 🎯 **Architecture Benefits**

### **Scalability**:
- **DynamoDB**: Auto-scaling read/write capacity
- **Lambda**: Automatic scaling based on request volume
- **S3**: Unlimited storage capacity

### **Reliability**:
- **Multi-AZ**: DynamoDB and S3 replicated across availability zones
- **Fallback Logic**: S3 CSV files as backup if DynamoDB unavailable
- **Error Handling**: Comprehensive exception handling in Lambda

### **Performance**:
- **DynamoDB**: Single-digit millisecond latency
- **Lambda**: Cold start optimization with connection reuse
- **API Gateway**: Built-in caching capabilities

---

## 📚 **Additional Resources**

- **AWS Lambda Developer Guide**: [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- **DynamoDB Developer Guide**: [Amazon DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- **API Gateway Developer Guide**: [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- **S3 User Guide**: [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
- **Boto3 Documentation**: [AWS SDK for Python](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

🎓 **Cal Poly SLO AI Summer Camp Project**  
*Leveraging AWS Serverless Architecture for Scalable Supplier Diversity Analysis*
