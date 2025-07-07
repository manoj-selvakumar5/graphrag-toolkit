# SSL Certificate Fix - Run this cell first in your notebook
import os
import ssl
import certifi
import urllib3

# Configure SSL certificates
cert_path = certifi.where()
os.environ['SSL_CERT_FILE'] = cert_path
os.environ['REQUESTS_CA_BUNDLE'] = cert_path
os.environ['AWS_CA_BUNDLE'] = cert_path
os.environ['CURL_CA_BUNDLE'] = cert_path

# Create SSL context with proper certificates
ssl_context = ssl.create_default_context(cafile=cert_path)
ssl._create_default_https_context = lambda: ssl_context

# Disable SSL warnings (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(f"✅ SSL certificates configured using: {cert_path}")
print("✅ Environment variables set for AWS, requests, and curl")
print("✅ Ready to make secure HTTPS connections!")
