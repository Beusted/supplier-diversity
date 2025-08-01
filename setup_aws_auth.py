#!/usr/bin/env python3
"""
AWS Cognito Setup Script for Supplier Diversity Dashboard
This script helps set up AWS Cognito User Pool and App Client
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

class CognitoSetup:
    def __init__(self, region='us-west-2'):
        self.region = region
        self.cognito_client = boto3.client('cognito-idp', region_name=region)
        
    def create_user_pool(self, pool_name="SupplierDiversityDashboard"):
        """Create a Cognito User Pool"""
        try:
            response = self.cognito_client.create_user_pool(
                PoolName=pool_name,
                Policies={
                    'PasswordPolicy': {
                        'MinimumLength': 8,
                        'RequireUppercase': True,
                        'RequireLowercase': True,
                        'RequireNumbers': True,
                        'RequireSymbols': True,
                        'TemporaryPasswordValidityDays': 7
                    }
                },
                AutoVerifiedAttributes=['email'],
                AliasAttributes=['email'],
                UsernameAttributes=['email'],
                Schema=[
                    {
                        'Name': 'email',
                        'AttributeDataType': 'String',
                        'Required': True,
                        'Mutable': True
                    },
                    {
                        'Name': 'name',
                        'AttributeDataType': 'String',
                        'Required': False,
                        'Mutable': True
                    },
                    {
                        'Name': 'role',
                        'AttributeDataType': 'String',
                        'Required': False,
                        'Mutable': True,
                        'DeveloperOnlyAttribute': False
                    }
                ],
                AdminCreateUserConfig={
                    'AllowAdminCreateUserOnly': False,
                    'UnusedAccountValidityDays': 7,
                    'InviteMessageAction': 'EMAIL',
                    'TemporaryPasswordValidityDays': 1
                },
                EmailConfiguration={
                    'EmailSendingAccount': 'COGNITO_DEFAULT'
                },
                VerificationMessageTemplate={
                    'DefaultEmailOption': 'CONFIRM_WITH_CODE',
                    'EmailSubject': 'Supplier Diversity Dashboard - Verify your email',
                    'EmailMessage': 'Welcome to the Supplier Diversity Dashboard! Your verification code is {####}'
                },
                UserPoolTags={
                    'Project': 'SupplierDiversityDashboard',
                    'Environment': 'Production',
                    'CreatedBy': 'SetupScript'
                }
            )
            
            user_pool_id = response['UserPool']['Id']
            print(f"✅ User Pool created successfully!")
            print(f"   User Pool ID: {user_pool_id}")
            return user_pool_id
            
        except ClientError as e:
            print(f"❌ Error creating User Pool: {e}")
            return None
    
    def create_user_pool_client(self, user_pool_id, client_name="SupplierDiversityDashboardClient"):
        """Create a User Pool App Client"""
        try:
            response = self.cognito_client.create_user_pool_client(
                UserPoolId=user_pool_id,
                ClientName=client_name,
                GenerateSecret=True,  # Generate client secret for server-side apps
                RefreshTokenValidity=30,  # 30 days
                AccessTokenValidity=60,   # 60 minutes
                IdTokenValidity=60,       # 60 minutes
                TokenValidityUnits={
                    'AccessToken': 'minutes',
                    'IdToken': 'minutes',
                    'RefreshToken': 'days'
                },
                ExplicitAuthFlows=[
                    'ALLOW_USER_PASSWORD_AUTH',
                    'ALLOW_REFRESH_TOKEN_AUTH',
                    'ALLOW_USER_SRP_AUTH'
                ],
                SupportedIdentityProviders=['COGNITO'],
                ReadAttributes=[
                    'email',
                    'email_verified',
                    'name',
                    'custom:role'
                ],
                WriteAttributes=[
                    'email',
                    'name',
                    'custom:role'
                ],
                PreventUserExistenceErrors='ENABLED'
            )
            
            client_id = response['UserPoolClient']['ClientId']
            client_secret = response['UserPoolClient']['ClientSecret']
            
            print(f"✅ User Pool Client created successfully!")
            print(f"   Client ID: {client_id}")
            print(f"   Client Secret: {client_secret}")
            
            return client_id, client_secret
            
        except ClientError as e:
            print(f"❌ Error creating User Pool Client: {e}")
            return None, None
    
    def create_admin_user(self, user_pool_id, username, email, temporary_password, full_name="Admin User"):
        """Create an admin user"""
        try:
            response = self.cognito_client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=username,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'true'},
                    {'Name': 'name', 'Value': full_name},
                    {'Name': 'custom:role', 'Value': 'admin'}
                ],
                TemporaryPassword=temporary_password,
                MessageAction='SUPPRESS',  # Don't send welcome email
                DesiredDeliveryMediums=['EMAIL']
            )
            
            print(f"✅ Admin user created successfully!")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Temporary Password: {temporary_password}")
            print(f"   ⚠️  User must change password on first login")
            
            return True
            
        except ClientError as e:
            print(f"❌ Error creating admin user: {e}")
            return False
    
    def save_config(self, user_pool_id, client_id, client_secret, region):
        """Save configuration to environment file"""
        config = {
            'AWS_COGNITO_USER_POOL_ID': user_pool_id,
            'AWS_COGNITO_CLIENT_ID': client_id,
            'AWS_COGNITO_CLIENT_SECRET': client_secret,
            'AWS_REGION': region
        }
        
        # Save as .env file
        with open('.env', 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        # Save as JSON for reference
        with open('aws_cognito_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to .env and aws_cognito_config.json")
        print(f"   Make sure to add .env to your .gitignore file!")

def main():
    print("🚀 AWS Cognito Setup for Supplier Diversity Dashboard")
    print("=" * 60)
    
    # Get user input
    region = input("Enter AWS region (default: us-west-2): ").strip() or 'us-west-2'
    pool_name = input("Enter User Pool name (default: SupplierDiversityDashboard): ").strip() or 'SupplierDiversityDashboard'
    
    # Initialize setup
    setup = CognitoSetup(region)
    
    print(f"\n📝 Creating User Pool: {pool_name}")
    user_pool_id = setup.create_user_pool(pool_name)
    
    if not user_pool_id:
        print("❌ Failed to create User Pool. Exiting.")
        return
    
    print(f"\n📱 Creating User Pool Client...")
    client_id, client_secret = setup.create_user_pool_client(user_pool_id)
    
    if not client_id:
        print("❌ Failed to create User Pool Client. Exiting.")
        return
    
    # Ask if user wants to create admin user
    create_admin = input("\n👤 Create admin user? (y/n): ").strip().lower() == 'y'
    
    if create_admin:
        admin_username = input("Admin username: ").strip()
        admin_email = input("Admin email: ").strip()
        admin_name = input("Admin full name: ").strip()
        temp_password = input("Temporary password (min 8 chars, mixed case, numbers, symbols): ").strip()
        
        setup.create_admin_user(user_pool_id, admin_username, admin_email, temp_password, admin_name)
    
    # Save configuration
    print(f"\n💾 Saving configuration...")
    setup.save_config(user_pool_id, client_id, client_secret, region)
    
    print(f"\n🎉 Setup Complete!")
    print(f"=" * 60)
    print(f"Next steps:")
    print(f"1. Add the .env file to your .gitignore")
    print(f"2. Install required packages: pip install boto3 python-dotenv")
    print(f"3. Update your dashboard to use the authenticated version")
    print(f"4. Test the authentication system")
    
    if create_admin:
        print(f"5. Login with admin credentials and change the temporary password")

if __name__ == "__main__":
    main()
