"""
Claude-powered chatbot engine for supplier diversity dashboard
Integrates AWS Bedrock Claude 3.0 Haiku with existing data analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import re
import json
from pathlib import Path
import logging

from .aws_bedrock_engine import AWSBedrockEngine
from .data_analyzer import ProcurementDataAnalyzer
from .response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

class ClaudeSupplierDiversityChatbot:
    """Claude-powered chatbot engine for supplier diversity questions"""
    
    def __init__(self):
        """Initialize the Claude chatbot with AWS Bedrock integration"""
        self.backend_dir = Path(__file__).parent.parent
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize AWS Bedrock engine
        self.aws_engine = AWSBedrockEngine()
        
        # Initialize data analyzer and response generator as fallbacks
        try:
            self.data_analyzer = ProcurementDataAnalyzer()
            self.response_generator = ResponseGenerator()
            self.fallback_available = True
        except Exception as e:
            logger.warning(f"Fallback systems unavailable: {e}")
            self.fallback_available = False
        
        # Track conversation context
        self.conversation_context = []
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load procurement data for context"""
        knowledge = {}
        try:
            # Load test results for supplier matching context
            test_results_path = self.backend_dir / "test_results.csv"
            if test_results_path.exists():
                knowledge['test_results'] = pd.read_csv(test_results_path)
            
            # Load detailed analysis
            detailed_path = self.backend_dir / "detailed_similarity_analysis.csv"
            if detailed_path.exists():
                knowledge['detailed_analysis'] = pd.read_csv(detailed_path)
                
            # Load small businesses data
            small_biz_path = self.backend_dir / "sample_small_businesses.csv"
            if small_biz_path.exists():
                knowledge['small_businesses'] = pd.read_csv(small_biz_path)
                
        except Exception as e:
            logger.warning(f"Could not load knowledge base: {e}")
            
        return knowledge
    
    def get_response(self, user_message: str, context_data: Optional[Dict] = None) -> str:
        """
        Generate AI response to user questions using Claude 3.0 Haiku
        
        Args:
            user_message: User's input message
            context_data: Dashboard context data
            
        Returns:
            AI-generated response or fallback response
        """
        try:
            # Check if AWS Bedrock is available
            if not self.aws_engine.is_available():
                return self._get_fallback_response(user_message, context_data)
            
            # Check message relevance first
            if not self.aws_engine.check_relevance(user_message):
                return "I cannot help you with this. I specialize in supplier diversity and procurement analytics. Please ask about achieving your 25% small business target, supplier matching, or related procurement topics."
            
            # Prepare context data
            if context_data is None:
                context_data = self._generate_context_data()
            
            # Create system prompt with context
            system_prompt = self.aws_engine.create_context_prompt(user_message, context_data)
            
            # Add conversation history for context
            enhanced_message = self._enhance_message_with_context(user_message)
            
            # Generate response using Claude
            response = self.aws_engine.generate_response(enhanced_message, system_prompt)
            
            # Update conversation context
            self._update_conversation_context(user_message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating Claude response: {e}")
            return self._get_fallback_response(user_message, context_data)
    
    def _enhance_message_with_context(self, user_message: str) -> str:
        """
        Enhance user message with conversation context and data insights
        
        Args:
            user_message: Original user message
            
        Returns:
            Enhanced message with context
        """
        enhanced_parts = [user_message]
        
        # Add recent conversation context if available
        if self.conversation_context:
            recent_context = self.conversation_context[-2:]  # Last 2 exchanges
            context_summary = "Recent conversation: " + " | ".join([
                f"Q: {ctx['user']} A: {ctx['assistant'][:100]}..." 
                for ctx in recent_context
            ])
            enhanced_parts.append(f"\n\nContext: {context_summary}")
        
        # Add relevant data insights
        data_insights = self._get_relevant_data_insights(user_message)
        if data_insights:
            enhanced_parts.append(f"\n\nRelevant data: {data_insights}")
        
        return "\n".join(enhanced_parts)
    
    def _get_relevant_data_insights(self, user_message: str) -> str:
        """
        Extract relevant data insights based on user message keywords
        
        Args:
            user_message: User's input message
            
        Returns:
            Relevant data insights as string
        """
        insights = []
        message_lower = user_message.lower()
        
        try:
            # Supplier matching insights
            if any(word in message_lower for word in ['match', 'similar', 'supplier', 'find']):
                if 'test_results' in self.knowledge_base:
                    df = self.knowledge_base['test_results']
                    if not df.empty and 'similarity_score' in df.columns:
                        avg_score = df['similarity_score'].mean()
                        high_matches = len(df[df['similarity_score'] >= 0.4])
                        insights.append(f"Average similarity score: {avg_score:.2f}, High-confidence matches: {high_matches}")
            
            # Small business insights
            if any(word in message_lower for word in ['small business', 'sbe', 'database']):
                if 'small_businesses' in self.knowledge_base:
                    df = self.knowledge_base['small_businesses']
                    if not df.empty:
                        count = len(df)
                        categories = df['Category'].nunique() if 'Category' in df.columns else 'Unknown'
                        insights.append(f"Small business database: {count} suppliers across {categories} categories")
            
        except Exception as e:
            logger.debug(f"Error extracting data insights: {e}")
        
        return " | ".join(insights) if insights else ""
    
    def _update_conversation_context(self, user_message: str, assistant_response: str):
        """
        Update conversation context for better continuity
        
        Args:
            user_message: User's message
            assistant_response: Assistant's response
        """
        self.conversation_context.append({
            'user': user_message,
            'assistant': assistant_response
        })
        
        # Keep only last 5 exchanges to manage memory
        if len(self.conversation_context) > 5:
            self.conversation_context = self.conversation_context[-5:]
    
    def _generate_context_data(self) -> Dict[str, Any]:
        """
        Generate context data from available knowledge base
        
        Returns:
            Context data dictionary
        """
        context = {
            'current_percentage': 0.0,
            'total_pos': 0,
            'current_small_business_pos': 0,
            'gap_pos_needed': 0
        }
        
        try:
            # Try to extract from test results
            if 'test_results' in self.knowledge_base:
                df = self.knowledge_base['test_results']
                if not df.empty:
                    # Calculate basic metrics
                    context['total_pos'] = len(df)
                    
                    # Estimate current small business percentage
                    if 'is_small_business' in df.columns:
                        current_sb = df['is_small_business'].sum()
                        context['current_small_business_pos'] = current_sb
                        context['current_percentage'] = (current_sb / len(df)) * 100
                        
                        # Calculate gap
                        target_pos = len(df) * 0.25
                        context['gap_pos_needed'] = max(0, int(target_pos - current_sb))
            
        except Exception as e:
            logger.debug(f"Error generating context data: {e}")
        
        return context
    
    def _get_fallback_response(self, user_message: str, context_data: Optional[Dict] = None) -> str:
        """
        Generate fallback response when Claude is unavailable
        
        Args:
            user_message: User's input message
            context_data: Dashboard context data
            
        Returns:
            Fallback response
        """
        if self.fallback_available:
            try:
                # Use original chatbot engine as fallback
                from .chatbot_engine import SupplierDiversityChatbot
                fallback_bot = SupplierDiversityChatbot()
                return fallback_bot.get_response(user_message, context_data)
            except Exception as e:
                logger.error(f"Fallback system error: {e}")
        
        # Basic fallback based on keywords
        return self._basic_keyword_response(user_message)
    
    def _basic_keyword_response(self, user_message: str) -> str:
        """
        Generate basic response based on keyword matching
        
        Args:
            user_message: User's input message
            
        Returns:
            Basic keyword-based response
        """
        message_lower = user_message.lower()
        
        # Check for irrelevant topics
        irrelevant_keywords = [
            'weather', 'sports', 'movie', 'music', 'food', 'personal',
            'health', 'medical', 'dating', 'relationship', 'politics'
        ]
        
        if any(keyword in message_lower for keyword in irrelevant_keywords):
            return "I cannot help you with this. I specialize in supplier diversity and procurement analytics. Please ask about achieving your 25% small business target, supplier matching, or related procurement topics."
        
        # Basic responses for relevant topics
        if any(word in message_lower for word in ['target', '25%', 'goal']):
            return """🎯 **25% Small Business Target**

The 25% target helps ensure small businesses get fair opportunities in procurement, promoting economic diversity and innovation. Our AI-powered system helps identify the best small business matches for your current suppliers.

Ask me about supplier matching or implementation strategies!"""
        
        elif any(word in message_lower for word in ['supplier', 'match', 'similar']):
            return """🔍 **AI-Powered Supplier Matching**

Our system uses TF-IDF and Cosine Similarity to find the best small business matches:
- Analyzes supplier descriptions 
- Calculates similarity scores (0-1 scale)
- Provides confidence-based recommendations

Ask me to explain the algorithm or show current matching data!"""
        
        elif any(word in message_lower for word in ['hello', 'hi', 'help']):
            return """👋 **Hello! I'm your Supplier Diversity AI Assistant**

I can help with:
- **Target Analysis**: Progress toward 25% small business goal
- **Supplier Matching**: AI-powered recommendations
- **Data Insights**: Dashboard analytics explained
- **Implementation**: Strategic planning advice

What would you like to know about achieving your supplier diversity goals?"""
        
        else:
            return """💡 **I'm here to help with supplier diversity!**

Try asking about:
- "How does supplier matching work?"
- "What's our progress toward 25%?"
- "Explain the TF-IDF algorithm"
- "Show me implementation strategies"

What specific aspect would you like to explore?"""
    
    def reset_conversation(self):
        """Reset conversation context"""
        self.conversation_context = []
        logger.info("Conversation context reset")
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and capabilities
        
        Returns:
            System status information
        """
        return {
            'aws_bedrock_available': self.aws_engine.is_available(),
            'fallback_available': self.fallback_available,
            'knowledge_base_loaded': bool(self.knowledge_base),
            'conversation_length': len(self.conversation_context),
            'model_id': self.aws_engine.model_id if self.aws_engine.is_available() else None
        }