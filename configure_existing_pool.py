#!/usr/bin/env python3
"""
Configuration script for existing AWS Cognito User Pool
Use this when you already have a User Pool created
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

def list_user_pools(region='us-west-2'):
    """List all user pools in the region"""
    try:
        cognito_client = boto3.client('cognito-idp', region_name=region)
        response = cognito_client.list_user_pools(MaxResults=50)
        
        print(f"📋 User Pools in {region}:")
        print("-" * 50)
        
        for i, pool in enumerate(response['UserPools'], 1):
            print(f"{i}. Name: {pool['Name']}")
            print(f"   ID: {pool['Id']}")
            print(f"   Created: {pool['CreationDate']}")
            print()
        
        return response['UserPools']
    except ClientError as e:
        print(f"❌ Error listing user pools: {e}")
        return []

def get_user_pool_details(user_pool_id, region='us-west-2'):
    """Get detailed information about a user pool"""
    try:
        cognito_client = boto3.client('cognito-idp', region_name=region)
        response = cognito_client.describe_user_pool(UserPoolId=user_pool_id)
        
        pool = response['UserPool']
        print(f"📊 User Pool Details:")
        print(f"   Name: {pool['Name']}")
        print(f"   ID: {pool['Id']}")
        print(f"   Status: {pool['Status']}")
        print(f"   Domain: {pool.get('Domain', 'Not configured')}")
        
        return pool
    except ClientError as e:
        print(f"❌ Error getting user pool details: {e}")
        return None

def list_user_pool_clients(user_pool_id, region='us-west-2'):
    """List all app clients for a user pool"""
    try:
        cognito_client = boto3.client('cognito-idp', region_name=region)
        response = cognito_client.list_user_pool_clients(
            UserPoolId=user_pool_id,
            MaxResults=50
        )
        
        print(f"📱 App Clients:")
        print("-" * 30)
        
        for i, client in enumerate(response['UserPoolClients'], 1):
            print(f"{i}. Name: {client['ClientName']}")
            print(f"   ID: {client['ClientId']}")
            print(f"   Created: {client['CreationDate']}")
            print()
        
        return response['UserPoolClients']
    except ClientError as e:
        print(f"❌ Error listing app clients: {e}")
        return []

def get_client_details(user_pool_id, client_id, region='us-west-2'):
    """Get detailed information about an app client"""
    try:
        cognito_client = boto3.client('cognito-idp', region_name=region)
        response = cognito_client.describe_user_pool_client(
            UserPoolId=user_pool_id,
            ClientId=client_id
        )
        
        client = response['UserPoolClient']
        print(f"🔧 App Client Details:")
        print(f"   Name: {client['ClientName']}")
        print(f"   ID: {client['ClientId']}")
        print(f"   Has Secret: {'Yes' if 'ClientSecret' in client else 'No'}")
        print(f"   Auth Flows: {', '.join(client.get('ExplicitAuthFlows', []))}")
        
        return client
    except ClientError as e:
        print(f"❌ Error getting client details: {e}")
        return None

def create_app_client(user_pool_id, region='us-west-2'):
    """Create a new app client for the dashboard"""
    try:
        cognito_client = boto3.client('cognito-idp', region_name=region)
        
        print("🔨 Creating new app client for dashboard...")
        
        response = cognito_client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName="SupplierDiversityDashboard",
            GenerateSecret=True,
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
                'name'
            ],
            WriteAttributes=[
                'email',
                'name'
            ],
            PreventUserExistenceErrors='ENABLED'
        )
        
        client_id = response['UserPoolClient']['ClientId']
        client_secret = response['UserPoolClient']['ClientSecret']
        
        print(f"✅ App client created successfully!")
        print(f"   Client ID: {client_id}")
        print(f"   Client Secret: {client_secret}")
        
        return client_id, client_secret
        
    except ClientError as e:
        print(f"❌ Error creating app client: {e}")
        return None, None

def save_configuration(user_pool_id, client_id, client_secret, region):
    """Save configuration to .env file"""
    config_content = f"""# AWS Cognito Configuration
AWS_COGNITO_USER_POOL_ID={user_pool_id}
AWS_COGNITO_CLIENT_ID={client_id}
AWS_COGNITO_CLIENT_SECRET={client_secret}
AWS_REGION={region}

# Optional: Session timeout (minutes)
SESSION_TIMEOUT_MINUTES=60
"""
    
    # Save .env file
    with open('.env', 'w') as f:
        f.write(config_content)
    
    # Save JSON config for reference
    config_json = {
        'AWS_COGNITO_USER_POOL_ID': user_pool_id,
        'AWS_COGNITO_CLIENT_ID': client_id,
        'AWS_COGNITO_CLIENT_SECRET': client_secret,
        'AWS_REGION': region
    }
    
    with open('aws_cognito_config.json', 'w') as f:
        json.dump(config_json, f, indent=2)
    
    print(f"✅ Configuration saved to .env and aws_cognito_config.json")
    print(f"⚠️  Make sure to add .env to your .gitignore file!")

def main():
    print("🔧 Configure Existing AWS Cognito User Pool")
    print("=" * 50)
    
    # Get region
    region = input("Enter AWS region (default: us-west-2): ").strip() or 'us-west-2'
    
    # List user pools
    pools = list_user_pools(region)
    if not pools:
        print("❌ No user pools found. Please create one first.")
        return
    
    # Get user pool selection
    while True:
        try:
            choice = input(f"\nSelect user pool (1-{len(pools)}): ").strip()
            pool_index = int(choice) - 1
            if 0 <= pool_index < len(pools):
                selected_pool = pools[pool_index]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    user_pool_id = selected_pool['Id']
    print(f"\n✅ Selected: {selected_pool['Name']} ({user_pool_id})")
    
    # Get pool details
    get_user_pool_details(user_pool_id, region)
    
    # List existing clients
    print(f"\n📱 Checking existing app clients...")
    clients = list_user_pool_clients(user_pool_id, region)
    
    # Ask if user wants to use existing client or create new one
    if clients:
        print(f"\nFound {len(clients)} existing app client(s).")
        use_existing = input("Use existing app client? (y/n): ").strip().lower() == 'y'
        
        if use_existing:
            while True:
                try:
                    choice = input(f"Select app client (1-{len(clients)}): ").strip()
                    client_index = int(choice) - 1
                    if 0 <= client_index < len(clients):
                        selected_client = clients[client_index]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a number.")
            
            client_id = selected_client['ClientId']
            
            # Get client details
            client_details = get_client_details(user_pool_id, client_id, region)
            
            if client_details and 'ClientSecret' in client_details:
                client_secret = client_details['ClientSecret']
                print(f"✅ Using existing client with secret")
            else:
                print("❌ Selected client doesn't have a secret. Creating new client...")
                client_id, client_secret = create_app_client(user_pool_id, region)
        else:
            client_id, client_secret = create_app_client(user_pool_id, region)
    else:
        print("No existing app clients found. Creating new one...")
        client_id, client_secret = create_app_client(user_pool_id, region)
    
    if not client_id or not client_secret:
        print("❌ Failed to get app client configuration.")
        return
    
    # Save configuration
    print(f"\n💾 Saving configuration...")
    save_configuration(user_pool_id, client_id, client_secret, region)
    
    print(f"\n🎉 Configuration Complete!")
    print(f"=" * 50)
    print(f"Next steps:")
    print(f"1. Install dependencies: pip install -r requirements.txt")
    print(f"2. Test configuration: python test_auth_setup.py")
    print(f"3. Start dashboard: python start_dashboard.py")

if __name__ == "__main__":
    main()
