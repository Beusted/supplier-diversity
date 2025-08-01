"""
AI-powered chatbot engine for the Supplier Diversity Dashboard
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import re
import json
from pathlib import Path

class SupplierDiversityChatbot:
    """Main chatbot engine for supplier diversity questions"""
    
    def __init__(self):
        self.is_ai_enabled = True
        self.backend_dir = Path(__file__).parent.parent
        self.knowledge_base = self._load_knowledge_base()
        
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
            print(f"Warning: Could not load knowledge base: {e}")
            
        return knowledge
    
    def get_response(self, user_message: str, context_data: Optional[Dict] = None) -> str:
        """Generate AI response to user questions"""
        user_message = user_message.lower().strip()
        
        # Handle different types of questions
        if any(word in user_message for word in ['target', '25%', 'goal', 'percentage']):
            return self._handle_target_questions(context_data)
            
        elif any(word in user_message for word in ['supplier', 'match', 'similar', 'find']):
            return self._handle_supplier_questions(context_data)
            
        elif any(word in user_message for word in ['small business', 'small-business', 'sbe']):
            return self._handle_small_business_questions(context_data)
            
        elif any(word in user_message for word in ['how', 'what', 'why', 'explain']):
            return self._handle_explanation_questions(user_message, context_data)
            
        elif any(word in user_message for word in ['data', 'analytics', 'analysis']):
            return self._handle_data_questions(context_data)
            
        else:
            return self._handle_general_questions(user_message)
    
    def _handle_target_questions(self, context_data: Optional[Dict] = None) -> str:
        """Handle questions about the 25% target"""
        if context_data and 'current_percentage' in context_data:
            current = context_data['current_percentage']
            gap = 25.0 - current
            return f"""🎯 **25% Small Business Target Analysis**

**Current Status:** {current:.1f}% of POs go to small businesses
**Target:** 25.0%
**Gap:** {gap:.1f} percentage points to reach target

**Why 25%?** This target helps ensure small businesses get fair opportunities in procurement, promoting economic diversity and innovation.

**Next Steps:** Focus on transitioning {context_data.get('gap_pos_needed', 'additional')} POs to small businesses through our AI-powered supplier matching system."""
        
        return """🎯 **About the 25% Target**

The 25% small business procurement target is designed to:
- Promote economic diversity
- Support small business growth  
- Encourage innovation through diverse suppliers
- Meet organizational diversity goals

Use our dashboard analytics to track progress and identify transition opportunities!"""
    
    def _handle_supplier_questions(self, context_data: Optional[Dict] = None) -> str:
        """Handle supplier matching questions"""
        return """🔍 **AI-Powered Supplier Matching**

Our system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Cosine Similarity** to find the best small business matches for your current suppliers.

**How it works:**
1. **Text Analysis:** Analyzes supplier descriptions and services
2. **Similarity Scoring:** Calculates match confidence (0-1 scale)  
3. **Smart Recommendations:** Suggests high-confidence transitions

**Confidence Levels:**
- **High (≥0.4):** Strong match, low risk transition
- **Medium (≥0.2):** Good match, moderate planning needed
- **Low (<0.2):** Requires careful evaluation

Check the "PO Transition Scenarios" section for specific recommendations!"""
    
    def _handle_small_business_questions(self, context_data: Optional[Dict] = None) -> str:
        """Handle small business related questions"""
        if 'small_businesses' in self.knowledge_base:
            sb_data = self.knowledge_base['small_businesses']
            count = len(sb_data)
            return f"""🏢 **Small Business Database**

**Available Small Businesses:** {count} verified suppliers
**Categories:** {', '.join(sb_data['Category'].unique()[:5]) if 'Category' in sb_data.columns else 'Various industries'}

**Benefits of Small Business Partnerships:**
- Innovation and agility
- Personalized service
- Economic impact in local communities
- Diverse perspectives and solutions

Our AI system matches your current suppliers with these small businesses based on service similarity and capability alignment."""
        
        return """🏢 **Small Business Advantages**

**Why Choose Small Businesses:**
- **Innovation:** More agile and innovative solutions
- **Service:** Personalized attention and flexibility  
- **Impact:** Direct economic impact on communities
- **Diversity:** Brings diverse perspectives to your supply chain

**Our Role:** We help you identify the best small business matches for seamless transitions while maintaining service quality."""
    
    def _handle_explanation_questions(self, user_message: str, context_data: Optional[Dict] = None) -> str:
        """Handle how/what/why questions"""
        if 'tf-idf' in user_message or 'algorithm' in user_message:
            return """🧠 **TF-IDF Algorithm Explained**

**TF-IDF = Term Frequency × Inverse Document Frequency**

**Simple Explanation:**
- **TF:** How often important words appear in supplier descriptions
- **IDF:** How unique/important those words are across all suppliers
- **Result:** Numerical "fingerprint" for each supplier

**Cosine Similarity:** Measures how similar two supplier "fingerprints" are (0-1 scale)

**Example:** "Office Supplies" supplier matches well with "Office Equipment" supplier because they share the important word "Office"."""
            
        elif 'work' in user_message or 'process' in user_message:
            return """⚙️ **How Our System Works**

**Step 1:** Load your current supplier data
**Step 2:** Analyze supplier descriptions using AI
**Step 3:** Compare with small business database  
**Step 4:** Calculate similarity scores
**Step 5:** Rank recommendations by confidence
**Step 6:** Present actionable transition plans

**Result:** Data-driven recommendations for achieving your 25% small business target!"""
        
        return """💡 **General Information**

I'm here to help with questions about:
- Small business procurement targets
- Supplier matching algorithms  
- Dashboard analytics and data
- Implementation strategies
- TF-IDF and similarity analysis

Ask me anything about achieving your 25% small business procurement goal!"""
    
    def _handle_data_questions(self, context_data: Optional[Dict] = None) -> str:
        """Handle data and analytics questions"""
        if context_data:
            return f"""📊 **Current Data Overview**

**Procurement Status:**
- Current small business %: {context_data.get('current_percentage', 'N/A'):.1f}%
- Total POs analyzed: {context_data.get('total_pos', 'N/A'):,}
- Small business POs: {context_data.get('current_small_business_pos', 'N/A'):,}
- POs needed for target: {context_data.get('gap_pos_needed', 'N/A'):,}

**Data Sources:**
- Supplier matching analysis
- Historical procurement records
- Small business database
- AI similarity calculations

All data is processed using machine learning for accurate recommendations."""
        
        return """📊 **Data & Analytics**

Our dashboard analyzes:
- **Procurement Patterns:** Historical PO data
- **Supplier Profiles:** Service descriptions and capabilities
- **Similarity Metrics:** AI-calculated match scores
- **Implementation Plans:** Phased transition strategies

**Data Quality:** All recommendations are based on verified data and advanced ML algorithms for maximum accuracy."""
    
    def _handle_general_questions(self, user_message: str) -> str:
        """Handle general questions"""
        return """👋 **Hello! I'm your Supplier Diversity AI Assistant**

I can help you with:
- **Target Analysis:** Understanding the 25% small business goal
- **Supplier Matching:** How our AI finds the best matches
- **Data Insights:** Explaining dashboard analytics
- **Implementation:** Planning your transition strategy

**Try asking:**
- "How does the supplier matching work?"
- "What's our current progress toward 25%?"
- "Explain the TF-IDF algorithm"
- "Show me small business data"

What would you like to know about achieving your supplier diversity goals?"""
