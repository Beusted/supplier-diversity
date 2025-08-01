#!/usr/bin/env python3
"""
Quick setup for existing AWS Cognito User Pool
Just enter your User Pool details and we'll create the configuration
"""

def create_env_file(user_pool_id, client_id, client_secret, region):
    """Create .env file with configuration"""
    config_content = f"""# AWS Cognito Configuration
AWS_COGNITO_USER_POOL_ID={user_pool_id}
AWS_COGNITO_CLIENT_ID={client_id}
AWS_COGNITO_CLIENT_SECRET={client_secret}
AWS_REGION={region}

# Optional: Session timeout (minutes)
SESSION_TIMEOUT_MINUTES=60
"""
    
    with open('.env', 'w') as f:
        f.write(config_content)
    
    print("✅ Configuration saved to .env file")
    print("⚠️  Make sure .env is in your .gitignore file!")

def main():
    print("🚀 Quick Setup for Supplier Diversity Dashboard")
    print("=" * 50)
    print("Enter your AWS Cognito details:")
    print()
    
    # Get user input
    region = input("AWS Region (e.g., us-west-2): ").strip()
    user_pool_id = input("User Pool ID (e.g., us-west-2_xxxxxxxxx): ").strip()
    client_id = input("App Client ID: ").strip()
    client_secret = input("App Client Secret: ").strip()
    
    # Validate input
    if not all([region, user_pool_id, client_id, client_secret]):
        print("❌ All fields are required!")
        return
    
    # Create configuration
    create_env_file(user_pool_id, client_id, client_secret, region)
    
    print("\n🎉 Setup Complete!")
    print("=" * 30)
    print("Next steps:")
    print("1. Run: python test_auth_setup.py")
    print("2. Run: python start_dashboard.py")
    print("3. Register your first user!")

if __name__ == "__main__":
    main()
