import json
import boto3
import pandas as pd
from io import StringIO
import logging
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Configuration
S3_BUCKET = 'supplier-diversity-analysis'
DYNAMODB_TABLE = 'SupplierMatches'

def lambda_handler(event, context):
    """
    AWS Lambda function to serve supplier diversity data to React frontend
    """
    
    # Enable CORS for React frontend
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    try:
        # Handle preflight OPTIONS request
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Get the API endpoint from the path
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        logger.info(f"Processing {method} request to {path}")
        
        # Route to appropriate handler
        if path == '/api/summary':
            response_data = get_summary_stats()
        elif path == '/api/po-analysis':
            response_data = get_po_analysis()
        elif path == '/api/matches':
            limit = int(event.get('queryStringParameters', {}).get('limit', 20))
            response_data = get_top_matches(limit)
        elif path == '/api/categories':
            response_data = get_category_analysis()
        elif path == '/api/small-businesses':
            response_data = get_small_businesses()
        elif path == '/api/optimization-plan':
            response_data = get_optimization_plan()
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data, cls=DecimalEncoder)
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def get_summary_stats():
    """Get overall summary statistics"""
    try:
        # Get data from S3
        response = s3_client.get_object(Bucket=S3_BUCKET, Key='demo_summary.csv')
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        
        # Calculate summary stats
        df['Total_Amount_Clean'] = df['Total Amount'].str.replace('$', '').str.replace(',', '').astype(float)
        
        total_matches = df['Number of Matches'].sum()
        total_amount = df['Total_Amount_Clean'].sum()
        avg_score = df['Avg Score'].mean()
        
        high_confidence = df[df['Confidence Level'] == 'High']
        high_confidence_matches = high_confidence['Number of Matches'].iloc[0] if len(high_confidence) > 0 else 0
        high_confidence_amount = high_confidence['Total_Amount_Clean'].iloc[0] if len(high_confidence) > 0 else 0
        
        return {
            'total_matches': int(total_matches),
            'total_amount': float(total_amount),
            'avg_score': float(avg_score),
            'high_confidence_matches': int(high_confidence_matches),
            'high_confidence_amount': float(high_confidence_amount)
        }
        
    except Exception as e:
        logger.error(f"Error getting summary stats: {str(e)}")
        raise

def get_po_analysis():
    """Get PO percentage analysis"""
    try:
        # Get detailed analysis from S3
        response = s3_client.get_object(Bucket=S3_BUCKET, Key='test_results.csv')
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        
        # Calculate PO percentages
        total_pos = len(df)
        
        # Identify current small businesses
        small_business_indicators = ['OSB', 'SB', 'SMALL', 'MINORITY', 'WOMEN', 'DIVERSE']
        df['IsCurrentSmallBusiness'] = df['CurrentSupplierType'].fillna('').str.upper().apply(
            lambda x: any(indicator in str(x) for indicator in small_business_indicators)
        )
        
        current_small_business_pos = df['IsCurrentSmallBusiness'].sum()
        current_percentage = (current_small_business_pos / total_pos * 100) if total_pos > 0 else 0
        
        target_percentage = 25.0
        target_pos_needed = int(total_pos * target_percentage / 100)
        gap_pos_needed = max(0, target_pos_needed - current_small_business_pos)
        gap_percentage = max(0, target_percentage - current_percentage)
        
        return {
            'total_pos': total_pos,
            'current_small_business_pos': int(current_small_business_pos),
            'current_percentage': float(current_percentage),
            'target_percentage': target_percentage,
            'target_pos_needed': target_pos_needed,
            'gap_pos_needed': gap_pos_needed,
            'gap_percentage': float(gap_percentage),
            'current_non_small_business_pos': total_pos - int(current_small_business_pos)
        }
        
    except Exception as e:
        logger.error(f"Error getting PO analysis: {str(e)}")
        raise

def get_top_matches(limit=20):
    """Get top similarity matches"""
    try:
        # Get from DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        
        response = table.scan(
            Limit=limit,
            FilterExpression='attribute_exists(Similarity_Score)'
        )
        
        matches = response['Items']
        
        # Sort by similarity score
        matches.sort(key=lambda x: float(x.get('Similarity_Score', 0)), reverse=True)
        
        return {
            'matches': matches[:limit],
            'total_count': len(matches)
        }
        
    except Exception as e:
        logger.error(f"Error getting top matches: {str(e)}")
        # Fallback to S3 if DynamoDB fails
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key='detailed_similarity_analysis.csv')
            csv_content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_content))
            
            top_matches = df.head(limit).to_dict('records')
            
            return {
                'matches': top_matches,
                'total_count': len(df)
            }
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
            raise

def get_category_analysis():
    """Get analysis by business category"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key='detailed_similarity_analysis.csv')
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        
        # Group by category
        category_summary = df.groupby('Business_Category').agg({
            'Purchase_Amount': ['count', 'sum', 'mean'],
            'Similarity_Score': 'mean'
        }).round(3)
        
        category_summary.columns = ['PO_Count', 'Total_Amount', 'Avg_Amount', 'Avg_Similarity']
        category_summary = category_summary.reset_index()
        category_summary = category_summary.sort_values('Total_Amount', ascending=False)
        
        # Calculate percentage impact
        total_pos = len(df)
        category_summary['PO_Percentage'] = (category_summary['PO_Count'] / total_pos * 100).round(2)
        
        return {
            'categories': category_summary.to_dict('records'),
            'total_categories': len(category_summary)
        }
        
    except Exception as e:
        logger.error(f"Error getting category analysis: {str(e)}")
        raise

def get_small_businesses():
    """Get small business directory"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key='sample_small_businesses.csv')
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        
        return {
            'businesses': df.to_dict('records'),
            'total_count': len(df)
        }
        
    except Exception as e:
        logger.error(f"Error getting small businesses: {str(e)}")
        raise

def get_optimization_plan():
    """Get optimization plan to reach 25%"""
    try:
        po_analysis = get_po_analysis()
        matches_data = get_top_matches(1000)  # Get more matches for analysis
        
        matches = matches_data['matches']
        current_stats = po_analysis
        
        # Create scenarios
        scenarios = {}
        
        # High confidence scenario
        high_confidence = [m for m in matches if float(m.get('Similarity_Score', 0)) >= 0.4]
        high_conf_count = len(high_confidence)
        high_conf_new_percentage = ((current_stats['current_small_business_pos'] + high_conf_count) / 
                                   current_stats['total_pos'] * 100)
        
        scenarios['high_confidence'] = {
            'threshold': '>= 0.4',
            'pos_to_transition': high_conf_count,
            'resulting_percentage': high_conf_new_percentage,
            'target_achieved': high_conf_new_percentage >= 25.0
        }
        
        # Medium confidence scenario
        medium_confidence = [m for m in matches if float(m.get('Similarity_Score', 0)) >= 0.2]
        medium_conf_count = len(medium_confidence)
        medium_conf_new_percentage = ((current_stats['current_small_business_pos'] + medium_conf_count) / 
                                     current_stats['total_pos'] * 100)
        
        scenarios['medium_confidence'] = {
            'threshold': '>= 0.2',
            'pos_to_transition': medium_conf_count,
            'resulting_percentage': medium_conf_new_percentage,
            'target_achieved': medium_conf_new_percentage >= 25.0
        }
        
        return {
            'current_stats': current_stats,
            'scenarios': scenarios,
            'total_potential_matches': len(matches)
        }
        
    except Exception as e:
        logger.error(f"Error getting optimization plan: {str(e)}")
        raise

class DecimalEncoder(json.JSONEncoder):
    """Helper class to encode Decimal objects from DynamoDB"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
