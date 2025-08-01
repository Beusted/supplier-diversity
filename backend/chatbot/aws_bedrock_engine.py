"""
AWS Bedrock integration engine for Claude 3.0 Haiku chatbot
"""

import json
import os
import logging
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSBedrockEngine:
    """AWS Bedrock client for Claude 3.0 Haiku integration"""
    
    def __init__(self):
        """Initialize AWS Bedrock client"""
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        self.region_name = os.getenv('AWS_REGION', 'us-east-1')
        self.max_tokens = 4000
        self.temperature = 0.7
        
        # Initialize client
        self.bedrock_client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the Bedrock runtime client"""
        try:
            # Initialize Bedrock client
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.region_name,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                aws_session_token=os.getenv('AWS_SESSION_TOKEN')  # Optional for temporary credentials
            )
            
            logger.info("AWS Bedrock client initialized successfully")
            
        except NoCredentialsError:
            logger.error("AWS credentials not found. Please configure AWS credentials.")
            self.bedrock_client = None
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock client: {e}")
            self.bedrock_client = None
    
    def is_available(self) -> bool:
        """Check if AWS Bedrock is available"""
        return self.bedrock_client is not None
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response using Claude 3.0 Haiku via AWS Bedrock
        
        Args:
            prompt: User's input message
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated response from Claude
        """
        if not self.is_available():
            return "I'm currently unable to connect to AWS services. Please try again later."
        
        try:
            # Prepare the request body for Claude 3.0 Haiku
            messages = [{"role": "user", "content": prompt}]
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }
            
            # Add system prompt if provided
            if system_prompt:
                body["system"] = system_prompt
            
            # Invoke the model
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and response_body['content']:
                return response_body['content'][0]['text']
            else:
                logger.error(f"Unexpected response format: {response_body}")
                return "I encountered an error processing your request. Please try again."
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ValidationException':
                logger.error(f"Invalid request: {e}")
                return "I received an invalid request. Please rephrase your question."
            elif error_code == 'ThrottlingException':
                logger.error(f"Rate limit exceeded: {e}")
                return "I'm currently experiencing high demand. Please try again in a moment."
            else:
                logger.error(f"AWS Bedrock error: {e}")
                return "I'm experiencing technical difficulties. Please try again later."
                
        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {e}")
            return "I encountered an unexpected error. Please try again."
    
    def check_relevance(self, user_message: str) -> bool:
        """
        Check if user message is relevant to supplier diversity topics
        
        Args:
            user_message: The user's input message
            
        Returns:
            True if relevant, False if irrelevant
        """
        if not self.is_available():
            # Fallback to basic keyword matching if AWS unavailable
            return self._basic_relevance_check(user_message)
        
        relevance_prompt = f"""
You are a relevance checker for a supplier diversity and procurement chatbot. 

Determine if the following user message is relevant to supplier diversity, procurement, small business partnerships, or related business topics.

User message: "{user_message}"

Respond with only "RELEVANT" or "IRRELEVANT". 

RELEVANT topics include:
- Supplier diversity
- Procurement processes
- Small business partnerships
- Purchase orders
- Vendor management
- Business analytics related to suppliers
- Implementation strategies
- Data analysis for procurement

IRRELEVANT topics include:
- Personal questions
- General conversation
- Topics unrelated to business/procurement
- Technical support for unrelated software
- Weather, sports, entertainment
- Medical advice
- Legal advice outside of procurement
"""
        
        try:
            response = self.generate_response(relevance_prompt)
            return "RELEVANT" in response.upper()
        except Exception as e:
            logger.error(f"Error checking relevance: {e}")
            # Fallback to basic check
            return self._basic_relevance_check(user_message)
    
    def _basic_relevance_check(self, user_message: str) -> bool:
        """
        Basic keyword-based relevance check as fallback
        
        Args:
            user_message: The user's input message
            
        Returns:
            True if appears relevant based on keywords
        """
        relevant_keywords = [
            'supplier', 'procurement', 'small business', 'vendor', 'purchase',
            'contract', 'diversity', 'analytics', 'dashboard', 'data',
            'target', '25%', 'percentage', 'matching', 'algorithm',
            'tf-idf', 'similarity', 'implementation', 'strategy',
            'po', 'purchase order', 'business', 'analysis'
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in relevant_keywords)
    
    def create_context_prompt(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """
        Create a context-aware system prompt for supplier diversity chatbot
        
        Args:
            user_message: User's input message
            context_data: Current dashboard data and analytics
            
        Returns:
            Formatted system prompt with context
        """
        system_prompt = f"""
You are an AI assistant specialized in supplier diversity and procurement analytics. You help users understand and achieve their 25% small business procurement target.

CURRENT DATA CONTEXT:
- Current small business percentage: {context_data.get('current_percentage', 'N/A')}%
- Total purchase orders: {context_data.get('total_pos', 'N/A'):,}
- Small business POs: {context_data.get('current_small_business_pos', 'N/A'):,}
- Gap to target: {context_data.get('gap_pos_needed', 'N/A')} POs needed

KEY CAPABILITIES:
1. Explain supplier diversity targets and progress
2. Describe AI-powered supplier matching using TF-IDF and cosine similarity
3. Provide implementation strategies for reaching 25% target
4. Analyze procurement data and trends
5. Explain technical algorithms in simple terms

IMPORTANT GUIDELINES:
- Only respond to supplier diversity, procurement, and related business topics
- If asked about irrelevant topics, respond with: "I cannot help you with this. I specialize in supplier diversity and procurement analytics. Please ask about achieving your 25% small business target, supplier matching, or related procurement topics."
- Use data from the context when available
- Be helpful, professional, and concise
- Focus on actionable insights and recommendations

RESPONSE STYLE:
- Use markdown formatting for better readability
- Include relevant emojis for section headers
- Provide specific, data-driven answers when possible
- Break complex information into digestible sections
"""
        return system_prompt