# Authentication Setup Guide

## Overview

This guide walks you through setting up AWS Cognito authentication for the Supplier Diversity Dashboard. The authentication system provides:

- **Secure user registration and login**
- **Role-based access control** (User, Manager, Admin)
- **Password management** (change password, forgot password)
- **Session management** with automatic token refresh
- **AWS Cognito integration** for enterprise-grade security

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Python packages** installed: `boto3`, `python-dotenv`

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up AWS Cognito

### Option A: Automated Setup (Recommended)

Run the setup script:

```bash
python setup_aws_auth.py
```

This will:
- Create a Cognito User Pool
- Create an App Client with proper settings
- Optionally create an admin user
- Generate configuration files

### Option B: Manual Setup

1. **Create User Pool** in AWS Console:
   - Go to AWS Cognito → User Pools
   - Click "Create user pool"
   - Configure as follows:

2. **User Pool Settings**:
   ```
   Pool name: SupplierDiversityDashboard
   Sign-in options: Email
   Password policy: 
     - Minimum length: 8 characters
     - Require uppercase, lowercase, numbers, symbols
   ```

3. **Create App Client**:
   ```
   App client name: SupplierDiversityDashboardClient
   Generate client secret: Yes
   Auth flows: 
     - USER_PASSWORD_AUTH
     - REFRESH_TOKEN_AUTH
     - USER_SRP_AUTH
   ```

## Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# AWS Cognito Configuration
AWS_COGNITO_USER_POOL_ID=us-west-2_xxxxxxxxx
AWS_COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_COGNITO_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-west-2

# Optional: Session timeout (minutes)
SESSION_TIMEOUT_MINUTES=60
```

**Important**: Add `.env` to your `.gitignore` file to keep credentials secure!

## Step 4: Update Your Dashboard

### Option A: Use the Pre-built Authenticated Dashboard

Replace your current dashboard with the authenticated version:

```bash
# Backup current dashboard
mv frontend/procurement_dashboard.py frontend/procurement_dashboard_backup.py

# Use authenticated version
mv frontend/procurement_dashboard_with_auth.py frontend/procurement_dashboard.py
```

### Option B: Add Authentication to Existing Dashboard

Add these imports to your dashboard:

```python
from auth_ui import require_authentication, get_user_role, check_permission

def main():
    # Add this at the start of your main function
    if not require_authentication():
        return
    
    # Your existing dashboard code here...
```

## Step 5: Test the Authentication System

1. **Start the dashboard**:
   ```bash
   python start_dashboard.py
   ```

2. **Test user registration**:
   - Click "Register" 
   - Fill in user details
   - Check email for verification (if email is configured)

3. **Test login**:
   - Use registered credentials
   - Verify dashboard access

4. **Test admin features** (if admin user created):
   - Login with admin credentials
   - Verify additional features are visible

## User Roles and Permissions

### User (Default)
- View dashboard analytics
- Access basic reports
- Change own password

### Manager
- All User permissions
- View implementation strategy
- Access detailed analysis
- View timeline and planning tools

### Admin
- All Manager permissions
- Export data and reports
- User management (future feature)
- System configuration access

## Security Features

### Password Requirements
- Minimum 8 characters
- Must contain uppercase and lowercase letters
- Must contain at least one number
- Must contain at least one special character

### Session Management
- Automatic token refresh
- Configurable session timeout
- Secure logout functionality

### AWS Cognito Benefits
- Enterprise-grade security
- Built-in protection against common attacks
- Compliance with security standards
- Scalable user management

## Troubleshooting

### Common Issues

1. **"Configuration not found" error**:
   - Ensure `.env` file exists in project root
   - Verify all required environment variables are set
   - Check AWS credentials are configured

2. **"Access denied" error**:
   - Verify AWS IAM permissions for Cognito
   - Check User Pool and Client IDs are correct

3. **"User not confirmed" error**:
   - Check email for verification code
   - For testing, you can manually confirm users in AWS Console

4. **Import errors**:
   - Ensure all required packages are installed
   - Check Python path includes the frontend directory

### AWS IAM Permissions Required

Your AWS user/role needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cognito-idp:CreateUserPool",
                "cognito-idp:CreateUserPoolClient",
                "cognito-idp:AdminCreateUser",
                "cognito-idp:InitiateAuth",
                "cognito-idp:GetUser",
                "cognito-idp:ChangePassword",
                "cognito-idp:SignUp"
            ],
            "Resource": "*"
        }
    ]
}
```

## Advanced Configuration

### Custom User Attributes

Add custom attributes in the User Pool schema:

```python
# In setup_aws_auth.py, add to Schema array:
{
    'Name': 'department',
    'AttributeDataType': 'String',
    'Required': False,
    'Mutable': True
}
```

### Email Configuration

For production, configure SES for email delivery:

1. Set up Amazon SES
2. Verify your domain
3. Update User Pool email configuration

### Multi-Factor Authentication (MFA)

Enable MFA in User Pool settings:
- SMS MFA
- TOTP MFA (Google Authenticator, etc.)

## Production Deployment

### Environment Variables in Production

Set environment variables in your deployment platform:

- **Heroku**: Use Config Vars
- **AWS Lambda**: Use Environment Variables
- **Docker**: Use environment files or secrets
- **Railway**: Use Environment Variables

### Security Best Practices

1. **Never commit `.env` files**
2. **Use different User Pools for different environments**
3. **Enable CloudTrail logging for audit trails**
4. **Regularly rotate client secrets**
5. **Monitor authentication metrics**

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review AWS Cognito documentation
3. Check application logs for detailed error messages
4. Verify AWS service status

---

**Next Steps**: Once authentication is working, you can extend the system with additional features like user management, audit logging, and advanced role-based permissions.
