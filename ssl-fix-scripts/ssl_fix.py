#!/usr/bin/env python3
"""
SSL Certificate Fix for GraphRAG Toolkit
Run this script to configure SSL certificates properly for AWS services.
"""

import os
import ssl
import certifi
import urllib3

def fix_ssl_certificates():
    """Configure SSL certificates for AWS and other HTTPS connections."""
    
    # Get the path to certifi's certificate bundle
    cert_path = certifi.where()
    print(f"Using certificate bundle: {cert_path}")
    
    # Set environment variables for SSL certificate verification
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    os.environ['AWS_CA_BUNDLE'] = cert_path
    os.environ['CURL_CA_BUNDLE'] = cert_path
    
    # Configure SSL context to use system certificates
    ssl_context = ssl.create_default_context(cafile=cert_path)
    ssl._create_default_https_context = lambda: ssl_context
    
    print("SSL certificates configured successfully!")
    print("Environment variables set:")
    print(f"  SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE')}")
    print(f"  REQUESTS_CA_BUNDLE: {os.environ.get('REQUESTS_CA_BUNDLE')}")
    print(f"  AWS_CA_BUNDLE: {os.environ.get('AWS_CA_BUNDLE')}")
    
    return cert_path

if __name__ == "__main__":
    fix_ssl_certificates()
