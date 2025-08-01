import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

class POQuantityAnalytics:
    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent / "backend"
        self.target_percentage = 25.0  # 25% of POs should go to small businesses
        
    def load_test_results(self) -> pd.DataFrame:
        """Load the full test results data"""
        try:
            return pd.read_csv(self.backend_dir / "test_results.csv")
        except FileNotFoundError:
            return pd.DataFrame()
    
    def load_detailed_analysis(self) -> pd.DataFrame:
        """Load detailed similarity analysis"""
        try:
            return pd.read_csv(self.backend_dir / "detailed_similarity_analysis.csv")
        except FileNotFoundError:
            return pd.DataFrame()
    
    def load_small_business_contacts(self) -> pd.DataFrame:
        """Load small business contact information"""
        try:
            return pd.read_csv(self.backend_dir / "small_business_contacts.csv")
        except FileNotFoundError:
            return pd.DataFrame()
    
    def calculate_current_po_percentage(self) -> Dict:
        """Calculate current small business PO percentage (by quantity, not amount)"""
        test_results = self.load_test_results()
        
        if test_results.empty:
            return {"error": "No test results data available"}
        
        # Each row represents a PO/purchase transaction
        total_pos = len(test_results)
        
        # Identify current small businesses (those marked as OSB, SB, etc.)
        small_business_indicators = ['OSB', 'SB', 'SMALL', 'MINORITY', 'WOMEN', 'DIVERSE']
        test_results['IsCurrentSmallBusiness'] = test_results['CurrentSupplierType'].fillna('').str.upper().apply(
            lambda x: any(indicator in str(x) for indicator in small_business_indicators)
        )
        
        current_small_business_pos = test_results['IsCurrentSmallBusiness'].sum()
        current_percentage = (current_small_business_pos / total_pos * 100) if total_pos > 0 else 0
        
        # Calculate gap
        target_pos_needed = int(total_pos * self.target_percentage / 100)
        gap_pos_needed = target_pos_needed - current_small_business_pos
        gap_percentage = self.target_percentage - current_percentage
        
        return {
            'total_pos': total_pos,
            'current_small_business_pos': current_small_business_pos,
            'current_percentage': current_percentage,
            'target_percentage': self.target_percentage,
            'target_pos_needed': target_pos_needed,
            'gap_pos_needed': max(0, gap_pos_needed),
            'gap_percentage': max(0, gap_percentage),
            'current_non_small_business_pos': total_pos - current_small_business_pos
        }
    
    def generate_po_optimization_plan(self) -> Dict:
        """Generate optimization plan to reach 25% of POs going to small businesses"""
        current_stats = self.calculate_current_po_percentage()
        detailed_analysis = self.load_detailed_analysis()
        
        if detailed_analysis.empty or 'error' in current_stats:
            return {"error": "Insufficient data for optimization plan"}
        
        # Sort matches by similarity score (best matches first)
        detailed_analysis = detailed_analysis.sort_values('Similarity_Score', ascending=False)
        
        # Each match represents a potential PO transition
        total_potential_transitions = len(detailed_analysis)
        
        # Calculate scenarios based on similarity thresholds
        scenarios = {}
        
        # High Confidence Scenario (>= 0.4 similarity)
        high_confidence = detailed_analysis[detailed_analysis['Similarity_Score'] >= 0.4]
        high_conf_pos = len(high_confidence)
        high_conf_new_percentage = ((current_stats['current_small_business_pos'] + high_conf_pos) / 
                                   current_stats['total_pos'] * 100)
        
        scenarios['high_confidence'] = {
            'threshold': '>= 0.4',
            'pos_to_transition': high_conf_pos,
            'resulting_small_business_pos': current_stats['current_small_business_pos'] + high_conf_pos,
            'resulting_percentage': high_conf_new_percentage,
            'target_achieved': high_conf_new_percentage >= self.target_percentage
        }
        
        # Medium Confidence Scenario (>= 0.2 similarity)
        medium_confidence = detailed_analysis[detailed_analysis['Similarity_Score'] >= 0.2]
        medium_conf_pos = len(medium_confidence)
        medium_conf_new_percentage = ((current_stats['current_small_business_pos'] + medium_conf_pos) / 
                                     current_stats['total_pos'] * 100)
        
        scenarios['medium_confidence'] = {
            'threshold': '>= 0.2',
            'pos_to_transition': medium_conf_pos,
            'resulting_small_business_pos': current_stats['current_small_business_pos'] + medium_conf_pos,
            'resulting_percentage': medium_conf_new_percentage,
            'target_achieved': medium_conf_new_percentage >= self.target_percentage
        }
        
        # All Matches Scenario
        all_matches_new_percentage = ((current_stats['current_small_business_pos'] + total_potential_transitions) / 
                                     current_stats['total_pos'] * 100)
        
        scenarios['all_matches'] = {
            'threshold': 'All matches',
            'pos_to_transition': total_potential_transitions,
            'resulting_small_business_pos': current_stats['current_small_business_pos'] + total_potential_transitions,
            'resulting_percentage': all_matches_new_percentage,
            'target_achieved': all_matches_new_percentage >= self.target_percentage
        }
        
        # Find optimal path to exactly 25%
        pos_needed_for_target = current_stats['gap_pos_needed']
        
        if pos_needed_for_target <= 0:
            optimal_path = {
                'pos_to_transition': 0,
                'resulting_percentage': current_stats['current_percentage'],
                'target_achieved': True,
                'message': 'Target already achieved'
            }
        elif pos_needed_for_target <= total_potential_transitions:
            # We can achieve exactly 25% with available matches
            optimal_matches = detailed_analysis.head(pos_needed_for_target)
            optimal_path = {
                'pos_to_transition': pos_needed_for_target,
                'resulting_percentage': self.target_percentage,
                'target_achieved': True,
                'top_recommendations': optimal_matches.head(10).to_dict('records') if len(optimal_matches) > 0 else [],
                'avg_similarity_score': optimal_matches['Similarity_Score'].mean() if len(optimal_matches) > 0 else 0
            }
        else:
            # We need more matches than available
            optimal_path = {
                'pos_to_transition': total_potential_transitions,
                'resulting_percentage': all_matches_new_percentage,
                'target_achieved': False,
                'message': f'Need {pos_needed_for_target} POs but only {total_potential_transitions} matches available',
                'shortfall': pos_needed_for_target - total_potential_transitions
            }
        
        # Create implementation phases
        implementation_phases = []
        cumulative_pos = 0
        
        for threshold in [0.6, 0.4, 0.3, 0.2, 0.1]:
            phase_matches = detailed_analysis[
                (detailed_analysis['Similarity_Score'] >= threshold) & 
                (detailed_analysis['Similarity_Score'] < threshold + 0.2 if threshold < 0.6 else True)
            ]
            
            if len(phase_matches) > 0:
                cumulative_pos += len(phase_matches)
                new_percentage = ((current_stats['current_small_business_pos'] + cumulative_pos) / 
                                current_stats['total_pos'] * 100)
                
                implementation_phases.append({
                    'phase': f"Phase {len(implementation_phases) + 1}",
                    'similarity_threshold': f">= {threshold:.1f}",
                    'pos_in_phase': len(phase_matches),
                    'cumulative_pos': cumulative_pos,
                    'resulting_percentage': new_percentage,
                    'target_achieved': new_percentage >= self.target_percentage
                })
                
                if new_percentage >= self.target_percentage:
                    break
        
        return {
            'current_stats': current_stats,
            'scenarios': scenarios,
            'optimal_path': optimal_path,
            'implementation_phases': implementation_phases,
            'total_potential_transitions': total_potential_transitions
        }
    
    def get_supplier_transition_analysis(self) -> Dict:
        """Analyze which current suppliers would need to be replaced"""
        detailed_analysis = self.load_detailed_analysis()
        
        if detailed_analysis.empty:
            return {"error": "No detailed analysis data"}
        
        # Group by current supplier to see transition opportunities
        supplier_analysis = detailed_analysis.groupby('Current_Supplier').agg({
            'Purchase_Amount': ['sum', 'count'],
            'Similarity_Score': 'mean',
            'Small_Business': lambda x: ', '.join(x.unique()[:3])  # Top 3 small business options
        }).round(3)
        
        supplier_analysis.columns = ['Total_Amount', 'PO_Count', 'Avg_Similarity', 'Small_Business_Options']
        supplier_analysis = supplier_analysis.reset_index()
        supplier_analysis = supplier_analysis.sort_values('PO_Count', ascending=False)
        
        return {
            'supplier_analysis': supplier_analysis.to_dict('records'),
            'top_suppliers_by_po_count': supplier_analysis.head(10).to_dict('records'),
            'suppliers_with_best_matches': supplier_analysis.nlargest(10, 'Avg_Similarity').to_dict('records')
        }
    
    def get_category_po_impact(self) -> Dict:
        """Analyze PO impact by business category"""
        detailed_analysis = self.load_detailed_analysis()
        
        if detailed_analysis.empty:
            return {"error": "No detailed analysis data"}
        
        # Group by business category - each row is a PO
        category_impact = detailed_analysis.groupby('Business_Category').agg({
            'Purchase_Amount': ['sum', 'mean'],
            'Similarity_Score': 'mean'
        }).round(2)
        
        category_impact.columns = ['Total_Amount', 'Avg_Amount', 'Avg_Similarity']
        category_impact['PO_Count'] = detailed_analysis.groupby('Business_Category').size()
        category_impact = category_impact.reset_index()
        category_impact = category_impact.sort_values('PO_Count', ascending=False)
        
        # Calculate what percentage of total POs each category represents
        total_pos = len(detailed_analysis)
        category_impact['PO_Percentage'] = (category_impact['PO_Count'] / total_pos * 100).round(2)
        
        return {
            'category_analysis': category_impact.to_dict('records'),
            'top_categories_by_po_count': category_impact.head(8).to_dict('records'),
            'most_efficient_categories': category_impact.nlargest(5, 'Avg_Similarity').to_dict('records')
        }
    
    def get_quick_wins_by_po_impact(self, limit: int = 15) -> List[Dict]:
        """Get quick wins prioritized by PO transition impact"""
        detailed_analysis = self.load_detailed_analysis()
        contacts = self.load_small_business_contacts()
        
        if detailed_analysis.empty:
            return []
        
        # For PO analysis, we prioritize by similarity score since each match = 1 PO
        # But we can also consider the supplier's total PO volume for strategic impact
        
        # Calculate how many POs each current supplier has
        supplier_po_counts = detailed_analysis.groupby('Current_Supplier').size().to_dict()
        detailed_analysis['Supplier_PO_Count'] = detailed_analysis['Current_Supplier'].map(supplier_po_counts)
        
        # Create impact score: 70% similarity, 30% supplier PO volume (normalized)
        max_po_count = detailed_analysis['Supplier_PO_Count'].max()
        detailed_analysis['PO_Impact_Score'] = (
            detailed_analysis['Similarity_Score'] * 0.7 + 
            (detailed_analysis['Supplier_PO_Count'] / max_po_count) * 0.3
        )
        
        quick_wins = detailed_analysis.nlargest(limit, 'PO_Impact_Score')
        
        # Merge with contact information
        if not contacts.empty:
            quick_wins = quick_wins.merge(
                contacts, 
                left_on='Small_Business', 
                right_on='business_name', 
                how='left'
            )
            # Create a combined contact column showing both email and phone
            quick_wins['Contact_Info'] = quick_wins.apply(
                lambda row: f"{row.get('contact_email', 'N/A')} | {row.get('contact_phone', 'N/A')}" 
                if pd.notna(row.get('contact_email')) else 'Contact info not available',
                axis=1
            )
            
            return quick_wins[['Current_Supplier', 'Small_Business', 'Contact_Info', 'Purchase_Amount', 
                              'Similarity_Score', 'Business_Category', 'Supplier_PO_Count',
                              'PO_Impact_Score', 'contact_person']].to_dict('records')
        else:
            # If no contact data available, add placeholder
            quick_wins['Contact_Info'] = 'Contact info not available'
            quick_wins['contact_person'] = 'N/A'
            
            return quick_wins[['Current_Supplier', 'Small_Business', 'Contact_Info', 'Purchase_Amount', 
                              'Similarity_Score', 'Business_Category', 'Supplier_PO_Count',
                              'PO_Impact_Score', 'contact_person']].to_dict('records')
