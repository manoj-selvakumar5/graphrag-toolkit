#!/usr/bin/env python3
"""
Test SSL certificate configuration with AWS
"""

import os
import ssl
import certifi
import boto3
from botocore.exceptions import ClientError

# Apply SSL fix
cert_path = certifi.where()
os.environ['SSL_CERT_FILE'] = cert_path
os.environ['REQUESTS_CA_BUNDLE'] = cert_path
os.environ['AWS_CA_BUNDLE'] = cert_path

# Create SSL context
ssl_context = ssl.create_default_context(cafile=cert_path)
ssl._create_default_https_context = lambda: ssl_context

print(f"Using certificate bundle: {cert_path}")
print("Testing AWS connection...")

try:
    # Test with a simple AWS service call
    sts = boto3.client('sts', region_name='us-east-1')
    identity = sts.get_caller_identity()
    print("✅ SSL connection successful!")
    print(f"AWS Account ID: {identity.get('Account', 'N/A')}")
    print(f"User ARN: {identity.get('Arn', 'N/A')}")
except Exception as e:
    print(f"❌ SSL connection failed: {e}")
    print("Error type:", type(e).__name__)
