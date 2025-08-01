"""
Data analyzer for procurement analytics and insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class ProcurementDataAnalyzer:
    """Analyzes procurement data for chatbot insights"""
    
    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent
        self.data_cache = {}
        self._load_data()
    
    def _load_data(self):
        """Load all available data files"""
        try:
            # Load test results
            test_results_path = self.backend_dir / "test_results.csv"
            if test_results_path.exists():
                self.data_cache['test_results'] = pd.read_csv(test_results_path)
            
            # Load detailed analysis
            detailed_path = self.backend_dir / "detailed_similarity_analysis.csv"
            if detailed_path.exists():
                self.data_cache['detailed_analysis'] = pd.read_csv(detailed_path)
            
            # Load small businesses
            small_biz_path = self.backend_dir / "sample_small_businesses.csv"
            if small_biz_path.exists():
                self.data_cache['small_businesses'] = pd.read_csv(small_biz_path)
                
            # Load category analysis
            category_path = self.backend_dir / "category_analysis.csv"
            if category_path.exists():
                self.data_cache['category_analysis'] = pd.read_csv(category_path)
                
        except Exception as e:
            print(f"Warning: Could not load some data files: {e}")
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current procurement statistics"""
        if 'test_results' not in self.data_cache:
            return self._get_demo_stats()
        
        df = self.data_cache['test_results']
        
        # Calculate basic stats
        total_pos = len(df)
        current_small_business_pos = len(df[df['is_small_business'] == True])
        current_percentage = (current_small_business_pos / total_pos) * 100 if total_pos > 0 else 0
        
        # Calculate gap to 25%
        target_percentage = 25.0
        target_pos = int(total_pos * (target_percentage / 100))
        gap_pos_needed = max(0, target_pos - current_small_business_pos)
        
        return {
            'total_pos': total_pos,
            'current_small_business_pos': current_small_business_pos,
            'current_percentage': current_percentage,
            'target_percentage': target_percentage,
            'target_pos': target_pos,
            'gap_pos_needed': gap_pos_needed
        }
    
    def _get_demo_stats(self) -> Dict[str, Any]:
        """Return demo statistics when real data isn't available"""
        return {
            'total_pos': 1000,
            'current_small_business_pos': 163,
            'current_percentage': 16.3,
            'target_percentage': 25.0,
            'target_pos': 250,
            'gap_pos_needed': 87
        }
    
    def get_supplier_insights(self) -> Dict[str, Any]:
        """Get insights about supplier matching"""
        if 'detailed_analysis' not in self.data_cache:
            return self._get_demo_supplier_insights()
        
        df = self.data_cache['detailed_analysis']
        
        # Analyze similarity scores
        high_confidence = len(df[df['similarity_score'] >= 0.4])
        medium_confidence = len(df[(df['similarity_score'] >= 0.2) & (df['similarity_score'] < 0.4)])
        low_confidence = len(df[df['similarity_score'] < 0.2])
        
        # Average similarity
        avg_similarity = df['similarity_score'].mean() if len(df) > 0 else 0
        
        return {
            'total_matches': len(df),
            'high_confidence_matches': high_confidence,
            'medium_confidence_matches': medium_confidence,
            'low_confidence_matches': low_confidence,
            'average_similarity': avg_similarity,
            'best_match_score': df['similarity_score'].max() if len(df) > 0 else 0
        }
    
    def _get_demo_supplier_insights(self) -> Dict[str, Any]:
        """Return demo supplier insights"""
        return {
            'total_matches': 500,
            'high_confidence_matches': 45,
            'medium_confidence_matches': 120,
            'low_confidence_matches': 335,
            'average_similarity': 0.23,
            'best_match_score': 0.87
        }
    
    def get_category_breakdown(self) -> Dict[str, Any]:
        """Get breakdown by category"""
        if 'category_analysis' not in self.data_cache:
            return self._get_demo_category_breakdown()
        
        df = self.data_cache['category_analysis']
        
        # Convert to dictionary format
        categories = {}
        for _, row in df.iterrows():
            categories[row['category']] = {
                'total_pos': row.get('total_pos', 0),
                'small_business_pos': row.get('small_business_pos', 0),
                'percentage': row.get('percentage', 0)
            }
        
        return categories
    
    def _get_demo_category_breakdown(self) -> Dict[str, Any]:
        """Return demo category breakdown"""
        return {
            'Professional Services': {'total_pos': 200, 'small_business_pos': 45, 'percentage': 22.5},
            'IT Services': {'total_pos': 150, 'small_business_pos': 20, 'percentage': 13.3},
            'Office Supplies': {'total_pos': 300, 'small_business_pos': 60, 'percentage': 20.0},
            'Consulting': {'total_pos': 180, 'small_business_pos': 25, 'percentage': 13.9},
            'Maintenance': {'total_pos': 170, 'small_business_pos': 13, 'percentage': 7.6}
        }
    
    def get_transition_scenarios(self) -> Dict[str, Any]:
        """Get transition scenarios for reaching 25%"""
        current_stats = self.get_current_stats()
        supplier_insights = self.get_supplier_insights()
        
        # Calculate scenarios based on confidence levels
        high_conf_available = supplier_insights['high_confidence_matches']
        medium_conf_available = supplier_insights['medium_confidence_matches']
        
        gap_needed = current_stats['gap_pos_needed']
        
        # High confidence scenario
        high_conf_scenario = {
            'pos_to_transition': min(high_conf_available, gap_needed),
            'resulting_small_business_pos': current_stats['current_small_business_pos'] + min(high_conf_available, gap_needed),
            'target_achieved': high_conf_available >= gap_needed
        }
        high_conf_scenario['resulting_percentage'] = (high_conf_scenario['resulting_small_business_pos'] / current_stats['total_pos']) * 100
        
        # Medium confidence scenario  
        remaining_gap = max(0, gap_needed - high_conf_available)
        medium_conf_scenario = {
            'pos_to_transition': min(medium_conf_available, remaining_gap),
            'resulting_small_business_pos': high_conf_scenario['resulting_small_business_pos'] + min(medium_conf_available, remaining_gap),
            'target_achieved': (high_conf_available + medium_conf_available) >= gap_needed
        }
        medium_conf_scenario['resulting_percentage'] = (medium_conf_scenario['resulting_small_business_pos'] / current_stats['total_pos']) * 100
        
        return {
            'high_confidence': high_conf_scenario,
            'medium_confidence': medium_conf_scenario,
            'gap_needed': gap_needed,
            'total_available_matches': high_conf_available + medium_conf_available
        }
    
    def get_small_business_data(self) -> Dict[str, Any]:
        """Get small business database information"""
        if 'small_businesses' not in self.data_cache:
            return self._get_demo_small_business_data()
        
        df = self.data_cache['small_businesses']
        
        # Analyze small business data
        total_businesses = len(df)
        categories = df['Category'].unique().tolist() if 'Category' in df.columns else []
        
        # Get top categories
        if 'Category' in df.columns:
            category_counts = df['Category'].value_counts().head(5).to_dict()
        else:
            category_counts = {}
        
        return {
            'total_businesses': total_businesses,
            'categories': categories,
            'top_categories': category_counts,
            'data_available': True
        }
    
    def _get_demo_small_business_data(self) -> Dict[str, Any]:
        """Return demo small business data"""
        return {
            'total_businesses': 150,
            'categories': ['Professional Services', 'IT Services', 'Consulting', 'Office Supplies', 'Maintenance'],
            'top_categories': {
                'Professional Services': 35,
                'IT Services': 28,
                'Consulting': 22,
                'Office Supplies': 20,
                'Maintenance': 15
            },
            'data_available': False
        }
    
    def analyze_user_query(self, query: str) -> Dict[str, Any]:
        """Analyze user query and return relevant data context"""
        query_lower = query.lower()
        context = {}
        
        # Always include basic stats
        context.update(self.get_current_stats())
        
        # Add specific data based on query content
        if any(word in query_lower for word in ['supplier', 'match', 'similar']):
            context['supplier_insights'] = self.get_supplier_insights()
        
        if any(word in query_lower for word in ['category', 'breakdown', 'type']):
            context['category_breakdown'] = self.get_category_breakdown()
        
        if any(word in query_lower for word in ['scenario', 'transition', 'plan']):
            context['transition_scenarios'] = self.get_transition_scenarios()
        
        if any(word in query_lower for word in ['small business', 'sbe', 'database']):
            context['small_business_data'] = self.get_small_business_data()
        
        return context
