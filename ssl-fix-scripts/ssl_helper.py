"""
SSL Helper for AWS connections in Python environments
Based on successful resolution from SSL certificate issue analysis
"""
import os
import boto3
from botocore.config import Config

def setup_ssl_for_aws():
    """Configure SSL using certifi certificate bundle"""
    try:
        import certifi
        cert_path = certifi.where()
        
        # Set environment variables
        os.environ['SSL_CERT_FILE'] = cert_path
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['CURL_CA_BUNDLE'] = cert_path
        
        print(f"✅ SSL configured successfully using certifi certificates")
        print(f"Certificate path: {cert_path}")
        return cert_path
    except ImportError:
        # Fallback to system certificates
        cert_path = '/opt/homebrew/etc/ca-certificates/cert.pem'
        os.environ['SSL_CERT_FILE'] = cert_path
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['CURL_CA_BUNDLE'] = cert_path
        print(f"✅ SSL configured using system certificates: {cert_path}")
        return cert_path

def create_aws_client(service_name, region_name='us-east-1'):
    """Create boto3 client with proper SSL verification"""
    cert_path = setup_ssl_for_aws()
    
    config = Config(
        region_name=region_name,
        retries={'max_attempts': 3, 'mode': 'adaptive'}
    )
    
    # This is the key fix: explicitly set verify parameter with cert_path
    client = boto3.client(service_name, config=config, verify=cert_path)
    return client

def test_aws_connection():
    """Test AWS connectivity using STS"""
    try:
        sts_client = create_aws_client('sts')
        identity = sts_client.get_caller_identity()
        
        account_id = identity['Account']
        user_arn = identity['Arn']
        
        print(f"🌍 AWS Connection successful to account ID: {account_id}")
        print(f"👤 Connected as: {user_arn}")
        return True
    except Exception as e:
        print(f"❌ AWS connection failed: {e}")
        return False

if __name__ == "__main__":
    test_aws_connection()
