"""
Response generator for creating contextual chatbot responses
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import re

class ResponseGenerator:
    """Generates contextual responses for the chatbot"""
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
    
    def _load_response_templates(self) -> Dict[str, str]:
        """Load response templates for different question types"""
        return {
            'greeting': """👋 **Welcome to your Supplier Diversity AI Assistant!**

I'm here to help you achieve your 25% small business procurement target. I can assist with:

🎯 **Target Analysis** - Current progress and gap analysis
🔍 **Supplier Matching** - AI-powered recommendations  
📊 **Data Insights** - Analytics and trends
📋 **Implementation** - Strategic planning advice

What would you like to explore first?""",

            'target_status': """🎯 **Current Target Progress**

**Status:** {current_percentage:.1f}% of POs go to small businesses
**Target:** 25.0%
**Gap:** {gap:.1f} percentage points remaining

**Action Needed:** Transition {gap_pos_needed:,} additional POs to small businesses

**Quick Wins Available:** {high_confidence_matches} high-confidence supplier matches ready for transition!""",

            'supplier_matching': """🔍 **AI Supplier Matching Results**

**Total Matches Found:** {total_matches:,}
**High Confidence (≥0.4):** {high_confidence_matches} matches
**Medium Confidence (≥0.2):** {medium_confidence_matches} matches
**Average Match Score:** {average_similarity:.2f}

**Best Match:** {best_match_score:.2f} similarity score

Our TF-IDF algorithm analyzes supplier descriptions to find the most compatible small business alternatives.""",

            'implementation_plan': """📋 **Implementation Strategy**

**Phase 1 - Quick Wins (High Confidence)**
- Transition {high_conf_pos} POs immediately
- Low risk, high success probability
- Achieves {high_conf_percentage:.1f}% small business rate

**Phase 2 - Strategic Transitions (Medium Confidence)**  
- Transition additional {medium_conf_pos} POs
- Requires more planning and evaluation
- Final target: {final_percentage:.1f}%

**Timeline:** 3-6 months for full implementation""",

            'data_summary': """📊 **Data Overview**

**Procurement Analysis:**
- Total POs: {total_pos:,}
- Current small business POs: {current_small_business_pos:,}
- Small businesses in database: {total_businesses}

**Top Categories:**
{top_categories_text}

**Match Quality:** {average_similarity:.1%} average similarity score indicates strong matching potential.""",

            'algorithm_explanation': """🧠 **How Our AI Matching Works**

**TF-IDF (Term Frequency-Inverse Document Frequency):**
1. Analyzes words in supplier descriptions
2. Identifies important/unique terms
3. Creates numerical "fingerprints" for each supplier

**Cosine Similarity:**
- Measures how similar two supplier fingerprints are
- Scale: 0 (no similarity) to 1 (identical)
- ≥0.4 = High confidence match

**Example:** "Office Supplies Inc." matches well with "Business Office Equipment LLC" because they share key terms like "office" and similar service descriptions.""",

            'small_business_info': """🏢 **Small Business Database**

**Available Suppliers:** {total_businesses} verified small businesses
**Categories Covered:** {category_count} different service areas

**Top Service Areas:**
{top_categories_text}

**Why Small Businesses?**
- Innovation and agility
- Personalized service  
- Economic community impact
- Diverse perspectives

Our AI ensures you find the best matches while maintaining service quality.""",

            'error_fallback': """⚠️ **Data Temporarily Unavailable**

I'm having trouble accessing some data right now, but I can still help with:

- General supplier diversity questions
- Algorithm explanations
- Implementation strategies
- Best practices

Try asking: "How does the matching algorithm work?" or "What are the benefits of small business partnerships?"

""",

            'unknown_query': """🤔 **I'd be happy to help!**

I specialize in supplier diversity and procurement analytics. Try asking about:

**📊 Analytics:** "What's our current progress?" or "Show me the data"
**🔍 Matching:** "How does supplier matching work?" or "Find similar suppliers"  
**🎯 Strategy:** "How do we reach 25%?" or "What's the implementation plan?"
**🧠 Technical:** "Explain the algorithm" or "How does TF-IDF work?"

What specific aspect of supplier diversity would you like to explore?"""
        }
    
    def generate_response(self, query_type: str, context_data: Dict[str, Any]) -> str:
        """Generate a response based on query type and context"""
        
        if query_type == 'greeting':
            return self.response_templates['greeting']
        
        elif query_type == 'target_status':
            return self._generate_target_status_response(context_data)
        
        elif query_type == 'supplier_matching':
            return self._generate_supplier_matching_response(context_data)
        
        elif query_type == 'implementation_plan':
            return self._generate_implementation_response(context_data)
        
        elif query_type == 'data_summary':
            return self._generate_data_summary_response(context_data)
        
        elif query_type == 'algorithm_explanation':
            return self.response_templates['algorithm_explanation']
        
        elif query_type == 'small_business_info':
            return self._generate_small_business_response(context_data)
        
        elif query_type == 'error_fallback':
            return self.response_templates['error_fallback']
        
        else:
            return self.response_templates['unknown_query']
    
    def _generate_target_status_response(self, context_data: Dict[str, Any]) -> str:
        """Generate target status response with current data"""
        try:
            current_percentage = context_data.get('current_percentage', 0)
            gap = 25.0 - current_percentage
            gap_pos_needed = context_data.get('gap_pos_needed', 0)
            
            # Get supplier insights if available
            supplier_insights = context_data.get('supplier_insights', {})
            high_confidence_matches = supplier_insights.get('high_confidence_matches', 0)
            
            return self.response_templates['target_status'].format(
                current_percentage=current_percentage,
                gap=gap,
                gap_pos_needed=gap_pos_needed,
                high_confidence_matches=high_confidence_matches
            )
        except Exception:
            return self.response_templates['error_fallback']
    
    def _generate_supplier_matching_response(self, context_data: Dict[str, Any]) -> str:
        """Generate supplier matching response"""
        try:
            supplier_insights = context_data.get('supplier_insights', {})
            
            return self.response_templates['supplier_matching'].format(
                total_matches=supplier_insights.get('total_matches', 0),
                high_confidence_matches=supplier_insights.get('high_confidence_matches', 0),
                medium_confidence_matches=supplier_insights.get('medium_confidence_matches', 0),
                average_similarity=supplier_insights.get('average_similarity', 0),
                best_match_score=supplier_insights.get('best_match_score', 0)
            )
        except Exception:
            return self.response_templates['error_fallback']
    
    def _generate_implementation_response(self, context_data: Dict[str, Any]) -> str:
        """Generate implementation plan response"""
        try:
            scenarios = context_data.get('transition_scenarios', {})
            high_conf = scenarios.get('high_confidence', {})
            medium_conf = scenarios.get('medium_confidence', {})
            
            return self.response_templates['implementation_plan'].format(
                high_conf_pos=high_conf.get('pos_to_transition', 0),
                high_conf_percentage=high_conf.get('resulting_percentage', 0),
                medium_conf_pos=medium_conf.get('pos_to_transition', 0),
                final_percentage=medium_conf.get('resulting_percentage', 0)
            )
        except Exception:
            return self.response_templates['error_fallback']
    
    def _generate_data_summary_response(self, context_data: Dict[str, Any]) -> str:
        """Generate data summary response"""
        try:
            # Basic stats
            total_pos = context_data.get('total_pos', 0)
            current_small_business_pos = context_data.get('current_small_business_pos', 0)
            
            # Small business data
            sb_data = context_data.get('small_business_data', {})
            total_businesses = sb_data.get('total_businesses', 0)
            
            # Top categories
            top_categories = sb_data.get('top_categories', {})
            top_categories_text = self._format_top_categories(top_categories)
            
            # Supplier insights
            supplier_insights = context_data.get('supplier_insights', {})
            average_similarity = supplier_insights.get('average_similarity', 0)
            
            return self.response_templates['data_summary'].format(
                total_pos=total_pos,
                current_small_business_pos=current_small_business_pos,
                total_businesses=total_businesses,
                top_categories_text=top_categories_text,
                average_similarity=average_similarity
            )
        except Exception:
            return self.response_templates['error_fallback']
    
    def _generate_small_business_response(self, context_data: Dict[str, Any]) -> str:
        """Generate small business info response"""
        try:
            sb_data = context_data.get('small_business_data', {})
            total_businesses = sb_data.get('total_businesses', 0)
            categories = sb_data.get('categories', [])
            top_categories = sb_data.get('top_categories', {})
            
            top_categories_text = self._format_top_categories(top_categories)
            
            return self.response_templates['small_business_info'].format(
                total_businesses=total_businesses,
                category_count=len(categories),
                top_categories_text=top_categories_text
            )
        except Exception:
            return self.response_templates['error_fallback']
    
    def _format_top_categories(self, top_categories: Dict[str, int]) -> str:
        """Format top categories for display"""
        if not top_categories:
            return "- Data loading..."
        
        formatted = []
        for category, count in list(top_categories.items())[:5]:
            formatted.append(f"- {category}: {count} suppliers")
        
        return "\n".join(formatted)
    
    def classify_query(self, user_message: str) -> str:
        """Classify the user query to determine response type"""
        user_message = user_message.lower().strip()
        
        # Greeting patterns
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'start', 'help']):
            return 'greeting'
        
        # Target/status questions
        if any(word in user_message for word in ['target', '25%', 'progress', 'status', 'current']):
            return 'target_status'
        
        # Supplier matching questions
        if any(word in user_message for word in ['supplier', 'match', 'similar', 'find', 'recommend']):
            return 'supplier_matching'
        
        # Implementation questions
        if any(word in user_message for word in ['plan', 'implement', 'strategy', 'how to', 'steps']):
            return 'implementation_plan'
        
        # Data questions
        if any(word in user_message for word in ['data', 'analytics', 'summary', 'overview', 'stats']):
            return 'data_summary'
        
        # Algorithm questions
        if any(word in user_message for word in ['algorithm', 'tf-idf', 'cosine', 'similarity', 'how does', 'explain']):
            return 'algorithm_explanation'
        
        # Small business questions
        if any(word in user_message for word in ['small business', 'sbe', 'database', 'suppliers']):
            return 'small_business_info'
        
        # Default to unknown
        return 'unknown_query'
