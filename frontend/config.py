import os
from pathlib import Path
from typing import Optional

def load_env_file(env_path: Optional[str] = None):
    """
    Load environment variables from .env file
    This is a simple implementation - you can also use python-dotenv package
    """
    if env_path is None:
        # Look for .env file in parent directory (project root)
        env_path = Path(__file__).parent.parent / '.env'
    
    if not os.path.exists(env_path):
        print(f"⚠️  Warning: .env file not found at {env_path}")
        return
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ Environment variables loaded from {env_path}")
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")

# Load environment variables when this module is imported
load_env_file()

# Configuration class for easy access
class Config:
    """Configuration settings for the application"""
    
    # AWS Cognito settings
    AWS_COGNITO_USER_POOL_ID = os.getenv('AWS_COGNITO_USER_POOL_ID')
    AWS_COGNITO_CLIENT_ID = os.getenv('AWS_COGNITO_CLIENT_ID')
    AWS_COGNITO_CLIENT_SECRET = os.getenv('AWS_COGNITO_CLIENT_SECRET')
    AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
    
    # Application settings
    APP_NAME = "Supplier Diversity Dashboard"
    APP_VERSION = "1.0.0"
    
    # Security settings
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if all required configuration is present"""
        required_vars = [
            cls.AWS_COGNITO_USER_POOL_ID,
            cls.AWS_COGNITO_CLIENT_ID,
            cls.AWS_COGNITO_CLIENT_SECRET
        ]
        return all(var is not None for var in required_vars)
    
    @classmethod
    def get_missing_config(cls) -> list:
        """Get list of missing configuration variables"""
        missing = []
        if not cls.AWS_COGNITO_USER_POOL_ID:
            missing.append('AWS_COGNITO_USER_POOL_ID')
        if not cls.AWS_COGNITO_CLIENT_ID:
            missing.append('AWS_COGNITO_CLIENT_ID')
        if not cls.AWS_COGNITO_CLIENT_SECRET:
            missing.append('AWS_COGNITO_CLIENT_SECRET')
        return missing
