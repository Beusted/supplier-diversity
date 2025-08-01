import streamlit as st
import boto3
import hmac
import hashlib
import base64
import json
from botocore.exceptions import ClientError
from typing import Dict, Optional, Tuple
import os
from datetime import datetime, timedelta

class CognitoAuthManager:
    """
    AWS Cognito authentication manager for Streamlit applications
    """
    
    def __init__(self):
        # AWS Cognito configuration - these should be set as environment variables
        self.user_pool_id = os.getenv('AWS_COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('AWS_COGNITO_CLIENT_ID')
        self.client_secret = os.getenv('AWS_COGNITO_CLIENT_SECRET')
        self.region = os.getenv('AWS_REGION', 'us-west-2')
        
        # Initialize Cognito client
        self.cognito_client = boto3.client('cognito-idp', region_name=self.region)
        
        # Session keys
        self.SESSION_KEY_USER = 'authenticated_user'
        self.SESSION_KEY_TOKEN = 'access_token'
        self.SESSION_KEY_REFRESH = 'refresh_token'
        self.SESSION_KEY_EXPIRES = 'token_expires'
    
    def _calculate_secret_hash(self, username: str) -> str:
        """Calculate the secret hash for Cognito client"""
        if not self.client_secret:
            return None
            
        message = username + self.client_id
        dig = hmac.new(
            str(self.client_secret).encode('utf-8'),
            msg=str(message).encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
    
    def register_user(self, username: str, password: str, email: str, 
                     full_name: str = "") -> Tuple[bool, str]:
        """
        Register a new user with AWS Cognito
        
        Args:
            username: Username for the new user
            password: Password for the new user
            email: Email address for the new user
            full_name: Full name of the user (optional)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Prepare user attributes
            user_attributes = [
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'}
            ]
            
            if full_name:
                user_attributes.append({'Name': 'name', 'Value': full_name})
            
            # Prepare parameters
            params = {
                'ClientId': self.client_id,
                'Username': username,
                'Password': password,
                'UserAttributes': user_attributes
            }
            
            # Add secret hash if client secret is configured
            secret_hash = self._calculate_secret_hash(username)
            if secret_hash:
                params['SecretHash'] = secret_hash
            
            # Register user
            response = self.cognito_client.sign_up(**params)
            
            return True, "User registered successfully. Please check your email for verification."
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'UsernameExistsException':
                return False, "Username already exists. Please choose a different username."
            elif error_code == 'InvalidPasswordException':
                return False, "Password does not meet requirements. Please use a stronger password."
            elif error_code == 'InvalidParameterException':
                return False, "Invalid parameters provided. Please check your input."
            else:
                return False, f"Registration failed: {error_message}"
        except Exception as e:
            return False, f"Unexpected error during registration: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Dict]:
        """
        Authenticate user with AWS Cognito
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Tuple of (success: bool, message: str, user_data: Dict)
        """
        try:
            # Prepare parameters
            params = {
                'ClientId': self.client_id,
                'AuthFlow': 'USER_PASSWORD_AUTH',
                'AuthParameters': {
                    'USERNAME': username,
                    'PASSWORD': password
                }
            }
            
            # Add secret hash if client secret is configured
            secret_hash = self._calculate_secret_hash(username)
            if secret_hash:
                params['AuthParameters']['SECRET_HASH'] = secret_hash
            
            # Authenticate
            response = self.cognito_client.initiate_auth(**params)
            
            # Extract tokens
            auth_result = response['AuthenticationResult']
            access_token = auth_result['AccessToken']
            refresh_token = auth_result['RefreshToken']
            expires_in = auth_result['ExpiresIn']  # seconds
            
            # Get user info
            user_info = self.cognito_client.get_user(AccessToken=access_token)
            
            # Parse user attributes
            user_data = {
                'username': username,
                'attributes': {}
            }
            
            for attr in user_info['UserAttributes']:
                user_data['attributes'][attr['Name']] = attr['Value']
            
            # Store in session
            st.session_state[self.SESSION_KEY_USER] = user_data
            st.session_state[self.SESSION_KEY_TOKEN] = access_token
            st.session_state[self.SESSION_KEY_REFRESH] = refresh_token
            st.session_state[self.SESSION_KEY_EXPIRES] = datetime.now() + timedelta(seconds=expires_in)
            
            return True, "Login successful!", user_data
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'NotAuthorizedException':
                return False, "Invalid username or password.", {}
            elif error_code == 'UserNotConfirmedException':
                return False, "User account not confirmed. Please check your email for verification.", {}
            elif error_code == 'UserNotFoundException':
                return False, "User not found. Please check your username or register.", {}
            else:
                return False, f"Authentication failed: {error_message}", {}
        except Exception as e:
            return False, f"Unexpected error during authentication: {str(e)}", {}
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        if self.SESSION_KEY_USER not in st.session_state:
            return False
        
        if self.SESSION_KEY_EXPIRES not in st.session_state:
            return False
        
        # Check if token is expired
        if datetime.now() > st.session_state[self.SESSION_KEY_EXPIRES]:
            self.logout()
            return False
        
        return True
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user data"""
        if self.is_authenticated():
            return st.session_state[self.SESSION_KEY_USER]
        return None
    
    def logout(self):
        """Logout current user"""
        # Clear session state
        keys_to_clear = [
            self.SESSION_KEY_USER,
            self.SESSION_KEY_TOKEN,
            self.SESSION_KEY_REFRESH,
            self.SESSION_KEY_EXPIRES
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def refresh_token(self) -> bool:
        """Refresh the access token using refresh token"""
        try:
            if self.SESSION_KEY_REFRESH not in st.session_state:
                return False
            
            refresh_token = st.session_state[self.SESSION_KEY_REFRESH]
            username = st.session_state[self.SESSION_KEY_USER]['username']
            
            # Prepare parameters
            params = {
                'ClientId': self.client_id,
                'AuthFlow': 'REFRESH_TOKEN_AUTH',
                'AuthParameters': {
                    'REFRESH_TOKEN': refresh_token
                }
            }
            
            # Add secret hash if client secret is configured
            secret_hash = self._calculate_secret_hash(username)
            if secret_hash:
                params['AuthParameters']['SECRET_HASH'] = secret_hash
            
            # Refresh token
            response = self.cognito_client.initiate_auth(**params)
            
            # Update session with new token
            auth_result = response['AuthenticationResult']
            access_token = auth_result['AccessToken']
            expires_in = auth_result['ExpiresIn']
            
            st.session_state[self.SESSION_KEY_TOKEN] = access_token
            st.session_state[self.SESSION_KEY_EXPIRES] = datetime.now() + timedelta(seconds=expires_in)
            
            return True
            
        except Exception as e:
            st.error(f"Token refresh failed: {str(e)}")
            self.logout()
            return False
    
    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        try:
            if not self.is_authenticated():
                return False, "User not authenticated"
            
            access_token = st.session_state[self.SESSION_KEY_TOKEN]
            
            self.cognito_client.change_password(
                AccessToken=access_token,
                PreviousPassword=old_password,
                ProposedPassword=new_password
            )
            
            return True, "Password changed successfully"
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'NotAuthorizedException':
                return False, "Current password is incorrect"
            elif error_code == 'InvalidPasswordException':
                return False, "New password does not meet requirements"
            else:
                return False, f"Password change failed: {error_message}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

# Global auth manager instance
auth_manager = CognitoAuthManager()
